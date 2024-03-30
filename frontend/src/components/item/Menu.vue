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
const menu = ref(null)


function getMenu() {
    store.loading = true

    axios.get(`${store.api}/api/menu/${props.data.path}`, store.header)
        .then(response => {
            menu.value = response.data
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
getMenu()

function readMenu() {
    store.loading = true

    const form = new FormData()
    form.append('menu_id', menu.value.id)

    axios.post(`${store.api}/api/knowledge`, form, store.header)
        .then(response => {
            store.noti = {
                'title': 'success',
                'content': 'Tham ngộ thành công'
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

function reload() {
    getMenu()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="menu">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ menu.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ menu.descripstion }}</td>
                </tr>
                <tr>
                    <th>Loại</th>
                    <td>{{ (menu.type == '1') ? 'Luyện khí' : 'Luyện đan' }}</td>
                </tr>
                <tr>
                    <th>Thành phẩm</th>
                    <td>
                        <div class="item-img-small" :class="`border-color-${menu.item.quality}`" @click="addCard('item', {
        name: menu.item.name,
        path: menu.item.id
    })">
                            <img :src="store.api + menu.item.image">
                        </div>
                    </td>
                </tr>
                <tr>
                    <th>Nguyên liệu</th>
                    <td class="" style="column-count: 3;">
                        <div class="item-img-small mb-1" :class="`border-color-${i.quality}`"
                            v-for="i in menu.materials" @click="addCard('item', {
        name: i.name,
        path: i.id
    })">
                            <img :src="store.api + i.image">
                        </div>
                    </td>
                </tr>
                <tr>
                    <th>Giá tham ngộ</th>
                    <td>{{ menu.price }} cống hiến</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group" v-if="props.data.parent == 'library'">
            <button type="button" class="btn btn-success" @click="readMenu">Tham ngộ</button>
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

<style></style>