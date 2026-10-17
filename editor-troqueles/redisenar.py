from pathlib import Path
import json
p=Path(__file__).parent/'dist'
models=json.loads((p/'assets/modelos.json').read_text())
for m in models:
    L,W,H=m['dims']['L'],m['dims']['W'],m['dims'].get('H',65)
    h=max(30,min(112,100*H/L)); y=175-h
    color='#c5a779' if 'Onda' in m['material'] else '#d6c8b4'
    top=f'<path d="M45 {y}l65-30 95 22-65 30z" fill="#e7d5b6"/>'
    if m['id']=='150010':
        h=40;y=135
        top='<path d="M45 135l18-90 102-22 40 104-65 30z" fill="#e1c99e"/><path d="M63 45l102-22 32 83-118 27z" fill="#edddbf"/><path d="M45 135l65-30 95 22-65 30z" fill="#ad8a56"/>'
    if m['id'] in ['112047','12109002','112310']:
        top=f'<path d="M45 {y}l40-35 55 27 65-22-35-35-85 30" fill="#e7d5b6"/><path d="M90 {y-24}v-16q0-12 15-12h25q15 0 15 12v16h-12v-14h-30v14z" fill="{color}" fill-rule="evenodd"/>'
    front=f'<path d="M45 {y}l95 22v{h}l-95-22z" fill="{color}"/>'
    side=f'<path d="M140 {y+22}l65-30v{h}l-65 30z" fill="#ad936e"/>'
    if m['id']=='180320':
        top='<path d="M45 170l65-105 95 105-65 25z" fill="#d1b388"/><path d="M70 157l43-69 60 69-34 17z" fill="#eff6f7" stroke="#b69b73" stroke-width="3"/>';front='<path d="M45 170l95 25v15l-95-25z" fill="#b79a71"/>';side='<path d="M140 195l65-25v15l-65 25z" fill="#9e8159"/>'
    if m['id']=='180370':
        top='<path d="M48 75l60-28 96 28-65 29z" fill="#9f7950"/>';front='<path d="M48 75q45 45 91 29l-10 94-60-14z" fill="#dbc19c"/>';side='<path d="M139 104l65-29-25 101-50 22z" fill="#b59569"/>'
    if m['id']=='10002003':
        top+=f'<path d="M110 {y-30}v-30l95 22v30z" fill="#d6c8b4"/><path d="M143 {y-43}l27 6" stroke="#7d6d56" stroke-width="6" stroke-linecap="round"/>'
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 240"><ellipse cx="128" cy="211" rx="85" ry="13" fill="#000" opacity=".07"/>{front}{side}{top}<path d="M64 {y+42}l51 12" stroke="#fff" stroke-width="2" opacity=".5"/></svg>'
    (p/f'assets/{m["id"]}-caja.svg').write_text(svg)
h=(p/'index.html').read_text().replace('<span>Básico</span>','<span>Medidas</span>')
h=h.replace('<div class="panel-heading"><div><span class="eyebrow">TU BIBLIOTECA</span><h1>Modelos</h1></div>', '<div class="panel-heading"><div><span class="eyebrow">SELECCIONA UNA ESTRUCTURA</span><h1>Biblioteca</h1></div>')
h=h.replace('<div class="model-mini">','<div class="model-mini"><span class="preview-label">Vista ilustrativa</span>')
h=h.replace('Vista general del troquel seleccionado','Ilustración de la caja seleccionada')
h=h.replace('<div class="dimension-summary">','<div class="dimension-summary">')
h=h.replace('<div id="viewport"', '<div class="box-dimensions" id="boxDimensions" aria-label="Medidas de la caja"></div><div id="viewport"')
h=h.replace('<span class="canvas-scale">Unidad del archivo: mm</span>', '<span class="canvas-scale">Unidad del archivo: mm</span>')
h=h.replace('</button></div><span class="canvas-scale">','</button><i></i><button id="toggleDimensions" aria-label="Mostrar u ocultar cotas" title="Cotas" aria-pressed="true"><span data-icon="ruler"></span></button><button id="toggleLayers" aria-label="Opciones del plano" title="Opciones del plano" aria-expanded="false"><span data-icon="layers"></span></button></div><span class="canvas-scale">')
h=h.replace('<section class="inspector-card"><div class="card-title"><h3>Capas del plano', '<section class="inspector-card layer-panel" id="layerPanel"><div class="card-title"><h3>Capas del plano')
h=h.replace('Conserva las medidas reales y las capas que tienes visibles.','Plano a escala real con líneas de corte y pliegue. Elige las capas que quieres incluir.')
(p/'index.html').write_text(h)
j=(p/'app.js').read_text()
j=j.replace('src="assets/${m.id}.svg" alt="Plano de ${m.name}"','src="assets/${m.id}-caja.svg" alt="Ilustración de ${m.name}"')
j=j.replace('`assets/${id}.svg`','`assets/${id}-caja.svg`').replace('`Plano de ${m.name}`','`Ilustración de ${m.name}`')
j=j.replace("$('#sheetSize').textContent=", "$('#boxDimensions').innerHTML=Object.entries(state.dims).map(([axis,v])=>`<span><small>${{L:'Longitud',W:'Anchura',H:'Altura'}[axis]}</small><strong>${format(v/factor,state.unit==='in'?4:2)} <em>${state.unit}</em></strong></span>`).join('');$('#boxDimensions').hidden=!state.settings.dimensions;$('#toggleDimensions').setAttribute('aria-pressed',state.settings.dimensions);$('#sheetSize').textContent=")
j+="\n$('#toggleDimensions').addEventListener('click',()=>{state.settings.dimensions=!state.settings.dimensions;$('#showDimensions').checked=state.settings.dimensions;renderCanvas();});\n$('#toggleLayers').addEventListener('click',()=>{const open=$('#layerPanel').classList.toggle('floating');$('#toggleLayers').setAttribute('aria-expanded',open);});\ndocument.addEventListener('keydown',e=>{if(e.key==='Escape'){$('#layerPanel').classList.remove('floating');$('#toggleLayers').setAttribute('aria-expanded','false');}});\n"
(p/'app.js').write_text(j)
with (p/'styles.css').open('a') as f:
    f.write('''
/* Biblioteca y editor: lienzo permanente, panel contextual y herramientas. */
:root{--blue:#0878ff;background:#eeeeef;color:#242424}.topbar{height:64px;padding:0 24px}.workspace{height:calc(100dvh - 64px);padding:22px 20px;grid-template-columns:320px minmax(300px,1fr) 252px;gap:24px;background:#eeeeef}.left-panel{border:0;border-radius:18px;box-shadow:0 5px 22px #00000009}.rail{width:80px;padding-top:18px}.rail-tab{width:66px;font-size:11px;height:80px}.rail-tab.active{background:transparent}.rail-tab.active:before{display:none}.sidebar-view{padding:23px 14px 0}.model-card .thumbnail{height:114px;background:#f4f4f5;border-radius:8px}.model-card img{width:100%;height:100%;mix-blend-mode:normal}.model-card-name{font-size:11px}.model-grid{gap:18px 10px}.panel-heading h1{font-size:20px}.search{height:40px}.search input,.category-label select{font-size:12px}.canvas-meta{flex-direction:column;gap:18px;padding-top:20px}.legend{font-size:11px}.dimension-summary{text-align:left}.dimension-summary>span{font-size:9px;letter-spacing:.6px}.dimension-summary strong{font-size:13px}.canvas-top{padding-top:0}.box-dimensions{display:flex;gap:25px;padding:17px 8px 0;flex-wrap:wrap}.box-dimensions span{display:flex;flex-direction:column;gap:5px}.box-dimensions small{font-size:10px;color:#868b92}.box-dimensions strong{font-size:14px;font-weight:500;color:#0878ff}.box-dimensions em{font-style:normal;font-size:11px}.artboard{padding:15px 8px}.canvas-toolbar{height:46px;padding:5px 8px;border:0;border-radius:8px;box-shadow:0 3px 14px #00000008}.canvas-toolbar button{width:32px;height:34px}.canvas-toolbar button[aria-pressed=true]{background:#edf4ff;color:var(--blue)}.canvas-toolbar svg{width:18px;height:18px}.canvas-bottom{height:52px}.canvas-hint,.canvas-scale{font-size:9px}.model-mini{position:relative;height:190px;background:linear-gradient(#dedddd,#efefef);margin:14px -17px 16px;border-radius:0}.model-mini img{height:180px;width:100%;mix-blend-mode:normal}.preview-label{position:absolute;top:10px;left:12px;font-size:9px;color:#787878}.inspector-card{border:0;border-radius:16px;padding:20px 18px}.model-info{overflow:hidden}.info-title h2{font-size:15px}.model-number{font-size:10px}.basic-view{padding:24px 17px}.field-input{height:40px}.field-input input{font-size:14px}.field-label{font-size:11px}.section-title h3,.setting-block h3{font-size:13px}.model-notice{font-size:11px}.material-card strong{font-size:12px}.material-card small{font-size:9px}.layer-control{font-size:12px}.layer-panel.floating{position:fixed;bottom:90px;left:50%;width:250px;z-index:5;box-shadow:0 8px 35px #0002;border:1px solid #e3e5e8}.export-card p{font-size:12px}.export-note{font-size:9px}.export-secondary{height:40px;font-size:12px}.count{font-size:11px}.eyebrow{font-size:8px}
@media(max-width:1150px){.workspace{grid-template-columns:300px minmax(260px,1fr) 218px;gap:14px;padding:18px 14px}.rail{width:68px}.rail-tab{width:56px}.model-card .thumbnail{height:105px}.box-dimensions{gap:18px}.canvas-hint,.canvas-scale{display:none}}
@media(max-width:950px){.workspace{grid-template-columns:300px minmax(260px,1fr)}.right-panel{display:none}.right-panel:has(.floating){display:block;position:absolute}.right-panel:has(.floating)>.inspector-card:not(.floating){display:none}}
@media(max-width:650px){.workspace{height:auto;display:flex;padding:12px;min-height:calc(100dvh - 64px)}.left-panel{height:310px}.rail{width:65px}.rail-tab{width:53px;height:75px}.sidebar-view{padding:17px 13px}.model-card{width:115px}.canvas-area{height:620px}.canvas-meta{padding-top:14px;gap:12px}.box-dimensions{padding-top:12px}.box-dimensions strong{font-size:13px}.canvas-toolbar{margin:auto}.layer-panel.floating{left:50%;transform:translateX(-50%);bottom:65px}.basic-view{padding:16px}.basic-view .model-notice{font-size:9px}.field-input{height:36px}}
''')
