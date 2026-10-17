(function(root){
  'use strict';
  const I18n=root.I18n||{t:key=>key,locale:'es-CL'},epsilon=1e-8;
  const modes={get manufacturing(){return I18n.t("Dimensiones de manufactura");},get inner(){return I18n.t("Dimensiones internas");},get outer(){return I18n.t("Dimensiones externas");}};
  const sameId=(a,b)=>String(a)===String(b);
  function profiles(cap){return [{materialIds:[cap.originalMaterialId],thickness:cap.originalThickness,offsets:cap.offsets,original:true},...(cap.physicalProfiles||[]).filter(p=>Number.isFinite(p.thickness)&&p.materialIds?.length&&!['unsupported','blocked','unverified'].includes(p.geometryStatus)&&(p.layer||p.original))];}
  function profile(cap,physical){if(!physical)return profiles(cap)[0];return profiles(cap).find(p=>p.materialIds.some(id=>sameId(id,physical.materialId))&&Math.abs(p.thickness-physical.thickness)<epsilon);}
  function limits(cap,material){const observed=cap.observedThicknessLimits||[-Infinity,Infinity];return [Math.max(material.min,observed[0]),Math.min(material.max,observed[1])];}
  function thicknesses(cap,material){const [lo,hi]=limits(cap,material);return [...new Set(profiles(cap).filter(p=>p.materialIds.some(id=>sameId(id,material.id))&&p.thickness>=lo-epsilon&&p.thickness<=hi+epsilon).map(p=>p.thickness))].sort((a,b)=>a-b);}
  function compatible(cap,materials){return materials.filter(m=>thicknesses(cap,m).length);}
  function reason(cap,material){return thicknesses(cap,material).length?'':I18n.t("No hay geometría verificada para este material y espesor.");}
  function offset(cap,mode,axis,physical){if(!Object.hasOwn(modes,mode))throw Error(I18n.t("Modo de tamaño inválido."));if(mode==='manufacturing')return 0;if(cap.onlyManufacturing)throw Error(I18n.t("Este modelo solo admite dimensiones de manufactura."));const selected=profile(cap,physical);const value=selected?.offsets?.[mode]?.[axis];if(!Number.isFinite(value))throw Error(I18n.t("Conversión de tamaño no verificada para este espesor."));return value;}
  function display(cap,dims,mode,physical){return Object.fromEntries(Object.entries(dims).map(([a,v])=>[a,v+offset(cap,mode,a,physical)]));}
  function manufacture(cap,dims,mode,physical){const result=Object.fromEntries(Object.entries(dims).map(([a,v])=>[a,v-offset(cap,mode,a,physical)]));if(Object.values(result).some(v=>!Number.isFinite(v)||v<=0))throw Error(I18n.t("Introduce dimensiones positivas y válidas."));return result;}
  function validate(cap,materials,physical){const material=materials.find(m=>sameId(m.id,physical.materialId));if(!material)throw Error(I18n.t("Material desconocido."));if(!Number.isFinite(physical.thickness))throw Error(I18n.t("Introduce un espesor válido."));if(!thicknesses(cap,material).some(t=>Math.abs(t-physical.thickness)<epsilon))throw Error(I18n.t("Selecciona un espesor verificado para este material."));return material;}
  function modelFor(model,physical){const p=profile(model.materialCapability,physical);if(!p)throw Error(I18n.t("Selecciona un espesor verificado para este material."));if(p.original)return model;const bounds=p.bounds||Object.fromEntries(Object.entries(model.dims).map(([a,v])=>[a,[v,v]]));return {...model,layer:p.layer,rule:p.rule||{},engine:p.engine||(p.rule?'derived':null),bounds};}
  function generate(model,dims,physical,materials){validate(model.materialCapability,materials,physical);const selected=modelFor(model,physical);for(const [axis,value] of Object.entries(dims)){const b=selected.bounds?.[axis];if(b&&(value<b[0]-epsilon||(b[1]!=null&&value>b[1]+epsilon)))throw Error(I18n.t("Las medidas están fuera del rango verificado para este espesor."));}return root.TroquelEngines.generate(selected,dims,physical);}
  root.TroquelMaterials={modes,display,manufacture,limits,reason,validate,generate,profiles,profile,thicknesses,compatible,modelFor};
  if(typeof module!=='undefined')module.exports=root.TroquelMaterials;
})(globalThis);
