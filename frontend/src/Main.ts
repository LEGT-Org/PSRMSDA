import { createApp } from 'vue';
import '@/assets/Css/App.css';

import App from './App.vue';
import router from './router/Router.ts';

const app = createApp(App);

app.use(router);

app.mount('#app');
