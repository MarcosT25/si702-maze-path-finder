import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueBlocksTree from 'vue3-blocks-tree';
import 'vue3-blocks-tree/dist/vue3-blocks-tree.css';

let defaultoptions = { treeName: 'blocks-tree' }

createApp(App).component('blocks-tree', VueBlocksTree).use(router, VueBlocksTree).mount('#app')
