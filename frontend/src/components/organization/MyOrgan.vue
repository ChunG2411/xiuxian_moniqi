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
const organ = ref(null)


function getOrgan() {
    store.loading = true

    axios.get(`${store.api}/api/organization/current`, store.header)
        .then(response => {
            organ.value = response.data
            store.loading = false
        })
        .catch(error => {
            organ.value = null
            store.loading = false
        })
}
getOrgan()

function outOrgan() {
    store.loading = true

    axios.get(`${store.api}/api/organization/${organ.value.id}/out`, store.header)
        .then(response => {
            organ.value = null
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': "Rời thế lực thành công"
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
    getOrgan()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="organ">
        <div class="item-img">
            <img :src="store.api + organ.image">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ organ.name }}</td>
                </tr>
                <tr>
                    <th>Giới thiệu</th>
                    <td>{{ organ.description }}</td>
                </tr>
                <tr>
                    <th>Nhân sĩ</th>
                    <td>{{ organ.member }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" class="btn btn-success" @click="addCard('member_organ', {name: organ.name})">Nhân sĩ</button>
            <button type="button" class="btn btn-primary" @click="addCard('organ_list')">Tổ chức khác</button>
            <button type="button" class="btn btn-dark" @click="outOrgan">Rời khỏi</button>
        </div>
    </div>
    <div class="align-items-center d-flex flex-column gap-3" v-else>
        <p>Bạn không tham gia vào tổ chức nào</p>
        <button type="button" class="btn btn-primary" @click="addCard('organ_list')">Danh sách tổ chức</button>
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