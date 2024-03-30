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
    if (tab == '3') {
        axios.get(`${store.api}/api/money`, store.header)
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
    else {
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
}
getBag('1')

function activeTab(e) {
    const tabs = document.querySelectorAll('.bag-tab-item')
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
    <div class="bag" v-if="bag">
        <div class="bag-tab">
            <p class="bag-tab-item active" id="1" @click="activeTab($event)">Vật phẩm</p>
            <p class="bag-tab-item" id="2" @click="activeTab($event)">Công pháp</p>
            <p class="bag-tab-item" id="3" @click="activeTab($event)">Linh thạch</p>
        </div>
        <div class="bag-content" v-if="active == '1'">
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
        parent: 'bag'
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
        <div class="bag-content" v-if="active == '2'">
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
        parent: 'bag'
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
        <div class="bag-content" v-if="active == '3'">
            <table class="table table-hover m-0">
                <tbody>
                    <tr>
                        <th>Linh thạch</th>
                        <td>{{ bag.money }}</td>
                    </tr>
                    <tr>
                        <th>Cống hiến</th>
                        <td>{{ bag.dedication }}</td>
                    </tr>
                    <tr>
                        <th>Quân công</th>
                        <td>{{ bag.merit }}</td>
                    </tr>
                </tbody>
            </table>
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
.bag-tab {
    display: flex;
    border-bottom: 1px solid var(--tab_border_color);
    position: absolute;
    top: 35px;
    width: calc(100% - 20px);
    background-color: var(--card_color);
    z-index: 100;
    padding-top: 10px;
}

.bag-tab .bag-tab-item {
    padding: 5px 15px;
    margin-bottom: -1px;
    cursor: pointer;
    height: 33px;
    max-height: 33px;
    overflow: hidden;
}

.bag-tab .active {
    border: 1px solid var(--tab_border_color);
    border-bottom: 0;
    background-color: var(--card_color);
}

.bag-content {
    margin-top: 40px;
}

.item-content-row {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    align-items: center
}

.item-content-row:hover {
    background-color: var(--hover_item_color);
    border-radius: 10px
}

.item-row-left{
    display: flex;
    gap: 10px;
    width: 50%;
    height: 50px;
    max-height: 50px;
    overflow: hidden;
    align-items: center;
}
.item-row-right{
    display: flex;
    gap: 10px;
    width: 40%;
    height: 50px;
    max-height: 50px;
    align-items: center;
    justify-content: end;
}
</style>