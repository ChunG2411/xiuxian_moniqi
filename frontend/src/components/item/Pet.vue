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
const pet = ref(null)
const own_pet = ref(null)
const show_reload = ref(true)
const money = ref(null)

function getPet() {
    store.loading = true

    axios.get(`${store.api}/api/pet/${props.data.path}`, store.header)
        .then(response => {
            pet.value = response.data
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

function getOwnPet() {
    store.loading = true

    axios.get(`${store.api}/api/pets/own?char=${props.data.id}`, store.header)
        .then(response => {
            pet.value = response.data.pet
            own_pet.value = response.data
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

if (props.data.id) {
    getOwnPet()
}
else {
    getPet()
}

function buy() {
    store.loading = true

    const form = new FormData()
    form.append('pet', pet.value.id)

    axios.post(`${store.api}/api/pets/own`, form, store.header)
        .then(response => {
            pet.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Bắt đầu nuôi sủng vật'
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

function remove() {
    store.loading = true

    // const form = new FormData()
    // form.append('pet', pet.value.id)

    axios.delete(`${store.api}/api/pets/own`, store.header)
        .then(response => {
            pet.value = null
            show_reload.value = false
            store.noti = {
                'title': 'success',
                'content': 'Đã vứt bỏ sủng vật'
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

function feed() {
    store.loading = true

    axios.patch(`${store.api}/api/pets/own?money=${money.value}`, {}, store.header)
        .then(response => {
            money.value = null
            getOwnPet()
            store.noti = {
                'title': 'success',
                'content': 'Đã cho ăn thành công'
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

function upLevel() {
    store.loading = true

    axios.put(`${store.api}/api/pets/own`, {}, store.header)
        .then(response => {
            getOwnPet()
            store.noti = {
                'title': 'success',
                'content': 'Tăng cấp thành công'
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
    if (props.data.id) {
        getOwnPet()
    }
    else {
        getPet()
    }
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="pet">
        <div class="item-img" :class="`border-color-${pet.quality}`">
            <img :src="store.api + pet.image">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ pet.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ pet.descripstion }}</td>
                </tr>
                <tr>
                    <th>Chất lượng</th>
                    <td>{{ pet.quality }}</td>
                </tr>
                <tr>
                    <th>Giá</th>
                    <td>{{ pet.price }} linh thạch</td>
                </tr>
                <tr v-if="own_pet">
                    <th>Cấp độ</th>
                    <td>Cấp {{ own_pet.level }}: {{ own_pet.exp }}/{{ own_pet.pet.price * own_pet.pet.quality * (own_pet.level + 1) }}</td>
                </tr>
                <tr>
                    <th>Thuộc tính</th>
                    <td v-if="own_pet">
                        <p v-for="value, key in own_pet.properties">{{ getProperties(key) }}: {{ value }}</p>
                    </td>
                    <td v-else>
                        <p v-for="value, key in pet.properties">{{ getProperties(key) }}: {{ value }}</p>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="props.data.parent == 'my_char'" class="w-100">
            <div class="d-flex align-items-center justify-content-center gap-2 mb-3">
                <input class="w-60" type="text" placeholder="Nhập số tinh thạch" v-model="money">
                <button type="button" class="btn btn-success" @click="feed">Cho ăn</button>
            </div>
            <div class="button-group">
                <button type="button" class="btn btn-primary" @click="upLevel">Tăng cấp</button>
                <button type="button" class="btn btn-danger" @click="remove">Vứt bỏ</button>
            </div>
        </div>

        <div class="button-group" v-if="props.data.parent == 'shop'">
            <button type="button" class="btn btn-success" @click="buy">Mua</button>
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