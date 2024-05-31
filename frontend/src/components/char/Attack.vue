<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'


const store = Store()

const props = defineProps({
    data: Object
})
const char_name = ref(null)
const my_char_name = ref(null)
const char_properties = ref(null)
const my_char_properties = ref(null)
const message = ref([])
const status = ref('')
const my_turn = ref(true)
var loop = null

const end = reactive({
    status: false,
    result: false
})
const prize = reactive({
    money: '',
    item: ''
})


async function getChar() {
    store.loading = true
    status.value = 'Đang chuẩn bị...'

    await axios.get(`${store.api}/api/characters/${props.data.path}`, store.header)
        .then(response => {
            char_name.value = response.data.name
            char_properties.value = response.data.properties
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
        })
    
    await axios.get(`${store.api}/api/character/current`, store.header)
        .then(response => {
            my_char_name.value = response.data.name
            my_char_properties.value = response.data.properties
            store.loading = false
            Start()
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

function Start() {
    setTimeout(()=>{
        status.value = 'Đang chiến đấu...'
        loop = setInterval(()=>{
            if (my_turn.value) {
                handleAction(my_char_name.value, my_char_properties.value, char_name.value, char_properties.value)
            }
            else{
                handleAction(char_name.value, char_properties.value, my_char_name.value, my_char_properties.value)
            }
        }, 500)
    }, 1000)
}

function handleAction(name_1, properties_1, name_2, properties_2) {
    if (Math.random() * 100 <= properties_1.hoi_phuc) {
        properties_1.mau_huyet += properties_1.luc_hoi_phuc
        message.value.unshift({
            name: name_1,
            content: 'Hồi phục ' + properties_1.luc_hoi_phuc + ' máu huyết'
        })
    }
    else {
        let dame = properties_1.cong_kich
        dame -= properties_2.phong_ngu
        if (Math.random() * 100 <= properties_2.ne_tranh) {
            message.value.unshift({
                name: name_1,
                content: 'Đòn đánh bị né tránh'
            })
        }
        else {
            if (Math.random() * 100 <= properties_1.chi_mang) {
                dame += properties_1.sat_thuong_chi_mang
                properties_2.mau_huyet -= dame
                message.value.unshift({
                    name: name_1,
                    content: 'Đánh chí mạng gây ' + dame + ' sát thương'
                })
            }
            else {
                properties_2.mau_huyet -= dame
                message.value.unshift({
                    name: name_1,
                    content: 'Gây ' + dame + ' sát thương'
                })
            }
        }
        if (Math.random() * 100 <= properties_1.hut_mau) {
            const hut_mau = dame * 0.1
            properties_1.mau_huyet += hut_mau
            message.value.unshift({
                name: name_1,
                content: 'Hồi lại ' + parseFloat(hut_mau).toFixed(2) + ' máu huyết từ đòn đánh'
            })
        }
        if (Math.random() * 100 <= properties_2.phan_kich) {
            const phan_kich = dame * 0.1
            properties_1.mau_huyet -= phan_kich
            message.value.unshift({
                name: name_2,
                content: 'Phản lại ' + parseFloat(phan_kich).toFixed(2) + ' sát thương'
            })
        }
    }
    if (properties_1.mau_huyet <= 0) {
        clearInterval(loop)
        properties_1.mau_huyet = 0
        status.value = name_2 + ' chiến thắng'
        End()
    }
    if (properties_2.mau_huyet <= 0) {
        clearInterval(loop)
        properties_2.mau_huyet = 0
        status.value = name_1 + ' chiến thắng'
        End()
    }
    my_turn.value = !my_turn.value
}

function End() {
    store.loading = true
    end.status = true
    
    const form = new FormData()
    form.append('type', '1')
    form.append('char_id', props.data.path)
    if (my_char_properties.value.mau_huyet <= 0) {
        form.append('results', '0')
        end.result = false
    }
    else {
        form.append('results', '1')
        end.result = true
    }

    axios.post(`${store.api}/api/fight`, form, store.header)
        .then(response => {
            prize.money = response.data.money
            prize.item = response.data.item
            store.loading = false
        })
        .catch(error => {
            store.loading = false
            prize.money = error.response.data.money
            prize.item = error.response.data.item
        })
}

</script>

<template>
    <div>
        <table class="table table-hover m-0">
            <tbody>
                <tr>
                    <th>{{ my_char_name }}</th>
                    <td>{{ parseInt(my_char_properties?.mau_huyet) }}</td>
                </tr>
                <tr>
                    <th>{{ char_name }}</th>
                    <td>{{ parseInt(char_properties?.mau_huyet) }}</td>
                </tr>
                <tr>
                    <th>Trạng thái</th>
                    <td>{{ status }}</td>
                </tr>
            </tbody>
        </table>
        <div class="m-2">
            <p v-for="i in message"><b>{{ i.name }}: </b>{{ i.content }}</p>
        </div>

        <div class="fullboard" v-if="end.status">
            <div class="d-flex flex-column gap-2 align-items-center">
                <div class="d-flex flex-column gap-2 align-items-center" v-if="end.result">
                    <h5>Chiến thắng</h5>
                    <p>Nhận được</p>
                </div>
                <div class="d-flex flex-column gap-2 align-items-center" v-else>
                    <h5>Thất bại</h5>
                    <p>Bị đoạt mất</p>
                </div>
                <div class="mb-4 mt-4">
                    <div class="d-flex align-items-center gap-2 mb-2">
                        <b>Linh thạch</b>
                        <p>{{ prize.money }}</p>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                        <b>Vật phẩm</b>
                        <div class="item-img-small" v-if="prize.item" @click="addCard('item', {
                            name: prize.item.name,
                            path: prize.item.id
                        })">
                            <img :src="store.api + prize.item.image" :class="`border-color-${prize.item.quality}`">
                        </div>
                        <p v-else>Không có</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>