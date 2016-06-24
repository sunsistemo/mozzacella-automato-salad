var CA=function(t){function e(r){if(n[r])return n[r].exports;var o=n[r]={exports:{},id:r,loaded:!1};return t[r].call(o.exports,o,o.exports,e),o.loaded=!0,o.exports}var n={};return e.m=t,e.c=n,e.p="",e(0)}([function(t,e,n){"use strict";function r(t,e,n){for(var r={},o=2*t+1,i=(0,v.reverse)((0,v.zfill)(n.toString(e),Math.pow(e,o))),a=0;a<Math.pow(e,o);a++)r[(0,v.zfill)(a.toString(e),o)]=parseInt(i[a]);return r}function o(t,e){for(var n=s,r=Array(n.length),o=0;o<e;o++)r[o]=String(t[n.slice(-e+o)+n.slice(0,e+o+1)]);for(var i=e;i<n.length-e;i++)r[i]=String(t[n.slice(i-e,i+e+1)]);for(var a=1;a<e+1;a++)r[n.length-a]=String(t[n.slice(-e-a)+n.slice(0,-a+e+1)]);s=r.join("")}function i(t,e){var n=(0,v.range)(e).map(String);s=(0,v.range)(t).map(function(){return(0,v.choice)(n)}).join("")}function u(t){t[0]=s;for(var e=1;e<t.length;e++)o(S,p),t[e]=s;return t}function l(t){if(2==t)B={0:"#e3e5e3",1:"rgba(0, 0, 0, 1.0)"};else if(3==t)B={0:"rgba(200, 0, 0, 1.0)",1:"rgba(0, 200, 0, 1.0)",2:"rgba(0, 0, 200, 1.0)"};else if(4==t)B={0:"#00BFFF",1:"#C000FF",2:"#FF4000",3:"#40FF00"};else{B={};var e=!0,n=!1,r=void 0;try{for(var o,i=(0,v.range)(t)[Symbol.iterator]();!(e=(o=i.next()).done);e=!0){var u=o.value,l=void 0,f=void 0,g=void 0;l=(0,v.randint)(0,255).toString(),f=(0,v.randint)(0,255).toString(),g=(0,v.randint)(0,255).toString(),B[String(u)]="rgba("+a+","+b+","+u+")"}}catch(d){n=!0,r=d}finally{try{!e&&i["return"]&&i["return"]()}finally{if(n)throw r}}}}function f(t,e,n,r){for(var i=Math.round(.9*w),a=0;a<e.length;a++)for(var u=0;u<s.length;u++)t.fillStyle=B[e[a][u]],t.fillRect(u*w,a*w,i,i);for(var l=e,g=0;g<e.length-1;g++)e[g]=l[g+1];r===!0&&j.push(s[0]),o(S,p),e[e.length-1]=s,A.indexOf(n)>-1&&window.setTimeout(f,100,t,e,n,r)}function g(){A.pop();var t=document.getElementById("input_rule");x=parseInt(t.value);var e=document.getElementById("input_states");y=parseInt(e.value);var n=document.getElementById("input_neighbours");p=parseInt(n.value);var o=document.getElementById("input_random");if(I=o.checked){var a=Math.pow(y,Math.pow(y,2*p+1));x=(0,v.randint)(0,a),t.value=x.toString()}var g=String((new Date).getTime());A.push(g),S=r(p,y,x),l(y),i(M,y),_=u(_),f(m,_,g)}function d(){A.pop();var t=String((new Date).getTime());A.push(t),p=1,y=2,x=30,S=r(p,y,x),i(M,y),F=u(F),j=[],D=[],T=0,l(y),f(E,F,t,!0),c(t)}function c(t){var e=j.join(""),n=D.slice(Math.max(0,D.length-32)).join(", ");if(j.length>=8){var r=parseInt(e,2);D.push(r),T+=r,j=[]}z.textContent=e,O.textContent=n,k.textContent=D.length.toString(),P.textContent=(T/D.length).toString(),A.indexOf(t)>-1&&window.setTimeout(c,100,t)}var v=n(1),s=void 0,h=document.getElementById("1D_CA"),m=h.getContext("2d"),p=void 0,y=void 0,x=void 0,S=void 0,I=void 0,w=10,M=Math.floor(h.width/w),_=Array(Math.floor(h.height/w)),A=[];y=2;var B=void 0;l(y),g();var C=document.getElementById("CA_bits"),E=C.getContext("2d"),F=(Math.floor(C.width/w),Array(Math.floor(C.height/w))),j=[],D=[],T=0,z=document.getElementById("span_bits"),O=document.getElementById("span_nums"),k=document.getElementById("bytes"),P=document.getElementById("mean");t.exports={start_1D_CA:g,start_bits:d}},function(t,e,n){"use strict";function r(t){if(Array.isArray(t)){for(var e=0,n=Array(t.length);e<t.length;e++)n[e]=t[e];return n}return Array.from(t)}function o(t,e){return f(t,e,"0")}function i(t){return[].concat(r(t)).reverse().join("")}function a(t,e){return t+Math.floor(Math.random()*(e-t))}function u(t){return t[a(0,t.length)]}function l(t,e){e||(e=t,t=0);for(var n=Array(e-t),r=0;r<e-t;r++)n[r]=t+r;return n}Object.defineProperty(e,"__esModule",{value:!0}),e.zfill=o,e.reverse=i,e.randint=a,e.choice=u,e.range=l;var f=n(2)},function(t,e){"use strict";function n(t,e,n){if(t+="",e-=t.length,e<=0)return t;if(n||0===n||(n=" "),n+=""," "===n&&e<10)return r[e]+t;for(var o="";;){if(1&e&&(o+=n),e>>=1,!e)break;n+=n}return o+t}t.exports=n;var r=[""," ","  ","   ","    ","     ","      ","       ","        ","         "]}]);