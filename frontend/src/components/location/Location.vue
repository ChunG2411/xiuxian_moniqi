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
    <div class="location">
        <div class="item-content-row">
            <div class="item-row-left">
                <div class="item-img-small">
                    <img src="../../assets/image/tower.png">
                </div>
                <b>Tháp thí luyện</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('tower')">
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
                    <img src="../../assets/image/arena.png">
                </div>
                <b>Đấu trường</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('arena')">
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
                    <img src="../../assets/image/rank.png">
                </div>
                <b>Bảng xếp hạng</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('rank')">
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
                <b>Hồ câu</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('fishing')">
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
                    <img src="../../assets/image/moutain.png">
                </div>
                <b>Bãi săn</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('hunt')">
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
                    <img src="../../assets/image/casino.png">
                </div>
                <b>Giải trí</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('casino')">
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
                    <img src="../../assets/image/ask.png">
                </div>
                <b>Trắc nghiệm</b>
            </div>
            <div class="item-row-right">
                <div class="icon-normal" @click="addCard('question')">
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
        <div class="icon-small">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38" />
            </svg>
        </div>
    </div>
</template>

<style></style>