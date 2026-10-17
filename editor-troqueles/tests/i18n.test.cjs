const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const dist=path.join(__dirname,'../dist');
function load(language='es-CL'){
 const saved=new Map(),events=[];
 const ctx=vm.createContext({navigator:{language},localStorage:{getItem:k=>saved.get(k),setItem:(k,v)=>saved.set(k,v)},document:{querySelectorAll:()=>[],documentElement:{},getElementById:()=>({addEventListener(){}}),dispatchEvent:e=>events.push(e)},CustomEvent:class{constructor(type,options){this.type=type;this.detail=options.detail;}}});
 for(const file of ['locales/es.js','locales/en.js','i18n.js','engines.js','materials.js'])vm.runInContext(fs.readFileSync(path.join(dist,file),'utf8'),ctx);
 return {ctx,saved,events};
}
test('all UI keys and catalog display fields exist in both languages',()=>{
 const {ctx}=load(),{es,en}=ctx.TallerLocales;
 assert.deepEqual(Object.keys(es).sort(),Object.keys(en).sort());
 for(const file of ['app.js','engines.js','dimensions.js','materials.js','index.html']){
  const source=fs.readFileSync(path.join(dist,file),'utf8');
  for(const match of source.matchAll(/I18n\.t\(["']([^"']+)["']\)|data-i18n(?:-[\w-]+)?="([^"]+)"/g))assert.ok(Object.hasOwn(en,match[1]||match[2]),`${file}: ${match[1]||match[2]}`);
 }
 for(const [file,fields] of [['modelos.json',['name','category']],['materiales.json',['name','group']],['capacidades-materiales.json',['blockedReason']]]){
  const data=JSON.parse(fs.readFileSync(path.join(dist,'assets',file),'utf8'));
  for(const record of Array.isArray(data)?data:data.materials||Object.values(data))for(const field of fields)assert.ok(Object.hasOwn(en,record[field]),`${file}: ${record[field]}`);
 }
});
test('switching language updates display getters and validation without changing identifiers',()=>{
 const {ctx,saved,events}=load(),i=ctx.I18n,record=i.fields({id:153,name:'Personalizado: papel arte'},['name']);
 assert.equal(record.name,'Personalizado: papel arte');i.setLanguage('en');
 assert.equal(record.name,'Custom: art paper');assert.equal(record.id,153);
 assert.equal(i.locale,'en-US');assert.equal(saved.get('taller.language'),'en');assert.equal(events[0].type,'languagechange');
 assert.equal(ctx.TroquelMaterials.modes.inner,'Inner dimensions');
 assert.throws(()=>ctx.TroquelEngines.sheetYield(-1,10,[100,100]),/Invalid sheet dimensions/);
 i.setLanguage('es');assert.equal(record.name,'Personalizado: papel arte');assert.equal(ctx.TroquelMaterials.modes.inner,'Dimensiones internas');
});
test('language detection, unsupported languages and interpolation have predictable fallback',()=>{
 assert.equal(load('en-GB').ctx.I18n.language,'en');assert.equal(load('fr-FR').ctx.I18n.language,'es');
 const {ctx}=load();ctx.I18n.setLanguage('xx');assert.equal(ctx.I18n.language,'es');assert.equal(ctx.I18n.t('unknown'),'unknown');
 ctx.TallerLocales.es.example='Modelo {id}';assert.equal(ctx.I18n.t('example',{id:42}),'Modelo 42');
});
