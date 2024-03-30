<script setup>
import { addCard } from '../utils/function.js'
import Card from '../components/main/Card.vue'
import Navbar from '../components/main/Navbar.vue'

import Signin from '../components/auth/Signin.vue'
import Signup from '../components/auth/Signup.vue'
import Pass from '../components/auth/Pass.vue'
import Setting from '../components/auth/Setting.vue'
import Information from '../components/auth/Information.vue'

import Store from '../utils/store.js'

const store = Store()

addCard('signin')

</script>

<template>
    <Navbar data="auth"></Navbar>

    <Card v-for="i in store.component">
        <template #title>
            <p>{{ i.title }}</p>
        </template>
        <template #body>
            <Signin :data="i.data" v-if="i.body == 'signin'"></Signin>
            <Signup :data="i.data" v-else-if="i.body == 'signup'"></Signup>
            <Pass :data="i.data" v-else-if="i.body == 'pass'"></Pass>
            <Setting :data="i.data" v-else-if="i.body == 'setting'"></Setting>
            <Information v-else-if="i.body == 'infor'"></Information>
        </template>
    </Card>
</template>

<style></style>