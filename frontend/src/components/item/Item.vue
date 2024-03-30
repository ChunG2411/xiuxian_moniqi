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
const item = ref(null)
const show_reload = ref(true)


function getItem() {
    store.loading = true

    axios.get(`${store.api}/api/items/${props.data.path}`, store.header)
        .then(response => {
            item.value = response.data
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
getItem()

function removeItem() {
    store.loading = true

    axios.get(`${store.api}/api/items/remove/${props.data.path}`, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Vứt bỏ vật phẩm thành công'
            }
            store.loading = false
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': 'Vui lòng tải lại cửa sổ'
            }
            store.loading = false
        })
}

function useItem() {
    store.loading = true

    axios.get(`${store.api}/api/items/use/${props.data.path}`, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Sử dụng vật phẩm thành công'
            }
            store.loading = false
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': 'Vui lòng tải lại cửa sổ'
            }
            store.loading = false
        })
}

function equipItem() {
    store.loading = true

    const form = new FormData()
    form.append('item_id', props.data.path)

    axios.post(`${store.api}/api/equipped`, form, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Trang bị vật phẩm thành công'
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

function unEquipItem() {
    store.loading = true

    const form = new FormData()
    form.append('item_id', props.data.path)

    axios.delete(`${store.api}/api/equipped?type=${item.value.type}`, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Gỡ vật phẩm thành công'
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

function study() {
    store.loading = true

    const form = new FormData()
    form.append('item', props.data.path)

    axios.post(`${store.api}/api/study/process/${props.data.id}`, form, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Phục dụng thành công'
            }
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': 'Vui lòng tải lại cửa sổ'
            }
            store.loading = false
        })
}

function send() {
    store.loading = true

    const form = new FormData()
    form.append('type', '2')
    form.append('item', props.data.path)

    axios.post(`${store.api}/api/clan/${props.data.id}/dedication`, form, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Gửi thành công'
            }
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': 'Vui lòng tải lại cửa sổ'
            }
            store.loading = false
        })
}

function clanBuy() {
    store.loading = true

    const form = new FormData()
    form.append('tab', '1')
    form.append('item_id', item.value.id)

    axios.post(`${store.api}/api/clan/${props.data.id}/shop`, form, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
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

function cityBuy() {
    store.loading = true

    const form = new FormData()
    form.append('tab', '1')
    form.append('item_id', item.value.id)

    axios.post(`${store.api}/api/city/${props.data.id}/shop`, form, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
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

function citySell() {
    store.loading = true

    const form = new FormData()
    form.append('tab', '1')
    form.append('item_id', item.value.id)

    axios.patch(`${store.api}/api/city/${props.data.id}/shop`, form, store.header)
        .then(response => {
            item.value = null
            show_reload.value = false
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Bán thành công'
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
    getItem()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="item">
        <div class="item-img" :class="`border-color-${item.quality}`">
            <img :src="store.api + item.image">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ item.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ item.descripstion }}</td>
                </tr>
                <tr>
                    <th>Loại</th>
                    <td>{{ getType(item.type) }}</td>
                </tr>
                <tr>
                    <th>Phẩm chất</th>
                    <td>{{ getQuality(item.quality) }}</td>
                </tr>
                <tr>
                    <th>Cảnh giới</th>
                    <td>{{ getLevel(item.level) }}</td>
                </tr>
                <tr>
                    <th>Giá thị trường</th>
                    <td>{{ item.price }}</td>
                </tr>
                <tr>
                    <th>Thuộc tính</th>
                    <td>
                        <p v-for="value, key in item.properties">{{ getProperties(key) }}: {{ value }}</p>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="button-group" v-if="props.data.parent == 'bag'">
            <button type="button" class="btn btn-success" v-if="item.type < 5" @click="equipItem">Trang bị</button>
            <button type="button" class="btn btn-success" v-if="item.type == 5" @click="useItem">Sử dụng</button>
            <button type="button" class="btn btn-danger" @click="removeItem">Vứt bỏ</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'char'">
            <button type="button" class="btn btn-danger" @click="unEquipItem">Gỡ xuống</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'study'">
            <button type="button" class="btn btn-primary" @click="study">Phục dụng</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'clan_dedication'">
            <button type="button" class="btn btn-primary" @click="send">Gửi</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'clan_shop'">
            <button type="button" class="btn btn-primary" @click="clanBuy">Mua</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'city_shop'">
            <button type="button" class="btn btn-primary" @click="cityBuy">Mua</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'sell'">
            <button type="button" class="btn btn-primary" @click="citySell">Bán</button>
        </div>
    </div>
    <div v-else></div>

    <div class="reload" v-if="show_reload">
        <div class="icon-small" @click="reload">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38" />
            </svg>
        </div>
    </div>
</template>

<style></style>