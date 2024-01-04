from django.urls import path

from app_user.views import (
    RegisterUser, LoginView, LogoutView,
    CharactersView, getCurrChar,
    getGiftedList, getGiftedDetail,
    getBag,
    MoneyView,
    EquippedView,
    useItem, buyItem, sellItem,
    KnowledgeView,
    LevelUpView,
    buyBook, sellBook, studyBook, getStudy,
    getRank,
    RelationshipView,
    restore
)
from app_item.views import (
    ItemView, ItemDetailView, getRandomItem,
    addItemtoBag, removeItemfromBag, removeBookfromBag,
    getMenu, createItem,
    getBook, getBookDetail
)
from app_clan.views import (
    ClanView, ClanDetailView, outClan,
    RequestClanView, acceptRequest, rejectRequest,
    DedicationView,
    upClan, upPosition,
    ClanShopView,
    OnlineClanView
)
from app_job.views import (
    getSeed, getSeedDetail,
    StoreHouseView,
    GardentView, upgrateGardent,
    GardentSlotView, upgradeSlot, getNextSlotPrice,
    HarvestSeedView,
    HouseView,
    getMines, getResultMines,
    Meditation,
    getCurTime
)
from app_location.views import (
    CityView, getCityDetail,
    OnlineCityView,
    TowerView, getTowerDetail,
    TowerChallengeView, ChallengeBoardView, getNearRankinBoard,
    FightResult
)

urlpatterns = [
    path('register', RegisterUser.as_view(), name="RegisterUser"),
    path('login', LoginView.as_view(), name="LoginView"),
    path('logout', LogoutView.as_view(), name="LogoutView"),
    
    path('characters', CharactersView.as_view(), name="CharactersView"),
    path('characters/<str:id>', CharactersView.as_view(), name="CharactersView-detail"),
    path('character/current', getCurrChar, name="getCurrChar"),

    path('gifted', getGiftedList, name="getGiftedList"),
    path('gifted/<str:id>', getGiftedDetail, name="getGiftedDetail"),

    path('bag', getBag, name="getBag"),
    path('money', MoneyView.as_view(), name="getMoney"),
    path('level-up', LevelUpView, name="LevelUpView"),
    path('meditation', Meditation, name="Meditation"),
    path('cur-time', getCurTime, name="getCurTime"),
    path('rank', getRank, name="getRank"),
    path('relationship', RelationshipView.as_view(), name="RelationshipView"),
    path('restore', restore, name="restore"),

    path('items', ItemView.as_view(), name="ItemView"),
    path('items/<str:id>', ItemDetailView, name="ItemDetailView"),
    path('items/random', getRandomItem, name="getRandomItem"),
    path('items/got/<str:id>', addItemtoBag, name="addItemtoBag"),
    path('items/remove/<str:id>', removeItemfromBag, name="removeItemfromBag"),
    path('items/use/<str:id>', useItem, name="useItem"),
    path('items/buy/<str:id>', buyItem, name="buyItem"),
    path('items/sell/<str:id>', sellItem, name="sellItem"),

    path('book', getBook, name="getBook"),
    path('book/<str:id>', getBookDetail, name="getBookDetail"),
    path('book/buy/<str:id>', buyBook, name="buyBook"),
    path('book/sell/<str:id>', sellBook, name="sellBook"),
    path('book/remove/<str:id>', removeBookfromBag, name="removeBookfromBag"),
    path('study', getStudy, name="getStudy"),
    path('book/study/<str:id>', studyBook, name="studyBook"),

    path('equipped', EquippedView.as_view(), name="EquippedView"),

    path('clan', ClanView.as_view(), name="ClanView"),
    path('clan/<str:id>', ClanDetailView.as_view(), name="ClanDetailView"),
    path('clan/<str:id>/out', outClan, name="outClan"),
    path('clan/<str:id>/request', RequestClanView.as_view(), name="RequestClanView"),
    path('clan-request/<str:id>/accept', acceptRequest, name="acceptRequest"),
    path('clan-request/<str:id>/reject', rejectRequest, name="rejectRequest"),
    path('clan/<str:id>/dedication', DedicationView, name="DedicationView"),
    path('clan/<str:id>/up-level', upClan, name="upClan"),
    path('clan/<str:id>/up-positon', upPosition, name="upPosition"),
    path('clan/<str:id>/shop', ClanShopView.as_view(), name="ClanShopView"),
    path('clan/<str:id>/online', OnlineClanView.as_view(), name="OnlineClanView"),

    path('menu/<str:id>', getMenu, name="getMenu"),
    path('knowledge', KnowledgeView.as_view(), name="KnowledgeView"),
    path('create', createItem, name="createItem"),
    
    path('seeds', getSeed, name="getSeed"),
    path('seeds/<str:id>', getSeedDetail, name="getSeedDetail"),
    path('storehouse', StoreHouseView.as_view(), name="StoreHouseView"),
    path('gardent', GardentView.as_view(), name="GardentView"),
    path('gardent/upgrate', upgrateGardent, name="upgrateGardent"),
    path('gardent/slot', GardentSlotView.as_view(), name="GardentSlotView"),
    path('gardent/slot/<str:id>/upgrate', upgradeSlot, name="upgradeSlot"),
    path('gardent/slot/next', getNextSlotPrice, name="getNextSlotPrice"),
    path('gardent/slot/<str:id>/seed', HarvestSeedView.as_view(), name="HarvestSeedView"),
    path('house', HouseView.as_view(), name="HouseView"),
    path('mines', getMines, name="getMines"),
    path('mines/got', getResultMines, name="getResultMines"),
    
    path('city', CityView.as_view(), name="CityView"),
    path('city/<str:id>', getCityDetail, name="getCityDetail"),
    path('city/<str:id>/online', OnlineCityView.as_view(), name="OnlineCityView"),

    path('tower', TowerView.as_view(), name="TowerView"),
    path('tower/<str:id>', getTowerDetail, name="getTowerDetail"),
    path('tower/<str:id>/challenge', TowerChallengeView.as_view(), name="TowerChallengeView"),

    path('board/<str:id>/challenge', ChallengeBoardView.as_view(), name="ChallengeBoardView"),
    path('board/<str:id>/suggest', getNearRankinBoard, name="getNearRankinBoard"),

    path('fight', FightResult, name="FightResult"),
    
]
