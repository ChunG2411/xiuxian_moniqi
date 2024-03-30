<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import {
    addCard, resetCard,
    getLevel, getType, getProperties, getQuality, getSeedType
} from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const seed = ref(null)
const show_reload = ref(true)

function getSeed() {
    store.loading = true

    axios.get(`${store.api}/api/seeds/${props.data.path}`, store.header)
        .then(response => {
            seed.value = response.data
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
getSeed()

function removeSeed() {
    store.loading = true

    axios.delete(`${store.api}/api/store/${props.data.path}`, store.header)
        .then(response => {
            seed.value = null
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

function buySeed() {
    store.loading = true

    axios.post(`${store.api}/api/store/${props.data.path}`, {}, store.header)
        .then(response => {
            store.noti = {
                'title': 'success',
                'content': 'Mua vật phẩm thành công'
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

function plantSeed(path) {
    store.loading = true

    const form = new FormData()
    form.append('seed_id', seed.value.id)

    axios.post(`${store.api}/api/${path}/slot/${props.data.id}/seed`, form, store.header)
        .then(response => {
            seed.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Nuôi trồng thành công'
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

function harvestSeed(path) {
    store.loading = true

    axios.get(`${store.api}/api/${path}/slot/${props.data.id}/seed`, store.header)
        .then(response => {
            seed.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Thu hoạch thành công'
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

function clearSeed(path) {
    store.loading = true

    axios.delete(`${store.api}/api/${path}/slot/${props.data.id}/seed`, store.header)
        .then(response => {
            seed.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Vứt bỏ thành công'
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
    getSeed()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="seed">
        <div class="item-img" :class="`border-color-${seed.quality}`">
            <img :src="store.api + seed.image">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ seed.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ seed.descripstion }}</td>
                </tr>
                <tr>
                    <th>Loại</th>
                    <td>{{ getSeedType(seed.type) }}</td>
                </tr>
                <tr>
                    <th>Trưởng thành</th>
                    <td>{{ seed.time }} phút</td>
                </tr>
                <tr>
                    <th>Thu hoạch</th>
                    <td>
                        <div class="item-img-small" :class="`border-color-${seed.item.quality}`" @click="addCard('item', {
                            name: seed.item.name,
                            path: seed.item.id
                        })">
                            <img :src="store.api + seed.item.image">
                        </div>
                    </td>
                </tr>
                <tr>
                    <th>Giá thị trường</th>
                    <td>{{ seed.price }} linh thạch</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group" v-if="props.data.parent == 'house'">
            <button type="button" class="btn btn-danger" @click="removeSeed">Vứt bỏ</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'gardent_plant'">
            <button type="button" class="btn btn-success" @click="plantSeed('gardent')">Nuôi trồng</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'gardent'">
            <button type="button" class="btn btn-success" @click="harvestSeed('gardent')">Thu hoạch</button>
            <button type="button" class="btn btn-danger" @click="clearSeed('gardent')">Vứt bỏ</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'cage_plant'">
            <button type="button" class="btn btn-success" @click="plantSeed('cage')">Nuôi trồng</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'cage'">
            <button type="button" class="btn btn-success" @click="harvestSeed('cage')">Thu hoạch</button>
            <button type="button" class="btn btn-danger" @click="clearSeed('cage')">Vứt bỏ</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'lake_plant'">
            <button type="button" class="btn btn-success" @click="plantSeed('lake')">Nuôi trồng</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'lake'">
            <button type="button" class="btn btn-success" @click="harvestSeed('lake')">Thu hoạch</button>
            <button type="button" class="btn btn-danger" @click="clearSeed('lake')">Vứt bỏ</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'shop'">
            <button type="button" class="btn btn-success" @click="buySeed">Mua</button>
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