<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard, getPositionClan } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const member = ref(null)


function getMember() {
    store.loading = true

    axios.patch(`${store.api}/api/organization/current`, {}, store.header)
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
getMember()

function loadMore(path) {
    store.loading = true

    axios.get(path, store.header)
        .then(response => {
            for (let i = 0; i < response.data.results.length; i++) {
                member.value.results.push(response.data.results[i])
            }
            member.value.next = response.data.next
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
    getMember()
}

</script>

<template>
    <div class="clan" v-if="member">
        <div class="item-content-row" v-for="(i, index) in member.results">
            <div class="item-row-left">
                <b>{{ i.name }}</b>
            </div>
            <div class="item-row-right">
                <p>Cấp độ: {{ i.level }}</p>
                <div class="icon-normal" @click="addCard('locality_detail', {
                    name: i.name,
                    path: i.id
                })" v-if="index != 0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
                <div class="icon-normal" @click="addCard('locality')" v-else>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
            </div>
        </div>
        <div v-if="member.next" class="w-100 text-center mt-2">
            <button type="button" class="btn btn-primary" @click="loadMore(member.next)">Xem thêm</button>
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