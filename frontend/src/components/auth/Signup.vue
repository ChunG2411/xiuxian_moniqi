<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'


const store = Store()

const props = defineProps({
    data: Object
})
const user = reactive({
    email: '',
    password: '',
    check: false
})


function Sigup() {
    if (!user.check || !user.email || !user.password) {
        store.noti = {
            'title': 'error',
            'content': 'Enter user information'
        }
        return
    }
    store.loading = true

    const form = new FormData()
    form.append('email', user.email)
    form.append('password', user.password)

    axios.post(`${store.api}/api/register`, form)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Register successfull'
            }
        })
        .catch(error => {
            store.loading = false
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
        })
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4">
        <h3>Đăng ký</h3>
        <div class="align-items-center d-flex flex-column gap-2 w-100">
            <input type="text" placeholder="Email" v-model="user.email">
            <input type="text" placeholder="Password" v-model="user.password" v-on:keyup.enter="Sigup">
            <div class="align-items-center d-flex gap-2">
                <input type="checkbox" class="checkbox" v-model="user.check">
                <small>Tôi đồng ý với điều khoản sử dụng</small>
            </div>
            <button class="btn btn-primary" type="button" @click="Sigup">Đăng ký</button>
        </div>
    </div>
</template>

<style></style>