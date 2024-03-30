<script setup>
import { ref } from 'vue'
import Store from '../../utils/store.js'

const store = Store()
store.card += 1
store.z_index += 1

const id = store.card
const z_index = ref(store.z_index)
const left = Math.floor(Math.random() * (300 - 65) + 65)
const top = Math.floor(Math.random() * (200 - 65) + 65)
const maximize = ref(false)
const card = ref(null)

setTimeout(() => {
    card.value = document.getElementById(`card-${id}`)
    card.value.style.left = String(left) + 'px'
    card.value.style.top = String(top) + 'px'
    card.value.style.display = 'block'
    card.value.style.zIndex = String(z_index.value)
}, 100);

function click() {
    store.z_index += 1
    z_index.value = store.z_index
    card.value.style.zIndex = String(z_index.value)
}

function zoom() {
    if (maximize.value) {
        card.value.style.width = '350px'
        card.value.style.height = '450px'
        maximize.value = false
    }
    else {
        card.value.style.width = 'calc(100vw - 85px)'
        card.value.style.height = 'calc(100vh - 20px)'
        card.value.style.left = '75px'
        card.value.style.top = '10px'
        maximize.value = true
    }
}

function remove() {
    card.value.remove()
}

function drag(e) {
    window.addEventListener('mousemove', mousemove)
    window.addEventListener('mouseup', mouseup)

    let prevX = e.clientX
    let prevY = e.clientY

    function mousemove(e) {
        const newX = prevX - e.clientX
        const newY = prevY - e.clientY

        const rect = card.value.getBoundingClientRect()
        card.value.style.left = rect.left - newX + 'px'
        card.value.style.top = rect.top - newY + 'px'

        prevX = e.clientX
        prevY = e.clientY
    }

    function mouseup() {
        window.removeEventListener('mousemove', mousemove)
        window.removeEventListener('mouseup', mouseup)
    }
}

</script>

<template>
    <div class="card" :id="`card-${id}`" @mousedown="click">
        <div class="card-head" @mousedown="drag">
            <div class="card-head-title">
                <slot name="title"></slot>
            </div>
            <div class="card-head-action">
                <div class="icon-small" @click="zoom()" v-if="maximize">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                </div>
                <div class="icon-small" @click="zoom()" v-else>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <path
                            d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3">
                        </path>
                    </svg>
                </div>
                <div class="icon-small" @click="remove(id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </div>
            </div>
        </div>
        <div class="card-body">
            <slot name="body"></slot>
        </div>
    </div>
</template>

<style>
.card {
    background-color: var(--card_color);
    color: var(--text_color);
    border-radius: 5px;
    border: 1px solid var(--border_color);
    box-shadow: 0 0 15px var(--shadow_color);
    position: fixed;
    width: max-content;
    height: max-content;
    width: 350px;
    height: 450px;
    /* overflow: hidden; */
    display: none;
    transition: width 0.5s, height 0.5s;
}

.card-head {
    height: max-content;
    background-color: #c5c5c5;
    color: #ffffff;
    display: flex;
    justify-content: space-between;
    padding: 5px 10px;
    align-items: center;
}

.card-head-title {
    width: 200px;
    height: 20px;
    overflow: hidden;
    align-items: center;
    font-weight: 600;
}

.card-head-action {
    display: flex;
    align-items: center;
    width: max-content;
}

.card-body {
    height: calc(100% - 35px);
    width: 100%;
    max-width: 100%;
    overflow-y: scroll;
    overflow-x: hidden;
    padding: 10px;
}

.card-body::-webkit-scrollbar {
    width: 5px;
}

.card-body::-webkit-scrollbar-track {
    background: transparent;
}

.card-body::-webkit-scrollbar-thumb {
    background: rgb(197, 197, 197);
    border-radius: 5px;
}
</style>