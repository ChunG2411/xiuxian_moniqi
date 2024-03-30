<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard, resetCard, getLevel, getPositionClan, getPositionOrgan } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const char = ref(null)
const equip = ref(null)


function getChar() {
    store.loading = true

    axios.get(`${store.api}/api/character/current`, store.header)
        .then(response => {
            char.value = response.data
            store.loading = false
        })
        .catch(error => {
            if (error.response.data.includes('exist')) {
                resetCard()
                addCard('create')
            }
            else {
                store.noti = {
                    'title': 'error',
                    'content': error.response.data
                }
            }
            store.loading = false
        })
}

function getEquip() {
    store.loading = true

    axios.get(`${store.api}/api/equipped`, store.header)
        .then(response => {
            equip.value = response.data
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

getChar()
getEquip()

function reload() {
    getChar()
    getEquip()
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="char">
        <div class="profile-img">
            <img :src="store.api + char.appearance">
        </div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>Tên</th>
                    <td>{{ char.name }}</td>
                </tr>
                <tr>
                    <th>Giới tính</th>
                    <td>{{ (char.gender == '1') ? 'Nam' : 'Nữ' }}</td>
                </tr>
                <tr>
                    <th>Tông phái</th>
                    <td v-if="char.clan">{{ getPositionClan(char.clan.position) }} {{ char.clan.clan.name }}</td>
                    <td v-else>Không có</td>
                </tr>
                <tr>
                    <th>Thế lực</th>
                    <td v-if="char.organization">{{ getPositionOrgan(char.organization.position) }} {{
        char.organization.organization.name
    }}</td>
                    <td v-else>Không có</td>
                </tr>
                <tr>
                    <th>Cảnh giới</th>
                    <td>{{ getLevel(char.properties.canh_gioi) }}</td>
                </tr>
                <tr>
                    <th>Linh lực</th>
                    <td>{{ char.properties.linh_luc }} / {{ char.properties.linh_luc_yeu_cau }}</td>
                </tr>
                <tr>
                    <th>Chiến lực</th>
                    <td>{{ char.properties.power }}</td>
                </tr>
            </tbody>
        </table>
        <div class="align-items-center d-flex flex-column gap-2 w-100">
            <h5>Chỉ số</h5>
            <table class="table table-hover m-0">
                <tbody>
                    <tr>
                        <th>Tuổi</th>
                        <td>{{ char.properties.tuoi }}</td>
                        <th>Máu huyết</th>
                        <td>{{ char.properties.mau_huyet }}</td>
                        <th>Luyện khí</th>
                        <td>{{ char.properties.luyen_khi }}</td>
                    </tr>
                    <tr>
                        <th>Thọ nguyên</th>
                        <td>{{ char.properties.tuoi_tho }}</td>
                        <th>Công kích</th>
                        <td>{{ char.properties.cong_kich }}</td>
                        <th>Luyện đan</th>
                        <td>{{ char.properties.luyen_dan }}</td>
                    </tr>
                    <tr>
                        <th>Tâm tình</th>
                        <td>{{ char.properties.tam_tinh }}</td>
                        <th>Phòng ngự</th>
                        <td>{{ char.properties.phong_ngu }}</td>
                        <th>Dược liệu</th>
                        <td>{{ char.properties.duoc_lieu }}</td>
                    </tr>
                    <tr>
                        <th>Sức khỏe</th>
                        <td>{{ char.properties.suc_khoe }}</td>
                        <th>Tốc độ</th>
                        <td>{{ char.properties.toc_do }}</td>
                        <th>May mắn</th>
                        <td>{{ char.properties.may_man }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="align-items-center d-flex flex-column gap-2 w-100">
            <h5>Trang bị</h5>
            <div class="d-flex gap-2" v-if="equip">
                <div class="item-img-small" :class="`border-color-${equip.hand.quality}`" v-if="equip.hand" @click="addCard('item', {
        name: equip.hand.name,
        path: equip.hand.id,
        parent: 'char'
    })">
                    <img :src="store.api + equip.hand.image">
                </div>
                <div class="item-img-small" v-else>
                </div>
                <div class="item-img-small" :class="`border-color-${equip.head.quality}`" v-if="equip.head" @click="addCard('item', {
        name: equip.head.name,
        path: equip.head.id,
        parent: 'char'
    })">
                    <img :src="store.api + equip.head.image">
                </div>
                <div class="item-img-small" v-else>
                </div>
                <div class="item-img-small" :class="`border-color-${equip.shirt.quality}`" v-if="equip.shirt" @click="addCard('item', {
        name: equip.shirt.name,
        path: equip.shirt.id,
        parent: 'char'
    })">
                    <img :src="store.api + equip.shirt.image">
                </div>
                <div class="item-img-small" v-else>
                </div>
                <div class="item-img-small" :class="`border-color-${equip.trousers.quality}`" v-if="equip.trousers"
                    @click="addCard('item', {
        name: equip.trousers.name,
        path: equip.trousers.id,
        parent: 'char'
    })">
                    <img :src="store.api + equip.trousers.image">
                </div>
                <div class="item-img-small" v-else>
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