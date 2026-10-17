(function(root){
  'use strict';
  const catalogs=root.TallerLocales;
  const supported=['es','en'];
  let language='es';
  try{const saved=localStorage.getItem('taller.language');language=supported.includes(saved)?saved:(navigator.language||'es').split('-')[0];}catch{}
  if(!supported.includes(language))language='es';
  function t(key,values={}){
    const message=catalogs[language]?.[key]??catalogs.es[key]??key;
    return String(message).replace(/\{(\w+)\}/g,(match,name)=>Object.hasOwn(values,name)?String(values[name]):match);
  }
  function apply(scope=document){
    scope.querySelectorAll('[data-i18n]').forEach(el=>{el.textContent=t(el.dataset.i18n);});
    for(const attr of ['aria-label','title','alt','placeholder','content']){
      scope.querySelectorAll(`[data-i18n-${attr}]`).forEach(el=>el.setAttribute(attr,t(el.getAttribute(`data-i18n-${attr}`))));
    }
    document.documentElement.lang=language;
    document.querySelectorAll('[data-language]').forEach(button=>{
      const active=button.dataset.language===language;
      button.classList.toggle('active',active);
      button.setAttribute('aria-pressed',String(active));
    });
  }
  function setLanguage(next){
    if(!supported.includes(next))return;
    language=next;try{localStorage.setItem('taller.language',next);}catch{}
    apply();document.dispatchEvent(new CustomEvent('languagechange',{detail:{language}}));
  }
  // Keep catalog records numeric and identifiers stable while localizing their display fields.
  function fields(record,names){
    for(const name of names){const key=record[name];if(typeof key==='string')Object.defineProperty(record,name,{enumerable:true,configurable:true,get:()=>t(key)});}
    return record;
  }
  root.I18n={t,apply,setLanguage,fields,get language(){return language;},get locale(){return language==='es'?'es-CL':'en-US';}};
  apply();
  document.querySelectorAll('[data-language]').forEach(button=>{
    button.addEventListener('click',()=>setLanguage(button.dataset.language));
  });
})(globalThis);
