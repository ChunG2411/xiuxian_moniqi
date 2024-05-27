<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard, formatDate } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const mail = ref(null)
const active = ref('1')


function getMail(type) {
    store.loading = true

    axios.get(`${store.api}/api/mail?type=${type}`, store.header)
        .then(response => {
            mail.value = response.data.results
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
getMail('1')

function loadMore(path) {
    store.loading = true

    axios.get(path, store.header)
        .then(response => {
            for (let i = 0; i < response.data.results.length; i++) {
                mail.value.results.push(response.data.results[i])
            }
            mail.value.next = response.data.next
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

function activeTab(e) {
    const tabs = document.querySelectorAll('.bag-tab-item')
    active.value = e.target.id
    getMail(e.target.id)
    tabs.forEach((tab) => {
        tab.classList.remove('active')
    })
    e.target.classList.add('active')
}

function reload() {
    getMail(active.value)
}

</script>

<template>
    <div class="bag" v-if="mail">
        <div class="bag-tab">
            <p class="bag-tab-item active" id="1" @click="activeTab($event)">Đã gửi</p>
            <p class="bag-tab-item" id="2" @click="activeTab($event)">Nhận được</p>
        </div>
        <div class="bag-content">
            <div class="item-content-row" v-for="i in mail">
                <div class="item-row-left">
                    <b>{{ i.sender.name }}</b>
                </div>
                <div class="item-row-right">
                    <p>{{ formatDate(i.created_at) }}</p>
                    <div class="icon-normal" @click="addCard('mail_detail', {
                        name: i.sender.name,
                        path: i.id,
                        tab: active
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
            <div v-if="mail.next" class="w-100 text-center mt-2">
                <button type="button" class="btn btn-primary" @click="loadMore(mail.next)">Xem thêm</button>
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