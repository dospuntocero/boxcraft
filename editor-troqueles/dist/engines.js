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
    if(model.engine==='derived')return ['totalX','totalY'].map(key=>{const r=model.rule.rules['/'+key];return r[0]+model.rule.axes.reduce((sum,axis,i)=>sum+r[i+1]*(dims[axis]-model.rule.base[i]),0);});
    if(model.engine==='features'){const vector=featureVector(model.rule,dims);return ['totalX','totalY'].map(key=>model.rule.rules['/'+key].reduce((sum,c,i)=>sum+c*vector[i],0));}
    if(model.engine==='height')return ['totalX','totalY'].map(key=>model.layer[key]+(model.rule.slopes['/'+key]||0)*(dims.H-model.rule.baseH));
    if(model.engine==='panels'&&model.rule.recipe==='10001006')return [12.5+2*dims.L+2*dims.W,dims.H+2*dims.W+21];
    return null;
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
    const layer=clone(model.layer),rule=model.rule;
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
    if(model.materialSheetMm&&extents(model,dims)){
      let low=bounds[0],high=Math.max(...model.materialSheetMm);
      for(let i=0;i<40;i++){
        const mid=(low+high)/2;
        const [x,y]=extents(model,{...dims,[axis]:mid});
        if(sheetFit(x,y,model.materialSheetMm))low=mid;else high=mid;
      }
      return [bounds[0],Math.floor(low*100)/100];
    }
    if(model.id==='200010'&&model.materialWidthMm&&(axis==='L'||axis==='W')){
      const rule=model.rule,total=rule.rules['/totalX'],i='LWH'.indexOf(axis);
      const remainder=total.base+total.slopes_LWH.reduce((sum,s,j)=>sum+(j===i?0:s*(dims['LWH'[j]]-rule.base[j])),0);
      return [bounds[0],rule.base[i]+(model.materialWidthMm-remainder)/total.slopes_LWH[i]];
    }
    return bounds;
  }
  root.TroquelEngines={generate,fieldBounds,sheetFit,sheetYield};
  if(typeof module!=='undefined')module.exports=root.TroquelEngines;
})(globalThis);
