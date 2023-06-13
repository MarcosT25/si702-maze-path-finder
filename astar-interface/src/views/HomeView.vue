<template>
  <div class="home">
    <h1>O jogo vai começar!</h1>
    <p>Selecione um ponto de entrada para o labirinto, a heurística desejada e uma seed</p>
    <p>OBS: o troféu será gerado em um ponto aleatório dentro do tracejado laranja, com base na seed</p>
    <img src="../assets/home-maze.png" alt="Maze">
    <div id="drops">
      <div class="drop">
        <label for="dropdown">Escolha uma entrada:</label>
        <select id="dropdown" v-model="start">
          <option value="1">Entrada 1</option>
          <option value="2">Entrada 2</option>
          <option value="3">Entrada 3</option>
          <option value="4">Entrada 4</option>
          <option value="5">Entrada 5</option>
          <option value="6">Entrada 6</option>
          <option value="7">Entrada 7</option>
          <option value="8">Entrada 8</option>
        </select>
      </div>
      <div class="drop">
        <label for="dropdown">Escolha uma heurística:</label>
        <select id="dropdown" v-model="heuristic">
          <option value="1">Heurística admissível</option>
          <option value="2">Heurística não admissível</option>
        </select>
      </div>
      <div class="drop">
        <label for="dropdown">Seed (número):</label>
        <input type="text" v-model="seed" />
      </div>
    </div>
    <button v-on:click="saveToStorage()" id="button">
      <router-link to="/tree">Ver resultado</router-link>
    </button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'Home',
  methods: {
    saveToStorage: async function () {
      var url = "http://localhost:5000/solve/" + this.start + '/' + this.heuristic + '/' + this.seed
      const res = await fetch(url)
      const obj = await res.json();
      localStorage.setItem('image', obj[Object.keys(obj)[0]]);
      localStorage.setItem('lists', obj[Object.keys(obj)[1]]);
      localStorage.setItem('tree', obj[Object.keys(obj)[2]]);
    }
  },
  setup() {
    const start = ref('1');
    const heuristic = ref('1')
    var seed = 0

    return {
      start, heuristic, seed
    };
  },
}
</script>

<style scoped>
img {
  height: 55vh;
}

#drops {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-left: auto;
  margin-right: auto;
  width: 30vw;
}

.drop {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 6vh;
}

#button {
  margin-top: 2vh;
  padding: 13px;
  color: black;
}
</style>