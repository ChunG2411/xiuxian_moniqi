<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard, resetCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})
const char = reactive({
    name: '',
    gender: '1'
})


function Create() {
    if (!char.name) {
        store.noti = {
            'title': 'error',
            'content': 'Vui lòng nhập tên nhân vật'
        }
        return
    }
    store.loading = true

    const form = new FormData()
    form.append('name', char.name)
    form.append('gender', char.gender)

    axios.post(`${store.api}/api/characters`, form, store.header)
        .then(response => {
            store.noti = {
                'title': 'success',
                'content': 'Tạo nhân vật thành công'
            }
            store.loading = false
            resetCard()
            addCard('mychar')
        })
        .catch(error => {
            store.noti = {
                'title': 'error',
                'content': error.response.data
            }
            store.loading = false
        })
}

</script>

<template>
    <div class="align-items-center d-flex flex-column gap-4">
        <h3>Tạo nhân vật</h3>
        <div class="align-items-center d-flex flex-column gap-2 w-100">
            <input type="text" placeholder="Tên nhân vật" v-model="char.name">
            <select class="form-select" name="gender" v-model="char.gender">
                <option value="1" selected>Nam</option>
                <option value="2">Nữ</option>
            </select>
            <button type="button" @click="Create">Tạo</button>
        </div>
    </div>
</template>

<style></style>