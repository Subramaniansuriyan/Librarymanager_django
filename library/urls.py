from django.urls import path
from .import views

urlpatterns=[
    path('sign_in',views.sign_in,name='sign_in'),
    path('create',views.add_member,name='add_member'),
    path('all',views.list_member,name='list_member'),
    path('update',views.edit_member,name='edit_member'),
    path('delete/<int:id>',views.delete_member,name='delete_member'),
    path('add_book',views.add_book,name='add_book'),
    path('all_books',views.list_book,name='list_book'),
    path('search',views.search,name='search'),
    path('edit_book/<int:id>',views.edit_book,name='edit_book'),
    path('get_book/<int:id>',views.get_book,name='get_book'),
    path('delete_book/<int:id>',views.delete_book,name='delete_book'),
    path('lend_book',views.lend_book,name='lend_book'),
    path('category_list',views.category_list,name='category_list')
]