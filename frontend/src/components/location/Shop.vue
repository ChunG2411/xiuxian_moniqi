<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const shop = ref(null)


function getShop() {
    store.loading = true
    axios.get(`${store.api}/api/pets`, store.header)
        .then(response => {
            shop.value = response.data
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
getShop()

function reload() {
    getShop()
}

</script>

<template>
    <div class="shop" v-if="shop">
        <div class="item-content-row" v-for="i in shop">
            <div class="item-row-left">
                <div class="item-img-small" :class="`border-color-${i.quality}`">
                    <img :src="store.api + i.image">
                </div>
                <b>{{ i.name }}</b>
            </div>
            <div class="item-row-right">
                <p>Linh thạch: {{ i.price }}</p>
                <div class="icon-normal" @click="addCard('pet', {
        name: i.name,
        path: i.id,
        parent: 'shop'
    })">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
            </div>
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