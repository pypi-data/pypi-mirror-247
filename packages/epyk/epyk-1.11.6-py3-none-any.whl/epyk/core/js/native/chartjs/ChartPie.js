function chartPie(c,a){if(c.python){result={datasets:[],labels:c.labels};c.datasets.forEach(function(b,c){if(typeof b.backgroundColor==="undefined"){b.backgroundColor=a.background_colors;};if(typeof b.borderColor==="undefined"){b.borderColor=a.colors;};if(typeof b.hoverBackgroundColor==="undefined"){b.hoverBackgroundColor=a.background_colors;};if(typeof a.commons!=="undefined"){Object.assign(b,a.commons);};result.datasets.push(b);});}else{var b={};var d=[];var e={};a.y_columns.forEach(function(a){b[a]={};});c.forEach(function(c){a.y_columns.forEach(function(f){if(c[f]!==undefined){if(!(c[a.x_axis]in e)){d.push(c[a.x_axis]);e[c[a.x_axis]]=true;};b[f][c[a.x_axis]]=c[f];}});});result={datasets:[],labels:d};a.y_columns.forEach(function(c,f){dataSet={label:c,data:[],backgroundColor:a.background_colors,type:a.type,borderColor:a.colors,hoverBackgroundColor:a.colors};if((typeof a.props!=='undefined')&&(typeof a.props[c]!=='undefined')){for(var e in a.props[c]){dataSet[e]=a.props[c][e];}}else if((typeof a.props!=='undefined')&&(typeof a.props[f]!=='undefined')){for(var e in a.props[f]){dataSet[e]=a.props[f][e];}}else if(typeof a.commons!=='undefined'){for(var e in a.commons){dataSet[e]=a.commons[e];};}d.forEach(function(d,e){dataSet.backgroundColor.push(a.colors);if(b[c][d]==undefined){dataSet.data.push(null);}else{dataSet.data.push(b[c][d]);}});if((typeof a.datasets!=='undefined')&&(typeof a.datasets[c]!=='undefined')){dataSet=Object.assign(dataSet,a.datasets[c]);}result.datasets.push(dataSet);});if(typeof a.labels!=="undefined"){result.labels=a.labels;}};return result;}