<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const clan = ref(null)


function getClan() {
    store.loading = true

    axios.get(`${store.api}/api/clan`, store.header)
        .then(response => {
            clan.value = response.data
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

function loadMore(path) {
    store.loading = true

    axios.get(path, store.header)
        .then(response => {
            for (let i = 0; i < response.data.results.length; i++) {
                clan.value.results.push(response.data.results[i])
            }
            clan.value.next = response.data.next
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
    getClan()
}

</script>

<template>
    <div class="clan" v-if="clan">
        <div v-if="clan.results.length == 0">
            <p>Không tìm thấy môn phái nào</p>
        </div>
        <div class="item-content-row" v-for="i in clan.results">
            <div class="item-row-left">
                <div class="item-img-small">
                    <img :src="store.api + i.image">
                </div>
                <b>{{ i.name }}</b>
            </div>
            <div class="item-row-right">
                <p>Nhân sĩ: {{ i.member }}</p>
                <div class="icon-normal" @click="addCard('clan_detail', {
        name: i.name,
        path: i.id
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
        <div v-if="clan.next" class="w-100 text-center mt-2">
            <button type="button" class="btn btn-primary" @click="loadMore(clan.next)">Xem thêm</button>
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