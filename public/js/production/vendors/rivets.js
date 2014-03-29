(function(){var e,t,n,r,i=function(e,t){return function(){return e.apply(t,arguments)}},s=[].indexOf||function(e){for(var t=0,n=this.length;t<n;t++)if(t in this&&this[t]===e)return t;return-1},o=[].slice,u={}.hasOwnProperty,a=function(e,t){function r(){this.constructor=e}for(var n in t)u.call(t,n)&&(e[n]=t[n]);return r.prototype=t.prototype,e.prototype=new r,e.__super__=t.prototype,e};e={binders:{},components:{},formatters:{},adapters:{},config:{prefix:"rv",templateDelimiters:["{","}"],rootInterface:".",preloadData:!0,handler:function(e,t,n){return this.call(e,t,n.view.models)}}},"jQuery"in window?(r="on"in jQuery?["on","off"]:["bind","unbind"],t=r[0],n=r[1],e.Util={bindEvent:function(e,n,r){return jQuery(e)[t](n,r)},unbindEvent:function(e,t,r){return jQuery(e)[n](t,r)},getInputValue:function(e){var t;return t=jQuery(e),t.attr("type")==="checkbox"?t.is(":checked"):t.val()}}):e.Util={bindEvent:function(){return"addEventListener"in window?function(e,t,n){return e.addEventListener(t,n,!1)}:function(e,t,n){return e.attachEvent("on"+t,n)}}(),unbindEvent:function(){return"removeEventListener"in window?function(e,t,n){return e.removeEventListener(t,n,!1)}:function(e,t,n){return e.detachEvent("on"+t,n)}}(),getInputValue:function(e){var t,n,r,i;if(e.type==="checkbox")return e.checked;if(e.type==="select-multiple"){i=[];for(n=0,r=e.length;n<r;n++)t=e[n],t.selected&&i.push(t.value);return i}return e.value}},e.View=function(){function t(t,n,r){var s,o,u,a,f,l,c,h,p;this.els=t,this.models=n,this.options=r!=null?r:{},this.update=i(this.update,this),this.publish=i(this.publish,this),this.sync=i(this.sync,this),this.unbind=i(this.unbind,this),this.bind=i(this.bind,this),this.select=i(this.select,this),this.build=i(this.build,this),this.componentRegExp=i(this.componentRegExp,this),this.bindingRegExp=i(this.bindingRegExp,this),this.els.jquery||this.els instanceof Array||(this.els=[this.els]),c=["config","binders","formatters","adapters"];for(f=0,l=c.length;f<l;f++){o=c[f],this[o]={};if(this.options[o]){h=this.options[o];for(s in h)u=h[s],this[o][s]=u}p=e[o];for(s in p)u=p[s],(a=this[o])[s]==null&&(a[s]=u)}this.build()}return t.prototype.bindingRegExp=function(){return new RegExp("^"+this.config.prefix+"-")},t.prototype.componentRegExp=function(){return new RegExp("^"+this.config.prefix.toUpperCase()+"-")},t.prototype.build=function(){var t,n,r,i,o,u,a,f,l,c=this;this.bindings=[],u=[],t=this.bindingRegExp(),r=this.componentRegExp(),n=function(t,n,r,i){var s,o,u,a,f,l,h;f={},h=function(){var e,t,n,r;n=i.split("|"),r=[];for(e=0,t=n.length;e<t;e++)l=n[e],r.push(l.trim());return r}(),s=function(){var e,t,n,r;n=h.shift().split("<"),r=[];for(e=0,t=n.length;e<t;e++)o=n[e],r.push(o.trim());return r}(),a=s.shift(),f.formatters=h;if(u=s.shift())f.dependencies=u.split(/\s+/);return c.bindings.push(new e[t](c,n,r,a,f))},o=function(i){var a,f,l,h,p,d,v,m,g,y,b,w,E,S,x,T,N,C,k,L,A,O,M,_,D,P,H,B,j,F;if(s.call(u,i)<0){if(i.nodeType===3){m=e.TextTemplateParser;if(p=c.config.templateDelimiters)if((w=m.parse(i.data,p)).length)if(w.length!==1||w[0].type!==m.types.text){for(x=0,k=w.length;x<k;x++)b=w[x],y=document.createTextNode(b.value),i.parentNode.insertBefore(y,i),b.type===1&&n("TextBinding",y,null,b.value);i.parentNode.removeChild(i)}}else if(r.test(i.tagName))E=i.tagName.replace(r,"").toLowerCase(),c.bindings.push(new e.ComponentBinding(c,i,E));else if(i.attributes!=null){D=i.attributes;for(T=0,L=D.length;T<L;T++){a=D[T];if(t.test(a.name)){E=a.name.replace(t,"");if(!(l=c.binders[E])){P=c.binders;for(d in P)S=P[d],d!=="*"&&d.indexOf("*")!==-1&&(g=new RegExp("^"+d.replace("*",".+")+"$"),g.test(E)&&(l=S))}l||(l=c.binders["*"]);if(l.block){H=i.childNodes;for(N=0,A=H.length;N<A;N++)v=H[N],u.push(v);f=[a]}}}B=f||i.attributes;for(C=0,O=B.length;C<O;C++)a=B[C],t.test(a.name)&&(E=a.name.replace(t,""),n("Binding",i,E,a.value))}j=function(){var e,t,n,r;n=i.childNodes,r=[];for(t=0,e=n.length;t<e;t++)v=n[t],r.push(v);return r}(),F=[];for(_=0,M=j.length;_<M;_++)h=j[_],F.push(o(h));return F}},l=this.els;for(a=0,f=l.length;a<f;a++)i=l[a],o(i)},t.prototype.select=function(e){var t,n,r,i,s;i=this.bindings,s=[];for(n=0,r=i.length;n<r;n++)t=i[n],e(t)&&s.push(t);return s},t.prototype.bind=function(){var e,t,n,r,i;r=this.bindings,i=[];for(t=0,n=r.length;t<n;t++)e=r[t],i.push(e.bind());return i},t.prototype.unbind=function(){var e,t,n,r,i;r=this.bindings,i=[];for(t=0,n=r.length;t<n;t++)e=r[t],i.push(e.unbind());return i},t.prototype.sync=function(){var e,t,n,r,i;r=this.bindings,i=[];for(t=0,n=r.length;t<n;t++)e=r[t],i.push(e.sync());return i},t.prototype.publish=function(){var e,t,n,r,i;r=this.select(function(e){return e.binder.publishes}),i=[];for(t=0,n=r.length;t<n;t++)e=r[t],i.push(e.publish());return i},t.prototype.update=function(e){var t,n,r,i,s,o,u;e==null&&(e={});for(n in e)r=e[n],this.models[n]=r;o=this.bindings,u=[];for(i=0,s=o.length;i<s;i++)t=o[i],u.push(t.update(e));return u},t}(),e.Binding=function(){function t(e,t,n,r,s){this.view=e,this.el=t,this.type=n,this.keypath=r,this.options=s!=null?s:{},this.update=i(this.update,this),this.unbind=i(this.unbind,this),this.bind=i(this.bind,this),this.publish=i(this.publish,this),this.sync=i(this.sync,this),this.set=i(this.set,this),this.eventHandler=i(this.eventHandler,this),this.formattedValue=i(this.formattedValue,this),this.setBinder=i(this.setBinder,this),this.formatters=this.options.formatters||[],this.dependencies=[],this.model=void 0,this.setBinder()}return t.prototype.setBinder=function(){var e,t,n,r;if(!(this.binder=this.view.binders[this.type])){r=this.view.binders;for(e in r)n=r[e],e!=="*"&&e.indexOf("*")!==-1&&(t=new RegExp("^"+e.replace("*",".+")+"$"),t.test(this.type)&&(this.binder=n,this.args=(new RegExp("^"+e.replace("*","(.+)")+"$")).exec(this.type),this.args.shift()))}this.binder||(this.binder=this.view.binders["*"]);if(this.binder instanceof Function)return this.binder={routine:this.binder}},t.prototype.formattedValue=function(e){var t,n,r,i,s,u;u=this.formatters;for(i=0,s=u.length;i<s;i++)n=u[i],t=n.split(/\s+/),r=t.shift(),n=this.view.formatters[r],(n!=null?n.read:void 0)instanceof Function?e=n.read.apply(n,[e].concat(o.call(t))):n instanceof Function&&(e=n.apply(null,[e].concat(o.call(t))));return e},t.prototype.eventHandler=function(e){var t,n;return n=(t=this).view.config.handler,function(r){return n.call(e,this,r,t)}},t.prototype.set=function(e){var t;return e=e instanceof Function&&!this.binder["function"]?this.formattedValue(e.call(this.model)):this.formattedValue(e),(t=this.binder.routine)!=null?t.call(this,this.el,e):void 0},t.prototype.sync=function(){var t,n,r,i,s,o,u,a,f;if(this.model!==this.observer.target){u=this.dependencies;for(r=0,s=u.length;r<s;r++)n=u[r],n.unobserve();this.dependencies=[];if((this.model=this.observer.target)!=null&&((a=this.options.dependencies)!=null?a.length:void 0)){f=this.options.dependencies;for(i=0,o=f.length;i<o;i++)t=f[i],n=new e.Observer(this.view,this.model,t,this.sync),this.dependencies.push(n)}}return this.set(this.observer.value())},t.prototype.publish=function(){var t,n,r,i,s,u,a,f,l;i=e.Util.getInputValue(this.el),a=this.formatters.slice(0).reverse();for(s=0,u=a.length;s<u;s++){n=a[s],t=n.split(/\s+/),r=t.shift();if((f=this.view.formatters[r])!=null?f.publish:void 0)i=(l=this.view.formatters[r]).publish.apply(l,[i].concat(o.call(t)))}return this.observer.publish(i)},t.prototype.bind=function(){var t,n,r,i,s,o,u;(s=this.binder.bind)!=null&&s.call(this,this.el),this.observer=new e.Observer(this.view,this.view.models,this.keypath,this.sync),this.model=this.observer.target;if(this.model!=null&&((o=this.options.dependencies)!=null?o.length:void 0)){u=this.options.dependencies;for(r=0,i=u.length;r<i;r++)t=u[r],n=new e.Observer(this.view,this.model,t,this.sync),this.dependencies.push(n)}if(this.view.config.preloadData)return this.sync()},t.prototype.unbind=function(){var e,t,n,r,i;(r=this.binder.unbind)!=null&&r.call(this,this.el),this.observer.unobserve(),i=this.dependencies;for(t=0,n=i.length;t<n;t++)e=i[t],e.unobserve();return this.dependencies=[]},t.prototype.update=function(e){var t;return e==null&&(e={}),this.model=this.observer.target,(t=this.binder.update)!=null?t.call(this,e):void 0},t}(),e.ComponentBinding=function(t){function n(t,n,r){var o,u,a,f,l;this.view=t,this.el=n,this.type=r,this.unbind=i(this.unbind,this),this.bind=i(this.bind,this),this.update=i(this.update,this),this.locals=i(this.locals,this),this.component=e.components[this.type],this.attributes={},this.inflections={},f=this.el.attributes||[];for(u=0,a=f.length;u<a;u++)o=f[u],(l=o.name,s.call(this.component.attributes,l)>=0)?this.attributes[o.name]=o.value:this.inflections[o.name]=o.value}return a(n,t),n.prototype.sync=function(){},n.prototype.locals=function(e){var t,n,r,i,s,o,u,a,f;e==null&&(e=this.view.models),s={},a=this.inflections;for(n in a){t=a[n],f=t.split(".");for(o=0,u=f.length;o<u;o++)i=f[o],s[n]=(s[n]||e)[i]}for(n in e)r=e[n],s[n]==null&&(s[n]=r);return s},n.prototype.update=function(e){var t;return(t=this.componentView)!=null?t.update(this.locals(e)):void 0},n.prototype.bind=function(){var t,n;return this.componentView!=null?(n=this.componentView)!=null?n.bind():void 0:(t=this.component.build.call(this.attributes),(this.componentView=new e.View(t,this.locals(),this.view.options)).bind(),this.el.parentNode.replaceChild(t,this.el))},n.prototype.unbind=function(){var e;return(e=this.componentView)!=null?e.unbind():void 0},n}(e.Binding),e.TextBinding=function(e){function t(e,t,n,r,s){this.view=e,this.el=t,this.type=n,this.keypath=r,this.options=s!=null?s:{},this.sync=i(this.sync,this),this.formatters=this.options.formatters||[],this.dependencies=[]}return a(t,e),t.prototype.binder={routine:function(e,t){return e.data=t!=null?t:""}},t.prototype.sync=function(){return t.__super__.sync.apply(this,arguments)},t}(e.Binding),e.KeypathParser=function(){function e(){}return e.parse=function(e,t,n){var r,i,o,u,a,f;u=[],i={"interface":n,path:""};for(o=a=0,f=e.length;a<f;o=a+=1)r=e.charAt(o),s.call(t,r)>=0?(u.push(i),i={"interface":r,path:""}):i.path+=r;return u.push(i),u},e}(),e.TextTemplateParser=function(){function e(){}return e.types={text:0,binding:1},e.parse=function(e,t){var n,r,i,s,o,u,a;u=[],s=e.length,n=0,r=0;while(r<s){n=e.indexOf(t[0],r);if(n<0){u.push({type:this.types.text,value:e.slice(r)});break}n>0&&r<n&&u.push({type:this.types.text,value:e.slice(r,n)}),r=n+t[0].length,n=e.indexOf(t[1],r);if(n<0){o=e.slice(r-t[1].length),i=u[u.length-1],(i!=null?i.type:void 0)===this.types.text?i.value+=o:u.push({type:this.types.text,value:o});break}a=e.slice(r,n).trim(),u.push({type:this.types.binding,value:a}),r=n+t[1].length}return u},e}(),e.Observer=function(){function t(e,t,n,r){this.view=e,this.model=t,this.keypath=n,this.callback=r,this.unobserve=i(this.unobserve,this),this.realize=i(this.realize,this),this.value=i(this.value,this),this.publish=i(this.publish,this),this.read=i(this.read,this),this.set=i(this.set,this),this.adapter=i(this.adapter,this),this.update=i(this.update,this),this.initialize=i(this.initialize,this),this.parse=i(this.parse,this),this.parse(),this.initialize()}return t.prototype.parse=function(){var t,n,r,i,o,u;return t=function(){var e,t;e=this.view.adapters,t=[];for(n in e)o=e[n],t.push(n);return t}.call(this),(u=this.keypath[0],s.call(t,u)>=0)?(i=this.keypath[0],r=this.keypath.substr(1)):(i=this.view.config.rootInterface,r=this.keypath),this.tokens=e.KeypathParser.parse(r,t,i),this.key=this.tokens.pop()},t.prototype.initialize=function(){this.objectPath=[],this.target=this.realize();if(this.target!=null)return this.set(!0,this.key,this.target,this.callback)},t.prototype.update=function(){var e,t;if((e=this.realize())!==this.target){this.target!=null&&this.set(!1,this.key,this.target,this.callback),e!=null&&this.set(!0,this.key,e,this.callback),t=this.value(),this.target=e;if(this.value()!==t)return this.callback()}},t.prototype.adapter=function(e){return this.view.adapters[e["interface"]]},t.prototype.set=function(e,t,n,r){var i;return i=e?"subscribe":"unsubscribe",this.adapter(t)[i](n,t.path,r)},t.prototype.read=function(e,t){return this.adapter(e).read(t,e.path)},t.prototype.publish=function(e){if(this.target!=null)return this.adapter(this.key).publish(this.target,this.key.path,e)},t.prototype.value=function(){if(this.target!=null)return this.read(this.key,this.target)},t.prototype.realize=function(){var e,t,n,r,i,s,o,u;e=this.model,i=null,u=this.tokens;for(t=s=0,o=u.length;s<o;t=++s)r=u[t],e!=null?(this.objectPath[t]!=null?e!==(n=this.objectPath[t])&&(this.set(!1,r,n,this.update),this.set(!0,r,e,this.update),this.objectPath[t]=e):(this.set(!0,r,e,this.update),this.objectPath[t]=e),e=this.read(r,e)):(i==null&&(i=t),(n=this.objectPath[t])&&this.set(!1,r,n,this.update));return i!=null&&this.objectPath.splice(i),e},t.prototype.unobserve=function(){var e,t,n,r,i,s,o;s=this.tokens,o=[];for(e=r=0,i=s.length;r<i;e=++r)n=s[e],(t=this.objectPath[e])?o.push(this.set(!1,n,t,this.update)):o.push(void 0);return o},t}(),e.binders.text=function(e,t){return e.textContent!=null?e.textContent=t!=null?t:"":e.innerText=t!=null?t:""},e.binders.html=function(e,t){return e.innerHTML=t!=null?t:""},e.binders.show=function(e,t){return e.style.display=t?"":"none"},e.binders.hide=function(e,t){return e.style.display=t?"none":""},e.binders.enabled=function(e,t){return e.disabled=!t},e.binders.disabled=function(e,t){return e.disabled=!!t},e.binders.checked={publishes:!0,bind:function(t){return e.Util.bindEvent(t,"change",this.publish)},unbind:function(t){return e.Util.unbindEvent(t,"change",this.publish)},routine:function(e,t){var n;return e.type==="radio"?e.checked=((n=e.value)!=null?n.toString():void 0)===(t!=null?t.toString():void 0):e.checked=!!t}},e.binders.unchecked={publishes:!0,bind:function(t){return e.Util.bindEvent(t,"change",this.publish)},unbind:function(t){return e.Util.unbindEvent(t,"change",this.publish)},routine:function(e,t){var n;return e.type==="radio"?e.checked=((n=e.value)!=null?n.toString():void 0)!==(t!=null?t.toString():void 0):e.checked=!t}},e.binders.value={publishes:!0,bind:function(t){return e.Util.bindEvent(t,"change",this.publish)},unbind:function(t){return e.Util.unbindEvent(t,"change",this.publish)},routine:function(e,t){var n,r,i,o,u,a,f;if(window.jQuery!=null){e=jQuery(e);if((t!=null?t.toString():void 0)!==((o=e.val())!=null?o.toString():void 0))return e.val(t!=null?t:"")}else if(e.type==="select-multiple"){if(t!=null){f=[];for(r=0,i=e.length;r<i;r++)n=e[r],f.push(n.selected=(u=n.value,s.call(t,u)>=0));return f}}else if((t!=null?t.toString():void 0)!==((a=e.value)!=null?a.toString():void 0))return e.value=t!=null?t:""}},e.binders["if"]={block:!0,bind:function(e){var t,n;if(this.marker==null)return t=[this.view.config.prefix,this.type].join("-").replace("--","-"),n=e.getAttribute(t),this.marker=document.createComment(" rivets: "+this.type+" "+n+" "),e.removeAttribute(t),e.parentNode.insertBefore(this.marker,e),e.parentNode.removeChild(e)},unbind:function(){var e;return(e=this.nested)!=null?e.unbind():void 0},routine:function(t,n){var r,i,s,o,u;if(!!n==(this.nested==null)){if(n){s={},u=this.view.models;for(r in u)i=u[r],s[r]=i;return o={binders:this.view.options.binders,formatters:this.view.options.formatters,adapters:this.view.options.adapters,config:this.view.options.config},(this.nested=new e.View(t,s,o)).bind(),this.marker.parentNode.insertBefore(t,this.marker.nextSibling)}return t.parentNode.removeChild(t),this.nested.unbind(),delete this.nested}},update:function(e){var t;return(t=this.nested)!=null?t.update(e):void 0}},e.binders.unless={block:!0,bind:function(t){return e.binders["if"].bind.call(this,t)},unbind:function(){return e.binders["if"].unbind.call(this)},routine:function(t,n){return e.binders["if"].routine.call(this,t,!n)},update:function(t){return e.binders["if"].update.call(this,t)}},e.binders["on-*"]={"function":!0,unbind:function(t){if(this.handler)return e.Util.unbindEvent(t,this.args[0],this.handler)},routine:function(t,n){return this.handler&&e.Util.unbindEvent(t,this.args[0],this.handler),e.Util.bindEvent(t,this.args[0],this.handler=this.eventHandler(n))}},e.binders["each-*"]={block:!0,bind:function(e){var t;if(this.marker==null)return t=[this.view.config.prefix,this.type].join("-").replace("--","-"),this.marker=document.createComment(" rivets: "+this.type+" "),this.iterated=[],e.removeAttribute(t),e.parentNode.insertBefore(this.marker,e),e.parentNode.removeChild(e)},unbind:function(e){var t,n,r,i,s;if(this.iterated!=null){i=this.iterated,s=[];for(n=0,r=i.length;n<r;n++)t=i[n],s.push(t.unbind());return s}},routine:function(t,n){var r,i,s,o,u,a,f,l,c,h,p,d,v,m,g,y,b,w,E,S,x,T,N,C;l=this.args[0],n=n||[];if(this.iterated.length>n.length){S=Array(this.iterated.length-n.length);for(m=0,b=S.length;m<b;m++)s=S[m],v=this.iterated.pop(),v.unbind(),this.marker.parentNode.removeChild(v.els[0])}for(o=g=0,w=n.length;g<w;o=++g){f=n[o],i={index:o},i[l]=f;if(this.iterated[o]==null){x=this.view.models;for(a in x)f=x[a],i[a]==null&&(i[a]=f);h=this.iterated.length?this.iterated[this.iterated.length-1].els[0]:this.marker,c={binders:this.view.options.binders,formatters:this.view.options.formatters,adapters:this.view.options.adapters,config:{}},T=this.view.options.config;for(u in T)d=T[u],c.config[u]=d;c.config.preloadData=!0,p=t.cloneNode(!0),v=new e.View(p,i,c),v.bind(),this.iterated.push(v),this.marker.parentNode.insertBefore(p,h.nextSibling)}else this.iterated[o].models[l]!==f&&this.iterated[o].update(i)}if(t.nodeName==="OPTION"){N=this.view.bindings,C=[];for(y=0,E=N.length;y<E;y++)r=N[y],r.el===this.marker.parentNode&&r.type==="value"?C.push(r.sync()):C.push(void 0);return C}},update:function(e){var t,n,r,i,s,o,u,a;t={};for(n in e)r=e[n],n!==this.args[0]&&(t[n]=r);u=this.iterated,a=[];for(s=0,o=u.length;s<o;s++)i=u[s],a.push(i.update(t));return a}},e.binders["class-*"]=function(e,t){var n;n=" "+e.className+" ";if(!t==(n.indexOf(" "+this.args[0]+" ")!==-1))return e.className=t?""+e.className+" "+this.args[0]:n.replace(" "+this.args[0]+" "," ").trim()},e.binders["*"]=function(e,t){return t!=null?e.setAttribute(this.type,t):e.removeAttribute(this.type)},e.adapters["."]={id:"_rv",counter:0,weakmap:{},weakReference:function(e){var t;return e[this.id]==null&&(t=this.counter++,this.weakmap[t]={callbacks:{}},Object.defineProperty(e,this.id,{value:t})),this.weakmap[e[this.id]]},stubFunction:function(e,t){var n,r,i;return r=e[t],n=this.weakReference(e),i=this.weakmap,e[t]=function(){var t,s,o,u,a,f,l,c,h,p;u=r.apply(e,arguments),l=n.pointers;for(o in l){s=l[o],p=(c=(h=i[o])!=null?h.callbacks[s]:void 0)!=null?c:[];for(a=0,f=p.length;a<f;a++)t=p[a],t()}return u}},observeMutations:function(e,t,n){var r,i,o,u,a,f;if(Array.isArray(e)){o=this.weakReference(e);if(o.pointers==null){o.pointers={},i=["push","pop","shift","unshift","sort","reverse","splice"];for(a=0,f=i.length;a<f;a++)r=i[a],this.stubFunction(e,r)}(u=o.pointers)[t]==null&&(u[t]=[]);if(s.call(o.pointers[t],n)<0)return o.pointers[t].push(n)}},unobserveMutations:function(e,t,n){var r,i;if(Array.isArray(e&&e[this.id]!=null))if(r=(i=this.weakReference(e).pointers)!=null?i[t]:void 0)return r.splice(r.indexOf(n),1)},subscribe:function(e,t,n){var r,i,o=this;return r=this.weakReference(e).callbacks,r[t]==null&&(r[t]=[],i=e[t],Object.defineProperty(e,t,{enumerable:!0,get:function(){return i},set:function(s){var u,a,f;if(s!==i){i=s,f=r[t];for(u=0,a=f.length;u<a;u++)n=f[u],n();return o.observeMutations(s,e[o.id],t)}}})),s.call(r[t],n)<0&&r[t].push(n),this.observeMutations(e[t],e[this.id],t)},unsubscribe:function(e,t,n){var r;return r=this.weakmap[e[this.id]].callbacks[t],r.splice(r.indexOf(n),1),this.unobserveMutations(e[t],e[this.id],t)},read:function(e,t){return e[t]},publish:function(e,t,n){return e[t]=n}},e.factory=function(t){return t._=e,t.binders=e.binders,t.components=e.components,t.formatters=e.formatters,t.adapters=e.adapters,t.config=e.config,t.configure=function(t){var n,r;t==null&&(t={});for(n in t)r=t[n],e.config[n]=r},t.bind=function(t,n,r){var i;return n==null&&(n={}),r==null&&(r={}),i=new e.View(t,n,r),i.bind(),i}},typeof exports=="object"?e.factory(exports):typeof define=="function"&&define.amd?define(["exports"],function(t){return e.factory(this.rivets=t),t}):e.factory(this.rivets={})}).call(this);