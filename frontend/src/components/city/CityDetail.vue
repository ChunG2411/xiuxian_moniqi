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
const city = ref(null)


function getCity() {
    store.loading = true

    axios.get(`${store.api}/api/city/${props.data.path}`, store.header)
        .then(response => {
            city.value = response.data
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
getCity()


function reload() {
    getCity()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="city">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ city.name }}</td>
                </tr>
                <tr>
                    <th>Mô tả</th>
                    <td>{{ city.descripstion }}</td>
                </tr>
                <tr>
                    <th>Cấp độ</th>
                    <td>Cấp {{ city.quality }}</td>
                </tr>
            </tbody>
        </table>
        <div class="button-group">
            <button type="button" class="btn btn-success" @click="addCard('restore')">Tửu quán</button>
            <button type="button" class="btn btn-primary" @click=" addCard('shop', {
        name: city.name,
        path: `city/${city.id}`,
        id: city.id,
        parent: 'city_shop'
    })">Cửa hàng</button>
            <button type="button" class="btn btn-warning" @click=" addCard('sell')">Bán đồ</button>
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