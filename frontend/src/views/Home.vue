<script setup>
import { ref } from 'vue'
import { addCard } from '../utils/function.js'
import Store from '../utils/store.js'

import Card from '../components/main/Card.vue'
import Navbar from '../components/main/Navbar.vue'

import MyChar from '../components/char/MyChar.vue'
import Char from '../components/char/Char.vue'
import CreateChar from '../components/char/CreateChar.vue'
import Bag from '../components/char/Bag.vue'
import BagItem from '../components/char/BagItem.vue'
import Time from '../components/char/Time.vue'
import Study from '../components/char/Study.vue'
import StudyProcess from '../components/char/StudyProcess.vue'
import Knowledge from '../components/char/Knowledge.vue'

import Item from '../components/item/Item.vue'
import Book from '../components/item/Book.vue'
import Shop from '../components/item/Shop.vue'
import Seed from '../components/item/Seed.vue'
import Menu from '../components/item/Menu.vue'
import Create from '../components/item/Create.vue'
import Pet from '../components/item/Pet.vue'

import MyClan from '../components/clan/MyClan.vue'
import ClanList from '../components/clan/ClanList.vue'
import ClanDetail from '../components/clan/ClanDetail.vue'
import ClanMember from '../components/clan/ClanMember.vue'
import ClanRequest from '../components/clan/ClanRequest.vue'
import ClanDedication from '../components/clan/ClanDedication.vue'
import ClanLibrary from '../components/clan/ClanLibrary.vue'

import CityList from '../components/city/CityList.vue'
import CityDetail from '../components/city/CityDetail.vue'
import CitySell from '../components/city/CitySell.vue'
import Restore from '../components/city/Restore.vue'

import Location from '../components/location/Location.vue'
import Tower from '../components/location/Tower.vue'
import Rank from '../components/location/Rank.vue'
import Question from '../components/location/Question.vue'
import Fishing from '../components/location/Fishing.vue'
import Hunt from '../components/location/Hunt.vue'
import ShopPet from '../components/location/Shop.vue'

import Job from '../components/job/Job.vue'
import House from '../components/job/House.vue'
import Gardent from '../components/job/Gardent.vue'
import Cage from '../components/job/Cage.vue'
import Lake from '../components/job/Lake.vue'
import Oven from '../components/job/Oven.vue'
import StoreHouse from '../components/job/Store.vue'
import ShopHouse from '../components/job/Shop.vue'


const store = Store()

addCard('mychar')

</script>

<template>
    <Navbar data="home"></Navbar>

    <Card v-for="i in store.component">
        <template #title>
            <p>{{ i.title }}</p>
        </template>
        <template #body>
            <MyChar :data="i.data" v-if="i.body == 'mychar'"></MyChar>
            <Char :data="i.data" v-if="i.body == 'char'"></Char>
            <CreateChar :data="i.data" v-if="i.body == 'create'"></CreateChar>
            <Time :data="i.data" v-if="i.body == 'time'"></Time>
            <Bag :data="i.data" v-if="i.body == 'bag'"></Bag>
            <Study :data="i.data" v-if="i.body == 'study'"></Study>
            <StudyProcess :data="i.data" v-if="i.body == 'process'"></StudyProcess>
            <BagItem :data="i.data" v-if="i.body == 'bag_item'"></BagItem>
            <Knowledge :data="i.data" v-if="i.body == 'knowledge'"></Knowledge>

            <Item :data="i.data" v-if="i.body == 'item'"></Item>
            <Book :data="i.data" v-if="i.body == 'book'"></Book>
            <Shop :data="i.data" v-if="i.body == 'shop'"></Shop>
            <Seed :data="i.data" v-if="i.body == 'seed'"></Seed>
            <Menu :data="i.data" v-if="i.body == 'menu'"></Menu>
            <Pet :data="i.data" v-if="i.body == 'pet'"></Pet>
            <Create :data="i.data" v-if="i.body == 'create_item'"></Create>

            <MyClan :data="i.data" v-if="i.body == 'clan'"></MyClan>
            <ClanList :data="i.data" v-if="i.body == 'clan_list'"></ClanList>
            <ClanDetail :data="i.data" v-if="i.body == 'clan_detail'"></ClanDetail>
            <ClanMember :data="i.data" v-if="i.body == 'member_clan'"></ClanMember>
            <ClanRequest :data="i.data" v-if="i.body == 'request_clan'"></ClanRequest>
            <ClanDedication :data="i.data" v-if="i.body == 'dedication'"></ClanDedication>
            <ClanLibrary :data="i.data" v-if="i.body == 'library'"></ClanLibrary>

            <CityList :data="i.data" v-if="i.body == 'city'"></CityList>
            <CityDetail :data="i.data" v-if="i.body == 'city_detail'"></CityDetail>
            <CitySell :data="i.data" v-if="i.body == 'sell'"></CitySell>
            <Restore :data="i.data" v-if="i.body == 'restore'"></Restore>

            <Location :data="i.data" v-if="i.body == 'location'"></Location>
            <Tower :data="i.data" v-if="i.body == 'tower'"></Tower>
            <Rank :data="i.data" v-if="i.body == 'rank'"></Rank>
            <Question :data="i.data" v-if="i.body == 'question'"></Question>
            <Fishing :data="i.data" v-if="i.body == 'fishing'"></Fishing>
            <Hunt :data="i.data" v-if="i.body == 'hunt'"></Hunt>
            <ShopPet :data="i.data" v-if="i.body == 'pet_shop'"></ShopPet>

            <Job :data="i.data" v-if="i.body == 'job'"></Job>
            <House :data="i.data" v-if="i.body == 'house'"></House>
            <Gardent :data="i.data" v-if="i.body == 'gardent'"></Gardent>
            <Cage :data="i.data" v-if="i.body == 'cage'"></Cage>
            <Lake :data="i.data" v-if="i.body == 'lake'"></Lake>
            <Oven :data="i.data" v-if="i.body == 'oven'"></Oven>
            <StoreHouse :data="i.data" v-if="i.body == 'store'"></StoreHouse>
            <ShopHouse :data="i.data" v-if="i.body == 'shop_house'"></ShopHouse>

        </template>
    </Card>
</template>

<style></style>