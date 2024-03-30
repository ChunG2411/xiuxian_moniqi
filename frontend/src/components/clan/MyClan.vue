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
const clan_name = ref(null)

function getClan() {
    store.loading = true

    axios.get(`${store.api}/api/clan/current`, store.header)
        .then(response => {
            clan.value = response.data
            store.loading = false
        })
        .catch(error => {
            clan.value = null
            store.loading = false
        })
}
getClan()

function outClan() {
    store.loading = true

    axios.get(`${store.api}/api/clan/${clan.value.id}/out`, store.header)
        .then(response => {
            clan.value = null
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': "Rời môn phái thành công"
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

function createClan() {
    if (!clan_name.value) {
        store.noti = {
            'title': 'error',
            'content': 'Vui lòng nhập tên môn phái'
        }
        return
    }
    store.loading = true

    const form = new FormData()
    form.append('name', clan_name.value)

    axios.post(`${store.api}/api/clan`, form, store.header)
        .then(response => {
            getClan()
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Tạo môn phái thành công'
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

function upLevel() {
    store.loading = true

    axios.get(`${store.api}/api/clan/${clan.value.id}/up-level`, store.header)
        .then(response => {
            getClan()
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': "Tăng cấp môn phái thành công"
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

function upPosition() {
    store.loading = true

    axios.get(`${store.api}/api/clan/${clan.value.id}/up-positon`, store.header)
        .then(response => {
            getClan()
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': "Thăng chức thành công"
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
                    <th>Mô tả</th>
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
            <button type="button" class="btn btn-success" @click="addCard('member_clan', {
        name: clan.name,
        path: clan.id,
        position: clan.position
    })">Nhân sĩ</button>
            <button type="button" class="btn btn-danger" v-if="clan.position == 0" @click="addCard('request_clan', {
        path: clan.id
    })">Yêu cầu</button>
            <button type="button" class="btn btn-primary back-color-orange" v-else @click="upPosition">
                Thăng chức
            </button>
            <button type="button" class="btn btn-primary" @click="addCard('dedication', {
        name: clan.name,
        path: clan.id
    })">Cống hiến</button>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-outline-primary" v-if="clan.position == 0" @click="upLevel">
                Tăng cấp
            </button>
            <button type="button" class="btn btn-primary back-color-violet" @click="addCard('library')">
                Tàng kinh các
            </button>
            <button type="button" class="btn btn-warning" @click="addCard('shop', {
        name: clan.name,
        path: `clan/${clan.id}`,
        id: clan.id,
        parent: 'clan_shop'
    })">Cửa hàng</button>
        </div>
        <div class="button-group">
            <button type="button" class="btn btn-secondary" @click="addCard('clan_list')">Môn phái khác</button>
            <button type="button" class="btn btn-dark" @click="outClan">Rời phái</button>
        </div>
    </div>

    <div class="d-flex align-items-center gap-2 flex-column" v-else>
        <div class="button-group">
            <button type="button" class="btn btn-warning" @click="addCard('clan_list')">Tìm môn phái</button>
        </div>
        <div class="create-clan">
            <h5>Tự tạo môn phái</h5>
            <small>Tạo môn phái với 100.000 linh thạch</small>
            <div class="d-flex flex-column gap-1 align-items-center">
                <input type="text" placeholder="Tên môn phái" v-model="clan_name">
                <button type="button" @click="createClan">Tạo</button>
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
    width: 100%
}
</style>