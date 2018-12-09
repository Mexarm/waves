(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(['exports'], factory) :
  (factory((global.WAutocomplete = {})));
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
  //
  //

  //import axios from "axios";

  var debounced = null;
  var script = {
    name: "WAutocomplete", // vue component name

    props: {
      // items: {
      //   default: function() {
      //       return []
      //       },
      //   type: Array
      // },
      id: {
          required: true
      },
      filterby: {
        type: String
      },
      title: {
        default: "Select One...",
        type: String
      },
      url: {
        type: String
      },
      shouldReset: {
        type: Boolean,
        default: true
      }
    },
    data: function data() {
      return {
        itemHeight: 39,
        selectedItem: null,
        selected: 0,
        query: "",
        visible: false,
        items: [],
        isLoading: false,
        //element: null,
      };
    },
    methods: {
      getItems: function getItems() {
        var this$1 = this;

        this.isLoading = true;
        var url = this.url.replace('__query__',this.query);
        axios
          .get(url)
          .then(function (res) { return res.data; })
          .then(function (data) { return data.content; })
          .then(function (content) {
            this$1.items = content;
            this$1.isLoading = false;
          });
      },
      toggleVisible: function toggleVisible() {
        var this$1 = this;

        this.visible = !this.visible;
        setTimeout(function () {
          this$1.$refs.input.focus();
        }, 50);
      },
      itemClicked: function itemClicked(index) {
        this.selected = index;
        this.selectItem();
      },
      selectItem: function selectItem() {
        if (!this.matches.length) {
          return;
        }
        this.selectedItem = this.matches[this.selected];
        //this.element.val(this.selectedItem[this.filterby])
        this.visible = false;
        if (this.shouldReset) {
          this.query = "";
          this.selected = 0;
        }
        this.$emit("selected", JSON.parse(JSON.stringify(this.selectedItem)));
      },
      up: function up() {
        if (this.selected == 0) {
          return;
        }
        this.selected -= 1;
        this.scrollToItem();
      },
      down: function down() {
        if (this.selected >= this.matches.length - 1) {
          return;
        }
        this.selected += 1;
        this.scrollToItem();
      },
      scrollToItem: function scrollToItem() {
        this.$refs.optionsList.scrollTop = this.selected * this.itemHeight;
      }
    },
    watch: {
      query: function query() {
        debounced();
      }
    },
    computed: {
      matches: function matches() {
        var this$1 = this;

        this.$emit("change", this.query);
        if (this.query == "") {
          return this.items.slice(0, 10);
        }
        return this.items.filter(function (item) { return item[this$1.filterby].toLowerCase().includes(this$1.query.toLowerCase()); }
        );
      },
      selectedId: function selectedId() {
        if (this.selectedItem) {
          return this.selectedItem['id']
        }
      }
    },
    mounted: function mounted() {
        var this$1 = this;

        this.$nextTick(function () {
            debounced = _.debounce(this$1.getItems, 200);
            this$1.getItems();
            //this.element = jQuery('#'+this.id)
            //this.query = this.element.val()

        });
    }
  };

  /* script */
              var __vue_script__ = script;
              
  /* template */
  var __vue_render__ = function() {
    var _vm = this;
    var _h = _vm.$createElement;
    var _c = _vm._self._c || _h;
    return _c("div", { staticClass: "autocomplete" }, [
      _c("div", {
        staticClass: "input",
        domProps: {
          textContent: _vm._s(
            _vm.selectedItem ? _vm.selectedItem[_vm.filterby] : ""
          )
        },
        on: { click: _vm.toggleVisible }
      }),
      _vm._v(" "),
      _vm.selectedItem == null
        ? _c("div", {
            staticClass: "placeholder",
            domProps: { textContent: _vm._s(_vm.title) }
          })
        : _vm._e(),
      _vm._v(" "),
      _vm.selectedItem
        ? _c(
            "button",
            {
              staticClass: "close",
              on: {
                click: function($event) {
                  _vm.selectedItem = null;
                }
              }
            },
            [_vm._v("x")]
          )
        : _vm._e(),
      _vm._v(" "),
      _c(
        "div",
        {
          directives: [
            {
              name: "show",
              rawName: "v-show",
              value: _vm.visible,
              expression: "visible"
            }
          ],
          staticClass: "popover"
        },
        [
          _c("input", {
            directives: [
              {
                name: "model",
                rawName: "v-model",
                value: _vm.query,
                expression: "query"
              }
            ],
            ref: "input",
            attrs: { type: "text", placeholder: "Start Typing..." },
            domProps: { value: _vm.query },
            on: {
              keydown: [
                function($event) {
                  if (
                    !("button" in $event) &&
                    _vm._k($event.keyCode, "up", 38, $event.key, [
                      "Up",
                      "ArrowUp"
                    ])
                  ) {
                    return null
                  }
                  return _vm.up($event)
                },
                function($event) {
                  if (
                    !("button" in $event) &&
                    _vm._k($event.keyCode, "down", 40, $event.key, [
                      "Down",
                      "ArrowDown"
                    ])
                  ) {
                    return null
                  }
                  return _vm.down($event)
                },
                function($event) {
                  if (
                    !("button" in $event) &&
                    _vm._k($event.keyCode, "enter", 13, $event.key, "Enter")
                  ) {
                    return null
                  }
                  $event.preventDefault();
                  return _vm.selectItem($event)
                }
              ],
              input: function($event) {
                if ($event.target.composing) {
                  return
                }
                _vm.query = $event.target.value;
              }
            }
          }),
          _vm._v(" "),
          _c(
            "div",
            {
              directives: [
                {
                  name: "show",
                  rawName: "v-show",
                  value: _vm.isLoading,
                  expression: "isLoading"
                }
              ],
              staticClass: "options"
            },
            [_vm._v("LOADING...")]
          ),
          _vm._v(" "),
          _c(
            "div",
            {
              directives: [
                {
                  name: "show",
                  rawName: "v-show",
                  value: !_vm.isLoading,
                  expression: "!isLoading"
                }
              ],
              ref: "optionsList",
              staticClass: "options"
            },
            [
              _c(
                "ul",
                _vm._l(_vm.matches, function(match, index) {
                  return _c("li", {
                    key: index,
                    class: { selected: _vm.selected == index },
                    domProps: { textContent: _vm._s(match[_vm.filterby]) },
                    on: {
                      click: function($event) {
                        _vm.itemClicked(index);
                      }
                    }
                  })
                })
              )
            ]
          )
        ]
      )
    ])
  };
  var __vue_staticRenderFns__ = [];
  __vue_render__._withStripped = true;

    /* style */
    var __vue_inject_styles__ = function (inject) {
      if (!inject) { return }
      inject("data-v-a6a304d6_0", { source: "\n.autocomplete[data-v-a6a304d6] {\n  width: 100%;\n  position: relative;\n}\n.input[data-v-a6a304d6] {\n  height: 40px;\n  border-radius: 3px;\n  border: 2px solid lightgray;\n  box-shadow: 0 0 10px #eceaea;\n  font-size: 25px;\n  padding-left: 10px;\n  padding-top: 10px;\n  cursor: text;\n}\n.close[data-v-a6a304d6] {\n  position: absolute;\n  right: 2px;\n  top: 4px;\n  background: none;\n  border: none;\n  font-size: 30px;\n  color: lightgrey;\n  cursor: pointer;\n}\n.placeholder[data-v-a6a304d6] {\n  position: absolute;\n  top: 11px;\n  left: 11px;\n  font-size: 25px;\n  color: #d0d0d0;\n  pointer-events: none;\n}\n.popover[data-v-a6a304d6] {\n  min-height: 50px;\n  border: 2px solid lightgray;\n  position: absolute;\n  top: 46px;\n  left: 0;\n  right: 0;\n  background: #fff;\n  border-radius: 3px;\n  text-align: center;\n}\n.popover input[data-v-a6a304d6] {\n  width: 95%;\n  margin-top: 5px;\n  height: 40px;\n  font-size: 16px;\n  border-radius: 3px;\n  border: 1px solid lightgray;\n  padding-left: 8px;\n}\n.options[data-v-a6a304d6] {\n  max-height: 150px;\n  overflow-y: scroll;\n  margin-top: 5px;\n}\n.options ul[data-v-a6a304d6] {\n  list-style-type: none;\n  text-align: left;\n  padding-left: 0;\n}\n.options ul li[data-v-a6a304d6] {\n  border-bottom: 1px solid lightgray;\n  padding: 10px;\n  cursor: pointer;\n  background: #f1f1f1;\n}\n.options ul li[data-v-a6a304d6]:first-child {\n  border-top: 2px solid #d6d6d6;\n}\n.options ul li[data-v-a6a304d6]:not(.selected):hover {\n  background: #8c8c8c;\n  color: #fff;\n}\n.options ul li.selected[data-v-a6a304d6] {\n  background: #58bd4c;\n  color: #fff;\n  font-weight: 600;\n}\n", map: {"version":3,"sources":["/Users/armandohm/web2py/applications/waves/components/w-autocomplete/src/w-autocomplete.vue"],"names":[],"mappings":";AAuJA;EACA,YAAA;EACA,mBAAA;CACA;AACA;EACA,aAAA;EACA,mBAAA;EACA,4BAAA;EACA,6BAAA;EACA,gBAAA;EACA,mBAAA;EACA,kBAAA;EACA,aAAA;CACA;AACA;EACA,mBAAA;EACA,WAAA;EACA,SAAA;EACA,iBAAA;EACA,aAAA;EACA,gBAAA;EACA,iBAAA;EACA,gBAAA;CACA;AACA;EACA,mBAAA;EACA,UAAA;EACA,WAAA;EACA,gBAAA;EACA,eAAA;EACA,qBAAA;CACA;AACA;EACA,iBAAA;EACA,4BAAA;EACA,mBAAA;EACA,UAAA;EACA,QAAA;EACA,SAAA;EACA,iBAAA;EACA,mBAAA;EACA,mBAAA;CACA;AACA;EACA,WAAA;EACA,gBAAA;EACA,aAAA;EACA,gBAAA;EACA,mBAAA;EACA,4BAAA;EACA,kBAAA;CACA;AACA;EACA,kBAAA;EACA,mBAAA;EACA,gBAAA;CACA;AACA;EACA,sBAAA;EACA,iBAAA;EACA,gBAAA;CACA;AACA;EACA,mCAAA;EACA,cAAA;EACA,gBAAA;EACA,oBAAA;CACA;AACA;EACA,8BAAA;CACA;AACA;EACA,oBAAA;EACA,YAAA;CACA;AACA;EACA,oBAAA;EACA,YAAA;EACA,iBAAA;CACA","file":"w-autocomplete.vue","sourcesContent":["<template>\n    <div class=\"autocomplete\">\n        <!-- <slot></slot> -->\n        <!-- <input :id=\"id+'__selectedId'\" :name=\"id+'__selectedId'\" v-model=\"selectedId\" type=\"text\" hidden>  -->\n        <div class=\"input\" @click=\"toggleVisible\" v-text=\"selectedItem ? selectedItem[filterby] : ''\"></div>\n        <div class=\"placeholder\" v-if=\"selectedItem == null\" v-text=\"title\"></div>\n        <button class=\"close\" @click=\"selectedItem = null\" v-if=\"selectedItem\">x</button>\n        <div class=\"popover\" v-show=\"visible\">\n            <input type=\"text\" ref=\"input\" v-model=\"query\" @keydown.up=\"up\" @keydown.down=\"down\" @keydown.enter.prevent=\"selectItem\" placeholder=\"Start Typing...\">\n            <div class=\"options\" v-show=\"isLoading\">LOADING...</div>\n            <div class=\"options\" v-show=\"!isLoading\" ref=\"optionsList\">\n                <ul>\n                    <li v-for=\"(match, index) in matches\" :key=\"index\" :class=\"{ 'selected': (selected == index)}\" @click=\"itemClicked(index)\" v-text=\"match[filterby]\"></li>\n                </ul>\n            </div>\n        </div>\n    </div>\n</template>\n\n<script>\n//import axios from \"axios\";\n\nlet debounced = null;\nexport default {\n  name: \"WAutocomplete\", // vue component name\n\n  props: {\n    // items: {\n    //   default: function() {\n    //       return []\n    //       },\n    //   type: Array\n    // },\n    id: {\n        required: true\n    },\n    filterby: {\n      type: String\n    },\n    title: {\n      default: \"Select One...\",\n      type: String\n    },\n    url: {\n      type: String\n    },\n    shouldReset: {\n      type: Boolean,\n      default: true\n    }\n  },\n  data() {\n    return {\n      itemHeight: 39,\n      selectedItem: null,\n      selected: 0,\n      query: \"\",\n      visible: false,\n      items: [],\n      isLoading: false,\n      //element: null,\n    };\n  },\n  methods: {\n    getItems() {\n      this.isLoading = true;\n      var url = this.url.replace('__query__',this.query)\n      axios\n        .get(url)\n        .then(res => res.data)\n        .then(data => data.content)\n        .then(content => {\n          this.items = content;\n          this.isLoading = false;\n        });\n    },\n    toggleVisible() {\n      this.visible = !this.visible;\n      setTimeout(() => {\n        this.$refs.input.focus();\n      }, 50);\n    },\n    itemClicked(index) {\n      this.selected = index;\n      this.selectItem();\n    },\n    selectItem() {\n      if (!this.matches.length) {\n        return;\n      }\n      this.selectedItem = this.matches[this.selected];\n      //this.element.val(this.selectedItem[this.filterby])\n      this.visible = false;\n      if (this.shouldReset) {\n        this.query = \"\";\n        this.selected = 0;\n      }\n      this.$emit(\"selected\", JSON.parse(JSON.stringify(this.selectedItem)));\n    },\n    up() {\n      if (this.selected == 0) {\n        return;\n      }\n      this.selected -= 1;\n      this.scrollToItem();\n    },\n    down() {\n      if (this.selected >= this.matches.length - 1) {\n        return;\n      }\n      this.selected += 1;\n      this.scrollToItem();\n    },\n    scrollToItem() {\n      this.$refs.optionsList.scrollTop = this.selected * this.itemHeight;\n    }\n  },\n  watch: {\n    query() {\n      debounced();\n    }\n  },\n  computed: {\n    matches() {\n      this.$emit(\"change\", this.query);\n      if (this.query == \"\") {\n        return this.items.slice(0, 10);\n      }\n      return this.items.filter(item =>\n        item[this.filterby].toLowerCase().includes(this.query.toLowerCase())\n      );\n    },\n    selectedId() {\n      if (this.selectedItem) {\n        return this.selectedItem['id']\n      }\n    }\n  },\n  mounted() {\n      this.$nextTick(() => {\n          debounced = _.debounce(this.getItems, 200);\n          this.getItems();\n          //this.element = jQuery('#'+this.id)\n          //this.query = this.element.val()\n\n      })\n  }\n};\n</script>\n\n<style scoped>\n.autocomplete {\n  width: 100%;\n  position: relative;\n}\n.input {\n  height: 40px;\n  border-radius: 3px;\n  border: 2px solid lightgray;\n  box-shadow: 0 0 10px #eceaea;\n  font-size: 25px;\n  padding-left: 10px;\n  padding-top: 10px;\n  cursor: text;\n}\n.close {\n  position: absolute;\n  right: 2px;\n  top: 4px;\n  background: none;\n  border: none;\n  font-size: 30px;\n  color: lightgrey;\n  cursor: pointer;\n}\n.placeholder {\n  position: absolute;\n  top: 11px;\n  left: 11px;\n  font-size: 25px;\n  color: #d0d0d0;\n  pointer-events: none;\n}\n.popover {\n  min-height: 50px;\n  border: 2px solid lightgray;\n  position: absolute;\n  top: 46px;\n  left: 0;\n  right: 0;\n  background: #fff;\n  border-radius: 3px;\n  text-align: center;\n}\n.popover input {\n  width: 95%;\n  margin-top: 5px;\n  height: 40px;\n  font-size: 16px;\n  border-radius: 3px;\n  border: 1px solid lightgray;\n  padding-left: 8px;\n}\n.options {\n  max-height: 150px;\n  overflow-y: scroll;\n  margin-top: 5px;\n}\n.options ul {\n  list-style-type: none;\n  text-align: left;\n  padding-left: 0;\n}\n.options ul li {\n  border-bottom: 1px solid lightgray;\n  padding: 10px;\n  cursor: pointer;\n  background: #f1f1f1;\n}\n.options ul li:first-child {\n  border-top: 2px solid #d6d6d6;\n}\n.options ul li:not(.selected):hover {\n  background: #8c8c8c;\n  color: #fff;\n}\n.options ul li.selected {\n  background: #58bd4c;\n  color: #fff;\n  font-weight: 600;\n}\n</style>\n"]}, media: undefined });

    };
    /* scoped */
    var __vue_scope_id__ = "data-v-a6a304d6";
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
      component.__file = "/Users/armandohm/web2py/applications/waves/components/w-autocomplete/src/w-autocomplete.vue";

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
    Vue.component('WAutocomplete', component);
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
