<script setup>
import { defineProps, ref, reactive } from 'vue'
import axios from 'axios'

import Store from '../../utils/store.js'
import { addCard } from '../../utils/function.js'


const store = Store()

const props = defineProps({
    data: Object
})

</script>

<template>
    <div class="job">
        <div class="item-content-row">
            <div class="item-row-left">
                <div class="item-img-small">
                    <img src="../../assets/image/house.jpg">
                </div>
                <b>Thế lực</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('locality')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
            </div>
        </div>
        <div class="item-content-row">
            <div class="item-row-left">
                <div class="item-img-small">
                    <img src="../../assets/image/house.jpg">
                </div>
                <b>Động phủ</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('house')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
            </div>
        </div>
        <div class="item-content-row">
            <div class="item-row-left">
                <div class="item-img-small">
                    <img src="../../assets/image/garden.svg">
                </div>
                <b>Linh điền</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('gardent')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
            </div>
        </div>
        <div class="item-content-row">
            <div class="item-row-left">
                <div class="item-img-small">
                    <img src="../../assets/image/cage.jpg">
                </div>
                <b>Chuồng thú</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('cage')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
            </div>
        </div>
        <div class="item-content-row">
            <div class="item-row-left">
                <div class="item-img-small">
                    <img src="../../assets/image/lake.jpg">
                </div>
                <b>Linh đàm</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('lake')">
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