from django.urls import path
from main.views import show_main, create_products, show_products, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_products, delete_products

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-products/', create_products ,name='create_products'),
    path('products/<str:id>/', show_products, name='show_products'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:products_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:products_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('products/<uuid:id>/edit/', edit_products, name='edit_products'),
    path('products/<uuid:id>/delete/', delete_products, name='delete_products'),
]