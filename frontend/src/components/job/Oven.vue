<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { quality } from '../../utils/variables.js'
import {
    addCard, resetCard,
    getLevel, getType, getProperties, getQuality
} from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const oven = ref(null)


function getOven() {
    store.loading = true

    axios.get(`${store.api}/api/oven`, store.header)
        .then(response => {
            oven.value = response.data
            store.loading = false
        })
        .catch(error => {
            oven.value = null
            store.loading = false
        })
}
getOven()

function deleteOven() {
    store.loading = true

    axios.delete(`${store.api}/api/oven`, store.header)
        .then(response => {
            oven.value = null
            store.noti = {
                'title': 'success',
                'content': 'Hủy lò luyện thành công'
            }
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

function buyOven() {
    store.loading = true

    axios.post(`${store.api}/api/oven`, {}, store.header)
        .then(response => {
            getOven()
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Mua thành công'
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

function upgrateOven() {
    store.loading = true

    axios.patch(`${store.api}/api/oven`, {}, store.header)
        .then(response => {
            getOven()
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Nâng cấp thành công'
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
    getOven()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="oven">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Cấp độ</th>
                    <td>{{ oven.level }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" class="btn btn-primary" @click="addCard('knowledge')">Công thức</button>
            <button type="button" class="btn btn-warning" @click="upgrateOven">Nâng cấp</button>
            <button type="button" class="btn btn-success" @click="addCard('create_item')">Luyện chế</button>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-dark" @click="deleteOven">Phá hủy</button>
        </div>
    </div>

    <div class="d-flex align-items-center gap-2 flex-column" v-else>
        <div class="create-clan">
            <h5>Mua lò luyện</h5>
            <div class="d-flex flex-column gap-1 align-items-center">
                <p>Mua lò luyện Phàm phẩm với giá</p>
                <b>100000 linh thạch</b>
                <button class="btn btn-primary" type="button" @click="buyOven">Mua</button>
            </div>
        </div>
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

<style>
.create-clan {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    border: 1px solid var(--border_color);
    border-radius: 10px;
    padding: 20px 30px;
    margin-top: 20px;
}
</style>