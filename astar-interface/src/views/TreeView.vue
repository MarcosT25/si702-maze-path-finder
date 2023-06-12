<template>
  <div class="tree">
    <h1>Grafo resultante</h1>
    <div>{{ $route.params.graphs }}</div>
    <!-- <div style="display: flex; flex-direction: row;">
    </div> -->
    <div>
      <div style="display: flex; flex-direction: row;">
        <blocks-tree :data="Data" :collapsable="true"
          :props="{ label: 'name', expand: 'expand', children: 'children', key: 'value' }"
          style="background-color: #f5f5f5;">
          <template #node="{ data, context }">
            <span :style="`color: ${data.color}`">{{ data.name }}</span>
            <br>
            <span :style="`color: ${data.color}`">{{ data.value }}</span>
          </template>
        </blocks-tree>
        <div>
          <button @click="start">&lt;&lt;</button>
          <button @click="increment">&lt;</button>
          <button @click="decrement">></button>
          <button @click="end">>></button>
          <p>Nós Abertos:</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, reactive } from 'vue';
import json from '../../public/final-graph.json'
import lists from '../../public/open-closed-lists.json'

export default defineComponent({
  props: {
    lists: {
      type: Array,
      default: () => lists
    }
  },
  data() {
    return {
      iteration: 0
    }
  },
  methods: {
    listsFilter(i) {
      return this.lists[i]
    },
    selectList(i) {
      this.iteration += i
    }
  },

  setup() {
    // let i = json.length;
    // const Data = ref({ value: json });
    // // const refresh = () => {
    // // }


    // const start = () => {
    //   i = 0
    //   Object.assign(Data.value, json[i])
    // }

    // const decrement = () => {
    //   i--
    //   // Data = ref({});
    //   // delete Data.value;
    //   Object.assign(Data.value, json[i])
    //   console.log(i);
    // }

    // const increment = () => {
    //   i++
    //   if (Data.value === null) {
    //     Object.assign(null, {})
    //   } else {
    //     Object.assign(Data.value, json[i])
    //   }
    //   console.log(i);
    // }

    // const end = () => {
    //   i = json.length
    //   Object.assign(Data.value, json[i])
    // }



    return { Data: json };
  },
});

</script>