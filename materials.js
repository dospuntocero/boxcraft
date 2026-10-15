(function(root){
  'use strict';
  const I18n=root.I18n||{t:key=>key,locale:'es-CL'};
  const modes={get manufacturing(){return I18n.t("Dimensiones de manufactura");},get inner(){return I18n.t("Dimensiones internas");},get outer(){return I18n.t("Dimensiones externas");}};
  function offset(cap,mode,axis){if(!Object.hasOwn(modes,mode))throw Error(I18n.t("Modo de tamaño inválido."));if(mode!=='manufacturing'&&cap.onlyManufacturing)throw Error(I18n.t("Este modelo solo admite dimensiones de manufactura."));return mode==='manufacturing'?0:cap.offsets[mode][axis];}
  function display(cap,dims,mode){return Object.fromEntries(Object.entries(dims).map(([a,v])=>[a,v+offset(cap,mode,a)]));}
  function manufacture(cap,dims,mode){const result=Object.fromEntries(Object.entries(dims).map(([a,v])=>[a,v-offset(cap,mode,a)]));if(Object.values(result).some(v=>!Number.isFinite(v)||v<=0))throw Error(I18n.t("Introduce dimensiones positivas y válidas."));return result;}
  function limits(cap,material){return [Math.max(material.min,cap.observedThicknessLimits[0]),Math.min(material.max,cap.observedThicknessLimits[1])];}
  function reason(cap,material){const [lo,hi]=limits(cap,material);if(lo>hi)return I18n.t("El espesor del material no es compatible con el límite observado del modelo.");if(material.id!==cap.originalMaterialId)return cap.blockedReason;return '';}
  function validate(cap,materials,physical){const material=materials.find(m=>m.id===physical.materialId);if(!material)throw Error(I18n.t("Material desconocido."));const blocked=reason(cap,material);if(blocked)throw Error(blocked);if(!Number.isFinite(physical.thickness))throw Error(I18n.t("Introduce un espesor válido."));const [lo,hi]=limits(cap,material);if(physical.thickness<lo-1e-8||physical.thickness>hi+1e-8)throw Error(`${I18n.t("Espesor permitido por el material:")} ${lo}–${hi} mm.`);const [verifiedLo,verifiedHi]=cap.verifiedThicknessRange;if(physical.thickness<verifiedLo-1e-8||physical.thickness>verifiedHi+1e-8)throw Error(cap.blockedReason);return material;}
  function generate(model,dims,physical,materials){validate(model.materialCapability,materials,physical);return root.TroquelEngines.generate(model,dims,physical);}
  root.TroquelMaterials={modes,display,manufacture,limits,reason,validate,generate};
  if(typeof module!=='undefined')module.exports=root.TroquelMaterials;
})(globalThis);
