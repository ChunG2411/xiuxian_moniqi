<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { getPositionClan } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const clan = ref(null)
const member = ref([])
// const form = reactive({
//     name: '',
//     description: '',
//     notification: '',
//     leader: ''
// })
const select_leader = ref(false)


function getClan() {
    store.loading = true

    axios.get(`${store.api}/api/clan/current`, store.header)
        .then(response => {
            clan.value = response.data
            clan.value.leader = null
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
getClan()

function getMember() {
    store.loading = true

    axios.get(`${store.api}/api/clan/${props.data.path}/member?all`, store.header)
        .then(response => {
            member.value = response.data
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

function handleButton() {
    select_leader.value = !select_leader.value
    clan.value.leader = null
    if (select_leader.value) {
        getMember()
    }
}

function submit() {
    store.loading = true

    const form = new FormData()
    if (clan.value.leader) {
        form.append('leader', clan.value.leader)
    }
    form.append('name', clan.value.name)
    form.append('description', clan.value.description)
    form.append('notification', clan.value.notification)

    axios.put(`${store.api}/api/clan/current`, form, store.header)
        .then(response => {
            store.noti = {
                'title': 'success',
                'content': 'Chỉnh sửa thành công'
            }
            store.loading = false
            clan.value = null
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
    getClan()
    select_leader.value = false
}

</script>

<template>
    <div class="d-flex flex-column gap-2 p-2" v-if="clan">
        <div class="row">
            <p class="col-4">Tên</p>
            <input type="text" class="col-8" placeholder="Nhập tên môn phái" v-model="clan.name">
        </div>
        <div class="row">
            <p class="col-4">Giới thiệu</p>
            <input type="text" class="col-8" placeholder="Nhập giới thiệu" v-model="clan.description">
        </div>
        <div class="row">
            <p class="col-4">Thông báo</p>
            <input type="text" class="col-8" placeholder="Nhập thông báo" v-model="clan.notification">
        </div>
        <div class="row">
            <div class="col-4">
                <button class="btn btn-dark" @click="handleButton">Thoái vị</button>
            </div>
            <select class="col-8" v-model="clan.leader" v-if="select_leader">
                <option :value="i.char.id" v-for="i in member">{{ i.char.name }} - {{ getPositionClan(i.position) }}</option>
            </select>
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