(function(root){
  'use strict';
  const I18n=root.I18n||{t:key=>key,locale:'es-CL'};
  const names={get L(){return I18n.t("Longitud");},get W(){return I18n.t("Anchura");},get H(){return I18n.t("Altura");}};
  function anchors(model,layer){
    const face=name=>layer.faces.find(f=>f.name===name);
    const horizontal=(axis,p,t=.8)=>({axis,x1:p.x,y1:p.y+p.h*t,x2:p.x+p.w,y2:p.y+p.h*t});
    const vertical=(axis,p,t=.7)=>({axis,x1:p.x+p.w*t,y1:p.y,x2:p.x+p.w*t,y2:p.y+p.h});
    let result;
    if(model.id==='150010')result=[horizontal('L',face('H'),.84),vertical('W',face('H'),.77),vertical('H',face('FB'),.48)];
    else if(model.id==='12109002')result=[horizontal('L',face('F'),.82),vertical('W',face('F'),.76),vertical('H',face('FT'),.52)];
    else if(model.id==='180370'){
      const b=face('HB'),t=face('FT');
      result=[horizontal('L',b,.42),vertical('W',{...b,h:t.y+t.h-b.y},.25),vertical('H',face('F'),.78)];
    }else if(model.id==='180320')result=[horizontal('L',face('B'),.76),vertical('W',face('B'),.72)];
    else result=[horizontal('L',face('H'),.8),horizontal('W',face('FR')||face('L'),.25),vertical('H',face('F'),.72)];
    return result.filter(a=>Object.hasOwn(model.dims,a.axis));
  }
  function markup(model,layer,dims,unit,interactive){
    const size=Math.max(layer.totalX,layer.totalY),font=size/31,stroke=size/600;
    const fmt=v=>new Intl.NumberFormat(I18n.locale,{maximumFractionDigits:unit==='in'?4:2}).format(v);
    let out='<defs><marker id="dimension-arrow" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L8 4L0 8Z" fill="#0878ff"/></marker></defs><g id="cotas-caja" fill="none" stroke="#0878ff" stroke-width="'+stroke+'">';
    for(const a of anchors(model,layer)){
      const value=dims[a.axis]/(unit==='in'?25.4:1),cx=(a.x1+a.x2)/2,cy=(a.y1+a.y2)/2;
      const width=font*(unit==='in'?6.3:5.1),height=font*1.85,tick=font*.55;
      const horizontal=Math.abs(a.y1-a.y2)<1e-7;
      out+=`<g data-dimension="${a.axis}"><path d="M${a.x1} ${a.y1}L${a.x2} ${a.y2}" marker-start="url(#dimension-arrow)" marker-end="url(#dimension-arrow)"/><path d="${horizontal?`M${a.x1} ${a.y1-tick}v${tick*2}M${a.x2} ${a.y2-tick}v${tick*2}`:`M${a.x1-tick} ${a.y1}h${tick*2}M${a.x2-tick} ${a.y2}h${tick*2}`}"/>`;
      if(interactive&&model.bounds[a.axis]){
        const inputValue=Number(value.toFixed(unit==='in'?5:3));
        out+=`<foreignObject x="${cx-width/2}" y="${cy-height/2}" width="${width}" height="${height}" style="overflow:visible"><div xmlns="http://www.w3.org/1999/xhtml" class="dimension-control" style="font-size:${font}px"><input data-canvas-axis="${a.axis}" type="text" inputmode="decimal" autocomplete="off" spellcheck="false" aria-label="${names[a.axis]} ${I18n.t("sobre el plano en")} ${unit}" title="${I18n.t("Editar")} ${names[a.axis].toLowerCase()} ${I18n.t("· Enter para aplicar · Escape para cancelar")}" value="${inputValue}"/><span>${unit}</span></div></foreignObject>`;
      }else{
        out+=`<rect x="${cx-width/2}" y="${cy-height/2}" width="${width}" height="${height}" rx="${font*.2}" fill="#eef6ff" stroke="none"/><text x="${cx}" y="${cy}" fill="#0878ff" stroke="none" font-family="Arial,sans-serif" font-size="${font}" text-anchor="middle" dominant-baseline="central">${fmt(value)} ${unit}</text>`;
      }
      out+='</g>';
    }
    return out+'</g>';
  }
  root.TroquelDimensions={anchors,markup};
  if(typeof module!=='undefined')module.exports=root.TroquelDimensions;
})(globalThis);
