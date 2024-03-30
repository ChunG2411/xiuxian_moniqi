import { defineStore } from 'pinia'

const Store = defineStore('store', {
    state: () => ({
        api: "http://127.0.0.1:8000",
        is_login: (localStorage.getItem('token') === null) ? false : true,
        header: {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}`},
        },
        card: 0,
        z_index: 0,
        component: [],
        loading: false,
        noti: {
            'title': '',
            'content': ''
        }
    }),
    actions: {
    }
})

export default Store