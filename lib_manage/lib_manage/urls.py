"""lib_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from basic_func.views import card, book, admin, account

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('', book.book_list),

    # 登录管理
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/edit/', admin.admin_edit),

    # 借书证的管理
    path('card/list/', card.card_list),
    path('card/add/', card.card_add),
    path('card/<int:nid>/delete/', card.card_delete),
    path('card/<int:nid>/edit/', card.card_edit),
    # path('card/<int:nid>/record_query/', card.record_query),
    path('card/record_query/', card.record_query),
    path('card/<int:nid>/record_expand/', card.record_expand),
    path('card/<int:nid>/record_return/', card.record_return),
    path('card/<int:nid>/record_delete/', card.record_delete),

    # 图书管理
    path('book/list/', book.book_list),
    path('book/add/', book.book_add),
    path('book/book_random_create/', book.book_random_create),
    path('book/book_create_from_excel/', book.book_create_from_excel),
    path('book/book_delete_all/', book.book_delete_all),
    path('book/<int:nid>/delete/', book.book_delete),
    path('book/<int:nid>/edit/', book.book_edit),

    # 借还书
    path('book/<int:nid>/borrow/', book.book_borrow),
    path('book/<int:nid>/return/', book.book_return),

]
