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
const book = ref(null)
const show_reload = ref(true)

function getBook() {
    store.loading = true

    axios.get(`${store.api}/api/books/${props.data.path}`, store.header)
        .then(response => {
            book.value = response.data
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
getBook()

function removeBook() {
    store.loading = true

    axios.get(`${store.api}/api/books/remove/${props.data.path}`, store.header)
        .then(response => {
            book.value = null
            show_reload.value = false
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Vứt bỏ vật phẩm thành công'
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

function studyBook() {
    store.loading = true

    const form = new FormData()
    form.append('book', props.data.path)

    axios.post(`${store.api}/api/study`, form, store.header)
        .then(response => {
            book.value = null
            show_reload.value = false
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Đang tham ngộ'
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

function clanBuy() {
    store.loading = true

    const form = new FormData()
    form.append('tab', '2')
    form.append('item_id', book.value.id)

    axios.post(`${store.api}/api/clan/${props.data.id}/shop`, form, store.header)
        .then(response => {
            book.value = null
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
    form.append('tab', '2')
    form.append('item_id', book.value.id)

    axios.post(`${store.api}/api/city/${props.data.id}/shop`, form, store.header)
        .then(response => {
            book.value = null
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
    form.append('tab', '2')
    form.append('item_id', book.value.id)

    axios.patch(`${store.api}/api/city/${props.data.id}/shop`, form, store.header)
        .then(response => {
            book.value = null
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
    getBook()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="book">
        <div class="item-img" :class="`border-color-${book.quality}`">
            <img :src="store.api + book.image">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ book.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ book.descripstion }}</td>
                </tr>
                <tr>
                    <th>Phẩm chất</th>
                    <td>{{ getQuality(book.quality) }}</td>
                </tr>
                <tr>
                    <th>Cảnh giới</th>
                    <td>{{ getLevel(book.level) }}</td>
                </tr>
                <tr>
                    <th>Giá thị trường</th>
                    <td>{{ book.price }}</td>
                </tr>
                <tr>
                    <th>Quy trình</th>
                    <td>{{ book.duration }} bậc</td>
                </tr>
                <tr>
                    <th>Thuộc tính</th>
                    <td>
                        <p v-for="value, key in book.properties">{{ getProperties(key) }}: {{ value }}</p>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="button-group" v-if="props.data.parent == 'bag'">
            <button type="button" class="btn btn-success" @click="studyBook">Lĩnh ngộ</button>
            <button type="button" class="btn btn-danger" @click="removeBook">Vứt bỏ</button>
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