<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const rank = ref(null)
const active = ref('1')


function getRank(tab) {
    store.loading = true
    axios.get(`${store.api}/api/rank?type=${tab}`, store.header)
        .then(response => {
            rank.value = response.data
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
getRank('1')

function activeTab(e) {
    const tabs = document.querySelectorAll('.rank-tab-item')
    active.value = e.target.id
    getRank(e.target.id)
    tabs.forEach((tab) => {
        tab.classList.remove('active')
    })
    e.target.classList.add('active')
}

function loadMore(path) {
    store.loading = true

    axios.get(path, store.header)
        .then(response => {
            for (let i = 0; i < response.data.results.length; i++) {
                rank.value.results.push(response.data.results[i])
            }
            rank.value.next = response.data.next
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
    getRank(active.value)
}

</script>

<template>
    <div class="rank" v-if="rank">
        <div class="rank-tab">
            <p class="rank-tab-item active" id="1" @click="activeTab($event)">Linh thạch</p>
            <p class="rank-tab-item" id="2" @click="activeTab($event)">Cống hiến</p>
            <p class="rank-tab-item" id="3" @click="activeTab($event)">Tháp</p>
        </div>
        <div class="rank-content" v-if="active == '1'">
            <table class="table table-hover m-0">
                <thead>
                    <tr>
                        <th scope="col"></th>
                        <th scope="col">Tu sĩ</th>
                        <th scope="col">Linh thạch</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[index, i] in rank.results.entries()">
                        <th>{{ index + 1 }}</th>
                        <td>{{ i.char.name }}</td>
                        <td>{{ i.money }}</td>
                        <td>
                            <div class="icon-normal" @click="addCard('char', {
        name: i.char.name,
        path: i.char.id
    })">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="#000000" stroke-width="2" stroke-linecap="square"
                                    stroke-linejoin="arcs">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <line x1="12" y1="8" x2="12" y2="12"></line>
                                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                                </svg>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="rank.next" class="w-100 text-center mt-2">
                <button type="button" class="btn btn-primary" @click="loadMore(rank.next)">Xem thêm</button>
            </div>
        </div>
        <div class="bag-content" v-if="active == '2'">
            <table class="table table-hover m-0">
                <thead>
                    <tr>
                        <th scope="col"></th>
                        <th scope="col">Tu sĩ</th>
                        <th scope="col">Cống hiến</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[index, i] in rank.results.entries()">
                        <th>{{ index + 1 }}</th>
                        <td>{{ i.char.name }}</td>
                        <td>{{ i.dedication }}</td>
                        <td>
                            <div class="icon-normal" @click="addCard('char', {
        name: i.char.name,
        path: i.char.id
    })">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="#000000" stroke-width="2" stroke-linecap="square"
                                    stroke-linejoin="arcs">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <line x1="12" y1="8" x2="12" y2="12"></line>
                                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                                </svg>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="rank.next" class="w-100 text-center mt-2">
                <button type="button" class="btn btn-primary" @click="loadMore(rank.next)">Xem thêm</button>
            </div>
        </div>
        <div class="bag-content" v-if="active == '3'">
            <table class="table table-hover m-0">
                <thead>
                    <tr>
                        <th scope="col"></th>
                        <th scope="col">Tu sĩ</th>
                        <th scope="col">Tầng</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="[index, i] in rank.results.entries()">
                        <th>{{ index + 1 }}</th>
                        <td>{{ i.char.name }}</td>
                        <td>{{ i.floor }}</td>
                        <td>
                            <div class="icon-normal" @click="addCard('char', {
        name: i.char.name,
        path: i.char.id
    })">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="#000000" stroke-width="2" stroke-linecap="square"
                                    stroke-linejoin="arcs">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <line x1="12" y1="8" x2="12" y2="12"></line>
                                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                                </svg>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="rank.next" class="w-100 text-center mt-2">
                <button type="button" class="btn btn-primary" @click="loadMore(rank.next)">Xem thêm</button>
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
.rank-tab {
    display: flex;
    border-bottom: 1px solid var(--tab_border_color);
    position: absolute;
    top: 35px;
    width: calc(100% - 20px);
    background-color: var(--card_color);
    z-index: 100;
    padding-top: 10px;
}

.rank-tab .rank-tab-item {
    padding: 5px 15px;
    margin-bottom: -1px;
    cursor: pointer;
    height: 33px;
    max-height: 33px;
    overflow: hidden;
}

.rank-tab .active {
    border: 1px solid var(--tab_border_color);
    border-bottom: 0;
    background-color: var(--card_color);
}

.rank-content {
    margin-top: 40px;
}
</style>