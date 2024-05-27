<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const range = ref(null)
const active = ref('1')


function getRange() {
    store.loading = true

    axios.get(`${store.api}/api/locality`, store.header)
        .then(response => {
            range.value = response.data
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
getRange()

function activeTab(e) {
    const tabs = document.querySelectorAll('.bag-tab-item')
    active.value = e.target.id
    tabs.forEach((tab) => {
        tab.classList.remove('active')
    })
    e.target.classList.add('active')
}

function reload() {
    getRange()
}

</script>

<template>
    <div class="bag" v-if="range">
        <div class="bag-tab">
            <p class="bag-tab-item active" id="1" @click="activeTab($event)">Thế lực</p>
            <p class="bag-tab-item" id="2" @click="activeTab($event)">Mỏ quặng</p>
            <p class="bag-tab-item" id="3" @click="activeTab($event)">Khu buôn bán</p>
        </div>
        <div class="bag-content" v-if="active == '1'">
            <div class="item-content-row" v-for="i in range.locality">
                <div class="item-row-left">
                    <b>{{ i.name }}</b>
                </div>
                <div class="item-row-right">
                    <p>Cấp độ: {{ i.level }}</p>
                    <div class="icon-normal" @click="addCard('locality_detail', {
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
        </div>
        <div class="bag-content" v-if="active == '2'">
            <div class="item-content-row" v-for="i in range.mine">
                <div class="item-row-left">
                    <b>{{ i.name }}</b>
                    <p>{{ i.owner ? 'Bị chiếm' : 'Trống' }}</p>
                </div>
                <div class="item-row-right">
                    <p>Cấp độ: {{ i.level }}</p>
                    <div class="icon-normal" @click="addCard('mine_detail', {
                        name: i.name,
                        path: i.id,
                        parent: range.owner
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
        <div class="bag-content" v-if="active == '3'">
            <div class="item-content-row" v-for="i in range.market">
                <div class="item-row-left">
                    <b>{{ i.name }}</b>
                    <p>{{ i.owner ? 'Bị chiếm' : 'Trống' }}</p>
                </div>
                <div class="item-row-right">
                    <p>Cấp độ: {{ i.level }}</p>
                    <div class="icon-normal"  @click="addCard('market_detail', {
                        name: i.name,
                        path: i.id,
                        parent: range.owner
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