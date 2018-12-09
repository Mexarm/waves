(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(['exports'], factory) :
  (factory((global.WChipList = {})));
}(this, (function (exports) { 'use strict';

  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //
  //

  var script = {
    name: "WChipList", // vue component name
    props: ["items", "display_prop"],
    data: function data() {
      return {
        counter: 5,
        initCounter: 5
      };
    },
    methods: {
      deleted: function deleted($event) {
          console.log($event.target);
        this.$emit("deleted", $event.target.id);
      }
    }
  };

  /* script */
              var __vue_script__ = script;
              
  /* template */
  var __vue_render__ = function() {
    var _vm = this;
    var _h = _vm.$createElement;
    var _c = _vm._self._c || _h;
    return _c("div", { staticClass: "w-chip-list" }, [
      _c(
        "ul",
        _vm._l(_vm.items, function(item) {
          return _c("li", { key: "item-" + item.id }, [
            _c(
              "div",
              {
                staticClass: "alert alert-warning alert-dismissible fade show",
                attrs: { role: "alert" }
              },
              [
                _vm._v(
                  "\n                " +
                    _vm._s(item[_vm.display_prop]) +
                    "\n                "
                ),
                _c(
                  "button",
                  {
                    staticClass: "close",
                    attrs: {
                      type: "button",
                      id: item["id"],
                      "aria-label": "Close"
                    },
                    on: { click: _vm.deleted }
                  },
                  [
                    _c(
                      "span",
                      { attrs: { id: item["id"], "aria-hidden": "true" } },
                      [_vm._v("×")]
                    )
                  ]
                )
              ]
            )
          ])
        })
      )
    ])
  };
  var __vue_staticRenderFns__ = [];
  __vue_render__._withStripped = true;

    /* style */
    var __vue_inject_styles__ = function (inject) {
      if (!inject) { return }
      inject("data-v-4c61cdea_0", { source: "\n.w-chip-list[data-v-4c61cdea] {\n  display: block;\n  width: 400px;\n  margin: 25px auto;\n  border: 1px solid #ccc;\n  background: #eaeaea;\n  text-align: center;\n  padding: 25px;\n}\n.w-chip-list p[data-v-4c61cdea] {\n  margin: 0 0 1em;\n}\n", map: {"version":3,"sources":["/Users/armandohm/web2py/applications/waves/components/w-chip-list/src/w-chip-list.vue"],"names":[],"mappings":";AAqCA;EACA,eAAA;EACA,aAAA;EACA,kBAAA;EACA,uBAAA;EACA,oBAAA;EACA,mBAAA;EACA,cAAA;CACA;AACA;EACA,gBAAA;CACA","file":"w-chip-list.vue","sourcesContent":["<template>\n    <div class=\"w-chip-list\">\n        <ul>\n            <li v-for=\"item in items\" :key=\"`item-${item.id}`\">\n\n                <div class=\"alert alert-warning alert-dismissible fade show\" role=\"alert\">\n                    {{item[display_prop]}}\n                    <button type=\"button\" :id=\"item['id']\" class=\"close\"  aria-label=\"Close\" @click=\"deleted\">\n                        <span :id=\"item['id']\" aria-hidden=\"true\">&times;</span>\n                    </button>\n                </div>\n\n            </li>\n        </ul>\n    </div>\n</template>\n\n<script>\nexport default {\n  name: \"WChipList\", // vue component name\n  props: [\"items\", \"display_prop\"],\n  data() {\n    return {\n      counter: 5,\n      initCounter: 5\n    };\n  },\n  methods: {\n    deleted($event) {\n        console.log($event.target)\n      this.$emit(\"deleted\", $event.target.id);\n    }\n  }\n};\n</script>\n\n<style scoped>\n.w-chip-list {\n  display: block;\n  width: 400px;\n  margin: 25px auto;\n  border: 1px solid #ccc;\n  background: #eaeaea;\n  text-align: center;\n  padding: 25px;\n}\n.w-chip-list p {\n  margin: 0 0 1em;\n}\n</style>\n"]}, media: undefined });

    };
    /* scoped */
    var __vue_scope_id__ = "data-v-4c61cdea";
    /* module identifier */
    var __vue_module_identifier__ = undefined;
    /* functional template */
    var __vue_is_functional_template__ = false;
    /* component normalizer */
    function __vue_normalize__(
      template, style, script$$1,
      scope, functional, moduleIdentifier,
      createInjector, createInjectorSSR
    ) {
      var component = (typeof script$$1 === 'function' ? script$$1.options : script$$1) || {};

      // For security concerns, we use only base name in production mode.
      component.__file = "/Users/armandohm/web2py/applications/waves/components/w-chip-list/src/w-chip-list.vue";

      if (!component.render) {
        component.render = template.render;
        component.staticRenderFns = template.staticRenderFns;
        component._compiled = true;

        if (functional) { component.functional = true; }
      }

      component._scopeId = scope;

      {
        var hook;
        if (style) {
          hook = function(context) {
            style.call(this, createInjector(context));
          };
        }

        if (hook !== undefined) {
          if (component.functional) {
            // register for functional component in vue file
            var originalRender = component.render;
            component.render = function renderWithStyleInjection(h, context) {
              hook.call(context);
              return originalRender(h, context)
            };
          } else {
            // inject component registration as beforeCreate hook
            var existing = component.beforeCreate;
            component.beforeCreate = existing ? [].concat(existing, hook) : [hook];
          }
        }
      }

      return component
    }
    /* style inject */
    function __vue_create_injector__() {
      var head = document.head || document.getElementsByTagName('head')[0];
      var styles = __vue_create_injector__.styles || (__vue_create_injector__.styles = {});
      var isOldIE =
        typeof navigator !== 'undefined' &&
        /msie [6-9]\\b/.test(navigator.userAgent.toLowerCase());

      return function addStyle(id, css) {
        if (document.querySelector('style[data-vue-ssr-id~="' + id + '"]')) { return } // SSR styles are present.

        var group = isOldIE ? css.media || 'default' : id;
        var style = styles[group] || (styles[group] = { ids: [], parts: [], element: undefined });

        if (!style.ids.includes(id)) {
          var code = css.source;
          var index = style.ids.length;

          style.ids.push(id);

          if (isOldIE) {
            style.element = style.element || document.querySelector('style[data-group=' + group + ']');
          }

          if (!style.element) {
            var el = style.element = document.createElement('style');
            el.type = 'text/css';

            if (css.media) { el.setAttribute('media', css.media); }
            if (isOldIE) {
              el.setAttribute('data-group', group);
              el.setAttribute('data-next-index', '0');
            }

            head.appendChild(el);
          }

          if (isOldIE) {
            index = parseInt(style.element.getAttribute('data-next-index'));
            style.element.setAttribute('data-next-index', index + 1);
          }

          if (style.element.styleSheet) {
            style.parts.push(code);
            style.element.styleSheet.cssText = style.parts
              .filter(Boolean)
              .join('\n');
          } else {
            var textNode = document.createTextNode(code);
            var nodes = style.element.childNodes;
            if (nodes[index]) { style.element.removeChild(nodes[index]); }
            if (nodes.length) { style.element.insertBefore(textNode, nodes[index]); }
            else { style.element.appendChild(textNode); }
          }
        }
      }
    }
    /* style inject SSR */
    

    
    var component = __vue_normalize__(
      { render: __vue_render__, staticRenderFns: __vue_staticRenderFns__ },
      __vue_inject_styles__,
      __vue_script__,
      __vue_scope_id__,
      __vue_is_functional_template__,
      __vue_module_identifier__,
      __vue_create_injector__,
      undefined
    );

  // Import vue component

  // install function executed by Vue.use()
  function install(Vue) {
    if (install.installed) { return; }
    install.installed = true;
    Vue.component('WChipList', component);
  }

  // Create module definition for Vue.use()
  var plugin = {
    install: install,
  };

  // To auto-install when vue is found
  /* global window global */
  var GlobalVue = null;
  if (typeof window !== 'undefined') {
    GlobalVue = window.Vue;
  } else if (typeof global !== 'undefined') {
    GlobalVue = global.Vue;
  }
  if (GlobalVue) {
    GlobalVue.use(plugin);
  }

  // It's possible to expose named exports when writing components that can
  // also be used as directives, etc. - eg. import { RollupDemoDirective } from 'rollup-demo';
  // export const RollupDemoDirective = component;

  exports.default = component;

  Object.defineProperty(exports, '__esModule', { value: true });

})));
