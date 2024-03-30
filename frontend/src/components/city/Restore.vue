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
const prize = reactive({
    tam_tinh: '',
    suc_khoe: ''
})


function use(money) {
    store.loading = true

    show_board.name = 'loading'
    show_board.status = true

    const form = new FormData()
    form.append('money', money)

    setTimeout(() => {
        axios.post(`${store.api}/api/restore`, form, store.header)
            .then(response => {
                showBoard('success', response.data)
                store.noti = {
                    'title': 'success',
                    'content': 'Dùng thành công'
                }
                store.loading = false
            })
            .catch(error => {
                show_board.status = false
                store.noti = {
                    'title': 'error',
                    'content': error.response.data
                }
                store.loading = false
            })
    }, 2000);
}

function showBoard(name, data) {
    prize.tam_tinh = data.tam_tinh
    prize.suc_khoe = data.suc_khoe
    show_board.name = name
    show_board.status = true
}

</script>

<template>
    <div class="restore">
        <div class="item-content-row">
            <div class="item-row-left">
                <b>Trà</b>
            </div>
            <div class="item-row-right">
                <p>Linh thạch: 1000</p>
                <div class="icon-normal" @click="use('1000')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="10" cy="20.5" r="1" />
                        <circle cx="18" cy="20.5" r="1" />
                        <path d="M2.5 2.5h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6l1.6-8.4H7.1" />
                    </svg>
                </div>
            </div>
        </div>
        <div class="item-content-row">
            <div class="item-row-left">
                <b>Cơm bình dân</b>
            </div>
            <div class="item-row-right">
                <p>Linh thạch: 5000</p>
                <div class="icon-normal" @click="use('5000')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="10" cy="20.5" r="1" />
                        <circle cx="18" cy="20.5" r="1" />
                        <path d="M2.5 2.5h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6l1.6-8.4H7.1" />
                    </svg>
                </div>
            </div>
        </div>
        <div class="item-content-row">
            <div class="item-row-left">
                <b>Tiệc nhỏ</b>
            </div>
            <div class="item-row-right">
                <p>Linh thạch: 10000</p>
                <div class="icon-normal" @click="use('10000')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="10" cy="20.5" r="1" />
                        <circle cx="18" cy="20.5" r="1" />
                        <path d="M2.5 2.5h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6l1.6-8.4H7.1" />
                    </svg>
                </div>
            </div>
        </div>
        <div class="item-content-row">
            <div class="item-row-left">
                <b>Tiệc cao cấp</b>
            </div>
            <div class="item-row-right">
                <p>Linh thạch: 20000</p>
                <div class="icon-normal" @click="use('20000')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="10" cy="20.5" r="1" />
                        <circle cx="18" cy="20.5" r="1" />
                        <path d="M2.5 2.5h3l2.7 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6l1.6-8.4H7.1" />
                    </svg>
                </div>
            </div>
        </div>
    </div>

    <div class="fullboard" v-if="show_board.status">
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'success'">
            <h5>Dùng thành công</h5>
            <small>Nhận được</small>
            <table class="table table-hover m-0">
                <tbody>
                    <tr>
                        <th>Tâm tình</th>
                        <td>{{ prize.tam_tinh }}</td>
                    </tr>
                    <tr>
                        <th>Sức khỏe</th>
                        <td>{{ prize.suc_khoe }}</td>
                    </tr>
                </tbody>
            </table>
            <button class="btn btn-success" type="button" @click="show_board.status = false">Đồng ý</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'loading'">
            <p>Đang dùng ...</p>
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