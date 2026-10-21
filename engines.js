(function(root){
  'use strict';
  const I18n=root.I18n||{t:key=>key,locale:'es-CL'};
  const clone=x=>JSON.parse(JSON.stringify(x));
  function assign(object,path,value){const parts=path.slice(1).split('/');let target=object;for(const key of parts.slice(0,-1))target=target[key];target[parts.at(-1)]=value;}
  function featureVector(rule,dims){
    const values=[dims.L,dims.W,dims.H,8,Math.floor(Math.min(dims.L/2,dims.W*.65)+1e-9),Math.max(7,Math.floor(dims.W*.15+1e-9))];
    return [1,...values.map((v,i)=>(v-rule.base[i])/rule.scale[i])];
  }
  function sheetFit(width,height,sheet){
    const [w,h]=sheet,tolerance=1e-7;
    if(width<=w+tolerance&&height<=h+tolerance)return 'direct';
    if(width<=h+tolerance&&height<=w+tolerance)return 'rotated';
    return null;
  }
  // Conservative rectangular grid: every blank reserves its 3 mm bleed on each side.
  function sheetYield(width,height,sheet,bleed=3){
    if(![width,height,...sheet,bleed].every(Number.isFinite)||width<=0||height<=0||sheet.some(v=>v<=0)||bleed<0)throw Error(I18n.t("Medidas de pliego inválidas."));
    const blankWidth=width+2*bleed,blankHeight=height+2*bleed;
    const grid=(w,h,rotated)=>{const columns=Math.floor((sheet[0]+1e-7)/w),rows=Math.floor((sheet[1]+1e-7)/h);return {count:columns*rows,columns,rows,rotated,blankWidth:w,blankHeight:h,bleed};};
    const direct=grid(blankWidth,blankHeight,false),rotated=grid(blankHeight,blankWidth,true);
    return rotated.count>direct.count?rotated:direct;
  }
  function extents(model,dims){
    if(model.engine==='pillow187000')return [dims.L+dims.H,(dims.W>=100?18:15)+2*dims.W];
    if(model.engine==='compiled'){const layer=buildCompiled(model,dims);return [layer.totalX,layer.totalY];}
    if(model.engine==='panel188060')return [135.5+2*dims.L,2*dims.W+dims.H];
    if(model.engine==='affine')return ['totalX','totalY'].map(key=>{const r=model.rule.rules['/'+key],axes=['L','W','H'];return r.base+r.slopes_LWH.reduce((sum,s,i)=>sum+s*(dims[axes[i]]-model.rule.base[i]),0);});
    if(model.engine==='derived')return ['totalX','totalY'].map(key=>{const r=model.rule.rules['/'+key];return r[0]+model.rule.axes.reduce((sum,axis,i)=>sum+r[i+1]*(dims[axis]-model.rule.base[i]),0);});
    if(model.engine==='features'){const vector=featureVector(model.rule,dims);return ['totalX','totalY'].map(key=>model.rule.rules['/'+key].reduce((sum,c,i)=>sum+c*vector[i],0));}
    if(model.engine==='height')return ['totalX','totalY'].map(key=>model.layer[key]+(model.rule.slopes['/'+key]||0)*(dims.H-model.rule.baseH));
    if(model.engine==='panels'&&model.rule.recipe==='10001006')return [12.5+2*dims.L+2*dims.W,dims.H+2*dims.W+21];
    return null;
  }
  // 187000 · pillow box. Local reconstruction derived from the rendered blue cut.
  // Coordinates in mm. The top flap height steps at W=100 (15 -> 18 mm) and the
  // lock notch radius follows the blank width (6..7.5 mm in 0.5 mm steps).
  function buildPillow187000(dims){
    const L=Number(dims.L),W=Number(dims.W),H=Number(dims.H);
    if(!(L>0&&W>0&&H>0))throw Error(I18n.t("Introduce dimensiones positivas y válidas."));
    if(H>=W)throw Error(I18n.t("La altura debe ser menor que la anchura en esta caja almohada."));
    const x0=H/2,xl=x0,xr=x0+L;
    const y0=W>=100?18:15;
    const R=(W*W+H*H)/(4*H),a=R-H/2;
    const rt=Math.max(6,Math.min(7.5,Math.round(((L+H)/25)*2)/2));
    const d=R-Math.sqrt(Math.max(0,R*R-rt*rt));
    const dy=W/2-y0;
    const i=-a+Math.sqrt(Math.max(0,R*R-dy*dy));
    const xtl=x0+i,xtr=xr-i;
    const xsR=xr+H/2-d,xsL=xl-H/2+d;
    const ys=y0+1.5*W;
    const M=(x,y)=>({mtd:'M',x,y});
    const P=(x,y)=>({mtd:'L',x,y});
    const A=(rx,x,y,dir)=>({mtd:'A',rx,ry:rx,ang:0,arc:0,dir,x,y});
    const Z=()=>({mtd:'Z'});
    const cuts=[M(xtl,0),P(xtr,0),A(R,xr,y0,0),A(R,xr,y0+W,1),A(R,xsR,ys-rt,1),A(rt,xsR,ys+rt,0),A(R,xr,y0+2*W,1),P(xl,y0+2*W),A(R,xsL,ys+rt,1),A(rt,xsL,ys-rt,0),A(R,xl,y0+W,1),A(R,xl,y0,1),A(R,xtl,0,0),Z()];
    const face=(name,dlist,x,y,w,h)=>({name,dlist,x,y,w,h,holes:null});
    const faces=[
      face('H',[M(xr,y0),A(R,xr,y0+W,0),P(xl,y0+W),A(R,xl,y0,0),Z()],xl,y0,L,W),
      face('F',[M(xr,y0+W),A(R,xr,y0+2*W,0),P(xl,y0+2*W),A(R,xl,y0+W,0),Z()],xl,y0+W,L,W),
      face('HL',[M(xr,y0),P(xl,y0),A(R,xtl,0,0),P(xtr,0),A(R,xr,y0,0),Z()],xl,0,L,y0),
      face('HT',[M(xr,y0),A(R,xr,y0+W,1),A(R,xr,y0,1),Z()],xr,y0,H/2,W),
      face('HB',[M(xl,y0),A(R,xl,y0+W,1),A(R,xl,y0,1),Z()],xl-H/2,y0,H/2,W),
      face('FT',[M(xr,y0+W),A(R,xsR,ys-rt,1),A(rt,xsR,ys+rt,0),A(R,xr,y0+2*W,1),A(R,xr,y0+W,1),Z()],xr,y0+W,H/2,W),
      face('FB',[M(xl,y0+W),A(R,xl,y0+2*W,1),A(R,xsL,ys+rt,1),A(rt,xsL,ys-rt,0),A(R,xl,y0+W,1),Z()],xl-H/2,y0+W,H/2,W)
    ];
    const arc='A'+R+' '+R+' 0 0 0';
    const folds=[
      {d:`M${xl} ${y0}L${xr} ${y0}`},
      {d:`M${xl} ${y0+W}L${xr} ${y0+W}`},
      {d:`M${xr} ${y0}${arc} ${xr} ${y0+W}`},
      {d:`M${xr} ${y0+W}${arc} ${xr} ${y0+2*W}`},
      {d:`M${xl} ${y0+W}${arc} ${xl} ${y0}`},
      {d:`M${xl} ${y0+2*W}${arc} ${xl} ${y0+W}`}
    ];
    return {
      faces,folds,holes:[],cuts,bleeds:[],bleedFromCuts:true,
      totalX:L+H,totalY:y0+2*W,
      knifeSize:{L,W,H,D:0,id:0,ed:0,like:null},
      size:{L,W,H,D:0,id:0,ed:0,like:null},
      outSize:{L,W,H,D:0,id:0,ed:0,like:null},
      science:{id:103,name:'350g white paperboard(0.5mm)'},bleedline:0,thickness:0.5
    };
  }
  // 188060 · hexagonal box. Panel-wise warp: X follows the six panel widths,
  // Y follows top flap (W), body (H), bottom flap (W). Radii stay fixed.
  function buildPanel188060(model,dims){
    const L=Number(dims.L),W=Number(dims.W),H=Number(dims.H);
    if(!(L>0&&W>0&&H>0))throw Error(I18n.t("Introduce dimensiones positivas y válidas."));
    const bL=100.6,bW=40.6,bH=181.6;
    const xb=[0,16,46,46+bL,76+bL,106+bL,106+2*bL,135.5+2*bL];
    const xn=[0,16,46,46+L,76+L,106+L,106+2*L,135.5+2*L];
    const yb=[0,bW,bW+bH,2*bW+bH],yn=[0,W,W+H,2*W+H];
    const map=(v,b,n)=>{for(let i=0;i<b.length-1;i++){if(v<=b[i+1]+1e-9)return n[i]+(v-b[i])*(n[i+1]-n[i])/(b[i+1]-b[i]);}return n[n.length-1]+(v-b[b.length-1]);};
    const layer=clone(model.layer);
    const point=p=>{if(typeof p.x==='number')p.x=map(p.x,xb,xn);if(typeof p.y==='number')p.y=map(p.y,yb,yn);};
    for(const f of layer.faces||[]){
      const x=f.x,y=f.y,w=f.w,h=f.h;
      f.x=map(x,xb,xn);f.y=map(y,yb,yn);f.w=map(x+w,xb,xn)-f.x;f.h=map(y+h,yb,yn)-f.y;
      for(const p of f.dlist||[])point(p);
      for(const hole of f.holes||[])for(const p of hole)point(p);
    }
    for(const c of layer.cuts||[])point(c);
    for(const f of layer.folds||[]){
      if(typeof f.x1==='number')f.x1=map(f.x1,xb,xn);
      if(typeof f.x2==='number')f.x2=map(f.x2,xb,xn);
      if(typeof f.y1==='number')f.y1=map(f.y1,yb,yn);
      if(typeof f.y2==='number')f.y2=map(f.y2,yb,yn);
      point(f);
    }
    layer.totalX=135.5+2*L;layer.totalY=2*W+H;
    if(layer.knifeSize)layer.knifeSize={...layer.knifeSize,L,W,H};
    return layer;
  }

  // 366010 · rigid two-piece box. The Pacdora server returns four layers and
  // changes the outer wrap depth at L>=200: outer = clamp(floor(H/2), 15, 20).
  // Within each regime the geometry is affine in L/W/H (and in outer for B);
  // the coefficients below are fitted from controlled server captures.
  function buildRigid366010Pieces(model,dims,physical){
    const rule=model.rule;
    if(!rule||!rule.regimes||!rule.pieces)throw Error(I18n.t("El modelo no tiene reglas paramétricas."));
    const L=Number(dims.L),W=Number(dims.W),H=Number(dims.H);
    const T=physical&&Number.isFinite(physical.thickness)?Number(physical.thickness):(rule.baseThickness||2);
    if(![L,W,H,T].every(Number.isFinite))throw Error(I18n.t("Introduce dimensiones válidas."));
    let regime=null;
    for(const candidate of rule.regimes){
      const [low,high]=candidate.L;
      if(L>=low-1e-9&&L<=high+1e-9){regime=candidate;break;}
    }
    if(!regime)throw Error(I18n.t("La longitud está fuera del rango paramétrico verificado."));
    const templates=regime.templatesByThickness&&regime.templatesByThickness[String(T)];
    if(!templates)throw Error(I18n.t("El espesor está fuera del rango paramétrico verificado."));
    const ref=regime.ref;
    const outer=regime.id==='B'?Math.min(20,Math.max(15,Math.floor(H/2))):15;
    return rule.pieces.map(piece=>{
      const layer=clone(templates[piece.id]);
      const slopes=regime.slopes[piece.id]||{};
      for(const [path,s] of Object.entries(slopes)){
        const parts=path.slice(1).split('/');
        let target=layer;
        for(let i=0;i<parts.length-1;i++)target=target[parts[i]];
        const key=parts[parts.length-1];
        target[key]+=s[0]*(L-ref.L)+s[1]*(W-ref.W)+s[2]*(H-ref.H)+(s[3]?s[3]*(outer-20):0);
      }
      layer.thickness=piece.paper?0.15:T;
      return {id:piece.id,prefix:piece.prefix,name:piece.name,row:piece.row,col:piece.col,paper:!!piece.paper,layer};
    });
  }
  function translateRigidLayer(layer,dx,dy){
    for(const face of layer.faces||[]){
      face.x+=dx;face.y+=dy;
      for(const p of face.dlist||[]){if(typeof p.x==='number')p.x+=dx;if(typeof p.y==='number')p.y+=dy;}
      for(const hole of face.holes||[])for(const p of hole){if(typeof p.x==='number')p.x+=dx;if(typeof p.y==='number')p.y+=dy;}
    }
    for(const c of layer.cuts||[]){if(typeof c.x==='number')c.x+=dx;if(typeof c.y==='number')c.y+=dy;}
    for(const c of layer.bleeds||[]){if(typeof c.x==='number')c.x+=dx;if(typeof c.y==='number')c.y+=dy;}
    for(const f of layer.folds||[]){
      if(typeof f.x1==='number')f.x1+=dx;
      if(typeof f.x2==='number')f.x2+=dx;
      if(typeof f.y1==='number')f.y1+=dy;
      if(typeof f.y2==='number')f.y2+=dy;
    }
    return layer;
  }
  function buildRigid366010(model,dims,physical,withPieces=false){
    const pieces=buildRigid366010Pieces(model,dims,physical);
    const T=physical&&Number.isFinite(physical.thickness)?Number(physical.thickness):(model.rule.baseThickness||2);
    const gap=25,widths=[0,0],heights=[0,0];
    for(const p of pieces){
      widths[p.col]=Math.max(widths[p.col],p.layer.totalX);
      heights[p.row]=Math.max(heights[p.row],p.layer.totalY);
    }
    const origins=pieces.map(p=>({
      x:p.col===0?0:widths[0]+gap,
      y:p.row===0?0:heights[0]+gap,
    }));
    const totalX=widths[0]+gap+widths[1],totalY=heights[0]+gap+heights[1];
    const composite={
      faces:[],cuts:[],folds:[],holes:[],bleeds:[],bleedCuts:[],bleedFaces:[],
      pieceLabels:[],multiPiece:true,officialBleeds:false,bleedFromCuts:true,
      totalX,totalY,thickness:T,bleedline:3,
    };
    pieces.forEach((p,index)=>{
      const origin=origins[index];
      translateRigidLayer(p.layer,origin.x,origin.y);
      composite.faces.push(...p.layer.faces);
      composite.cuts.push(...p.layer.cuts);
      composite.folds.push(...p.layer.folds);
      composite.holes.push(...p.layer.holes);
      composite.bleeds.push(...p.layer.bleeds);
      if(p.paper){composite.bleedCuts.push(...p.layer.cuts);composite.bleedFaces.push(...p.layer.faces);}
      composite.pieceLabels.push({id:p.id,name:p.name,x:origin.x+2,y:origin.y+5});
    });
    const L=Number(dims.L),W=Number(dims.W),H=Number(dims.H);
    composite.knifeSize={L,W,H,D:0,id:0,ed:0,like:null};
    composite.size={L,W,H,D:T,id:0,ed:0,like:null};
    composite.outSize={L:L+9.95,W:W+9.95,H:H+4.45,D:0,id:0,ed:0,like:null};
    composite.science=model.layer&&model.layer.science;
    if(withPieces)composite.pieces=pieces.map(p=>({id:p.id,prefix:p.prefix,name:p.name,paper:p.paper,layer:p.layer}));
    return composite;
  }
  // Compiled rules: features derived from L/W/H (linear, rounded, clamped,
  // or simple nonlinear arcs) plus per-path affine coefficients and optional
  // topology regimes. This keeps server-exposed intermediate parameters exact.
  function matchesCondition(cond,dims,features){
    for(const [key,rule] of Object.entries(cond||{})){
      const value=key in dims?dims[key]:features[key];
      if(!Number.isFinite(value))return false;
      if(rule.min!=null&&value<rule.min-1e-9)return false;
      if(rule.max!=null&&value>rule.max+1e-9)return false;
      if(rule.lt!=null&&!(value<rule.lt))return false;
      if(rule.lte!=null&&!(value<=rule.lte))return false;
      if(rule.gt!=null&&!(value>rule.gt))return false;
      if(rule.gte!=null&&!(value>=rule.gte))return false;
    }
    return true;
  }
  function evalExpr(expr,dims,features){
    if(expr==null)return 0;
    if(typeof expr==='number')return expr;
    if(expr.expr&&!expr.op)return evalExpr(expr.expr,dims,features);
    if(expr.op==='piecewise'){
      for(const item of expr.cases||[])if(matchesCondition(item.when,dims,features))return evalExpr(item.value,dims,features);
      return 0;
    }
    if(expr.op){
      const args=(expr.args||[]).map(a=>evalExpr(a,dims,features));
      if(expr.op==='sqrt')return Math.sqrt(Math.max(0,args[0]));
      if(expr.op==='hypot')return Math.hypot(...args);
      if(expr.op==='atan2')return Math.atan2(args[0],args[1]);
      if(expr.op==='min')return Math.min(...args);
      if(expr.op==='max')return Math.max(...args);
      throw Error(I18n.t("Operación de regla no soportada."));
    }
    let value=expr.const||0;
    for(const [key,coef] of Object.entries(expr)){
      if(key==='const')continue;
      const v=key in dims?dims[key]:(features?.[key]||0);
      value+=coef*v;
    }
    return value;
  }
  function evalFeature(spec,dims,features){
    if(spec.op==='piecewise'||spec.op==='min'||spec.op==='max')return evalExpr(spec,dims,features);
    let value=evalExpr(spec.expr,dims,features);
    const step=spec.step||1;
    if(spec.op==='round')value=Math.round(value/step)*step;
    else if(spec.op==='floor')value=Math.floor(value/step)*step;
    else if(spec.op==='ceil')value=Math.ceil(value/step)*step;
    else if(spec.op==='clamp')value=Math.min(spec.max??Infinity,Math.max(spec.min??-Infinity,value));
    else if(spec.op!=='none'&&spec.op)throw Error(I18n.t("Operación de parámetro no soportada."));
    return value;
  }
  function compiledFeatures(model,dims){
    const features={};
    for(const [name,spec] of Object.entries(model.rule.tables||{})){
      const raw=(dims[spec.key]-spec.from)/spec.step;
      const index=Math.max(0,Math.min(spec.values.length-1,Math.round(raw)));
      features[name]=spec.values[index];
    }
    for(const [name,spec] of Object.entries(model.rule.tables2d||{})){
      const [k1,k2]=spec.keys;
      const i=Math.max(0,Math.min(spec.size[0]-1,Math.round((dims[k1]-spec.from[0])/spec.step[0])));
      const j=Math.max(0,Math.min(spec.size[1]-1,Math.round((dims[k2]-spec.from[1])/spec.step[1])));
      features[name]=spec.values[i*spec.size[1]+j];
    }
    for(const [name,spec] of Object.entries(model.rule.features||{}))features[name]=evalFeature(spec,dims,features);
    return features;
  }
  function selectCompiledRegime(model,dims,features){
    const regimes=model.rule.regimes||[];
    for(const regime of regimes)if(matchesCondition(regime.when,dims,features))return regime;
    return regimes.find(regime=>!regime.when)||null;
  }
  function buildCompiled(model,dims){
    const rule=model.rule;
    if(!rule)throw Error(I18n.t("El modelo no tiene reglas paramétricas."));
    const features=compiledFeatures(model,dims);
    const regime=selectCompiledRegime(model,dims,features)||{template:model.layer,rules:rule.rules};
    const layer=clone(regime.template||model.layer);
    for(const [path,coeffs] of Object.entries(regime.rules||rule.rules||{})){
      let value=coeffs.const||0;
      for(const [key,coef] of Object.entries(coeffs)){
        if(key==='const')continue;
        const v=key in dims?dims[key]:features[key];
        if(!Number.isFinite(v))throw Error(I18n.t("Estas medidas no producen una geometría válida."));
        value+=coef*v;
      }
      assign(layer,path,value);
    }
    return layer;
  }
  function generate(model,dims,physical){
    if(physical&&model.materialCapability){
      const cap=model.materialCapability;
      if(!Number.isFinite(physical.thickness)||(root.TroquelMaterials? !root.TroquelMaterials.profile(cap,physical) : physical.materialId!==cap.originalMaterialId||Math.abs(physical.thickness-cap.originalThickness)>1e-8))throw Error(cap.blockedReason);
    }
    for(const [axis,value] of Object.entries(dims)){
      if(!Number.isFinite(value))throw Error(I18n.t("Introduce una medida válida."));
      if(model.bounds[axis]){const [min,max]=model.bounds[axis];if(value<min-1e-8||(max!=null&&value>max+1e-8))throw Error(`${{L:I18n.t("Longitud"),W:I18n.t("Anchura"),H:I18n.t("Altura")}[axis]}: ${max==null?`${I18n.t("mínimo")} `+min:min+'–'+max} mm.`);}
      else if(Math.abs(value-model.dims[axis])>1e-8)throw Error(I18n.t("Esta medida se conserva en su valor original."));
    }
    if(model.id==='102010'&&dims.L>2*dims.W+1e-6)throw Error(I18n.t("Para este fondo, la longitud no puede superar el doble de la anchura (L ≤ 2W)."));
    let layer=model.engine==='pillow187000'?buildPillow187000(dims):model.engine==='panel188060'?buildPanel188060(model,dims):model.engine==='rigid366010'?buildRigid366010(model,dims,physical):model.engine==='compiled'?buildCompiled(model,dims):clone(model.layer);
    const rule=model.rule;
    if(model.engine==='derived')for(const [path,r] of Object.entries(rule.rules))assign(layer,path,r[0]+rule.axes.reduce((sum,axis,i)=>sum+r[i+1]*(dims[axis]-rule.base[i]),0));
    if(model.engine==='panels'){
      // Piecewise panel coordinates keep the glue strip and terminal tongues fixed.
      // This is a local reconstruction, not the original server's formula.
      const L=dims.L,W=dims.W,H=dims.H;
      const xOld=rule.recipe==='10001006'?[0,13,53,93,133,172.5]:[0,20,94.5,214.5,model.layer.totalX];
      const xNew=rule.recipe==='10001006'?[0,13,13+L,13+L+W,13+2*L+W,12.5+2*L+2*W]:[0,20,W+19.5,W+19.5+L,W+19.5+L+(model.layer.totalX-214.5)*W/75];
      const top=82.37794000823277*W/75;
      const yOld=rule.recipe==='10001006'?[0,11,50.25,180.25,220,231]:[0,82.37794000823277,202.37794000823277,277.37794000823277,289.37794000823277];
      const yNew=rule.recipe==='10001006'?[0,11,W+10.25,H+W+10.25,H+2*W+10,H+2*W+21]:[0,top,top+L,top+L+W,top+L+W+12];
      function map(v,from,to){let i=0;while(i<from.length-2&&v>from[i+1])i++;return to[i]+(v-from[i])*(to[i+1]-to[i])/(from[i+1]-from[i]);}
      const mx=v=>map(v,xOld,xNew),my=v=>map(v,yOld,yNew);
      function transform(o){if(!o||typeof o!=='object')return;if(Array.isArray(o)){o.forEach(transform);return;}
        const x=o.x,y=o.y,w=o.w,h=o.h;
        for(const key of ['x','x1','x2'])if(typeof o[key]==='number')o[key]=mx(o[key]);
        for(const key of ['y','y1','y2'])if(typeof o[key]==='number')o[key]=my(o[key]);
        if(typeof x==='number'&&typeof w==='number')o.w=mx(x+w)-mx(x);
        if(typeof y==='number'&&typeof h==='number')o.h=my(y+h)-my(y);
        Object.values(o).forEach(transform);
      }
      transform(layer);layer.totalX=mx(model.layer.totalX);layer.totalY=my(model.layer.totalY);
    }
    if(model.engine==='affine')for(const [path,r] of Object.entries(rule.rules))assign(layer,path,r.base+r.slopes_LWH.reduce((sum,s,i)=>sum+s*(dims['LWH'[i]]-rule.base[i]),0));
    if(model.engine==='features'){
      const vector=featureVector(rule,dims);
      for(const [path,coeffs] of Object.entries(rule.rules))assign(layer,path,coeffs.reduce((sum,c,i)=>sum+c*vector[i],0));
    }
    if(model.engine==='height')for(const [path,slope] of Object.entries(rule.slopes)){
      const parts=path.slice(1).split('/');let t=layer;for(const key of parts.slice(0,-1))t=t[key];t[parts.at(-1)]+=slope*(dims.H-rule.baseH);
    }
    if(!Number.isFinite(layer.totalX)||!Number.isFinite(layer.totalY)||layer.totalX<=0||layer.totalY<=0)throw Error(I18n.t("Estas medidas no producen un plano válido."));
    if(model.materialWidthMm&&layer.totalX>model.materialWidthMm+1e-7)throw Error(`${I18n.t("El ancho del plano (")}${Number(layer.totalX.toFixed(3))} ${I18n.t("mm) supera el material de")} ${model.materialWidthMm} ${I18n.t("mm. Reduce longitud o anchura.")}`);
    if(model.materialSheetMm&&!sheetFit(layer.totalX,layer.totalY,model.materialSheetMm))throw Error(`${I18n.t("El plano de")} ${Number(layer.totalX.toFixed(2))} × ${Number(layer.totalY.toFixed(2))} ${I18n.t("mm no cabe en el pliego de")} ${model.materialSheetMm.join(' × ')} ${I18n.t("mm, tampoco girado. Reduce las medidas.")}`);
    function inspect(value){if(typeof value==='number'&&!Number.isFinite(value))throw Error(I18n.t("Estas medidas no producen una geometría válida."));if(value&&typeof value==='object'){for(const [key,v] of Object.entries(value)){if((key==='rx'||key==='ry')&&v<0)throw Error(I18n.t("Estas medidas producen un radio negativo."));inspect(v);}}}inspect(layer);
    return layer;
  }
  function fieldBounds(model,dims,axis){
    const bounds=model.bounds[axis];if(!bounds)return null;
    // FEFCO 200010: the 1200 mm width is the hard material constraint.
    if(model.id==='200010'&&model.materialWidthMm&&(axis==='L'||axis==='W')){
      const rule=model.rule,total=rule.rules['/totalX'],i='LWH'.indexOf(axis),axes=['L','W','H'];
      const remainder=total.base+total.slopes_LWH.reduce((sum,s,j)=>sum+(j===i?0:s*(dims[axes[j]]-rule.base[j])),0);
      return [bounds[0],rule.base[i]+(model.materialWidthMm-remainder)/total.slopes_LWH[i]];
    }
    if(model.materialSheetMm&&extents(model,dims)){
      let cap=bounds[1]==null?Math.max(...model.materialSheetMm):Math.min(bounds[1],Math.max(...model.materialSheetMm));
      if(model.engine==='pillow187000'&&axis==='H')cap=Math.min(cap,Math.max(bounds[0],dims.W-0.01));
      if(model.id==='102010'&&axis==='L')cap=Math.min(cap,Math.max(bounds[0],2*dims.W));
      let low=bounds[0],high=cap;
      for(let i=0;i<40;i++){
        const mid=(low+high)/2;
        const [x,y]=extents(model,{...dims,[axis]:mid});
        if(sheetFit(x,y,model.materialSheetMm))low=mid;else high=mid;
      }
      return [bounds[0],Math.floor(low*100)/100];
    }
    return bounds;
  }
  root.TroquelEngines={generate,fieldBounds,sheetFit,sheetYield,pillow187000:buildPillow187000,panel188060:buildPanel188060,rigid366010:buildRigid366010,rigid366010Pieces:buildRigid366010Pieces,compiled:buildCompiled};
  if(typeof module!=='undefined')module.exports=root.TroquelEngines;
})(globalThis);
