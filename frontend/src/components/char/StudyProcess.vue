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
const process = ref(null)
const show_board = ref(false)
const count = ref(0)


function getProcess() {
    store.loading = true

    axios.get(`${store.api}/api/study/process/${props.data.path}`, store.header)
        .then(response => {
            process.value = response.data
            store.loading = false
        })
        .catch(error => {
            process.value = null
            store.noti = {
                'title': 'success',
                'content': "Lĩnh ngộ hoàn tất"
            }
            store.loading = false
        })
}
getProcess()


function study() {
    store.loading = true
    show_board.value = false

    const form = new FormData()
    form.append('time', count.value)

    axios.post(`${store.api}/api/study/process/${process.value.id}`, form, store.header)
        .then(response => {
            getProcess()
            store.loading = false
            count.value = 0
            store.noti = {
                'title': 'success',
                'content': 'Đã dừng tham ngộ'
            }
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
    getProcess()
}

async function showBoard() {
    show_board.value = true
    if (show_board.value) {
        setInterval(() => {
            count.value += 1
        }, 1000);
    }
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="process">
        <div class="item-img" :class="`border-color-${process.book.quality}`">
            <img :src="store.api + process.book.image">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ process.book.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ process.book.descripstion }}</td>
                </tr>
                <tr>
                    <th>Phẩm chất</th>
                    <td>{{ getQuality(process.book.quality) }}</td>
                </tr>
                <tr>
                    <th>Cảnh giới</th>
                    <td>{{ getLevel(process.book.level) }}</td>
                </tr>
                <tr>
                    <th>Giá thị trường</th>
                    <td>{{ process.book.price }}</td>
                </tr>
                <tr>
                    <th>Thuộc tính</th>
                    <td>
                        <p v-for="value, key in process.book.properties">{{ getProperties(key) }}: {{ value }}</p>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="text-center d-flex flex-column gap-3 w-100 align-items-center">
            <h5>Quá trình lĩnh ngộ</h5>
            <div class="progress-custom">
                <div class="progress-bar-custom" :style="`width: ${ (process.process / process.book.duration * 100).toFixed(2) }%`">
                </div>
                <small>{{ (process.process / process.book.duration * 100).toFixed(2) }} %</small>
            </div>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-success" @click="showBoard">Lĩnh ngộ</button>
            <button type="button" class="btn btn-primary" @click="addCard('bag_item', {
        name: 'lĩnh ngộ',
        id: process.id,
        params: 'tab=1&type=7',
        parent: 'study'
    })">Dược tài</button>
        </div>
    </div>
    <div v-else></div>

    <div class="fullboard" v-if="show_board">
        <h5>Thời gian</h5>
        <h5>{{ count }}</h5>
        <button type="button" class="btn btn-warning" @click="study">Dừng</button>
    </div>

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