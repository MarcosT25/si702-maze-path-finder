<template>
  <div class="home">
    <h1>O jogo vai começar!</h1>
    <p>Selecione um ponto de entrada e um ponto de saída do labirinto</p>
    <p>OBS: a saída pode ser um outro ponto, ou um ponto aleatório dentro do tracejado laranja</p>
    <img src="../assets/home_maze.png" alt="Maze">
    <div id="drops">
      <div class="drop">
        <label for="dropdown">Escolha uma entrada:</label>
        <select id="dropdown" v-model="start">
          <option value="e1">Entrada 1</option>
          <option value="e2">Entrada 2</option>
          <option value="e3">Entrada 3</option>
          <option value="e4">Entrada 4</option>
          <option value="e5">Entrada 5</option>
          <option value="e6">Entrada 6</option>
          <option value="e7">Entrada 7</option>
          <option value="e8">Entrada 8</option>
        </select>
      </div>
      <div class="drop">
        <label for="dropdown">Escolha uma saída:</label>
        <select id="dropdown" v-model="end">
          <option value="random">Aleatório</option>
          <option value="e1">Entrada 1</option>
          <option value="e2">Entrada 2</option>
          <option value="e3">Entrada 3</option>
          <option value="e4">Entrada 4</option>
          <option value="e5">Entrada 5</option>
          <option value="e6">Entrada 6</option>
          <option value="e7">Entrada 7</option>
          <option value="e8">Entrada 8</option>
        </select>
      </div>
    </div>
    <p>Entrada: {{ start }}, Saída: {{ end }}</p>
    <button>
      <router-link to="/about">Ver resultado</router-link>
    </button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'Home',
  setup() {
    const start = ref('e1');
    const end = ref('random');

    return {
      start, end
    };
  },
};
</script>

<style scoped>
img {
  height: 55vh;
}

#drops {
  width: 20vw;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-left: auto;
  margin-right: auto;
}

.drop {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 6vh;
}
</style>