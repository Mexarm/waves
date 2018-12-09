<template>
    <div class="w-chip-list">
        <ul>
            <li v-for="item in items" :key="`item-${item.id}`">

                <div class="alert alert-warning alert-dismissible fade show" role="alert">
                    {{item[display_prop]}}
                    <button type="button" :id="item['id']" class="close"  aria-label="Close" @click="deleted">
                        <span :id="item['id']" aria-hidden="true">&times;</span>
                    </button>
                </div>

            </li>
        </ul>
    </div>
</template>

<script>
export default {
  name: "WChipList", // vue component name
  props: ["items", "display_prop"],
  data() {
    return {
      counter: 5,
      initCounter: 5
    };
  },
  methods: {
    deleted($event) {
        console.log($event.target)
      this.$emit("deleted", $event.target.id);
    }
  }
};
</script>

<style scoped>
.w-chip-list {
  display: block;
  width: 400px;
  margin: 25px auto;
  border: 1px solid #ccc;
  background: #eaeaea;
  text-align: center;
  padding: 25px;
}
.w-chip-list p {
  margin: 0 0 1em;
}
</style>
