<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const arena = ref([])
const my_arena = ref(null)


function myArena() {
    store.loading = true

    axios.get(`${store.api}/api/arena/current`, store.header)
        .then(response => {
            my_arena.value = response.data
            store.loading = false
        })
        .catch(_ => {
            store.loading = false
        })
}
myArena()

function listArena() {
    store.loading = true

    axios.get(`${store.api}/api/arena`, store.header)
        .then(response => {
            arena.value = response.data.results
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
listArena()

function createArena() {
    store.loading = true

    axios.post(`${store.api}/api/arena`, {}, store.header)
        .then(response => {
            store.loading = false
            my_arena.value = response.data
            store.noti = {
                'title': 'success',
                'content': "Đã tạo thành công"
            }
        })
        .catch(_ => {
            store.noti = {
                'title': 'error',
                'content': 'Vui lòng thử lại sau'
            }
            store.loading = false
        })
}

function delArena() {
    store.loading = true

    axios.delete(`${store.api}/api/arena`, store.header)
        .then(response => {
            store.loading = false
            my_arena.value = null
            store.noti = {
                'title': 'success',
                'content': "Đã huỷ thành công"
            }
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

function attack(id) {
    store.loading = true

    axios.post(`${store.api}/api/arena/${id}`, {}, store.header)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': "Đang tấn công"
            }
            listArena()
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

function loadMore(path) {
    store.loading = true

    axios.get(path, store.header)
        .then(response => {
            for (let i = 0; i < response.data.results.length; i++) {
                arena.value.results.push(response.data.results[i])
            }
            arena.value.next = response.data.next
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

function reload() {
    myArena()
    listArena()
}

</script>

<template>
    <div class="city">
        <div class="item-content-row" v-if="my_arena">
            <b>Số {{ my_arena.number }}</b>
            <p>Đang chờ đối thủ</p>
            <button class="btn btn-danger" @click="delArena">Huỷ</button>
        </div>
        <div class="w-100 d-flex justify-content-center" v-else>
            <button class="btn btn-primary" @click="createArena">Tạo đấu trường</button>
        </div>
        <div class="item-content-row" v-for="i in arena">
            <div class="item-row-left">
                <b>Số {{ i.number }}</b>
            </div>
            <div class="item-row-right w-75">
                <button class="btn btn-warning" @click="attack(i.id)">Tham chiến</button>
                <div class="icon-normal" @click="addCard('char', {
                    name: i.char.name,
                    path: i.char.id
                })">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
            </div>
        </div>
        <div v-if="arena.next" class="w-100 text-center mt-2">
            <button type="button" class="btn btn-primary" @click="loadMore(arena.next)">Xem thêm</button>
        </div>
    </div>

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