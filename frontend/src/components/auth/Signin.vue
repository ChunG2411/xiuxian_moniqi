<script setup>
import { defineProps, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import Store from '../../utils/store.js'
import { resetCard } from '../../utils/function.js'


const store = Store()
const router = useRouter()

const props = defineProps({
    data: Object
})
const user = reactive({
    username: '',
    password: ''
})


function Sigin() {
    if (!user.username || !user.password) {
        store.noti = {
            'title': 'error',
            'content': 'Enter user information'
        }
        return
    }
    store.loading = true
    
    const form = new FormData()
    form.append('username_email', user.username)
    form.append('password', user.password)

    axios.post(`${store.api}/api/login`, form)
        .then(response => {
            localStorage.setItem('token', response.data.access)
            resetCard()
            store.loading = false
            router.push({ path: '/' })
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4">
        <h3>Đăng nhập</h3>
        <div class="align-items-center d-flex flex-column gap-2 w-100">
            <input type="text" placeholder="Username or Email" v-model="user.username">
            <input type="password" placeholder="Password" v-model="user.password" v-on:keyup.enter="Sigin">
            <button class="btn btn-primary" type="button" @click="Sigin">Đăng nhập</button>
        </div>
    </div>
</template>

<style></style>