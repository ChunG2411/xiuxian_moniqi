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
const question = ref(null)
const show_board = ref(false)
const prize = ref(null)


function getQuestion() {
    store.loading = true
    show_board.value = false
    prize.value = null

    axios.get(`${store.api}/api/question/current`, store.header)
        .then(response => {
            question.value = response.data
            store.loading = false
        })
        .catch(error => {
            question.value = null
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}
getQuestion()

function Answer(answer) {
    store.loading = true

    const form = new FormData()
    form.append('question', question.value.id)
    form.append('answer', answer)

    axios.post(`${store.api}/api/question/current`, form, store.header)
        .then(response => {
            prize.value = response.data
            show_board.value = true
            store.loading = false
        })
        .catch(error => {
            prize.value = null
            show_board.value = true
            store.loading = false
        })
}

function reload() {
    getQuestion()
}

</script>

<template>
    <div class="question" v-if="question">
        <p><b>Câu hỏi {{ question.number }}:</b> {{ question.question }}</p>
        <div class="answer_group">
            <p class="answer" @click="Answer('1')">{{ question.answer_1 }}</p>
            <p class="answer" @click="Answer('2')">{{ question.answer_2 }}</p>
            <p class="answer" @click="Answer('3')">{{ question.answer_3 }}</p>
        </div>
    </div>

    <div class="fullboard" v-if="show_board">
        <div class="d-flex flex-column gap-3 align-items-center" v-if="prize">
            <h5>Trả lời đúng</h5>
            <small>Nhận được</small>
            <p>Linh thạch: {{ prize.money }}</p>
            <button class="btn btn-success" type="button" @click="getQuestion">Tiếp theo</button>
        </div>
        <div class="d-flex flex-column gap-3 align-items-center" v-else>
            <h5>Trả lời sai</h5>
            <button class="btn btn-success" type="button" @click="getQuestion">Tiếp theo</button>
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

<style>
.answer_group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 100%;
    align-items: center;
    margin-top: 15px;
}
.answer {
    width: 80%;
    min-height: 70px;
    padding: 10px;
    background-color: var(--hover_color);
    border-radius: 10px;
}
.answer:hover {
    border: 1px solid green;
}
</style>