from .import views
from django.urls import path
urlpatterns=[
  path('registration/',views.registration_api.as_view(),name='registration'),
  path('login/',views.login_api.as_view(),name='Login'),
  path('view_user/',views.viewuser_api.as_view(),name='view all users'),
  path('view_singleuser/<int:id>',views.single_user_api.as_view(),name='singleusers'),
  path('deltesingleusers/<int:id>',views.delete_single_user_api.as_view(),name='deletesingleusers'),
  path('updatuser/<int:id>',views.update_user_api.as_view(),name='updateuser'),
  path('food_items/', views.food_items_api.as_view(), name='food_items'),
  path('view_food_items/', views.view_item_api.as_view(), name='view food_items'),
  path('view_single_food_items/<int:id>', views.view_single_item_api.as_view(), name='view single food_items'),
  path('update_item/<int:id>',views.update_items_api.as_view(), name='updateproduct'),
  path('deleteproduct/<int:id>',views.delete_item_api.as_view(), name='deleteproduct'),
  path('item_category/',views.food_category_api.as_view(), name='item_category'),
  path('view_item_category/',views.view_category_api.as_view(), name='view item_category'),
  path('items/category/<int:itemcategory_id>/', views.ViewItemByCategoryAPI.as_view(), name='items_by_category'),
  path('delete/category/<int:itemcategory_id>/',views.delete_single_category_api.as_view(), name='delete-category'),

  path('item_review/',views.review_item_api.as_view(),name='reviews'),
  path('viewsinglereview/<int:id>',views.view_singlereview_api.as_view(),name='viewsinglereview'),
  path('updatesinglereview/<int:id>',views.update_single_review_api.as_view(),name='deletelereview'),
  path('deletesinglereview/<int:id>',views.delete_single_review_api.as_view(),name='deletelereview'),
  path('addcart/',views.addto_cart_api.as_view(),name='addtocart'),
  path('viewcart/',views.view_cart_api.as_view(),name='viewtocart'),
  path('deletecart/<int:id>',views.delete_cart_api.as_view(),name='deletecart'),
  path('viewsinglecart/<int:userid>',views.view_singlecart_api.as_view(),name='viewsinglecart'),
  path('wishlist/',views.wishlist_api.as_view(),name='wishlist'),
  path('placeorder/<int:userid>',views.placeorder_api.as_view(),name='placeOrder'),
  path('vieworder/<int:userid>',views.view_orders_api.as_view(),name='viewplaceOrder'),
  path('addaddress/',views.Addadress_api.as_view(),name='addaddress'),
  path('viewalladdress/',views.viewalladdress_api.as_view(),name='viewalladdress'),
  path('updateaddress/<int:userid>/',views.UpdateAddress_api.as_view(), name='update-address'),
  path('deleteaddress/<int:userid>/',views.DeleteAddress_api.as_view(), name='delete-address'),
  path('changepassword/<int:id>',views.change_pass_api.as_view(), name='changepassword'),
  path('search/',views.search_api.as_view(), name='search'),
  path('wishlist/view/<int:userid>/',views.ViewWishlistAPI.as_view(), name='view_wishlist'), 
  path('add_offer/', views.add_offer_api.as_view(), name='add offers'),
  path('view_offers_items/', views.view_offers_api.as_view(), name='view offers'),
  path('update_offers/<int:id>',views.update_offers_api.as_view(), name='updateoffers'),
  path('deleteoffer/<int:id>',views.delete_offers_api.as_view(), name='deleteoffer'),
  path('add_special/', views.add_special_api.as_view(), name='add offers'),
  path('increment_quantity/',views.IncrementQuantityAPI.as_view(), name='increment_quantity'),
  path('decrement_quantity/',views.DecrementQuantityAPI.as_view(), name='decrement_quantity'),




]

  




















