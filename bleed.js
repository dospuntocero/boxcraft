/* Outer bleed from the union of panels. Coordinates and offset are in millimetres. */
(function(root){
  const cache=new WeakMap(),scale=10000;
  function contours(layer){
    if(cache.has(layer))return cache.get(layer);
    const paths=[];
    // Some models only expose the outer cut; when the panel faces do not cover
    // the full blank (for example the bottom glue strip), offset the cut itself.
    const sources=layer.bleedFromCuts&&layer.cuts?[layer.cuts]:layer.faces.map(face=>face.dlist);
    for(const dlist of sources){
      let points=[],last=null;
      const finish=()=>{if(points.length>2){const p=ClipperLib.Clipper.CleanPolygon(points,2);if(!ClipperLib.Clipper.Orientation(p))p.reverse();paths.push(p);}points=[];};
      const add=(x,y)=>points.push({X:Math.round(x*scale),Y:Math.round(y*scale)});
      for(const c of dlist){
        if(c.mtd==='M'){finish();add(c.x,c.y);last=c;}
        else if(c.mtd==='L'){add(c.x,c.y);last=c;}
        else if(c.mtd==='A'){
          const arc=document.createElementNS('http://www.w3.org/2000/svg','path');
          arc.setAttribute('d',`M${last.x} ${last.y} A${Math.abs(c.rx)} ${Math.abs(c.ry)} ${c.ang} ${Math.round(c.arc)} ${Math.round(c.dir)} ${c.x} ${c.y}`);
          const length=arc.getTotalLength(),steps=Math.max(1,Math.ceil(length/.1));
          for(let i=1;i<=steps;i++){const p=arc.getPointAtLength(length*i/steps);add(p.x,p.y);}last=c;
        }else if(c.mtd==='Z')finish();
      }
      finish();
    }
    const union=new ClipperLib.Clipper(),merged=[];
    union.AddPaths(paths,ClipperLib.PolyType.ptSubject,true);
    union.Execute(ClipperLib.ClipType.ctUnion,merged,ClipperLib.PolyFillType.pftNonZero,ClipperLib.PolyFillType.pftNonZero);
    // Only outside boundaries receive bleed; windows and internal slots stay cut lines.
    const outer=merged.filter(p=>ClipperLib.Clipper.Orientation(p));
    const offset=new ClipperLib.ClipperOffset(2,.01*scale),result=[];
    offset.AddPaths(outer,ClipperLib.JoinType.jtRound,ClipperLib.EndType.etClosedPolygon);
    offset.Execute(result,3*scale);
    const d=result.map(p=>'M'+p.map(v=>`${v.X/scale} ${v.Y/scale}`).join('L')+'Z').join('');
    cache.set(layer,d);return d;
  }
  root.TroquelBleed={contours};
})(globalThis);
