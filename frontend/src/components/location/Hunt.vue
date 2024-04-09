<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import {
    addCard, resetCard,
    getLevel, getType, getProperties, getQuality
} from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const power = ref(null)
const show_board = reactive({
    name: '',
    status: false
})
const prize = ref(null)
const tool = ref(false)

function getChar() {
    store.loading = true

    axios.get(`${store.api}/api/character/current`, store.header)
        .then(response => {
            power.value = response.data.properties.power
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
getChar()

function Start() {
    if (tool.value) {
        const time = Math.floor(Math.random() * 60)
        show_board.name = 'start'
        show_board.status = true

        setTimeout(() => {
            show_board.name = 'process'
            prize.value = Math.floor(Math.random() * parseInt(power.value) * 2)
        }, time * 1000);
    }
}

function Restart() {
    show_board.status = false
    show_board.name = ''
    prize.value = null
}


function End() {
    if (power.value > prize.value) {
        store.loading = true
        show_board.name = 'success'
        tool.value = false

        const form = new FormData()
        form.append('result', '1')
        form.append('money', prize.value)

        axios.post(`${store.api}/api/game`, form, store.header)
            .then(response => {
                store.loading = false
            })
            .catch(error => {
                store.loading = false
            })
    }
    else {
        show_board.name = 'fail'
        tool.value = false
    }
}

function Fee() {
    store.loading = true

    const form = new FormData()
    form.append('result', '0')
    form.append('money', '100')

    axios.post(`${store.api}/api/game`, form, store.header)
        .then(response => {
            tool.value = true
            store.loading = false
        })
        .catch(error => {
            tool.value = true
            store.loading = false
        })
}

function reload() {
    getChar()
    Restart()
}

</script>

<template>
    <div class="d-flex flex-column gap-2 align-items-center">
        <h5>Bãi săn</h5>
        <p>Dùng 100 linh thạch mua mũi tên</p>
        <div class="button-group">
            <button class="btn btn-primary" type="button" v-if="tool" @click="Start">Chờ con mồi</button>
            <button class="btn btn-warning" type="button" v-else @click="Fee">Mua mũi tên</button>
            <button class="btn btn-danger" type="button" @click="addCard('pet_shop')">Mua thú</button>
        </div>
    </div>

    <div class="fullboard" v-if="show_board.status">
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'start'">
            <h5>Đang chờ con mồi ...</h5>
            <button class="btn btn-danger" type="button" @click="Restart">Hủy</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'process'">
            <h5>Tìm thấy con mồi</h5>
            <p>Chiến lực {{ prize }}</p>
            <button class="btn btn-success" type="button" @click="End">Chiến</button>
            <button class="btn btn-primary" type="button" @click="Start">Chờ tiếp</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'fail'">
            <h5>Thua</h5>
            <button class="btn btn-primary" type="button" @click="Restart">Đồng ý</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'success'">
            <h5>Thắng</h5>
            <p>Bán hoang thú được {{ prize }} linh thạch</p>
            <button class="btn btn-primary" type="button" @click="Restart">Đồng ý</button>
        </div>
    </div>

    <div class="reload" @click="reload">
        <div class="icon-small">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38" />
            </svg>
        </div>
    </div>
</template>

<style></style>