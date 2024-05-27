<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { getLocality } from '../../utils/function.js'


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


function restore(type) {
    store.loading = true

    const form = new FormData()
    form.append(type, '1')

    axios.put(`${store.api}/api/locality/current`, form, store.header)
        .then(response => {
            store.noti = {
                'title': 'success',
                'content': 'Hồi phục thành công'
            }
            store.loading = false
            getDetail()
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
        <div class="row d-flex align-items-center">
            <p class="col-8">Phòng thủ: {{ locality.defender }} / {{ getLocality('defender') * locality.level }}</p>
            <button class="btn btn-success col-4" @click="restore('defender')">Hồi phục</button>
        </div>
        <div class="row d-flex align-items-center">
            <p class="col-8">Nhân số: {{ locality.power }} / {{ getLocality('power') * locality.level }}</p>
            <button class="btn btn-success col-4" @click="restore('power')">Hồi phục</button>
        </div>
        <div class="row d-flex align-items-center">
            <p class="col-8">Cấp độ: {{ locality.level }}</p>
            <button class="btn btn-primary col-4" @click="restore('level')">Tăng cấp</button>
        </div>
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