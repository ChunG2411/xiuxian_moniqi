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
const money = ref(null)


function send() {
    store.loading = true
    if (!money.value) {
        store.noti = {
            'title': 'error',
            'content': 'Vui lòng nhập số tinh thạch'
        }
        return
    }

    const form = new FormData()
    form.append('type', '1')
    form.append('money', money.value)

    axios.post(`${store.api}/api/clan/${props.data.path}/dedication`, form, store.header)
        .then(response => {
            store.loading = false
            money.value = null
            store.noti = {
                'title': 'success',
                'content': 'Cống hiến thành công'
            }
        })
        .catch(error => {
            store.loading = false
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
        })
}

</script>

<template>
    <div class="d-flex align-items-center gap-2 flex-column">
        <div class="create-clan">
            <h5>Cống hiến tinh thạch</h5>
            <div class="d-flex flex-column gap-1 align-items-center">
                <input type="text" placeholder="Nhập số tinh thạch" v-model="money">
                <button type="button" class="btn btn-success" @click="send">Gửi</button>
            </div>
        </div>
        <div class="create-clan">
            <h5>Cống hiến vật phẩm</h5>
            <button type="button" class="btn btn-primary" @click="addCard('bag_item', {
                    name: 'cống hiến',
                    id: props.data.path,
                    params: 'tab=1',
                    parent: 'clan_dedication'
                })">Vật phẩm</button>
        </div>
    </div>

    <div class="reload">
        <div class="icon-small">
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