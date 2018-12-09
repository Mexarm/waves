# vue components
https://www.npmjs.com/package/vue-sfc-rollup

* install npm package vue-sfc-rollup & vue cli 3 globally
```
   npm install -g @vue/cli
   npm install -g @vue/cli-service-global
   npm install -g vue-sfc-rollup
   sfc-rollup-init
```
* fill in prompts 
* `cd path/to/my-component-or-lib`
* if single component 
   * `vue serve ./src/my-component.vue`
   * Use @vue/cli or other live-refresh coding 
* if library 
   * `vue serve ./src/lib-dev.vue`
   *  Use @vue/cli or other live-refresh coding 
* Do dev stuff... 
   * `npm run build`
* Ready to publish! 

* now copy dist/*.min.js to ../static/js

and in the view use your component

```html
<div id="app">
    <h1>
            [%myvar%]
    </h1>
    <w-autocomplete>
    </w-autocomplete>
</div>

{{=grid}}

{{if ('edit/tenant_attachment' in '/'.join(request.args)):}}
{{ if configuration.get('app.production'):}}
<script src="{{=URL('static','/js/vue.min.js')}}"></script>
{{else:}}
<script src="{{=URL('static','/js/vue.js')}}"></script>
{{pass}}
<!-- Include after Vue -->
<script src="{{=URL('static','/js/w-autocomplete.min.js')}}"></script>

<script>
console.log(WAutocomplete)
    var vm = new Vue({
        delimiters: ['[%', '%]'],
        components: {
            'w-autocomplete': WAutocomplete.default
        },
        el: '#app',
        data: {
             myvar: "Vue is awesome!!"
        }

    })
</script>
```

# waves
