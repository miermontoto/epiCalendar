(window.webpackJsonp=window.webpackJsonp||[]).push([[0],[,,,function(e,a,n){e.exports={form:"Form_form__3N9xP",control:"Form_control__2Hd3y","btn-anim1":"Form_btn-anim1__3_-pr","btn-anim2":"Form_btn-anim2__wFzsa","btn-anim3":"Form_btn-anim3__2vJJx","btn-anim4":"Form_btn-anim4__1e_AM",actions:"Form_actions__2_19Y",invalid:"Form_invalid__1zbxW",error:"Form_error__24IC1"}},,function(e,a,n){e.exports={backdrop:"Modal_backdrop__3bwxq",modal:"Modal_modal__1pZmX","slide-down":"Modal_slide-down__1H0HJ"}},function(e,a,n){e.exports={form:"Saver_form__3XrKa",invalid:"Saver_invalid__1dWqF",error:"Saver_error__35SK9",saveas:"Saver_saveas__1P7e9",extension:"Saver_extension__3WZap"}},function(e,a,n){e.exports={form:"Settings_form__1Qk8i",total:"Settings_total__1XkVL",overall:"Settings_overall__4QOs4",checkboxes:"Settings_checkboxes__19b_p",buttons:"Settings_buttons__2eU31","button--alt":"Settings_button--alt__uOqtR",button:"Settings_button__13X5e"}},function(e,a,n){e.exports={icon:"HeaderSettingsButton_icon__1Y1Bf",badge:"HeaderSettingsButton_badge__1lrE1",bump:"HeaderSettingsButton_bump__1uSXa"}},function(e,a,n){e.exports={options:"Options_options__2hcQg",separation:"Options_separation__3vDns"}},,,function(e,a,n){e.exports={overall:"Checkboxes_overall__12sVY"}},function(e,a,n){e.exports={form:"RadioButtons_form__1GDBR"}},function(e,a,n){},function(e,a,n){e.exports=n(24)},,,,,,,,function(e,a,n){},function(e,a,n){"use strict";n.r(a);var t=n(0),l=n.n(t),r=n(11),i=n.n(r),c=(n(23),n(1)),s=function(e){var a=Object(t.useState)(""),n=Object(c.a)(a,2),l=n[0],r=n[1],i=Object(t.useState)(!1),s=Object(c.a)(i,2),o=s[0],u=s[1],m=e(l);return{value:l,isValid:m,hasError:!m&&o,valueChangeHandler:function(e){r(e.target.value)},inputBlurHandler:function(){u(!0)},reset:function(){r(""),u(!1)}}},o=n(8),u=n.n(o),m=function(e){var a=Object(t.useState)(!1),n=Object(c.a)(a,1)[0],r="".concat(u.a.button," ").concat(n?u.a.bump:"");return l.a.createElement("button",{className:r,onClick:e.onClick},l.a.createElement("span",null),l.a.createElement("span",null),l.a.createElement("span",null),l.a.createElement("span",null),"\u2699")},d=n(2),p=Object(t.createContext)({check:function(e){},university:"",saveNameHandler:function(e){},saveas:"",parse:!0,experimental:!0,classParsing:!0,parseHandler:function(e){},experimentalHandler:function(e){},classParsingHandler:function(e){},update:!1,updateHandler:function(e){}}),b=function(e){var a=Object(t.useState)("epi"),n=Object(c.a)(a,2),r=n[0],i=n[1],s=Object(t.useState)("Calendario"),o=Object(c.a)(s,2),u=o[0],m=o[1],b=Object(t.useState)(!1),v=Object(c.a)(b,2),g=v[0],f=v[1],_=Object(t.useState)(!0),E=Object(c.a)(_,2),h=E[0],x=E[1],C=Object(t.useState)(!0),k=Object(c.a)(C,2),O=k[0],j=k[1],S=Object(t.useState)(!0),y=Object(c.a)(S,2),P=y[0],X=y[1],D=Object(t.useState)({parse:!1,experimental:!1,classParsing:!0,parseDisabled:!0,experimentalDisabled:!0,classParsingDisabled:!1}),H=Object(c.a)(D,2),N=H[0],F=H[1],B=Object(t.useState)({parse:!0,experimental:!0,classParsing:!0,parseDisabled:!1,experimentalDisabled:!1,classParsingDisabled:!1}),w=Object(c.a)(B,2),I=w[0],A=w[1];Object(t.useEffect)(function(){"epi"===r&&A(function(e){return Object(d.a)({},e,{parse:h,parseDisabled:!1,experimental:!0===h,experimentalDisabled:!0!==h,classParsingDisabled:!1})}),f(!1)},[h]),Object(t.useEffect)(function(){console.log("entra"),"epi"===r&&A(function(e){return Object(d.a)({},e,{experimental:!0===h&&O})}),f(!1)},[O]),Object(t.useEffect)(function(){console.log("entra en classParsing"),"uo"===r?F(function(e){return Object(d.a)({},e,{classParsing:P})}):A(function(e){return Object(d.a)({},e,{classParsing:P})}),f(!1)},[P]);return l.a.createElement(p.Provider,{value:{check:function(e){i(e)},university:r,saveNameHandler:function(e){m(e)},saveas:u,parseHandler:function(e){x(e)},experimentalHandler:function(e){j(e)},classParsingHandler:function(e){X(e)},oviedoCheck:N,epiCheck:I,update:g,updateHandler:function(e){f(e)}}},e.children)},v=p,g=n(3),f=n.n(g),_=function(e){var a=l.a.useContext(v),n=s(function(e){return 37===e.length&&"0"===e.charAt(0)&&"0"===e.charAt(1)&&"0"===e.charAt(2)&&"0"===e.charAt(3)&&":"===e.charAt(27)&&"1"===e.charAt(28)&&"d"===e.charAt(29)}),t=n.value,r=n.isValid,i=n.hasError,c=n.valueChangeHandler,o=n.inputBlurHandler,u=n.reset,d=!1;r&&(d=!0);var p=function(e){e.preventDefault(),r?(document.getElementById("form").submit(),a.saveNameHandler("Calendario"),a.check("epi"),u()):console.log("Code is not valid")},b="".concat(f.a.form," ").concat(i?f.a.invalid:"");return l.a.createElement(l.a.Fragment,null,l.a.createElement("form",{method:"post",onSubmit:p,id:"form"},l.a.createElement("legend",null,"epiCalendar"),l.a.createElement("div",{className:f.a.control},l.a.createElement("div",{className:b},l.a.createElement("label",{htmlFor:"codigo"},"JSESSIONID"),l.a.createElement("input",{type:"text",id:"codigo",name:"jsessionid",onChange:c,onBlur:o,value:t,placeholder:"0000XXXXXXXXXXXXXXXXXXXXXXX:1dXXXXXXX"}),i&&l.a.createElement(l.a.Fragment,null,l.a.createElement("p",{className:f.a.error},"El c\xf3digo no es v\xe1lido."))),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"filename",value:a.saveas})),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"location",value:"uo"===a.university?a.epiCheck.parse:a.oviedoCheck.parse})),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"experimental-location",value:"uo"===a.university?a.epiCheck.experimental:a.oviedoCheck.experimental})),l.a.createElement("div",null,l.a.createElement("input",{type:"hidden",name:"class-type",value:"uo"===a.university?a.epiCheck.classParsing:a.oviedoCheck.classParsing})))),l.a.createElement("div",{className:f.a.actions},l.a.createElement(m,{onClick:e.onShowSettings}),l.a.createElement("button",{className:"button",disabled:!d,onClick:p},l.a.createElement("span",null),l.a.createElement("span",null),l.a.createElement("span",null),l.a.createElement("span",null),"Generar")))},E=n(4),h=n.n(E),x=n(5),C=n.n(x),k=function(e){return l.a.createElement("div",{className:C.a.backdrop,onClick:e.onClose})},O=function(e){return l.a.createElement("div",{className:C.a.modal},l.a.createElement("div",{className:C.a.content},e.children))},j=document.getElementById("overlays"),S=function(e){return l.a.createElement(t.Fragment,null,h.a.createPortal(l.a.createElement(k,{onClose:e.onClose}),j),h.a.createPortal(l.a.createElement(O,null,e.children),j))},y=n(12),P=n.n(y),X=function(){var e=Object(t.useContext)(v),a=Object(t.useState)({parse:!0,parseDisabled:!1}),n=Object(c.a)(a,2),r=n[0],i=n[1],s=Object(t.useState)({experimental:!0,experimentalDisabled:!1}),o=Object(c.a)(s,2),u=o[0],m=o[1],p=Object(t.useState)({classParsing:!0,classParsingDisabled:!1}),b=Object(c.a)(p,2),g=b[0],f=b[1];Object(t.useEffect)(function(){"uo"===e.university?(console.log("entra uo"),i({parse:e.oviedoCheck.parse,parseDisabled:e.oviedoCheck.parseDisabled}),m({experimental:e.oviedoCheck.experimental,experimentalDisabled:e.oviedoCheck.experimentalDisabled}),f({classParsing:e.oviedoCheck.classParsing,classParsingDisabled:e.oviedoCheck.classParsingDisabled})):"epi"===e.university&&(console.log("entra epi"),i({parse:e.epiCheck.parse,parseDisabled:e.epiCheck.parseDisabled}),m({experimental:e.epiCheck.experimental,experimentalDisabled:e.epiCheck.experimentalDisabled}),f({classParsing:e.epiCheck.classParsing,classParsingDisabled:e.epiCheck.classParsingDisabled}))},[e.university,e.update]),Object(t.useEffect)(function(){e.parseHandler(r.parse),e.experimentalHandler(u.experimental),e.classParsingHandler(g.classParsing)},[r.parse,u.experimental,g.classParsing]);return l.a.createElement("div",{className:P.a.overall},l.a.createElement("div",null,l.a.createElement("input",{type:"checkbox",id:"location-parsing",checked:r.parse,onChange:function(){i(function(e){return Object(d.a)({},e,{parse:!e.parse})}),e.updateHandler(!0)},disabled:r.parseDisabled}),l.a.createElement("label",{htmlFor:"location-parsing"},"Enable location parsing (EPI Gij\xf3n)")),l.a.createElement("div",null,l.a.createElement("input",{type:"checkbox",id:"experimental-parsing",checked:u.experimental,onChange:function(){m(function(e){return Object(d.a)({},e,{experimental:!e.experimental})}),e.updateHandler(!0)},disabled:u.experimentalDisabled}),l.a.createElement("label",{htmlFor:"experimental-parsing"},"Enable experimental location parsing (EPI Gij\xf3n)")),l.a.createElement("div",null,l.a.createElement("input",{type:"checkbox",id:"class-parsing",checked:g.classParsing,onChange:function(){f(function(e){return Object(d.a)({},e,{classParsing:!e.classParsing})}),e.updateHandler(!0)}}),l.a.createElement("label",{htmlFor:"class-parsing"},"Enable class type parsing")))},D=n(9),H=n.n(D),N=n(13),F=n.n(N),B=[{value:"uo",label:"University of Oviedo",id:"uo"},{value:"epi",label:"EPI Gij\xf3n",id:"epi"}],w=function(e){var a=function(a){e.onClick(a.target.value)};return l.a.createElement("div",null,B.map(function(n){return l.a.createElement("div",{className:F.a.form,key:n.id},l.a.createElement("label",null,l.a.createElement("input",{type:"radio",name:"university",value:n.value,onChange:a,defaultChecked:n.value===e.university})," ",n.label))}))},I=function(e){return l.a.createElement(l.a.Fragment,null,l.a.createElement("div",{className:H.a.options},l.a.createElement("h2",null,"Settings")),l.a.createElement("div",{className:H.a.separation},l.a.createElement(w,{onClick:e.onCheck,university:e.university}),l.a.createElement("hr",{style:{color:"grey",backgroundColor:"grey",borderColor:"grey",height:115,fontWeight:"bold",width:5,marginTop:"0px",marginLeft:"auto",marginRight:"auto",borderRadius:14}}),l.a.createElement(X,{university:e.university})))},A=n(6),G=n.n(A),J=function(e){var a=s(function(e){return e.length>0}),n=a.value,t=a.valueChangeHandler,r=a.inputBlurHandler;return l.a.createElement(l.a.Fragment,null,l.a.createElement("div",{className:G.a.saveas},l.a.createElement("h2",null,"Guardar como")),l.a.createElement("div",{className:G.a.form},l.a.createElement("input",{type:"text",id:"saveAs",name:"filename",onChange:function(a){a.target.value.trim().length>0?(t(a),e.onSave(a.target.value)):""===a.target.value&&(console.log("Name is empty"),t(a),e.onSave("Calendario"))},onBlur:r,value:n,placeholder:"Calendario"}),l.a.createElement("input",{className:G.a.extension,type:"text",value:".csv",name:"extension",id:"extension",disabled:!0})))},R=n(7),L=n.n(R),M=function(e){var a=l.a.useContext(v);return l.a.createElement(S,{onClose:e.onClose},l.a.createElement("div",{className:L.a.overall},l.a.createElement(J,{onSave:a.saveNameHandler}),l.a.createElement(I,{onCheck:a.check,university:a.university}),l.a.createElement("div",{className:L.a.buttons},l.a.createElement("button",{className:L.a["button--alt"],onClick:e.onClose},"Close"))))},V=n(14),W=n.n(V);var q=function(){var e=Object(t.useState)(!1),a=Object(c.a)(e,2),n=a[0],r=a[1];return l.a.createElement("div",{className:W.a.app},n&&l.a.createElement(M,{onClose:function(){r(!1)}}),l.a.createElement("main",null,l.a.createElement(_,{onShowSettings:function(){r(!0)}})))},Q=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,25)).then(function(a){var n=a.getCLS,t=a.getFID,l=a.getFCP,r=a.getLCP,i=a.getTTFB;n(e),t(e),l(e),r(e),i(e)})};i.a.createRoot(document.getElementById("root")).render(l.a.createElement(b,null,l.a.createElement(q,null))),Q()}],[[15,1,2]]]);
//# sourceMappingURL=main.33897e85.chunk.js.map