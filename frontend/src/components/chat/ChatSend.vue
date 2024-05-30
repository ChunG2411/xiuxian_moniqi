<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'


const store = Store()

const props = defineProps({
    data: Object
})
const form_content = ref('')


function submit() {
    store.loading = true

    const form = new FormData()
    form.append('to', props.data.path)
    form.append('content', form_content.value)

    axios.post(`${store.api}/api/chat`, form, store.header)
        .then(response => {
            store.loading = false
            form_content.value = ''
            store.noti = {
                'title': 'success',
                'content': 'Gửi thành công'
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
    form_content.value = ''
}

</script>

<template>
    <div class="d-flex flex-column align-items-center gap-2">
        <h5>Nội dung</h5>
        <textarea type="text" class="form-control" placeholder="Nhập nội dung" v-model="form_content"></textarea>
        <button class="btn btn-success" @click="submit">Gửi</button>
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