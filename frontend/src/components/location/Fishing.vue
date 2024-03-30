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
const show_board = reactive({
    name: '',
    status: false
})
const prize = ref(null)
var loop = null

function Start() {
    Fee()
    const time = Math.floor(Math.random() * 60)
    show_board.name = 'start'
    show_board.status = true

    setTimeout(() => {
        show_board.name = 'process'
        prize.value = Math.floor(Math.random() * 30)
        let count = 0

        loop = setInterval(() => {
            count += 1
            if (count > 5) {
                show_board.name = 'fail'
                clearInterval(loop)
            }
        }, 1000);

    }, time * 1000);
}

function reload() {
    show_board.status = false
    show_board.name = ''
    prize.value = null
    loop = null
}

function End() {
    clearInterval(loop)
    store.loading = true
    show_board.name = 'success'

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

function Fee() {
    store.loading = true

    const form = new FormData()
    form.append('result', '0')
    form.append('money', '10')

    axios.post(`${store.api}/api/game`, form, store.header)
        .then(response => {
            store.loading = false
        })
        .catch(error => {
            store.loading = false
        })
}

</script>

<template>
    <div class="d-flex flex-column gap-2 align-items-center">
        <h5>Hồ câu</h5>
        <p>Dùng 10 linh thạch mua mồi câu</p>
        <button class="btn btn-success" type="button" @click="Start">Thả câu</button>
    </div>

    <div class="fullboard" v-if="show_board.status">
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'start'">
            <h5>Đang thả câu ...</h5>
            <button class="btn btn-danger" type="button" @click="reload">Hủy</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'process'">
            <h5>Cá đã cắn câu</h5>
            <button class="btn btn-success" type="button" @click="End">Giật</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'fail'">
            <h5>Trượt rồi</h5>
            <button class="btn btn-primary" type="button" @click="reload">Đồng ý</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'success'">
            <h5>Trúng rồi</h5>
            <p>Bán cá được {{ prize }} linh thạch</p>
            <button class="btn btn-primary" type="button" @click="reload">Đồng ý</button>
        </div>
    </div>

    <div class="reload">
        <div class="icon-small">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38" />
            </svg>
        </div>
    </div>
</template>

<style></style>