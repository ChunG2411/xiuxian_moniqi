<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'


const store = Store()

const props = defineProps({
    data: Object
})
const locality = ref(null)


function getDetail() {
    store.loading = true

    axios.get(`${store.api}/api/locality/current`, store.header)
        .then(response => {
            locality.value = response.data
            store.loading = false
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}
getDetail()


function submit() {
    store.loading = true

    const form = new FormData()
    form.append('name', locality.value.name)

    axios.put(`${store.api}/api/locality`, form, store.header)
        .then(response => {
            store.noti = {
                'title': 'success',
                'content': 'Chỉnh sửa thành công'
            }
            store.loading = false
            locality.value = null
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

function reload() {
    getDetail()
}

</script>

<template>
    <div class="d-flex flex-column gap-2 p-2" v-if="locality">
        <div class="row">
            <p class="col-4 d-flex align-items-center">Tên thế lực</p>
            <input type="text" class="col-8" placeholder="Nhập tên thế lực" v-model="locality.name">
        </div>
        <button class="btn btn-success" @click="submit">Thay đổi</button>
    </div>
    <div v-else></div>

    <div class="reload">
        <div class="icon-small" @click="reload">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38" />
            </svg>
        </div>
    </div>
</template>

<style></style>