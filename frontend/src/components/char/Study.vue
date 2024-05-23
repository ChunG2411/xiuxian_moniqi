<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const study = ref(null)
const active = ref('1')

function getStudy(tab) {
    store.loading = true

    if (tab == '2') {
        axios.get(`${store.api}/api/study/process`, store.header)
            .then(response => {
                study.value = response.data
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
        axios.get(`${store.api}/api/study`, store.header)
            .then(response => {
                study.value = response.data
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
getStudy('1')

function activeTab(e) {
    const tabs = document.querySelectorAll('.study-tab-item')
    active.value = e.target.id
    getStudy(e.target.id)
    tabs.forEach((tab) => {
        tab.classList.remove('active')
    })
    e.target.classList.add('active')
}

function reload() {
    getStudy(active.value)
}

function loadMore(path) {
    store.loading = true

    axios.get(path, store.header)
        .then(response => {
            for (let i = 0; i < response.data.results.length; i++) {
                study.value.results.push(response.data.results[i])
            }
            study.value.next = response.data.next
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

</script>

<template>
    <div class="study" v-if="study">
        <div class="study-tab">
            <p class="study-tab-item active" id="1" @click="activeTab($event)">Đã lĩnh ngộ</p>
            <p class="study-tab-item" id="2" @click="activeTab($event)">Đang lĩnh ngộ</p>
        </div>
        <div class="study-content" v-if="active == '1'">
            <div class="item-content-row" v-for="i in study.book">
                <div class="item-row-left">
                    <div class="item-img-small" :class="`border-color-${i.quality}`">
                        <img :src="store.api + i.image">
                    </div>
                    <b>{{ i.name }}</b>
                </div>
                <div class="item-row-right">
                    <div class="icon-normal" @click="addCard('book', {
        name: i.name,
        path: i.id,
        parent: 'study'
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
        <div class="study-content" v-if="active == '2'">
            <div class="item-content-row" v-for="i in study.results">
                <div class="item-row-left">
                    <div class="item-img-small" :class="`border-color-${i.book.quality}`">
                        <img :src="store.api + i.book.image">
                    </div>
                    <b>{{ i.book.name }}</b>
                </div>
                <div class="item-row-right">
                    <div class="progress-custom">
                        <div class="progress-bar-custom" :style="`width: ${(i.process / i.book.duration) * 100}%`">
                        </div>
                        <small>{{ (i.process / i.book.duration * 100).toFixed(2) }} %</small>
                    </div>
                    <div class="icon-normal" @click="addCard('process', {
        name: i.book.name,
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
            <div v-if="study.next" class="w-100 text-center mt-2">
                <button type="button" class="btn btn-primary" @click="loadMore(study.next)">Xem thêm</button>
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
.study-tab {
    display: flex;
    border-bottom: 1px solid var(--tab_border_color);
    position: absolute;
    top: 35px;
    width: calc(100% - 20px);
    background-color: var(--card_color);
    z-index: 100;
    padding-top: 10px;
}

.study-tab .study-tab-item {
    padding: 5px 15px;
    margin-bottom: -1px;
    cursor: pointer;
    height: 33px;
    max-height: 33px;
    overflow: hidden;
}

.study-tab .active {
    border: 1px solid var(--tab_border_color);
    border-bottom: 0;
    background-color: var(--card_color);
}

.study-content {
    margin-top: 40px;
}

</style>