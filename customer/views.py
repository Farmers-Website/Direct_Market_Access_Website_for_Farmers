



from django.shortcuts import render, redirect,HttpResponseRedirect

from django.contrib.auth import  logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from farmers.models.products import Product
from .models.category import Category
from .models.customer import Customer
from .models.order import Order
from .models.feedback import Feedback

from django.views import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from farmers.models.products import Product





def home(request):

    return render(request, 'customer/home.html')


def customer_home(request):
    if request.user.is_authenticated:
        return redirect('product_listing')  # Logged-in users go to product listing
    else:
        return redirect('customer_register')  # New users go to register page


class register(View):
       def get(self,request):
            
            return render(request,'customer/register.html')
       def post(self,request):
           
            postData=request.POST
            name=postData.get('name')
            phone=postData.get('phone')
            email=postData.get('email')
            password=postData.get('password')
            value={
                    'name':name,
                     'phone':phone,
                    'email':email,
        
                  }

               #validation
       
            customer=Customer(name=name,phone=phone,email=email,password=password)
            error_message=self.validateCustomer(customer)
            #saving
            if not error_message:
                  customer.password=make_password(customer.password)
                  customer.register()
                  return redirect('login')
            else:
             data={'error':error_message,
                   'values':value
              
              }
             return render(request,'customer/register.html',data)


       def validateCustomer(self,customer):
                        #validation
                   error_message=None
                   if len(customer.name)<3:
                      error_message="Name should be 3 char long or more"
        
                  # elif not phone:
                     #     error_message="Phone number required"
                   elif len(customer.phone)<10 or len(customer.phone)>10 or not customer.phone.isdigit:
                        error_message="phone number must be 10 digits"
                   elif len(customer.email)<5:
                          error_message="Email must be 5 char long"
                   elif customer.isExists():
                        error_message='Email Address already registered'
                   elif len(customer.password)<6:
                       error_message="Password must be 6 char long"
                   return error_message


@method_decorator(never_cache, name='dispatch')
class Login(View):
        return_url = None
        def get(self,request):
            Login.return_url = request.GET.get('return_url')
            return render(request,'customer/login.html')
        def post(self,request):
          postdata=request.POST
          email=postdata.get('email')
          password=postdata.get('password')
          customer=Customer.get_customer_by_email(email)
          error_message=None
          if customer:
             flag=check_password(password,customer.password)
             if flag:
               request.session['customer_id']=customer.id
               request.session['email']=customer.email
                
               if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
               else:
                    Login.return_url = None
                    return redirect('product_listing')
             else:
                error_message='Email or password invalid !'
          else:
             error_message=" You don't have account !!" 
          return render(request,'customer/login.html',{'error':error_message})


@method_decorator(never_cache, name='dispatch')
class customer_product(View):

    def get(self,request):
          
          cart=request.session.get('cart')
          if not cart:
               request.session['cart']={}
          products=None
          categories=Category.get_all_categories()
          CategoryId=request.GET.get('category')

        
          search_query = request.GET.get('search', '').strip()

          if CategoryId:
            products = Product.get_all_products_by_categoryid(CategoryId)
          elif search_query:
           
             products = Product.objects.filter(
                name__icontains=search_query
            ) | Product.objects.filter(
                category__name__icontains=search_query
            )  | Product.objects.filter(
                farmer__name__icontains=search_query
            )
          else:
              products = Product.get_all_products()

          data = {
            'products': products,
            'categories': categories,
            'search_query': search_query,  # Pass the search query back to the template
            'cart': cart,
        }
          
              
          return render(request,'customer\product_listing.html',data)

    def post(self,request):
         product=request.POST.get('product')
         remove=request.POST.get('remove')
         cart=request.session.get('cart')
         if cart:
              quantity=cart.get(product)
              if quantity:
                   if remove:
                         if quantity<=1:
                              cart.pop(product)
                         else:
                             cart[product]=quantity-1
                   else:   
                        cart[product]=quantity+1
              else:
                 cart[product]=1
         else:
            cart={}
            cart[product]=1 
         request.session['cart']=cart
         return redirect('cart')


@method_decorator(never_cache, name='dispatch')
class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys())
        cart_items = [
            {"product": product, "quantity": cart.get(str(product.id), 0)}
            for product in products
        ]
        return render(request, 'customer/cart.html', {'cart_items': cart_items})

    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        clear = request.POST.get('clear')
        cart = request.session.get('cart', {})
        if clear:
            cart = {}
        elif product_id:
            product_id = str(product_id)
            if remove:
                if cart.get(product_id, 0) > 1:
                    cart[product_id] -= 1
                else:
                    cart.pop(product_id, None)
            else:
                cart[product_id] = cart.get(product_id, 0) + 1

        request.session['cart'] = cart
        return redirect('cart')  # Redirect to the cart page

def checkout(request):
    if request.method == 'POST':
        # Get the address and phone from the form
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id') # Assuming the user is logged in
        cart = request.session.get('cart', {})

        if not cart:
            return redirect('cart')  # Redirect to cart if it's empty

        # Place orders for each product in the cart
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
           
            order = Order(
                customer=Customer.objects.get(id=customer),
                farmer_id=product.farmer_id,
                product=product,
                price=product.price,
                quantity=quantity,
                address=address,
                phone=phone,
            )
            order.save()

        # Clear the cart after placing the order
        request.session['cart'] = {}

        # Redirect to order confirmation or history page
        return redirect('order_history')  # Replace with your order history page URL
    else:
        return redirect('cart')  # Redirect to cart if accessed via GET



def order_history(request):
    customer = request.session.get('customer_id')
    orders = Order.objects.filter(customer=customer).order_by('-date')
    return render(request, 'customer/order.html', {'orders': orders})


from django.http import JsonResponse
import json

class FeedbackView(View):
    def get(self, request):
        
        return render(request, 'customer/feedback.html')

    def post(self, request):
        try:
            customer_id = request.session.get('customer_id')
            customer = Customer.objects.get(id=customer_id)

            
            data = json.loads(request.body.decode('utf-8'))
            rating = data.get('rating')
            message = data.get('message')
            
        
            if not customer_id:
                return JsonResponse({'error': 'Customer not logged in'}, status=401)
          
            if not (1 <= int(rating) <= 5) or not message:
                return JsonResponse({'error': 'Invalid input'}, status=400)

    
            Feedback.objects.create(customer=customer, rating=rating, message=message)
            return JsonResponse({'message': 'Feedback submitted successfully.'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)},status=500)




class ProfileView(View):
    def get(self, request):
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return redirect('login')  

        customer = Customer.objects.get(id=customer_id)
        return render(request, 'customer/profile.html', {'customer': customer})

    def post(self, request):
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return redirect('login')  # Redirect to login if not logged in

        customer = Customer.objects.get(id=customer_id)

     
        customer.name = request.POST.get('name')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')
        customer.dob = request.POST.get('dob')
        customer.bio = request.POST.get('bio')
        customer.gender = request.POST.get('gender')

    
        if 'profile_image' in request.FILES:
           customer.profile_image = request.FILES['profile_image']

        customer.save()

    
        request.session['profile_image_url'] = customer.profile_image.url if customer.profile_image else '/static/customer.jpg'

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')


def logout_view(request):
    logout(request)
    request.session.flush()

    return redirect('login') 

   


