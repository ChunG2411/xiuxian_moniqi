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
const gardent = ref(null)
const gardent_quality = ref('1')
const slot = ref(null)


function getGardent() {
    store.loading = true

    axios.get(`${store.api}/api/gardent`, store.header)
        .then(response => {
            gardent.value = response.data
            store.loading = false
        })
        .catch(error => {
            gardent.value = null
            store.loading = false
        })
}

function getGardentSlot() {
    store.loading = true

    axios.get(`${store.api}/api/gardent/slot`, store.header)
        .then(response => {
            slot.value = response.data
            store.loading = false
        })
        .catch(error => {
            slot.value = null
            store.loading = false
        })
}
getGardent()
getGardentSlot()

function deleteGardent() {
    store.loading = true

    axios.delete(`${store.api}/api/gardent`, store.header)
        .then(response => {
            gardent.value = null
            store.noti = {
                'title': 'success',
                'content': 'Hủy linh điền thành công'
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

function buyGardent() {
    store.loading = true

    const form = new FormData()
    form.append('quality', gardent_quality.value)

    axios.post(`${store.api}/api/gardent`, form, store.header)
        .then(response => {
            getGardent()
            getGardentSlot()
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

function upgrateGardent() {
    store.loading = true

    axios.get(`${store.api}/api/gardent/upgrate`, store.header)
        .then(response => {
            getGardent()
            store.noti = {
                'title': 'success',
                'content': 'Nâng cấp linh điền thành công'
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

function buySlot() {
    store.loading = true

    axios.post(`${store.api}/api/gardent/slot`, {}, store.header)
        .then(response => {
            getGardentSlot()
            store.noti = {
                'title': 'success',
                'content': 'Mua ô đất thành công'
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
    getGardent()
    getGardentSlot()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="gardent">
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Cấp độ</th>
                    <td>{{ gardent.level }} - {{ gardent.exp }}/{{ parseInt(gardent.level) * 100 }}</td>
                </tr>
                <tr>
                    <th>Chất lượng</th>
                    <td>{{ getQuality(gardent.quality) }}</td>
                </tr>
                <tr>
                    <th>Ô đất</th>
                    <td v-if="slot">{{ slot.length }}/{{ parseInt(gardent.quality) * 3 + parseInt(gardent.level) }}</td>
                    <td v-else>0/{{ parseInt(gardent.quality) * 3 + parseInt(gardent.level) }}</td>
                </tr>
            </tbody>
        </table>

        <div class="button-group">
            <button type="button" class="btn btn-success" @click="buySlot">Mua ô đất</button>
            <button type="button" class="btn btn-primary" @click="upgrateGardent">Nâng cấp</button>
            <button type="button" class="btn btn-dark" @click="deleteGardent">Phá hủy</button>
        </div>

        <div class="border-top w-100 text-center">
            <h5 class="pt-2">Ô đất</h5>
            <div class="item-content-row" v-for="i in slot">
                <div class="item-row-left" v-if="i.seed">
                    <div class="item-img-small">
                        <img :src="store.api + i.seed.image">
                    </div>
                    <b>{{ i.seed.name }}</b>
                </div>
                <div class="item-row-left" v-else>
                    <div class="item-img-small">
                    </div>
                    <b>Trống</b>
                </div>
                <div class="item-row-right" v-if="i.seed">
                    <p v-if="i.status == '1'">Trưởng thành</p>
                    <p v-else>{{ i.status }} giây</p>

                    <div class="icon-normal" @click="addCard('seed', {
        name: i.seed.name,
        path: i.seed.id,
        id: i.id,
        parent: 'gardent'
    })">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="8" x2="12" y2="12"></line>
                            <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                    </div>
                </div>
                <div class="item-row-right" v-else>
                    <div class="icon-normal" @click="addCard('store', {
        name: 'linh thảo',
        path: i.id,
        params: 'type=1',
        parent: 'gardent_plant'
    })">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                            <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <div class="d-flex align-items-center gap-2 flex-column" v-else>
        <div class="create-clan">
            <h5>Mua linh điền</h5>
            <div class="d-flex flex-column gap-1 align-items-center">
                <select class="form-select" name="quality" v-model="gardent_quality">
                    <option :value="key" v-for="value, key in quality">{{ value }}</option>
                </select>
                <p>Giá: {{ parseInt(gardent_quality) * 10000 }} linh thạch</p>
                <button class="btn btn-primary" type="button" @click="buyGardent">Mua</button>
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

<style></style>