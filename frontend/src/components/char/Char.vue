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
const pet = ref(null)

function getChar() {
    store.loading = true

    axios.get(`${store.api}/api/characters/${props.data.path}`, store.header)
        .then(response => {
            char.value = response.data
            store.loading = false
            getPet()
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

function getEquip() {
    store.loading = true

    axios.get(`${store.api}/api/equipped?char=${props.data.path}`, store.header)
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

function getPet() {
    store.loading = true

    axios.get(`${store.api}/api/pets/own?char=${char.value.id}`, store.header)
        .then(response => {
            pet.value = response.data
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
    getPet()
}

function acceptRequest() {
    store.loading = true

    axios.get(`${store.api}/api/clan-request/${props.data.id}/accept`, store.header)
        .then(response => {
            store.loading = false
            char.value = null
            store.noti = {
                'title': 'success',
                'content': 'Đã phê duyệt'
            }
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': 'Xin kiểm tra lại'
            }
            store.loading = false
        })
}

function rejectRequest() {
    store.loading = true

    axios.get(`${store.api}/api/clan-request/${props.data.id}/reject`, store.header)
        .then(response => {
            store.loading = false
            char.value = null
            store.noti = {
                'title': 'success',
                'content': 'Đã từ chối'
            }
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': 'Xin kiểm tra lại'
            }
            store.loading = false
        })
}

function removeMember() {
    store.loading = true

    axios.delete(`${store.api}/api/clan/${props.data.id}/member?${props.data.params}`, store.header)
        .then(response => {
            store.loading = false
            char.value = null
            store.noti = {
                'title': 'success',
                'content': 'Đã trục xuất'
            }
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': 'Xin kiểm tra lại'
            }
            store.loading = false
        })
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4" v-if="char && pet">
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
            <h5>Trang bị</h5>
            <div class="d-flex gap-2">
                <div class="item-img-small" :class="`border-color-${equip.hand.quality}`" v-if="equip.hand" @click="addCard('item', {
        name: equip.hand.name,
        path: equip.hand.id,
        parent: ''
    })">
                    <img :src="store.api + equip.hand.image">
                </div>
                <div class="item-img-small" v-else>
                </div>

                <div class="item-img-small" :class="`border-color-${equip.head.quality}`" v-if="equip.head" @click="addCard('item', {
        name: equip.head.name,
        path: equip.head.id,
        parent: ''
    })">
                    <img :src="store.api + equip.head.image">
                </div>
                <div class="item-img-small" v-else>
                </div>

                <div class="item-img-small" :class="`border-color-${equip.shirt.quality}`" v-if="equip.shirt" @click="addCard('item', {
        name: equip.shirt.name,
        path: equip.shirt.id,
        parent: ''
    })">
                    <img :src="store.api + equip.shirt.image">
                </div>
                <div class="item-img-small" v-else>
                </div>

                <div class="item-img-small" :class="`border-color-${equip.trousers.quality}`" v-if="equip.trousers"
                    @click="addCard('item', {
        name: equip.trousers.name,
        path: equip.trousers.id,
        parent: ''
    })">
                    <img :src="store.api + equip.trousers.image">
                </div>
                <div class="item-img-small" v-else>
                </div>

                <div class="item-img-small" :class="`border-color-${pet.pet.quality}`" v-if="pet.pet"
                    @click="addCard('pet', {
        name: pet.pet.name,
        path: pet.pet.id,
        id: char.id,
        parent: 'char'
    })">
                    <img :src="store.api + pet.pet.image">
                </div>
                <div class="item-img-small" v-else>
                </div>
            </div>
        </div>

        <div class="button-group" v-if="props.data.parent == 'request'">
            <button type="button" class="btn btn-success" @click="acceptRequest">Phê duyệt</button>
            <button type="button" class="btn btn-danger" @click="rejectRequest">Từ chối</button>
        </div>
        <div class="button-group" v-if="props.data.parent == 'member'">
            <button type="button" class="btn btn-success" @click="removeMember">Trục xuất</button>
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