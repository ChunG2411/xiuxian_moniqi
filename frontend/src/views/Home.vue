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
import ClanModify from '../components/clan/ClanModify.vue'

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
import Casino from '../components/location/Casino.vue'
import ShopPet from '../components/location/Shop.vue'

import Job from '../components/job/Job.vue'
import House from '../components/job/House.vue'
import Gardent from '../components/job/Gardent.vue'
import Cage from '../components/job/Cage.vue'
import Lake from '../components/job/Lake.vue'
import Oven from '../components/job/Oven.vue'
import StoreHouse from '../components/job/Store.vue'
import ShopHouse from '../components/job/Shop.vue'

import MyOrgan from '../components/organization/MyOrgan.vue'
import OrganList from '../components/organization/OrganList.vue'
import OrganDetail from '../components/organization/OrganDetail.vue'
import OrganMember from '../components/organization/OrganMember.vue'

import MyLocality from '../components/locality/MyLocality.vue'
import LocalityDetail from '../components/locality/LocalityDetail.vue'
import LocalityModify from '../components/locality/LocalityModify.vue'
import LocalityRestore from '../components/locality/LocalityRestore.vue'
import LocalityRange from '../components/locality/LocalityRange.vue'
import LocalityOwner from '../components/locality/LocalityOwner.vue'
import LocalityMail from '../components/locality/LocalityMail.vue'
import MailDetail from '../components/locality/MailDetail.vue'
import MailSend from '../components/locality/MailSend.vue'

import MineDetail from '../components/mine/MineDetail.vue'
import MarketDetail from '../components/mine/MarketDetail.vue'

import Chat from '../components/chat/Chat.vue'
import ChatDetail from '../components/chat/ChatDetail.vue'
import ChatSend from '../components/chat/ChatSend.vue'

import Arena from '../components/location/Arena.vue'


const store = Store()

// addCard('mychar')

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
            <ClanModify :data="i.data" v-if="i.body == 'clan_modify'"></ClanModify>

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
            <Casino :data="i.data" v-if="i.body == 'casino'"></Casino>
            <ShopPet :data="i.data" v-if="i.body == 'pet_shop'"></ShopPet>

            <Job :data="i.data" v-if="i.body == 'job'"></Job>
            <House :data="i.data" v-if="i.body == 'house'"></House>
            <Gardent :data="i.data" v-if="i.body == 'gardent'"></Gardent>
            <Cage :data="i.data" v-if="i.body == 'cage'"></Cage>
            <Lake :data="i.data" v-if="i.body == 'lake'"></Lake>
            <Oven :data="i.data" v-if="i.body == 'oven'"></Oven>
            <StoreHouse :data="i.data" v-if="i.body == 'store'"></StoreHouse>
            <ShopHouse :data="i.data" v-if="i.body == 'shop_house'"></ShopHouse>

            <MyOrgan :data="i.data" v-if="i.body == 'organization'"></MyOrgan>
            <OrganList :data="i.data" v-if="i.body == 'organ_list'"></OrganList>
            <OrganDetail :data="i.data" v-if="i.body == 'organ_detail'"></OrganDetail>
            <OrganMember :data="i.data" v-if="i.body == 'member_organ'"></OrganMember>

            <MyLocality :data="i.data" v-if="i.body == 'locality'"></MyLocality>
            <LocalityDetail :data="i.data" v-if="i.body == 'locality_detail'"></LocalityDetail>
            <LocalityModify :data="i.data" v-if="i.body == 'locality_modify'"></LocalityModify>
            <LocalityRestore :data="i.data" v-if="i.body == 'locality_restore'"></LocalityRestore>
            <LocalityRange :data="i.data" v-if="i.body == 'locality_range'"></LocalityRange>
            <LocalityOwner :data="i.data" v-if="i.body == 'locality_owner'"></LocalityOwner>
            <LocalityMail :data="i.data" v-if="i.body == 'locality_mail'"></LocalityMail>
            <MailDetail :data="i.data" v-if="i.body == 'mail_detail'"></MailDetail>
            <MailSend :data="i.data" v-if="i.body == 'mail_send'"></MailSend>

            <MineDetail :data="i.data" v-if="i.body == 'mine_detail'"></MineDetail>
            <MarketDetail :data="i.data" v-if="i.body == 'market_detail'"></MarketDetail>

            <Chat :data="i.data" v-if="i.body == 'chat'"></Chat>
            <ChatDetail :data="i.data" v-if="i.body == 'chat_detail'"></ChatDetail>
            <ChatSend :data="i.data" v-if="i.body == 'chat_send'"></ChatSend>

            <Arena :data="i.data" v-if="i.body == 'arena'"></Arena>

        </template>
    </Card>
</template>

<style></style>