from django.urls import path
from . import views


app_name="shakawi"


urlpatterns = [
    path('', views.home, name='login_page'),
    path('main',views.shakawi_user , name='main'),
    path('logout', views.home, name='logout'),
    path('new_shab_fit/<int:page_id>', views.new_shab, name='new_shab_fit'),
    path('new_shab_ability/<int:page_id>', views.new_shab, name='new_shab_ability'),
    path('new_shab_ten_percent/<int:page_id>', views.new_shab, name='new_shab_ten'),
    path('new_shab_unfit/<int:page_id>', views.new_shab, name='new_shab_unfit'),
    path('search_single', views.search_single, name='search_single'),
    path('search_reports', views.print_reports, name='search_reports'),
    path('denied',views.denied , name='denied'),
    path('md-nt',views.data , name='md-nt'),


]
