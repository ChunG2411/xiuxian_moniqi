import { createRouter, createWebHistory } from 'vue-router'

import Auth from '../views/Auth.vue'
import Home from '../views/Home.vue'


const routes = [
    {
        name: "auth",
        path: "/login",
        component: Auth
    },
    {
        name: "home",
        path: "/",
        component: Home
    },

]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router