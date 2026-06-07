import { createApp } from 'vue';
import { createPinia } from 'pinia';
import '@/assets/Css/App.css';

import App from './App.vue';
import router from './router/Router.ts';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount('#app');
