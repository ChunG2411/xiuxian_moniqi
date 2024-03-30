<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { quality } from '../../utils/variables.js'
import {
    addCard, resetCard,
    getLevel, getType, getProperties, getQuality
} from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const house = ref(null)
const house_name = ref(null)
const house_quality = ref('1')
const board = reactive({
    name: '',
    status: false
})
const count = ref(0)


function getHouse() {
    store.loading = true

    axios.get(`${store.api}/api/house`, store.header)
        .then(response => {
            house.value = response.data
            store.loading = false
        })
        .catch(error => {
            house.value = null
            store.loading = false
        })
}
getHouse()

function editHouse() {
    if (!house_name.value) {
        store.noti = {
            'title': 'error',
            'content': 'Vui lòng nhập tên động phủ'
        }
        return
    }
    store.loading = true

    const form = new FormData()
    form.append('name', house_name.value)

    axios.patch(`${store.api}/api/house`, form, store.header)
        .then(response => {
            getHouse()
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Đổi tên thành công'
            }
            board.status = false
            board.name = ''
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

function deleteHouse() {
    store.loading = true

    axios.delete(`${store.api}/api/house`, store.header)
        .then(response => {
            house.value = null
            store.noti = {
                'title': 'success',
                'content': 'Hủy động phủ thành công'
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

function meditation() {
    store.loading = true

    const form = new FormData()
    form.append('quality', house.value.quality)
    form.append('time', count.value)

    axios.post(`${store.api}/api/meditation`, form, store.header)
        .then(response => {
            getHouse()
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Tu luyện thành công'
            }
            board.status = false
            board.name = ''
            count.value = 0
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

function buyHouse() {
    store.loading = true

    const form = new FormData()
    form.append('quality', house_quality.value)

    axios.post(`${store.api}/api/house`, form, store.header)
        .then(response => {
            getHouse()
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

function changeTab(tab) {
    board.status = true
    board.name = tab
    if (tab == 'meditation') {
        setInterval(() => {
            count.value += 1
        }, 1000);
    }
}

function reload() {
    getHouse()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="house">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td class="d-flex align-items-center gap-2">
                        {{ house.name }}
                        <div class="icon-small" @click="changeTab('name')">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                fill="none" stroke="#000000" stroke-width="2" stroke-linecap="square"
                                stroke-linejoin="arcs">
                                <polygon points="14 2 18 6 7 17 3 17 3 13 14 2"></polygon>
                                <line x1="3" y1="22" x2="21" y2="22"></line>
                            </svg>
                        </div>
                    </td>
                </tr>
                <tr>
                    <th>Chất lượng</th>
                    <td>{{ getQuality(house.quality) }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" class="btn btn-success" @click="changeTab('meditation')">Đả tọa</button>
            <button type="button" class="btn btn-warning" @click="addCard('oven')">Lò luyện</button>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-primary" @click="addCard('store', {parent: 'house'})">Kho</button>
            <button type="button" class="btn btn-danger" @click="addCard('shop_house')">Cửa hàng</button>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-dark" @click="deleteHouse">Phá hủy</button>
        </div>
    </div>

    <div class="d-flex align-items-center gap-2 flex-column" v-else>
        <div class="create-clan">
            <h5>Mua động phủ</h5>
            <div class="d-flex flex-column gap-1 align-items-center">
                <select class="form-select" name="quality" v-model="house_quality">
                    <option :value="key" v-for="value, key in quality">{{ value }}</option>
                </select>
                <p>Giá: {{ parseInt(house_quality) * 20000 }} linh thạch</p>
                <button class="btn btn-primary" type="button" @click="buyHouse">Mua</button>
            </div>
        </div>
    </div>

    <div class="fullboard" v-if="board.status">
        <div class="d-flex flex-column gap-3 align-items-center" v-if="board.name == 'meditation'">
            <h5>Thời gian đả tọa</h5>
            <h5>{{ count }}</h5>
            <button class="btn btn-success" type="button" @click="meditation">Dừng</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-else>
            <h5>Đổi tên động phủ</h5>
            <input type="text" placeholder="Nhập tên động phủ" v-model="house_name">
            <div class="button-group">
                <button class="btn btn-primary" type="button" @click="editHouse">Thay đổi</button>
                <button class="btn btn-warning" type="button" @click="board.status = false">Hủy</button>
            </div>
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
.create-clan {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    border: 1px solid var(--border_color);
    border-radius: 10px;
    padding: 20px 30px;
    margin-top: 20px;
}
</style>