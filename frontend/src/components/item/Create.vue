<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const menu = ref(null)
const material = ref([])
const lucky = ref([])

const create = reactive({
    menu_id: '',
    materials: [],
    lucky_id: ''
})
const active = ref('1')


function getKnowledge() {
    store.loading = true

    axios.get(`${store.api}/api/knowledge`, store.header)
        .then(response => {
            menu.value = response.data.menu
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
function getMaterial() {
    store.loading = true

    axios.get(`${store.api}/api/bag?tab=1`, store.header)
        .then(response => {
            for (let i = 0; i < response.data.length; i++) {
                if (response.data[i].type == '10') {
                    lucky.value.push(response.data[i])
                }
                else if (response.data[i].type == '6') {
                    material.value.push(response.data[i])
                }
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
getKnowledge()
getMaterial()

function activeTab(e) {
    const tabs = document.querySelectorAll('.create-tab-item')
    active.value = e.target.id
    tabs.forEach((tab) => {
        tab.classList.remove('active')
    })
    e.target.classList.add('active')
}

function reload() {
    create.menu_id = ''
    create.materials = []
    create.lucky_id = ''
    menu.value = null
    material.value = []
    lucky.value = []

    getKnowledge()
    getMaterial()
}

function selectMenu(id) {
    const menus = document.querySelectorAll('.menu-row')
    create.menu_id = id
    menus.forEach((menu) => {
        if (menu.id == id) {
            menu.classList.add('select')
        }
        else {
            menu.classList.remove('select')
        }
    })
}

function selectMaterial(id) {
    const materials = document.querySelectorAll('.material-row')
    if (create.materials.includes(id)) {
        var index = create.materials.indexOf(id);
        create.materials.splice(index, 1);
    }
    else {
        create.materials.push(id)
    }
    materials.forEach((item) => {
        item.classList.remove('select')
        for (let i = 0; i < create.materials.length; i++) {
            if (create.materials[i] == item.id) {
                item.classList.add('select')
            }
        }
    })
}

function selectLucky(id) {
    const luckys = document.querySelectorAll('.lucky-row')
    create.lucky_id = id
    luckys.forEach((lucky) => {
        if (lucky.id == id) {
            lucky.classList.add('select')
        }
        else {
            lucky.classList.remove('select')
        }
    })
}

function createItem() {
    store.loading = true

    let mar = ''
    for (let i = 0; i < create.materials.length; i++) {
        mar += create.materials[i] + ','
    }
    const form = new FormData()
    form.append('menu_id', create.menu_id)
    form.append('materials', mar)
    form.append('lucky_id', create.lucky_id)

    axios.post(`${store.api}/api/create`, form, store.header)
        .then(response => {
            menu.value = null
            material.value = []
            lucky.value = []

            store.noti = {
                'title': 'success',
                'content': 'Chế tạo vật phẩm thành công'
            }
            store.loading = false
        })
        .catch(error => {
            menu.value = null
            material.value = []
            lucky.value = []

            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

</script>

<template>
    <div class="create">
        <div class="create-tab">
            <p class="create-tab-item active" id="1" @click="activeTab($event)">Bước 1</p>
            <p class="create-tab-item" id="2" @click="activeTab($event)">Bước 2</p>
            <p class="create-tab-item" id="3" @click="activeTab($event)">Bước 3</p>
            <p class="create-tab-item" id="4" @click="activeTab($event)">Bước 4</p>
        </div>
        <div class="create-content" v-show="active == '1'">
            <h6 class="text-center mb-2">Lựa chọn công thức</h6>
            <div class="item-content-row menu-row" :id="i.id" v-for="i in menu">
                <div class="item-row-left">
                    <div class="item-img-small" :class="`border-color-${i.item.quality}`">
                        <img src="../../assets/image/menu.png">
                    </div>
                    <b>{{ i.name }}</b>
                </div>
                <div class="item-row-right">
                    <div class="icon-normal" @click="selectMenu(i.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <div class="icon-normal" @click="addCard('menu', {
                name: i.name,
                path: i.id
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
        <div class="create-content" v-show="active == '2'">
            <h6 class="text-center mb-2">Lựa chọn nguyên liệu</h6>
            <div class="item-content-row material-row" :id="i.id" v-for="i in material">
                <div class="item-row-left">
                    <div class="item-img-small" :class="`border-color-${i.quality}`">
                        <img :src="store.api + i.image">
                    </div>
                    <b>{{ i.name }}</b>
                </div>
                <div class="item-row-right">
                    <div class="icon-normal" @click="selectMaterial(i.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <div class="icon-normal" @click="addCard('item', {
                name: i.name,
                path: i.id
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
        <div class="create-content" v-show="active == '3'">
            <h6 class="text-center mb-2">Lựa chọn phụ gia</h6>
            <div class="item-content-row lucky-row" :id="i.id" v-for="i in lucky">
                <div class="item-row-left">
                    <div class="item-img-small" :class="`border-color-${i.quality}`">
                        <img :src="store.api + i.image">
                    </div>
                    <b>{{ i.name }}</b>
                </div>
                <div class="item-row-right">
                    <div class="icon-normal" @click="selectLucky(i.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <div class="icon-normal" @click="addCard('item', {
                name: i.name,
                path: i.id
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
        <div class="create-content text-center" v-show="active == '4'">
            <button class="btn btn-success" type="button" @click="createItem">Chế tạo</button>
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
.create-tab {
    display: flex;
    border-bottom: 1px solid var(--tab_border_color);
    position: absolute;
    top: 35px;
    width: calc(100% - 20px);
    background-color: var(--card_color);
    z-index: 100;
    padding-top: 10px;
}

.create-tab .create-tab-item {
    padding: 5px 15px;
    margin-bottom: -1px;
    cursor: pointer;
    height: 33px;
    max-height: 33px;
    overflow: hidden;
}

.create-tab .active {
    border: 1px solid var(--tab_border_color);
    border-bottom: 0;
    background-color: var(--card_color);
}

.create-content {
    margin-top: 40px;
}

.select {
    border: 1px solid green;
    border-radius: 10px;
}
</style>