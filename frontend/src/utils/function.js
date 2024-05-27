import { useRouter } from 'vue-router'
import Store from '../utils/store.js'
import {
    title, level, type, properties, quality, position_clan, seed,
    locality, mine, market
 } from '../utils/variables.js'


const CheckLogin = () => {
    const router = useRouter()
    const store = Store()
    if (!store.is_login) {
        router.push({ path: '/login' })
    }
}

const resetCard = () => {
    const store = Store()
    store.component = []
    store.card = 0
    store.z_index = 0
}

const addCard = (type, data = {}) => {
    const store = Store()
    store.component.push({
        'title': data.name ? title[type] + ' ' + data.name : title[type],
        'body': type,
        'data': data
    })
}

const formatDate = (datetime) => {
    const date = datetime.split('T')[0]
    const time = datetime.split('T')[1].split('.')[0]
    return date + ' ' + time
}

const getLevel = (num) => {
    return level[num]
}

const getType = (num) => {
    return type[num]
}

const getProperties = (num) => {
    return properties[num]
}

const getQuality = (num) => {
    return quality[num]
}

const getPositionClan = (num) => {
    return position_clan[num]
}

const getSeedType = (num) => {
    return seed[num]
}

const getLocality = (type) => {
    return locality[type]
}

const getMine = (type) => {
    return mine[type]
}

const getMarket = (type) => {
    return market[type]
}

export {
    CheckLogin, addCard, resetCard,
    getLevel, getType, getProperties, getQuality, getPositionClan, getSeedType,
    getLocality, getMine, getMarket,
    formatDate
}