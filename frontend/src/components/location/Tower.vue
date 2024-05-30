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
const tower = ref(null)
const show_board = reactive({
    name: '',
    status: false
})
const prize = reactive({
    money: '',
    item: ''
})

function getTower() {
    store.loading = true

    axios.get(`${store.api}/api/tower`, store.header)
        .then(response => {
            tower.value = response.data
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
getTower()

function fight(floor) {
    store.loading = true

    show_board.name = 'fight'
    show_board.status = true

    const form = new FormData()
    form.append('floor', parseInt(floor) + 1)

    setTimeout(() => {
        axios.post(`${store.api}/api/tower`, form, store.header)
            .then(response => {
                showBoard('win', response.data)
                getTower()
                store.noti = {
                    'title': 'success',
                    'content': 'Khiêu chiến thành công'
                }
                store.loading = false
            })
            .catch(error => {
                show_board.status = false
                store.noti = {
                    'title': 'error',
                    'content': error.response.data
                }
                store.loading = false
            })
    }, 2000);
}

function showBoard(name, data) {
    prize.money = data.money
    prize.item = data.item
    show_board.name = name
    show_board.status = true
}

function reload() {
    getTower()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="tower">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tầng</th>
                    <td>{{ tower.floor }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" class="btn btn-primary" @click="fight(tower.floor)">Khiêu chiến</button>
        </div>
    </div>
    <div v-else></div>

    <div class="fullboard" v-if="show_board.status">
        <div class="d-flex flex-column gap-2 align-items-center" v-if="show_board.name == 'win'">
            <h5>Chiến thắng</h5>
            <p>Nhận được</p>
            <div class="mb-4 mt-4">
                <div class="d-flex align-items-center gap-2 mb-2">
                    <b>Linh thạch</b>
                    <p>{{ prize.money }}</p>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <b>Vật phẩm</b>
                    <div class="item-img-small" @click="addCard('item', {
                        name: prize.item.name,
                        path: prize.item.id
                    })">
                        <img :src="store.api + prize.item.image" :class="`border-color-${prize.item.quality}`">
                    </div>
                </div>
            </div>
            <button class="btn btn-success" type="button" @click="show_board.status = false">Đồng ý</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-if="show_board.name == 'fight'">
            <p>Đang tự động chiến đấu ...</p>
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

<style></style>