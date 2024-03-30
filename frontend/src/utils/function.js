import { useRouter } from 'vue-router'
import Store from '../utils/store.js'
import { title, level, type, properties, quality, position_clan, position_organ, seed } from '../utils/variables.js'


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

const getPositionOrgan = (num) => {
    return position_organ[num]
}

const getSeedType = (num) => {
    return seed[num]
}

export {
    CheckLogin,
    addCard, resetCard,
    getLevel, getType, getProperties, getQuality, getPositionClan, getPositionOrgan, getSeedType
}