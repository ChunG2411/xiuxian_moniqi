<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import {
    addCard, formatDate, getMarket
} from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const market = ref(null)


function getDetail() {
    store.loading = true

    axios.get(`${store.api}/api/market/${props.data.path}`, store.header)
        .then(response => {
            market.value = response.data
            store.loading = false
        })
        .catch(error => {
            market.value = null
            store.loading = false
        })
}
getDetail()

function attack() {
    store.loading = true

    axios.get(`${store.api}/api/market/${props.data.path}/attack`, store.header)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': response.data
            }
            getDetail()
        })
        .catch(error => {
            store.loading = false
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            getDetail()
        })
}

function interact(type) {
    store.loading = true

    const form = new FormData()
    form.append('market', market.value.id)
    form.append('type', type)

    axios.patch(`${store.api}/api/market`, form, store.header)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': response.data
            }
            getDetail()
        })
        .catch(error => {
            store.loading = false
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
        })
}

function remove() {
    store.loading = true

    const form = new FormData()
    form.append('market', market.value.id)

    axios.put(`${store.api}/api/market`, form, store.header)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Vứt bỏ thành công'
            }
            market.value = null
        })
        .catch(error => {
            store.loading = false
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
        })
}

function reload() {
    getDetail()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="market">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ market.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ market.description }}</td>
                </tr>
                <tr>
                    <th>Sở hữu</th>
                    <td>{{ market.owner.name }}</td>
                </tr>
                <tr>
                    <th>Vị trí</th>
                    <td>{{ market.pos_x }}, {{ market.pos_y }}</td>
                </tr>
                <tr>
                    <th>Cấp độ</th>
                    <td>{{ market.level }}</td>
                </tr>
                <tr>
                    <th>Phòng thủ</th>
                    <td>{{ market.defender }} / {{ getMarket('defender') * market.level }}</td>
                </tr>
                <tr>
                    <th>Sản lượng</th>
                    <td>{{ market.produce }} linh thạch / phút</td>
                </tr>
                <tr>
                    <th>Dự trữ</th>
                    <td>{{ market.store }} / {{ market.limit }} linh thạch</td>
                </tr>
                <tr>
                    <th>Bảo hộ đến</th>
                    <td>{{ market.time_protect ? formatDate(market.time_protect) : 'Không được bảo hộ' }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group" v-if="market.owner.id == props.data.parent">
            <button type="button" class="btn btn-success" @click="interact('collect')">Thu hoạch</button>
            <button type="button" class="btn btn-primary" @click="interact('restore')">Hồi phục</button>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-dark" v-if="market.owner.id == props.data.parent" @click="remove">Vứt bỏ</button>
            <button type="button" class="btn btn-danger" v-else @click="attack">Công đánh</button>
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
</style>