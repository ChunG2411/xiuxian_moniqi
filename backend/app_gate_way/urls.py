from django.urls import path

from app_user.views import (
    RegisterUser, LoginView, LogoutView,
    CharactersView, getCurrChar, getBag, MoneyView, EquippedView, LevelUpView,
    useItem, buyItem, sellItem,
    KnowledgeView,
    buyBook, sellBook, StudyView, StudyProcessView, StudyProcessDetailView,
    getRank, restore,
    OwnPetView,
    ChatView, ChatDetailView
)
from app_item.views import (
    ItemView, ItemDetailView, getRandomItem,
    addItemtoBag, removeItemfromBag, removeBookfromBag, addBooktoBag,
    MenuView, MenuDetailView, createItem,
    BookView, BookDetailView, getRandomBook,
    PetView, PetDetailView
)
from app_clan.views import (
    ClanView, ClanDetailView, outClan, MemberClanView,
    RequestClanView, acceptRequest, rejectRequest,
    DedicationView, upClan, upPosition_Clan,
    ClanShopView
)
from app_organization.views import (
    OrganizationView, OrganizationDetailView,
    joinOrganization, outOrganization,
    LocalityView, LocalityDetailView,
    MineView, MarketView,
    attackMine, attackMarket, attackLocality,
    MailView, MailDetailView
)
from app_job.views import (
    HouseView, StoreView, OvenView,
    SeedView, SeedDetailView,
    GardentView, upgrateGardent, GardentSlotView, HarvestSeedView,
    CageView, upgrateCage, CageSlotView, SlaughterSeedView,
    LakeView, upgrateLake, LakeSlotView, FishingSeedView,
    Meditation,
    getCurTime
)
from app_location.views import (
    CityView, CityDetailView, CityShopView,
    TowerView,
    FightResult, GameResult,
    QuestionView, QuestionCharView,
    ArenaView, ArenaDetailView
)


urlpatterns = [
    path('register', RegisterUser.as_view(), name="RegisterUser"),
    path('login', LoginView.as_view(), name="LoginView"),
    path('logout', LogoutView.as_view(), name="LogoutView"),
    
    path('characters', CharactersView.as_view(), name="CharactersView"),
    path('characters/<str:id>', CharactersView.as_view(), name="CharactersView-detail"),
    path('character/current', getCurrChar, name="getCurrChar"),
    path('cur-time', getCurTime, name="getCurTime"),

    path('bag', getBag, name="getBag"),
    path('money', MoneyView.as_view(), name="getMoney"),
    path('level-up', LevelUpView, name="LevelUpView"),
    path('meditation', Meditation, name="Meditation"),
    path('rank', getRank, name="getRank"),
    path('restore', restore, name="restore"),
    path('chat', ChatView.as_view(), name="ChatView"),
    path('chat/<str:id>', ChatDetailView.as_view(), name="ChatDetailView"),

    path('items', ItemView.as_view(), name="ItemView"),
    path('items/<str:id>', ItemDetailView.as_view(), name="ItemDetailView"),
    path('item/random', getRandomItem, name="getRandomItem"),
    path('items/got/<str:id>', addItemtoBag, name="addItemtoBag"),
    path('items/remove/<str:id>', removeItemfromBag, name="removeItemfromBag"),
    path('items/use/<str:id>', useItem, name="useItem"),
    path('items/buy/<str:id>', buyItem, name="buyItem"),
    path('items/sell/<str:id>', sellItem, name="sellItem"),

    path('books', BookView.as_view(), name="BookView"),
    path('books/<str:id>', BookDetailView.as_view(), name="BookDetailView"),
    path('book/random', getRandomBook, name="getRandomBook"),
    path('books/buy/<str:id>', buyBook, name="buyBook"),
    path('books/sell/<str:id>', sellBook, name="sellBook"),
    path('books/got/<str:id>', addBooktoBag, name="addBooktoBag"),
    path('books/remove/<str:id>', removeBookfromBag, name="removeBookfromBag"),

    path('study', StudyView.as_view(), name="StudyView"),
    path('study/process', StudyProcessView.as_view(), name="StudyProcessView"),
    path('study/process/<str:id>', StudyProcessDetailView.as_view(), name="StudyProcessDetailView"),

    path('equipped', EquippedView.as_view(), name="EquippedView"),

    path('pets', PetView.as_view(), name="PetView"),
    path('pets/own', OwnPetView.as_view(), name="OwnPetView"),
    path('pet/<str:id>', PetDetailView.as_view(), name="PetDetailView"),

    path('clan', ClanView.as_view(), name="ClanView"),
    path('clan/<str:id>', ClanDetailView.as_view(), name="ClanDetailView"),
    path('clan/<str:id>/member', MemberClanView.as_view(), name="MemberClanView"),
    path('clan/<str:id>/out', outClan, name="outClan"),
    path('clan/<str:id>/request', RequestClanView.as_view(), name="RequestClanView"),
    path('clan-request/<str:id>/accept', acceptRequest, name="acceptRequest"),
    path('clan-request/<str:id>/reject', rejectRequest, name="rejectRequest"),
    path('clan/<str:id>/dedication', DedicationView, name="DedicationView"),
    path('clan/<str:id>/up-level', upClan, name="upClan"),
    path('clan/<str:id>/up-positon', upPosition_Clan, name="upPosition"),
    path('clan/<str:id>/shop', ClanShopView.as_view(), name="ClanShopView"),

    path('organization', OrganizationView.as_view(), name="OrganizationView"),
    path('organization/<str:id>', OrganizationDetailView.as_view(), name="OrganizationDetailView"),
    path('organization/<str:id>/join', joinOrganization, name="joinOrganization"),
    path('organization/<str:id>/out', outOrganization, name="outOrganization"),

    path('locality', LocalityView.as_view(), name="LocalityView"),
    path('locality/<str:id>', LocalityDetailView.as_view(), name="LocalityDetailView"),
    path('locality/<str:id>/attack', attackLocality, name="attackLocality"),
    path('mine', MineView.as_view(), name="MineView"),
    path('mine/<str:id>', MineView.as_view(), name="MineView"),
    path('mine/<str:id>/attack', attackMine, name="attackMine"),
    path('market', MarketView.as_view(), name="MarketView"),
    path('market/<str:id>', MarketView.as_view(), name="MarketView"),
    path('market/<str:id>/attack', attackMarket, name="attackMarket"),
    path('mail', MailView.as_view(), name="MailView"),
    path('mail/<str:id>', MailDetailView.as_view(), name="MailDetailView"),

    path('menu', MenuView.as_view(), name="MenuView"),
    path('menu/<str:id>', MenuDetailView.as_view(), name="MenuDetailView"),
    path('knowledge', KnowledgeView.as_view(), name="KnowledgeView"),
    path('create', createItem, name="createItem"),
    
    path('house', HouseView.as_view(), name="HouseView"),
    path('store/<str:id>', StoreView.as_view(), name="StoreView"),
    path('seeds', SeedView.as_view(), name="SeedView"),
    path('seeds/<str:id>', SeedDetailView.as_view(), name="SeedDetailView"),

    path('gardent', GardentView.as_view(), name="GardentView"),
    path('gardent/upgrate', upgrateGardent, name="upgrateGardent"),
    path('gardent/slot', GardentSlotView.as_view(), name="GardentSlotView"),
    path('gardent/slot/<str:id>/seed', HarvestSeedView.as_view(), name="HarvestSeedView"),

    path('cage', CageView.as_view(), name="CageView"),
    path('cage/upgrate', upgrateCage, name="upgrateCage"),
    path('cage/slot', CageSlotView.as_view(), name="CageSlotView"),
    path('cage/slot/<str:id>/seed', SlaughterSeedView.as_view(), name="SlaughterSeedView"),

    path('lake', LakeView.as_view(), name="LakeView"),
    path('lake/upgrate', upgrateLake, name="upgrateLake"),
    path('lake/slot', LakeSlotView.as_view(), name="LakeSlotView"),
    path('lake/slot/<str:id>/seed', FishingSeedView.as_view(), name="FishingSeedView"),
    
    path('oven', OvenView.as_view(), name="OvenView"),

    path('city', CityView.as_view(), name="CityView"),
    path('city/<str:id>', CityDetailView.as_view(), name="CityDetailView"),
    path('city/<str:id>/shop', CityShopView.as_view(), name="CityShopView"),

    path('tower', TowerView.as_view(), name="TowerView"),
    path('fight', FightResult, name="FightResult"),
    path('game', GameResult, name="GameResult"),
    path('question', QuestionView.as_view(), name="QuestionView"),
    path('question/current', QuestionCharView.as_view(), name="QuestionCharView"),
    path('arena', ArenaView.as_view(), name="ArenaView"),
    path('arena/<str:id>', ArenaDetailView.as_view(), name="ArenaDetailView"),

]
