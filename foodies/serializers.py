from rest_framework import serializers
from.models import Registration,Login,Fooditems,Foodcategory,Review,Cart,Wishlist,Placeorder,Address,Special_offer

class RegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model=Registration
    fields='__all__'

class LoginSerializer(serializers.ModelSerializer):
  class Meta:
    model=Login
    fields='__all__'

class FooditemsSerializer(serializers.ModelSerializer):
  class Meta:
    model=Fooditems
    fields='__all__'

class FoodcategorySerializer(serializers.ModelSerializer):
  class Meta:
    model=Foodcategory
    fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model=Review
    fields='__all__'

class CartSerializer(serializers.ModelSerializer):
  class Meta:
    model=Cart
    fields='__all__'

class WishlistSerializer(serializers.ModelSerializer):
  class Meta:
    model=Wishlist
    fields='__all__'

class PlaceorderSerializer(serializers.ModelSerializer):
  class Meta:
    model=Placeorder
    fields='__all__'

class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model=Address
    fields='__all__'

class SpecialofferSerializer(serializers.ModelSerializer):
  class Meta:
    model=Special_offer
    fields='__all__'