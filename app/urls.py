from django.urls import path
from . views import *

urlpatterns = [
    path('add/', UserView.as_view()), # user qo'shish
    path('get/', GetDataView.as_view()), # user ma'lumotlarini telegramdan yuborish
    path('', home),
    path('del/', DeleteUser.as_view()), # foydalanuvchini o'chirish
    path('new/', NewCompany.as_view()), # Yangi Kompaniya qo'shish
    path('keldi/', UserJoin.as_view()), # User keldi
    path('ketdi/', UserLeft.as_view()), # User ketdi
    path('newtoken/', NewToken.as_view()), # tokenni o'zgartirish
    path('newkanal/', NewChannel.as_view()), # Kanal qo'shish
    path('alluser/', GetAllUserList.as_view()), # Barcha userlar ro'yxatini olish
]
