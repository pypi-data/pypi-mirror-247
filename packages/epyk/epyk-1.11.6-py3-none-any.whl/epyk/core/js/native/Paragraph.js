function paragraph(c,b,a){if(a.templateMode=='loading'){b=a.templateLoading(b);}else if(a.templateMode=='error'){b=a.templateError(b);}else if(typeof a.template!=='undefined'&&b){b=a.template(b);}if(typeof a.reset==='undefined'||a.reset){c.innerHTML='';};if(typeof b==='string'||b instanceof String){b=b.split('\\n');};if(typeof b!=='undefined'){b.forEach(function(d,f){if(a.showdown){var e=new showdown.Converter(a.showdown);d=e.makeHtml(d).replace("<p>","<p style='margin:0'>");}var b=document.createElement('p');b.style.margin=0;b.innerHTML=d;c.appendChild(b);});}if(typeof a.css!=='undefined'){for(var d in a.css){c.style[d]=a.css[d];}}}