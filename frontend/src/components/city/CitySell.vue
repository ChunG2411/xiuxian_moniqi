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


function getBag(tab) {
    store.loading = true

    axios.get(`${store.api}/api/bag?tab=${tab}`, store.header)
        .then(response => {
            bag.value = response.data
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
getBag('1')

function activeTab(e) {
    const tabs = document.querySelectorAll('.city-tab-item')
    active.value = e.target.id
    getBag(e.target.id)
    tabs.forEach((tab) => {
        tab.classList.remove('active')
    })
    e.target.classList.add('active')
}

function reload() {
    getBag(active.value)
}

</script>

<template>
    <div class="city" v-if="bag">
        <div class="city-tab">
            <p class="city-tab-item active" id="1" @click="activeTab($event)">Vật phẩm</p>
            <p class="city-tab-item" id="2" @click="activeTab($event)">Công pháp</p>
        </div>
        <div class="city-content" v-if="active == '1'">
            <div class="item-content-row" v-for="i in bag">
                <div class="item-row-left">
                    <div class="item-img-small" :class="`border-color-${i.quality}`">
                        <img :src="store.api + i.image">
                    </div>
                    <b>{{ i.name }}</b>
                </div>
                <div class="item-row-right">
                    <p>Số lượng: {{ i.quantity }}</p>
                    <div class="icon-normal" @click="addCard('item', {
        name: i.name,
        path: i.id,
        parent: 'sell'
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
        </div>
        <div class="city-content" v-if="active == '2'">
            <div class="item-content-row" v-for="i in bag">
                <div class="item-row-left">
                    <div class="item-img-small" :class="`border-color-${i.quality}`">
                        <img :src="store.api + i.image">
                    </div>
                    <b>{{ i.name }}</b>
                </div>
                <div class="item-row-right" @click="addCard('book', {
        name: i.name,
        path: i.id,
        parent: 'sell'
    })">
                    <p>Số lượng: {{ i.quantity }}</p>
                    <div class="icon-normal">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="8" x2="12" y2="12"></line>
                            <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                    </div>
                </div>
            </div>
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

<style>
.city-tab {
    display: flex;
    border-bottom: 1px solid var(--tab_border_color);
    position: absolute;
    top: 35px;
    width: calc(100% - 20px);
    background-color: var(--card_color);
    z-index: 100;
    padding-top: 10px;
}

.city-tab .city-tab-item {
    padding: 5px 15px;
    margin-bottom: -1px;
    cursor: pointer;
    height: 33px;
    max-height: 33px;
    overflow: hidden;
}

.city-tab .active {
    border: 1px solid var(--tab_border_color);
    border-bottom: 0;
    background-color: var(--card_color);
}

.city-content {
    margin-top: 40px;
}
</style>