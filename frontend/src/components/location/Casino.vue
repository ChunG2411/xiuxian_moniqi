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
var loop_wait_1 = null
var loop_result_1 = null
const input_big_1 = ref(null)
const input_small_1 = ref(null)
const time_wait_1 = ref(30)
const time_result_1 = ref(10)
const result_1 = ref(null)

const start_2 = ref(false)
const input_2 = ref(null)
const my_point_2 = ref(0)
const point_2 = ref(null)
const end_2 = ref(false)
const results_2 = ref(null)

const start_3 = ref(false)
const number_1 = ref(null)
const number_2 = ref(null)
const number_3 = ref(null)
const results_3 = ref([])


function Start_1() {
    loop_wait_1 = setInterval(() => {
        time_wait_1.value -= 1
        if (time_wait_1.value <= 0) {
            clearInterval(loop_wait_1)
            showResult_1()
        }
    }, 1000);
}

function showResult_1() {
    result_1.value = Math.floor(Math.random() * 10 + 1)

    if (input_big_1.value) {
        if (result_1.value <= 5) {
            sendResult('0', input_big_1.value)
        }
        else {
            sendResult('1', parseInt(input_big_1.value)-parseInt(input_big_1.value)/10)
        }
    }
    if (input_small_1.value) {
        if (result_1.value > 5) {
            sendResult('0', input_small_1.value)
        }
        else {
            sendResult('1', parseInt(input_small_1.value)-parseInt(input_small_1.value)/10)
        }
    }
    End()
}

function End() {
    loop_result_1 = setInterval(() => {
        time_result_1.value -= 1
        if (time_result_1.value <= 0) {
            clearInterval(loop_result_1)
            Restart_1()
        }
    }, 1000);
}

function Restart_1() {
    result_1.value = null
    input_big_1.value = null
    input_small_1.value = null
    time_wait_1.value = 30
    time_result_1.value = 10
    clearInterval(loop_result_1)
    clearInterval(loop_wait_1)
    Start_1()
}

function Start_2() {
    if (!input_2.value) {
        store.noti = {
            'title': 'error',
            'content': 'Cần nhập số linh thạch để bắt đầu'
        }
    }
    else {
        start_2.value = true
    }
}
function addPoint_2() {
    my_point_2.value += Math.floor(Math.random() * 10 + 1)
    if (my_point_2.value > 23) {
        end_2.value = true
        results_2.value = '0'
        sendResult('0', input_2.value)
    }
}

function viewPoint_2() {
    point_2.value += Math.floor(Math.random() * 5 + 20)
    end_2.value = true
    if (point_2.value > 23) {
        results_2.value = '1'
        sendResult('1', parseInt(input_2.value)-parseInt(input_2.value)/10)
    }
    else if (point_2.value > my_point_2.value) {
        results_2.value = '0'
        sendResult('0', input_2.value)
    }
    else if (point_2.value < my_point_2.value) {
        results_2.value = '1'
        sendResult('1', parseInt(input_2.value)-parseInt(input_2.value)/10)
    }
}

function Restart_2() {
    input_2.value = null
    start_2.value = false
    my_point_2.value = 0
    point_2.value = null
    end_2.value = false
    results_2.value = null
}

function Start_3() {
    start_3.value = true
    results_3.value = []
    let count_1 = 0
    let count_2 = 0
    let count_3 = 0

    var loop_1 = setInterval(() => {
        count_1 += 1
        if (count_1 <= 50) {
            number_1.value += 1
            if (number_1.value > 7) {
                number_1.value = 0
            }
        } else {
            number_1.value = Math.floor(Math.random() * 7 + 1)
            clearInterval(loop_1)
        }
    }, 100);
    var loop_2 = setInterval(() => {
        count_2 += 1
        if (count_2 <= 100) {
            number_2.value += 1
            if (number_2.value > 7) {
                number_2.value = 0
            }
        } else {
            number_2.value = Math.floor(Math.random() * 7 + 1)
            if (number_2.value == number_1.value) {
                results_3.value.push('1')
                results_3.value.push('2')
            }
            clearInterval(loop_2)
        }
    }, 100);
    var loop_3 = setInterval(() => {
        count_3 += 1
        if (count_3 <= 150) {
            number_3.value += 1
            if (number_3.value > 7) {
                number_3.value = 0
            }
        } else {
            number_3.value = Math.floor(Math.random() * 7 + 1)
            if (number_3.value == number_2.value) {
                results_3.value.push('2')
                results_3.value.push('3')
            }
            clearInterval(loop_3)
            End_3()
        }
    }, 100);
}

function End_3() {
    start_3.value = false
    if (results_3.value.length == 2) {
        sendResult('1', 200)
    }
    else if (results_3.value.length > 2) {
        sendResult('1', 1000)
    }
    else {
        sendResult('0', 100)
    }
}

function sendResult(result, money) {
    store.loading = true

    const form = new FormData()
    form.append('result', result)
    form.append('money', parseInt(money))

    axios.post(`${store.api}/api/game`, form, store.header)
        .then(response => {
            store.loading = false
            store.noti = {
                'title': 'success',
                'content': 'Bạn đã thắng ' + response.data.money
            }
        })
        .catch(error => {
            store.loading = false
            store.noti = {
                'title': 'error',
                'content': 'Bạn đã thua ' + error.response.data.money
            }
        })
}

Start_1()
function reload() {
    Restart_1()
    Restart_2()
}

</script>

<template>
    <div class="d-flex flex-column gap-2 align-items-center border p-2">
        <h5>Đặt cược</h5>
        <div class="d-flex mb-1">
            <div class="d-flex flex-column align-items-center gap-1">
                <div>
                    <b>Tiểu</b>
                    <small class="ms-1">(1-5)</small>
                </div>
                <input type="number" min="1" placeholder="Nhập số linh thạch" v-model="input_small_1">
            </div>
            <div class="d-flex flex-column align-items-center gap-1">
                <div>
                    <b>Đại</b>
                    <small class="ms-1">(6-10)</small>
                </div>
                <input type="number" min="1" placeholder="Nhập số linh thạch" v-model="input_big_1">
            </div>
        </div>
        <div v-if="result_1">
            <h6>Kết quả: {{ result_1 }}</h6>
            <h6>Bắt đầu sau: {{ time_result_1 }} giây</h6>
        </div>
        <div v-else>
            <h6>Đang chờ đặt cược</h6>
            <h6>Thời gian còn: {{ time_wait_1 }} giây</h6>
        </div>
    </div>

    <div class="d-flex flex-column gap-2 align-items-center border p-2 mt-3">
        <h5>Rút điểm</h5>
        <div class="d-flex flex-column gap-2 align-items-center" v-if="!start_2">
            <input type="number" min="1" placeholder="Số linh thạch cược" v-model="input_2">
            <button class="btn btn-success" @click="Start_2">Bắt đầu</button>
        </div>
        <div class="w-100 d-flex flex-column align-items-center text-center" v-else>
            <p>Điểm tối đa là 23, điểm của bạn vượt quá 23 sẽ thua</p>
            <div class="d-flex mb-3 mt-1 gap-5">
                <div class="d-flex flex-column align-items-center gap-1">
                    <b>Điểm của bạn</b>
                    <b :class="(results_2=='1')?'text-success':(results_2=='0')?'text-danger':''">{{ my_point_2 }}</b>
                </div>
                <div class="d-flex flex-column align-items-center gap-1">
                    <b>Điểm đối thủ</b>
                    <b :class="(results_2=='1')?'text-danger':(results_2=='0')?'text-success':''">{{ point_2 ? point_2 : '...' }}</b>
                </div>
            </div>
            <div v-if="end_2">
                <button class="btn btn-success" @click="Restart_2">Ván mới</button>
            </div>
            <div class="button-group" v-else>
                <button class="btn btn-primary" @click="addPoint_2">Rút <small class="text-white">(1-10)</small></button>
                <button class="btn btn-warning" @click="viewPoint_2">Xem điểm</button>
            </div>
        </div>
    </div>

    <div class="d-flex flex-column gap-2 align-items-center border p-2 mt-3">
        <h5>Nối số</h5>
        <p>Mỗi lần nối tiêu hao 100 linh thạch</p>
        <div class="w-100 d-flex flex-column align-items-center text-center">
            <div class="d-flex mb-3 mt-1 gap-4">
                <b :class="(results_3.includes('1') ? 'text-success' : '')">{{ number_1 }}</b>
                <b :class="(results_3.includes('2') ? 'text-success' : '')">{{ number_2 }}</b>
                <b :class="(results_3.includes('3') ? 'text-success' : '')">{{ number_3 }}</b>
            </div>
            <div v-if="!start_3">
                <button class="btn btn-primary" @click="Start_3">Xoay</button>
            </div>
        </div>
    </div>

    <div class="reload" @click="reload">
        <div class="icon-small">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38" />
            </svg>
        </div>
    </div>
</template>

<style scoped></style>