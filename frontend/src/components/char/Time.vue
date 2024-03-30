<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const bag = ref(null)
const active = ref('1')
const time = ref(null)


function getTime() {
    axios.get(`${store.api}/api/cur-time`)
        .then(response => {
            time.value = response.data
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
        })
}
getTime()

function reload() {
    getTime()
}

</script>

<template>
    <div class="bag" v-if="time">
        <b>Ngày {{ time.day }} Năm Khai Thổ thứ {{ time.year }}</b>
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

<style>
.nav-tab {
    display: flex;
    border-bottom: 1px solid var(--tab_border_color);
    position: absolute;
    top: 35px;
    width: calc(100% - 20px);
    background-color: var(--card_color);
    z-index: 100;
    padding-top: 10px;
}

.nav-tab .tab {
    padding: 5px 15px;
    margin-bottom: -1px;
    cursor: pointer;
}

.nav-tab .active {
    border: 1px solid var(--tab_border_color);
    border-bottom: 0;
    background-color: var(--card_color);
}

.nav-content {
    margin-top: 40px;
}

.nav-content-row {
    display: flex;
    justify-content: space-between;
    padding: 10px;
}

.nav-content-row:hover {
    background-color: var(--hover_item_color);
    border-radius: 10px
}
</style>