<template>
  <h1>Caminho final</h1>
  <img :src="imageSrc" alt="Solve" style="height: 30vh;" />
  <div class="tree">
    <h1>Árvore e listas resultantes</h1>
    <div>{{ $route.params.graphs }}</div>
    <div>
      <div style="display: flex; flex-direction: row; justify-content: center;">
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
          <div>
            <button type="button" v-show="iteration > 0" @click="selectList(-iteration)">&lt;&lt;</button>
            <button type="button" v-show="iteration > 0" @click="selectList(-1)">&lt;</button>
            <button type="button" v-show="iteration < lists.length - 1" @click="selectList(1)">></button>
            <button type="button" v-show="iteration < lists.length - 1"
              @click="selectList(lists.length - iteration - 1)">>></button>
          </div>
          <p>Expansão: {{ iteration + 1 }}</p>
          <ul>
            <li v-for="(list, i) in listsFilter(iteration)" :key="i">
              <p>{{ i }}</p>
              <ul v-if="list.length">
                <li v-for="item in list">
                  <p>{{ item }}</p>
                </li>
              </ul>
              <p v-else>lista vazia</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, reactive } from 'vue';

export default defineComponent({
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

  computed: {
    imageSrc() {
      return `data:image/jpeg;base64,${localStorage.getItem('image')}`;
    },
  },

  setup() {
    var lists = JSON.parse(localStorage.getItem('lists'));
    var tree = JSON.parse(localStorage.getItem('tree'));
    return { Data: tree, lists };

  },
});

</script>