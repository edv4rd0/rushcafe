from django.contrib.auth import views as auth_views
from django.urls import path

from rushcafe import views
from rushcafe.forms import RushCafeAuthForm


handler404 = 'rushcafe.views.handler404'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='login.html',
             redirect_field_name='index',
             authentication_form=RushCafeAuthForm
         ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menucategories/', views.menu_categories, name='menu-categories'),
    path('menucategories/new/',
         views.new_menu_category, name='menu-category-add'),
    path('menucategories/<int:pk>/',
         views.menu_category, name='menu-category-view'),
    path('menucategories/<int:pk>/edit/',
         views.MenuCategoryView.as_view(), name='menu-category'),
    path('menucategories/<int:pk>/delete/',
         views.delete_menu_category, name='menu-category-delete'),
    path('menuitems/', views.menu_items, name='menu-items'),
    path('menuitems/new/', views.new_menu_item, name='menu-item-add'),
    path('menuitems/<int:pk>/',
         views.MenuItemView.as_view(), name='menu-item'),
    path('menuitems/<int:pk>/delete',
         views.delete_menu_item, name='menu-item-delete'),
    path('webhook',
         views.webhook, name='webhook')
]
