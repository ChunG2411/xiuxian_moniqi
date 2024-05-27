<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import {
    addCard, formatDate, getLocality
} from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const locality = ref(null)
const form_name = ref('')


function getDetail() {
    store.loading = true

    axios.get(`${store.api}/api/locality/current`, store.header)
        .then(response => {
            locality.value = response.data
            store.loading = false
        })
        .catch(error => {
            locality.value = null
            store.loading = false
        })
}
getDetail()

function delLocality() {
    store.loading = true

    axios.delete(`${store.api}/api/locality`, store.header)
        .then(response => {
            locality.value = null
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': "Bỏ thế lực thành công"
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

function createLocality() {
    if (!form_name.value) {
        store.noti = {
            'title': 'error',
            'content': 'Vui lòng nhập tên thế lực'
        }
        return
    }
    store.loading = true
    
    const form = new FormData()
    form.append('name', form_name.value)

    axios.post(`${store.api}/api/locality`, form, store.header)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': "Tạo thế lực thành công"
            }
            getDetail()
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
    getDetail()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="locality">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ locality.name }}</td>
                </tr>
                <tr>
                    <th>Tổ chức</th>
                    <td>{{ locality.organization.name }}</td>
                </tr>
                <tr>
                    <th>Lãnh đạo</th>
                    <td>{{ locality.char.name }}</td>
                </tr>
                <tr>
                    <th>Vị trí</th>
                    <td>{{ locality.pos_x }}, {{ locality.pos_y }}</td>
                </tr>
                <tr>
                    <th>Cấp độ</th>
                    <td>{{ locality.level }}</td>
                </tr>
                <tr>
                    <th>Phòng thủ</th>
                    <td>{{ locality.defender }} / {{ getLocality('defender') * locality.level }}</td>
                </tr>
                <tr>
                    <th>Nhân số</th>
                    <td>{{ locality.power }} / {{ getLocality('power') * locality.level }}</td>
                </tr>
                <tr>
                    <th>Bảo hộ đến</th>
                    <td>{{ locality.time_protect ? formatDate(locality.time_protect) : 'Không được bảo hộ' }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" class="btn btn-primary" @click="addCard('locality_range', {name:locality.name})">Lân cận</button>
            <button type="button" class="btn btn-success" @click="addCard('locality_restore', {name:locality.name})">Hồi phục</button>
            <button type="button" class="btn btn-warning" @click="addCard('locality_owner', {name:locality.name})">Đã chiếm</button>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-outline-success" @click="addCard('locality_mail')">Quân tin</button>
            <button type="button" class="btn btn-outline-primary" @click="addCard('locality_modify', {name: locality.name})">Chỉnh sửa</button>
            <button type="button" class="btn btn-dark" @click="delLocality">Vứt bỏ</button>
        </div>
    </div>
    <div class="align-items-center d-flex flex-column gap-3" v-else>
        <h5>Kiến tạo thế lực</h5>
        <div class="d-flex flex-column gap-1 align-items-center">
            <input type="text" placeholder="Tên thế lực" v-model="form_name">
            <button type="button" class="btn btn-primary" @click="createLocality">Tạo</button>
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