<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard, formatDate } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const mail = ref(null)


function getDetail() {
    store.loading = true

    axios.get(`${store.api}/api/mail/${props.data.path}`, store.header)
        .then(response => {
            mail.value = response.data
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
getDetail()

function reload() {
    getDetail()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="mail">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Gửi từ</th>
                    <td>{{ mail.sender.name }} ( {{ mail.sender.organization }} )</td>
                </tr>
                <tr>
                    <th>Gửi đến</th>
                    <td>{{ mail.receiver.name }} ( {{ mail.receiver.organization }} )</td>
                </tr>
                <tr>
                    <th>Nội dung</th>
                    <td>{{ mail.content }}</td>
                </tr>
                <tr>
                    <th>Thời gian</th>
                    <td>{{ formatDate(mail.created_at) }}</td>
                </tr>
            </tbody>
        </table>
        <button class="btn btn-success" @click="addCard('locality_detail', {
            name: mail.sender.name,
            path: mail.sender.id
        })" v-if="props.data.tab=='2'">Thông tin người gửi</button>
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