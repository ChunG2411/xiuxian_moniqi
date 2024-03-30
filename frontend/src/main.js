import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from "vue-toastification";

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import "vue-toastification/dist/index.css";

import './assets/css/style.css'
import App from './App.vue'
import router from './router/router.js'

const app = createApp(App)
const pinia = createPinia()

const options = {
    closeButtonClassName: 'toast-button',
    icon: false,
    timeout: 3000,
    closeButton: false,
    toastClassName: "custom-toast",
    bodyClassName: ["custom-toast-body"],
    position: 'bottom-right'
};

app.use(pinia)
app.use(Toast, options);
app.use(router)
app.mount('#app')
