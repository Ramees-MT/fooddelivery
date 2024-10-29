from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegistrationSerializer,LoginSerializer,FooditemsSerializer,FoodcategorySerializer,ReviewSerializer,CartSerializer,WishlistSerializer,PlaceorderSerializer,AddressSerializer,SpecialofferSerializer
from .models import Registration,Login,Fooditems,Foodcategory,Review,Cart,Wishlist,Placeorder,Address,Special_offer
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Q
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api



from . import models

# Create your views here.
class registration_api(GenericAPIView):
  serializer_class=RegistrationSerializer
  serializer_class_login=LoginSerializer
  def post(self,request):
   username=  request.data.get('username')
   email=  request.data.get('email')
   password=  request.data.get('password')
   login_id=request.data.get('login_id')
   phone=  request.data.get('phone')
   role='user'

   if Registration.objects.filter(email=email).exists():
      return Response({'message':'Duplicate email found!'},status=status.HTTP_400_BAD_REQUEST)
   if Registration.objects.filter(phone=phone).exists():
      return Response({'message':'Duplicate number found!'},status=status.HTTP_400_BAD_REQUEST)
   login_data={'email':email,'password':password,'role':role}
   serializer_login=self.serializer_class_login(data=login_data)
   if serializer_login.is_valid():
      log=serializer_login.save()
      login_id=log.id
   else:
      return Response({'message':'Login creation failed!','errors':serializer_login.errors},status=status.HTTP_400_BAD_REQUEST)
   
   registration_data={
'username':username,
'email':email,
'password':password,
'phone':phone,
'login_id':login_id,
'role':role



   }
   serializer=self.serializer_class(data=registration_data)
   if serializer.is_valid():
      serializer.save()
      return Response({'data':serializer.data,'message':'Registration successfull','success':1,},status=status.HTTP_200_OK)
   return Response({'data':serializer.errors,'message':'Registration Failed','success':1,},status=status.HTTP_400_BAD_REQUEST)
  

class login_api(GenericAPIView):
  serializer_class=LoginSerializer
  def post(self,request):
    email= request.data.get('email')
    password= request.data.get('password')
    log_var=Login.objects.filter(email=email,password=password)
    if log_var.count()>0:
      a=LoginSerializer(log_var,many=True)
      for i in a.data:
        login_id=i['id']
        role=i['role']
        register_data=Registration.objects.filter(login_id=login_id).values()
        print(register_data)
        for i in register_data:
          id=i['id']
          username=i['username']
          phone=i['phone']
      return Response({'data':{'login_id':login_id,'user_id':id,'email':email,'password':password,'username':username,'role':role,'phone':phone,'message':'Login successfull','success':1,}},status=status.HTTP_200_OK)
    else:

      return Response({'data':'invalid username or password'},status=status.HTTP_400_BAD_REQUEST)
  
class viewuser_api(GenericAPIView):
  serializer_class=RegistrationSerializer
  def get(self,request):
    user=Registration.objects.all()
    if user.count()>0:
      serializer=RegistrationSerializer(user,many=True)
      return Response({'data':serializer.data,'message':'Data get','success':True},status=status.HTTP_200_OK)
    else:
      return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
    

class single_user_api(GenericAPIView):
  def get(self,request,id):
    result=Registration.objects.get(pk=id)
    serializer=RegistrationSerializer(result)
    return Response(serializer.data)
  
class delete_single_user_api(GenericAPIView):
  def delete(self,request,id):
    result=Registration.objects.get(pk=id)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
  

class update_user_api(GenericAPIView):
 
    serializer_class=RegistrationSerializer
    def put(self,request,id):
      result=Registration.objects.get(pk=id)
      serializer=RegistrationSerializer(instance = result,data=request.data,partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully'},status=status.HTTP_200_OK)
      else:
        return Response({'data':'not uodated'})
      

# class food_items_api(GenericAPIView):
#   serializer_class=FooditemsSerializer
#   def post(self,request):
#     itemname=request.data.get('itemname')
#     itemprice=request.data.get('itemprice')
#     itemdescription=request.data.get('itemdescription')
#     itemimage=request.data.get('itemimage')
#     itemcategory=request.data.get('itemcategory')

#     serializer=self.serializer_class(data={'itemname':itemname,'itemprice':itemprice,'itemdescription':itemdescription,'itemimage':itemimage,'itemcategory':itemcategory})

#     if serializer.is_valid():
#       serializer.save()
#       return Response({'data':serializer.data,'message':'product added successfully','succes':1},status=status.HTTP_200_OK)
   
#     return Response({'data':serializer.errors,'message':'failed','succes':0})


cloudinary.config(cloud_name ='dbhudbwpy',api_key='767256978968971',api_secret='UwjEUJ3JcyiTPP-kOgM_GK0O-yg' )

class food_items_api(GenericAPIView):
    serializer_class = FooditemsSerializer

    def post(self, request):
        itemname = request.data.get('itemname')
        itemprice = request.data.get('itemprice')
        itemdescription = request.data.get('itemdescription')
        itemimage = request.FILES.get('itemimage')
        itemcategory_id = request.data.get('itemcategory')

        if not itemimage:
            return Response({'message': 'Upload a valid image', 'error': True}, status=status.HTTP_400_BAD_REQUEST)

        try:
            upload_data = cloudinary.uploader.upload(itemimage)
            itemimage_url = upload_data['url'] 
            serializer = self.serializer_class(data={
            'itemname': itemname,
            'itemprice': itemprice,
            'itemdescription': itemdescription,
            'itemimage': itemimage_url, 
            'itemcategory': itemcategory_id
        })
            if serializer.is_valid():
                 serializer.save()
                 print(serializer)

                 return Response({'data': serializer.data, 'message': 'Product added successfully', 'success': 1}, status=status.HTTP_200_OK)

            return Response({'data': serializer.errors, 'message': 'Failed to add product', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as a:
            return Response({'data': {'itemcategory': 'Category not found'}, 'message': 'failed', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)
        


# class food_items_api(GenericAPIView):
#     serializer_class = FooditemsSerializer

#     def post(self, request):
#         itemname = request.data.get('itemname')
#         itemprice = request.data.get('itemprice')
#         itemdescription = request.data.get('itemdescription')
#         itemimage = request.FILES.get('itemimage')
#         itemcategory_id = request.data.get('itemcategory')  # Expected to be a category ID from the request

#         if not itemimage:
#             return Response({'message': 'Upload a valid image', 'error': True}, status=status.HTTP_400_BAD_REQUEST)

#         # Verify if the category exists
#         try:
#             category = models.Category.objects.get(id=itemcategory_id)
#         except models.Category.DoesNotExist:
#             return Response({'data': {'itemcategory': 'Category not found'}, 'message': 'Failed', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Upload image to Cloudinary
#             upload_data = cloudinary.uploader.upload(itemimage)
#             itemimage_url = upload_data['url']

#             # Prepare data for serializer
#             serializer_data = {
#                 'itemname': itemname,
#                 'itemprice': itemprice,
#                 'itemdescription': itemdescription,
#                 'itemimage': itemimage_url,
#                 'itemcategory': itemcategory_id  # Directly using itemcategory_id here
#             }

#             serializer = self.serializer_class(data=serializer_data)

#             if serializer.is_valid():
#                 # Save the food item and retrieve its data
#                 food_item = serializer.save()
#                 return Response({
#                     'data': {
#                         'id': food_item.id,
#                         'itemname': food_item.itemname,
#                         'itemprice': food_item.itemprice,
#                         'itemdescription': food_item.itemdescription,
#                         'itemimage': food_item.itemimage,
#                         'itemcategory': category.categoryname
#                     },
#                     'message': 'Product added successfully',
#                     'success': 1
#                 }, status=status.HTTP_201_CREATED)

#             return Response({'data': serializer.errors, 'message': 'Failed to add product', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return Response({'data': {'error': 'Unexpected error occurred'}, 'message': 'Failed', 'success': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

       
    

class view_item_api(GenericAPIView):
    serializer_class=FooditemsSerializer
    def get(self,request):
        user=Fooditems.objects.all()
        if (user.count()>0):
            serializer=FooditemsSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
    

class view_single_item_api(GenericAPIView):
  def get(self,request,id):
    result=Fooditems.objects.get(pk=id)
    serializer=FooditemsSerializer(result)
    return Response(serializer.data)
  
class delete_item_api(GenericAPIView):
  def delete(self,request,id):
    result=Fooditems.objects.get(pk=id)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
   

class update_items_api(GenericAPIView):
 
    serializer_class=FooditemsSerializer
    def put(self,request,id):
      result=Fooditems.objects.get(pk=id)
      serializer=FooditemsSerializer(instance = result,data=request.data,partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully'},status=status.HTTP_200_OK)
      else:
        return Response({'data':'not uodated'})
      
cloudinary.config(cloud_name ='dbhudbwpy',api_key='767256978968971',api_secret='UwjEUJ3JcyiTPP-kOgM_GK0O-yg' )



class food_category_api(GenericAPIView):
    serializer_class = FoodcategorySerializer

    def post(self, request):
        categoryname = request.data.get('categoryname')
        categoryimage = request.FILES.get('categoryimage')  # Correctly access FILES

        if not categoryimage:
            return Response({'message': 'Upload a valid image', 'error': True}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Upload the image to Cloudinary
            upload_data = cloudinary.uploader.upload(categoryimage)
            itemimage_url = upload_data['url']  # Get the URL of the uploaded image
            
            # Prepare data for the serializer
            serializer_data = {
                'categoryname': categoryname,
                'categoryimage': itemimage_url  # Use the uploaded image URL
            }

            serializer = self.serializer_class(data=serializer_data)
            if serializer.is_valid():
                serializer.save()  # Save the new category to the database
                return Response({'data': serializer.data, 'message': 'Product added successfully', 'success': 1}, 
                                status=status.HTTP_201_CREATED)
            
            return Response({'data': serializer.errors, 'message': 'Failed to save category', 'success': 0}, 
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e), 'error': True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
  

class view_category_api(GenericAPIView):
    serializer_class=FoodcategorySerializer
    def get(self,request):
        user=Foodcategory.objects.all()
        print(user)
        if (user.count()>0):
            serializer=FoodcategorySerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
    
   

class ViewItemByCategoryAPI(GenericAPIView):
    serializer_class = FooditemsSerializer

    def get(self, request, itemcategory_id=None):
        if itemcategory_id:
            food_items = Fooditems.objects.filter(itemcategory_id=itemcategory_id)
        else:
            food_items = Fooditems.objects.all()
        
        if food_items.exists():
            serializer = FooditemsSerializer(food_items, many=True)
            return Response({'data': serializer.data, 'message': 'data retrieved', 'success': True}, status=status.HTTP_200_OK)
        return Response({'data': 'No data available', 'message': 'No items found for the specified category', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
class delete_single_category_api(GenericAPIView):
  def delete(self,request,id):
    result=Foodcategory.objects.get(pk=id)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
  
  
   
   
class review_item_api(GenericAPIView):
  serializer_class=ReviewSerializer
  def post(self,request):
    itemname=""
    itemid=request.data.get('itemid')
    userid=request.data.get('userid')
    username=""
    itemdescription=request.data.get('itemdescription')

    product_data=Fooditems.objects.filter(id=itemid).values()
    for i in product_data:
      itemname=i['itemname']
      print(itemname)
    user_data=Registration.objects.filter(login_id=userid).values()
    for i in user_data:
      username=i['username']
      print(username)
    serializer=self.serializer_class(data={'itemid':itemid,'userid':userid,'itemname':itemname,'username':username,'itemdescription':itemdescription})
    print(serializer)
    if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'review add successfully','success':1},status=status.HTTP_200_OK)
    return Response({'data':serializer.errors,'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)

class view_singlereview_api(GenericAPIView):
  def get(self,request,id):
    result=Review.objects.get(pk=id)
    serializer=ReviewSerializer(result)
    return Response(serializer.data)
  
class delete_single_review_api(GenericAPIView):
  def delete(self,request,id):
    result=Review.objects.get(pk=id)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
  
class update_single_review_api(GenericAPIView):
 
    serializer_class=ReviewSerializer
    def put(self,request,id):
      result=Review.objects.get(pk=id)
      serializer=ReviewSerializer(instance = result,data=request.data,partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully'},status=status.HTTP_200_OK)
      else:
        return Response({'data':'not uodated'})
      
class addto_cart_api(GenericAPIView):
    serializer_class = CartSerializer

    def post(self, request):
        itemid = request.data.get('itemid')
        userid = request.data.get('userid')
        quantity = 1  
        cart = Cart.objects.filter(itemid=itemid, userid=userid)
        if cart.exists():
            return Response({'Message': 'Item already exists', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        itemdata = Fooditems.objects.filter(id=itemid).first()
        print(f"Product data fetched: {itemdata}")

        if not itemdata:
            return Response({'Message': 'Product not found', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        itemname = itemdata.itemname
        itemprice = itemdata.itemprice
        itemimage = itemdata.itemimage
        totalprice = quantity * itemprice  

        cart_status = 1  

        print(f"Total price: {totalprice}")

        serializer = self.serializer_class(
            data={
                'itemid': itemid,
                'userid': userid,
                'itemname': itemname,
                'quantity': quantity,
                'itemimage': itemimage,
                'itemprice': totalprice,
                'cart_status': cart_status  
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Added to cart', 'success': True}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
class view_cart_api(GenericAPIView):
   serializer_class=CartSerializer
   def get(self,request):
    cart=Cart.objects.all()
    if cart.count()>0:
      serializer=CartSerializer(cart,many=True)
      return Response({'data':serializer.data,'message':'Data get','success':True},status=status.HTTP_200_OK)
    else:
      return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
    

class delete_cart_api(GenericAPIView):
  def delete(self,request,id):
    result=Cart.objects.get(pk=id)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
  
class view_singlecart_api(GenericAPIView):
    def get(self, request, userid):
        carts = Cart.objects.filter(userid=userid)
        
        if carts.exists():
            serializer = CartSerializer(carts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No carts found for this user"}, status=status.HTTP_404_NOT_FOUND)
        

class wishlist_api(GenericAPIView):
     serializer_class = WishlistSerializer

     def post(self, request):
        itemid = request.data.get('itemid')
        userid = request.data.get('userid')

        wishlist = Wishlist.objects.filter(itemid=itemid, userid=userid)
        if wishlist.exists():
            wishlist.delete()
            return Response({'Message': 'Item already exists in wishlist', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

       
        itemdata = Fooditems.objects.filter(id=itemid).first()
        if not itemdata:
            return Response({'Message': 'Product not found', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        itemname = itemdata.itemname
        itemprice = itemdata.itemprice
        itemimage = itemdata.itemimage
        quantity = 1  
        wishliststatus = 1  

       
        serializer = self.serializer_class(
            data={
                'itemid': itemid,
                'userid': userid,
                'itemname': itemname,
                'quantity': quantity, 
                'itemimage': itemimage,
                'itemprice': itemprice,  
                'wishliststatus': wishliststatus
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Added to wishlist', 'success': True}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
     

class ViewWishlistAPI(GenericAPIView):
   serializer_class=WishlistSerializer


   def get(self,request,userid):
        wishlist_items=Wishlist.objects.filter(userid=userid,wishliststatus=1)

        if wishlist_items.exists():
           serializer=self.serializer_class(wishlist_items,many=True)
           return Response({'data': serializer.data, 'success': True}, status=status.HTTP_200_OK)
        return Response({'Message':'No items found','success':False},status=status.HTTP_400_BAD_REQUEST)



     
class placeorder_api(GenericAPIView):
    serializer_class = PlaceorderSerializer

    def post(self, request, userid):
        # Fetching cart items where cart_status is 1
        cart_item = Cart.objects.filter(userid=userid, cart_status=1)

        # Check if there are any cart items
        if cart_item.exists():
            orders = []

            # Loop through each item in the cart
            for i in cart_item:
                
                productimage=request.FILES.get('itemimage') if 'itemimage' in request.FILES else i.itemimage
                ordered = {
                    'itemid': i.itemid,
                    'itemname': i.itemname,
                    'itemimage': i.itemimage,
                    'itemprice': i.itemprice,
                    'userid': i.userid,
                    'quantity': i.quantity,
                }

                # Serialize the order data
                serializer = self.serializer_class(data=ordered)

                # Check if the serializer is valid and save the data
                if serializer.is_valid():
                    serializer.save()
                    orders.append(serializer.data)
                else:
                    # Return errors if the serializer is invalid
                    return Response({'errors': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            # Delete cart items after successful order placement
            cart_item.delete()

            # Return success response with the placed orders
            return Response({'data': orders, 'message': 'Order placed', 'success': True}, status=status.HTTP_200_OK)

        else:
            # If no cart items exist
            return Response({'error': 'No order placed', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

class view_orders_api(GenericAPIView):
   serializer_class=PlaceorderSerializer
   def get(self,request,userid):
    
      orders=Placeorder.objects.filter(userid=userid)
      serializer=PlaceorderSerializer(orders,many=True)
      print(f"Serialized data: {serializer.data}")
      return Response({'data':serializer.data,'message':'Data get','success':True},status=status.HTTP_200_OK)
   
class Addadress_api(GenericAPIView):
    serializer_class = AddressSerializer    

    def post(self, request):
        # Extracting data from the request
        userid = request.data.get('userid')
        name = request.data.get('name')
        street = request.data.get('street')
        city = request.data.get('city')
        state = request.data.get('state')
        country = request.data.get('country')
        postal_code = request.data.get('postal_code')

        # Check if an address already exists for the given userid
        if Address.objects.filter(userid=userid).exists():
            return Response({'error': 'Address already exists for this user'}, status=status.HTTP_400_BAD_REQUEST)

        # Creating an address instance
        address_data = {
            'userid': userid,
            'name': name,
            'street': street,
            'city': city,
            'state': state,
            'country': country,
            'postal_code': postal_code,
        }

        # Serialize the data
        serializer = self.serializer_class(data=address_data)

        # Validate the serializer
        if serializer.is_valid():
            # Save the new address
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Address added successfully', 'success': True}, status=status.HTTP_201_CREATED)
        else:
            # If serializer is invalid, return errors
            return Response({'errors': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        

class viewalladdress_api(GenericAPIView):
    serializer_class = AddressSerializer

    def get(self, request):
        
            # Fetch the address for the given userid
        address = Address.objects.all()
        if (address.count()>0):
              serializer=AddressSerializer(address,many=True)
              return Response({'data': serializer.data, 'message': 'Address retrieved successfully', 'success': True}, status=status.HTTP_200_OK)
        return Response({'error': 'Address not found for this user', 'success': False}, status=status.HTTP_404_NOT_FOUND)
    

class UpdateAddress_api(GenericAPIView):
 
    serializer_class=AddressSerializer
    def put(self,request,userid):
      result=Address.objects.get(userid=userid)
      serializer=AddressSerializer(instance = result,data=request.data,partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully'},status=status.HTTP_200_OK)
      else:
        return Response({'data':'not uodated'})
      
class DeleteAddress_api(GenericAPIView):
  def delete(self,request,userid):
    result=Address.objects.get(pk=userid)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
  


class change_pass_api(GenericAPIView):
   serializer_class=LoginSerializer
   def put(self,request,id):
      try:
         user=Login.objects.get(pk=id)
      except Login.DoesNotExist:
         return Response({'message':'user not found'},status=status.HTTP_400_BAD_REQUEST)
      serializer=self.serializer_class(user,data=request.data,partial=True)
      if serializer.is_valid():
         new_password=serializer.validated_data.get('password')
         if new_password:
            user.password=new_password
            user.save()
            return Response({'Message':'password updated successfully'},status=status.HTTP_200_OK)
         else:
            return Response({'Message':'no password provided'},status=status.HTTP_400_BAD_REQUEST) 
      return Response({'Message':'password updated successfully','errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)



class search_api(GenericAPIView):
   serializer_class=FooditemsSerializer
   def post(self,request):
      search_query=request.data.get('search_query','')
      if search_query:
         items=Fooditems.objects.filter(
            Q(itemname__exact=search_query)
         )
         print('filtered products',items)
         if not items:
             return Response({'Message':'no products found'},status=status.HTTP_400_BAD_REQUEST)
         serializer=self.serializer_class(items,many=True)
         for product in serializer.data:
            if product['itemimage']:
               product['itemimage']=settings.MEDIA_URL+product['itemimage']
            return Response({'data': serializer.data, 'message': 'image fetched successfully', 'success': True}, status=status.HTTP_200_OK)

         return Response({'error': 'no query found', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
      
   def get(self, request):
    search_query = request.query_params.get('search_query', '')
    print(search_query)  
    if search_query:
        items = Fooditems.objects.filter(
            Q(itemname__icontains=search_query) 
        ).values('itemname').distinct()[:10] 
        
        if not Fooditems.objects.exists(): 
            return Response({'Message': 'no suggestions found'}, status=status.HTTP_400_BAD_REQUEST)

        suggestion_list = [{'item_name': item['itemname']} for item in items]
        
        return Response({'suggestion': suggestion_list, 'message': 'suggestions fetched successfully', 'success': True}, status=status.HTTP_200_OK)

    return Response({'error': 'no search query provided', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
   

class add_offer_api(GenericAPIView):
  serializer_class=SpecialofferSerializer
  def post(self,request):
    itemname=request.data.get('itemname')
    
    offerdetails=request.data.get('offerdetails')
    itemimage=request.data.get('itemimage')
    serializer=self.serializer_class(data={'itemname':itemname,'itemimage':itemimage,'offerdetails':offerdetails})

    if serializer.is_valid():
      serializer.save()
      return Response({'data':serializer.data,'message':'product added successfully','succes':1},status=status.HTTP_200_OK)
   
    return Response({'data':serializer.errors,'message':'failed','succes':0})
  


class view_offers_api(GenericAPIView):
    serializer_class=SpecialofferSerializer
    def get(self,request):
        user=Special_offer.objects.all()
        if (user.count()>0):
            serializer=SpecialofferSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
    
class update_offers_api(GenericAPIView):
 
    serializer_class=SpecialofferSerializer
    def put(self,request,id):
      result=Special_offer.objects.get(pk=id)
      serializer=SpecialofferSerializer(instance = result,data=request.data,partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully'},status=status.HTTP_200_OK)
      else:
        return Response({'data':'not uodated'})
      
class delete_offers_api(GenericAPIView):
  def delete(self,request,id):
    result=Special_offer.objects.get(pk=id)
    result.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
   
