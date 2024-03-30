<script setup>
import { defineProps, watch, ref } from 'vue'
import { useToast } from "vue-toastification";
import { useRouter } from 'vue-router'

import { addCard, resetCard } from '../../utils/function.js'
import Store from '../../utils/store.js'

const store = Store()
const toast = useToast()
const router = useRouter()

const props = defineProps({
    data: String
})


watch(() => store.noti, (currentvalue, oldvalue) => {
    if (currentvalue.title == 'success') {
        toast.success(currentvalue.content);
    }
    else if (currentvalue.title == 'warning') {
        toast.warning(currentvalue.content);
    }
    else if (currentvalue.title == 'error') {
        toast.error(currentvalue.content);
    }
})

function logout() {
    localStorage.removeItem('token')
    resetCard()
    router.push({ path: '/login' })
}

</script>

<template>
    <div class="navbar" v-if="props.data == 'auth'">
        <div class="navbar-slot" @click="addCard('signin')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <path d="M5.52 19c.64-2.2 1.84-3 3.22-3h6.52c1.38 0 2.58.8 3.22 3" />
                    <circle cx="12" cy="10" r="3" />
                    <circle cx="12" cy="12" r="10" />
                </svg>
            </div>
            <div class="navbar-title">
                <p>Đăng nhập</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('signup')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <path d="M20 14.66V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5.34"></path>
                    <polygon points="18 2 22 6 12 16 8 16 8 12 18 2"></polygon>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Đăng ký</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('pass')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Quên mật khẩu</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('setting')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path
                        d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z">
                    </path>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Thiết lập</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('infor')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Thông tin</p>
            </div>
        </div>
    </div>
    <div class="navbar" v-if="props.data == 'home'">
        <div class="navbar-slot" @click="addCard('mychar')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Nhân vật</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('bag')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <path d="M6 2L3 6v14c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2V6l-3-4H6zM3.8 6h16.4M16 10a4 4 0 1 1-8 0" />
                </svg>
            </div>
            <div class="navbar-title">
                <p>Túi trữ vật</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('study')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z" />
                    <path d="M14 3v5h5M16 13H8M16 17H8M10 9H8" />
                </svg>
            </div>
            <div class="navbar-title">
                <p>Công pháp</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('clan')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512">
                    <path d="M560 160A80 80 0 1 0 560 0a80 80 0 1 0 0
                        160zM55.9 512H381.1h75H578.9c33.8 0 61.1-27.4
                        61.1-61.1c0-11.2-3.1-22.2-8.9-31.8l-132-216.3C495
                        196.1 487.8 192 480 192s-15 4.1-19.1 10.7l-48.2
                        79L286.8 81c-6.6-10.6-18.3-17-30.8-17s-24.1 6.4-30.8
                        17L8.6 426.4C3 435.3 0 445.6 0 456.1C0 487 25 512 55.9 512z" />
                </svg>
            </div>
            <div class="navbar-title">
                <p>Môn phái</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('city')">
            <div class="icon-normal">
                <img src="../../assets/image/city.png">
            </div>
            <div class="navbar-title">
                <p>Thành trấn</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('location')">
            <div class="icon-normal">
                <img src="../../assets/image/location.png">
            </div>
            <div class="navbar-title">
                <p>Bí cảnh</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('job')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Nghề nghiệp</p>
            </div>
        </div>
        <div class="navbar-slot" @click="addCard('time')">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Thời gian</p>
            </div>
        </div>
        <div class="navbar-slot" @click="">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z">
                    </path>
                    <line x1="12" y1="9" x2="12" y2="13"></line>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
            </div>
            <div class="navbar-title">
                <p>Bách hiểu sinh</p>
            </div>
        </div>
        <div class="navbar-slot" @click="logout">
            <div class="icon-normal">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="#000000" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs">
                    <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M13.8 12H3" />
                </svg>
            </div>
            <div class="navbar-title">
                <p>Đăng xuất</p>
            </div>
        </div>
    </div>

    <div class="loading" v-if="store.loading">
        <h6>Vui lòng chờ...</h6>
    </div>
</template>

<style>
.navbar {
    height: 100vh;
    background-color: var(--card_color);
    top: 0;
    left: 0;
    border-right: 1px solid var(--border_color);
    box-shadow: 0 0 10px var(--shadow_color);
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
    padding: 10px;
    position: relative;
    z-index: 99;
    width: max-content;
}

.navbar-slot {
    position: relative;
}

.navbar-slot:hover .navbar-title {
    display: block;
}

.navbar-title {
    position: absolute;
    left: 70px;
    width: max-content;
    max-height: 40px;
    background-color: var(--card_color);
    padding: 10px 15px;
    border-radius: 10px;
    top: 0;
    display: none;
    box-shadow: 0 5px 20px var(--shadow_color);
}

.navbar-title::before {
    content: "";
    position: absolute;
    width: 0px;
    height: 0px;
    border: 10px solid;
    border-color: transparent var(--card_color) transparent transparent;
    left: -20px;
    top: 10px;
}

.loading {
    padding: 10px 20px;
    border: var(--border_color);
    border-radius: 10px;
    background-color: var(--card_color);
    box-shadow: 0 0 5px var(--shadow_color);
    position: absolute;
    top: 5px;
    left: 50%;
    animation: topdown 0.5s;
    z-index: 100;
}
</style>