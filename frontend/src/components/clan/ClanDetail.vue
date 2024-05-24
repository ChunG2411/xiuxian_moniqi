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
const clan = ref(null)


function getClan() {
    store.loading = true

    axios.get(`${store.api}/api/clan/${props.data.path}`, store.header)
        .then(response => {
            clan.value = response.data
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
getClan()

function joinClan() {
    store.loading = true

    axios.post(`${store.api}/api/clan/${props.data.path}/request`, {}, store.header)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Xin gia nhập thành công'
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
    getClan()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="clan">
        <div class="item-img">
            <img :src="store.api + clan.image">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ clan.name }}</td>
                </tr>
                <tr>
                    <th>Giới thiệu</th>
                    <td>{{ clan.descripstion }}</td>
                </tr>
                <tr>
                    <th>Nhân sĩ</th>
                    <td>{{ clan.member }}</td>
                </tr>
                <tr>
                    <th>Cấp độ</th>
                    <td>Cấp {{ clan.level }} - {{ clan.exp }}%</td>
                </tr>
                <tr>
                    <th>Trưởng môn</th>
                    <td>{{ clan.leader.name }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" class="btn btn-success" @click="joinClan">Xin vào</button>
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