from django.urls import path
from . import views
app_name = 'core'

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('news/', views.NewsView, name='news'),
    path('districts/', views.DistrictsView, name='districts'),
    path('district/<int:id>/maps/', views.MapsView, name='maps'),
    path('contact/', views.ContactView, name='contact'),
    path('about/', views.AboutView, name='about'),
    path('agents/', views.AgentsView, name='agents'),
    path('properties/', views.PropertiesView, name='properties'),
    path('property/<int:id>/', views.PropertyView, name='property'),


    path('user-profile/', views.UserProfileView, name='userprofile'),
    path('my-properties/', views.myProperties, name='myproperties'),
    path('hide-property/<int:id>/', views.hideProperty, name='hideproperty'),
    path('show-property/<int:id>/', views.showProperty, name='showproperty'),

    path('my-bookmarks/', views.BookmarkView, name='bookmarks'),
    path('add-to-bookmarks/<int:id>/', views.add_to_bookmark, name='addtobookmarks'),
    path('remove-from-bookmarks/<int:id>/', views.remove_from_bookmark, name='removefrombookmarks'),

    path('addproperty/', views.addProperty, name='addproperty'),
    path('editproperty/<int:id>/', views.editProperty, name='editproperty'),
    path('deleteproperty/<int:id>/', views.deleteProperty, name='deleteproperty'),

    path('compare-properties/', views.ComparisonView, name='compare'),
    path('add-to-compare/<int:id>/', views.add_to_compare, name='addtocompare'),
    path('remove-from-compare/<int:id>/', views.remove_from_compare, name='removefromcompare'),
]