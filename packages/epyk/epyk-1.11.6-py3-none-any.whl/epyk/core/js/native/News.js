function news(e,d,b){var c=document.createElement("p");c.style.margin="0 0 5px 0";if(b.showdown){var h=new showdown.Converter(b.showdown);d=h.makeHtml(d.trim());};c.innerHTML=d;e.prepend(c);if(b.dated){var f=new Date();var g=moment(f).format('YYYY-MM-DD HH:mm:ss');var a=document.createElement("p");a.style.margin=0;a.style.fontWeight='bold';a.innerHTML=g;e.prepend(a);}}