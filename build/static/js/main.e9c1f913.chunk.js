(window.webpackJsonp=window.webpackJsonp||[]).push([[0],[,,,function(e,a,n){e.exports={backdrop:"Modal_backdrop__2TEft",center:"Modal_center__3EcRR",modal:"Modal_modal__2Vs3-","slide-down":"Modal_slide-down__2kcor"}},function(e,a,n){e.exports={form:"Saver_form__3Wbqv",extension:"Saver_extension__25b5g",invalid:"Saver_invalid__4hM6-",error:"Saver_error__sNSpp",saveas:"Saver_saveas__2h607"}},function(e,a,n){e.exports={form:"Settings_form__jUy8v",total:"Settings_total__ciSFp",overall:"Settings_overall__3bFKM",checkboxes:"Settings_checkboxes__13SHL",buttons:"Settings_buttons__uFsu5"}},,function(e,a,n){e.exports={options:"Options_options__3UwTo",cajitas:"Options_cajitas__3bxOO",separation:"Options_separation__1pQ8q"}},,,function(e,a,n){e.exports={overall:"Checkboxes_overall__JrJgo"}},function(e,a,n){e.exports=n(35)},,,,,,,,function(e,a,n){},,,function(e,a,n){},,function(e,a,n){},,function(e,a,n){},,,,,,,function(e,a,n){},,function(e,a,n){"use strict";n.r(a);var t=n(0),l=n.n(t),r=n(9),c=n.n(r),i=(n(19),n(1)),o=(n(22),n(24),function(e){var a=Object(t.useState)(""),n=Object(i.a)(a,2),l=n[0],r=n[1],c=Object(t.useState)(!1),o=Object(i.a)(c,2),s=o[0],u=o[1],d=e(l);return{value:l,isValid:d,hasError:!d&&s,valueChangeHandler:function(e){r(e.target.value)},inputBlurHandler:function(){0===l.trim().length?u(!1):u(!0)},reset:function(){r(""),u(!1)}}}),s=(n(36),Object(t.createContext)({saveNameHandler:function(e){},saveas:"",parse:!0,parseHandler:function(e){},classParsing:!0,classParsingHandler:function(e){},links:!0,linksHandler:function(e){},update:!1,updateHandler:function(e){},extension:".ics",extensionHandler:function(e){}})),u=function(e){var a=Object(t.useState)("Calendario"),n=Object(i.a)(a,2),r=n[0],c=n[1],o=Object(t.useState)(!1),u=Object(i.a)(o,2),d=u[0],m=u[1],v=Object(t.useState)(!0),E=Object(i.a)(v,2),p=E[0],f=E[1],g=Object(t.useState)(!0),h=Object(i.a)(g,2),b=h[0],_=h[1],k=Object(t.useState)(!0),C=Object(i.a)(k,2),S=C[0],N=C[1],x=Object(t.useState)(".ics"),y=Object(i.a)(x,2),j=y[0],H=y[1];return l.a.createElement(s.Provider,{value:{saveNameHandler:function(e){c(e)},saveas:r,parseHandler:function(e){f(e)},parse:p,classParsing:b,classParsingHandler:function(e){_(e)},links:S,linksHandler:function(e){N(e)},update:d,updateHandler:function(e){m(e)},extension:j,extensionHandler:function(e){H(e)}}},e.children)},d=s,m=(n(26),function(){return l.a.createElement("div",{className:"msal-button"},l.a.createElement("button",{id:"msal-but"},l.a.createElement("div",{className:"inline"},l.a.createElement("i",{className:"btn-microsoft"}),"Sign in")))}),v=function(e){var a=l.a.useContext(d),n=o(function(e){return 37===e.length&&"0"===e.charAt(0)&&"0"===e.charAt(1)&&"0"===e.charAt(2)&&"0"===e.charAt(3)&&":"===e.charAt(27)&&"1"===e.charAt(28)&&"d"===e.charAt(29)}),r=n.value,c=n.isValid,i=n.hasError,s=n.valueChangeHandler,u=n.inputBlurHandler,v=n.reset,E=c,p=function(e){e.preventDefault(),c?(document.getElementById("form").submit(),a.saveNameHandler("Calendario"),v()):console.log("Code is not valid")},f="form-container cookies"+(i?" invalid":"");return console.log(E),Object(t.useEffect)(function(){var e=document.getElementById("cookies-sign"),a=document.getElementById("signIn"),n=document.getElementById("container");a.addEventListener("click",function(){n.classList.add("right-panel-active")}),e.addEventListener("click",function(){n.classList.remove("right-panel-active")})},[]),l.a.createElement(l.a.Fragment,null,l.a.createElement("h1",{id:"title"},"autoUniCalendar: Descarga tu calendario de Uniovi."),l.a.createElement("div",{id:"container",className:"container"},l.a.createElement("div",{className:f},l.a.createElement("form",{id:"form",method:"post",onSubmit:p},l.a.createElement("h1",null,"Cookies"),l.a.createElement("span",{id:"cookies-span"},"Introduce tu cookie de sesi\xf3n."),l.a.createElement("div",{className:"floating-input"},l.a.createElement("label",null,l.a.createElement("input",{type:"text",name:"jsessionid",id:"jsessionid",required:!0,onChange:s,onBlur:u,value:r}),l.a.createElement("span",{className:"floating-label"},"JSession"))),l.a.createElement("a",{href:"https://bimo99b9.github.io/scripts-autounicalendar/#",target:"_blank",rel:"noopener noreferrer"},"\xbfNecesitas ayuda?"),l.a.createElement("button",{disabled:!E,onClick:p},"DESCARGAR"),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"filename",value:a.saveas})),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"location",value:a.parse})),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"class-type",value:a.classParsing})),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"links",value:a.links})),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"extension",value:a.extension})))),l.a.createElement("div",{className:"form-container signin"},l.a.createElement("form",{action:""},l.a.createElement("h1",null,"Descargar usando credenciales"),l.a.createElement("p",null," Usa tus credenciales para tramitar la solicitud y descargar el calendario."),l.a.createElement(m,null))),l.a.createElement("div",{className:"overlay-container"},l.a.createElement("div",{className:"overlay"},l.a.createElement("div",{className:"overlay-panel overlay-left"},l.a.createElement("h1",null,"Descargar usando cookie."),l.a.createElement("p",null,"Puedes descargar el calendario usando una cookie de sesi\xf3n, haciendo click aqu\xed."),l.a.createElement("button",{id:"cookies-sign",className:"ghost"},"Usar cookie")),l.a.createElement("div",{className:"overlay-panel overlay-right"},l.a.createElement("h1",null,"Descargar usando credenciales."),l.a.createElement("p",null,"Si lo prefieres, puedes usar tus credenciales en lugar de tus cookies de sesi\xf3n para descargar el calendario."),l.a.createElement("button",{id:"signIn",className:"ghost"},"Usar crendeciales"))))),l.a.createElement("div",{className:"settings-button"},l.a.createElement("button",{onClick:e.onShowSettings},"Opciones")))},E=n(2),p=n.n(E),f=n(3),g=n.n(f),h=function(e){return l.a.createElement("div",{className:g.a.backdrop,onClick:e.onClose})},b=function(e){return l.a.createElement("div",{className:g.a.center},l.a.createElement("div",{className:g.a.modal},e.children))},_=document.getElementById("modal"),k=function(e){return l.a.createElement(t.Fragment,null,p.a.createPortal(l.a.createElement(h,{onClose:e.onClose}),_),p.a.createPortal(l.a.createElement(b,null,e.children),_))},C=n(10),S=n.n(C),N=function(){var e=Object(t.useContext)(d);return l.a.createElement("div",{className:S.a.overall},l.a.createElement("div",null,l.a.createElement("input",{type:"checkbox",id:"location-parsing",checked:e.parse,onChange:function(){e.parseHandler(!e.parse),e.updateHandler(!0)}}),l.a.createElement("label",{htmlFor:"location-parsing"},"Filtrado de nombres de aulas (solo EPI Gij\xf3n)")),l.a.createElement("div",null,l.a.createElement("input",{type:"checkbox",id:"class-parsing",checked:e.classParsing,onChange:function(){e.classParsingHandler(!e.classParsing),e.updateHandler(!0)}}),l.a.createElement("label",{htmlFor:"class-parsing"},"Filtrado de tipo de clases")),l.a.createElement("div",null,l.a.createElement("input",{type:"checkbox",id:"links",checked:e.links,onChange:function(){e.linksHandler(!e.links),e.updateHandler(!0)}}),l.a.createElement("label",{htmlFor:"links"},"A\xf1adir enlaces de ubicaci\xf3n en la descripci\xf3n")))},x=n(7),y=n.n(x),j=function(e){return l.a.createElement(l.a.Fragment,null,l.a.createElement("div",{className:y.a.options},l.a.createElement("h3",null,"Opciones")),l.a.createElement("div",{className:y.a.cajitas},l.a.createElement(N,{university:e.university})))},H=n(4),O=n.n(H),F=function(e){var a=l.a.useContext(d),n=o(function(e){return e.length>0}),t=n.value,r=n.valueChangeHandler,c=n.inputBlurHandler;return l.a.createElement(l.a.Fragment,null,l.a.createElement("div",{className:O.a.saveas},l.a.createElement("h3",null,"Guardar como")),l.a.createElement("div",{className:O.a.form},l.a.createElement("input",{type:"text",id:"saveAs",name:"filename",onChange:function(a){a.target.value.trim().length>0?(r(a),e.onSave(a.target.value)):""===a.target.value&&(r(a),e.onSave("Calendario"))},onBlur:c,value:t,placeholder:"Calendario"}),l.a.createElement("div",{className:O.a.extension},l.a.createElement("select",{value:a.extension,onChange:function(e){a.extensionHandler(e.target.value)}},l.a.createElement("option",{value:".ics"},".ics"),l.a.createElement("option",{value:".csv"},".csv")))))},P=n(5),A=n.n(P),B=function(e){var a=l.a.useContext(d);return l.a.createElement(k,{onClose:e.onClose},l.a.createElement("div",{className:A.a.overall},l.a.createElement(F,{onSave:a.saveNameHandler}),l.a.createElement(j,{onCheck:a.check,university:a.university}),l.a.createElement("div",{className:A.a.buttons},l.a.createElement("button",{className:A.a["button--alt"],onClick:e.onClose},l.a.createElement("span",null),l.a.createElement("span",null),l.a.createElement("span",null),l.a.createElement("span",null),"Cerrar"))))},w=(n(33),function(){return l.a.createElement("footer",null,l.a.createElement("p",null,"Created with love by",l.a.createElement("a",{id:"links",href:"https://bimo99b9.github.io/",target:"_blank",rel:"noopener noreferrer"}," Daniel L\xf3pez Gala"),",",l.a.createElement("a",{id:"links",href:"https://github.com/miermontoto",target:"_blank",rel:"noopener noreferrer"}," Juan Francisco Mier Montoto")," and",l.a.createElement("a",{id:"links",href:"https://github.com/JonathanAriass",target:"_blank",rel:"noopener noreferrer"}," Jonathan Arias Busto"),". v1.1"))});var I=function(){var e=Object(t.useState)(!1),a=Object(i.a)(e,2),n=a[0],r=a[1];return l.a.createElement("div",{className:"group"},n&&l.a.createElement(B,{onClose:function(){r(!1)}}),l.a.createElement(v,{onShowSettings:function(){r(!0)}}),l.a.createElement(w,null))},M=function(e){e&&e instanceof Function&&n.e(1).then(n.bind(null,37)).then(function(a){var n=a.getCLS,t=a.getFID,l=a.getFCP,r=a.getLCP,c=a.getTTFB;n(e),t(e),l(e),r(e),c(e)})};c.a.createRoot(document.getElementById("root")).render(l.a.createElement(l.a.StrictMode,null,l.a.createElement(u,null,l.a.createElement(I,null)))),M()}],[[11,3,2]]]);
//# sourceMappingURL=main.e9c1f913.chunk.js.map