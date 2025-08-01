
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models.categories import Category
from .models.farmers import Farmer
from .models.products import Product
from customer.models.order import Order
from customer.models.feedback import Feedback
# from .forms import FarmerProfileForm,ProductForm
from django.views import View
from django.contrib.auth.hashers import  check_password,make_password
from django import forms
from django.db import IntegrityError
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
class Login(View):
    return_url = None
    def get(self, request):
            Login.return_url = request.GET.get('return_url')
            return render(request,'login.html')

        # # Fetch return_url from the query parameters
        # return_url = request.GET.get('return_url', '/farmers/')
        
        # if request.user.is_authenticated:
        #     farmer = Farmer.objects.filter(user=request.user).first()
        #     if farmer:
        #         return redirect('farmer_dashboard', id=farmer.id)  
        # return render(request, 'login.html',{'return_url': return_url})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        # return_url = request.POST.get('return_url', '/farmers/')  # Default to homepage if not set
        farmer = Farmer.get_farmer_by_email(email=email)
        error_message = None
        print(farmer)

        if farmer:
            flag = check_password(password, farmer.password)
            if flag:
                request.session['farmer_id'] = farmer.id
                request.session['email']=farmer.email
                request.session.save()
                # return_url = reverse('farmer_dashboard', kwargs={'id': farmer.id})
                # print(f"Redirecting to: {return_url}")
                # return redirect(return_url)

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return reverse('farmer_dashboard', kwargs={'id': farmer.id})
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = "You don't have account !!"

            return render(request, 'login.html', {
            'error': error_message,
            'return_url': return_url,
            'values': {'email': email, 'password': ''}})
        return redirect('farmer_login')

def logout(request):
    request.session.clear()
    return redirect('farmer_login')

class Register(View):
       def get(self,request):
            return render(request,'register.html')
       
       def post(self,request):
            postData=request.POST
            name=postData.get('name')
            phone=postData.get('phone')
            email=postData.get('email')
            password=postData.get('password')
            location=postData.get('location')
            image=postData.get('image')
            # image = request.FILES['image']  # Access the uploaded file

            
            hashed_password = make_password(password)

            value={
                    'name':name,
                    'phone':phone,
                    'email':email,
                    'password':password,
                     'location':location,
                     'image':image,
                  }

               #validation
  
            farmer=Farmer(name=name,phone=phone,email=email,password=hashed_password,location=location,image=image)
            print(farmer)
            error_message=self.validateFarmer(farmer)
            #saving
            if not error_message:
                try:
                  user = User.objects.create_user(username=email, password=farmer.password, email=email)
                  farmer.user = user 
                  farmer.register()
                  farmer.save()
                  return redirect('farmer_login')
                except IntegrityError:
                  messages.error(request, 'Username already exists. Please choose another one.')
                  return redirect('register')
            else:
             data={'error':error_message,
                   'values':value
              }
             return render(request,'register.html',data)


       def validateFarmer(self,farmer):
                        #validation
                   error_message=None
                   if len(farmer.name)<3:
                      error_message="Name should be 3 char long or more"
        
                  # elif not phone:
                     #     error_message="Phone number required"
                   elif not farmer.phone:
                        error_message = 'Phone Number required'
                   elif len(farmer.phone) < 10:
                        error_message = 'Phone Number must be 10 char Long'
                   elif len(farmer.email)<5:
                          error_message="Email must be 5 char long"
                   elif farmer.isExists():
                        error_message='Email Address already registered'
                   elif len(farmer.password)<6:
                       error_message="Password must be 6 char long"
                   return error_message
       
class Farmer_dashboard(View):

    def post(self,request):
        product=request.POST.get('product')
        print(product)
        return redirect('farmer_dashboard',id=request.session.get('farmer_id'))
    
    def get(self,request,id):
            farmer = Farmer.objects.get(id=id)
        
        # orders = Order.objects.filter(farmer=farmer)
            print(farmer.name)
    
            
            try:
                farmer = Farmer.objects.select_related('user').get(id=id)
                print("farmer is ",farmer)
                request.session['farmer_id'] = farmer.id 
                products = Product.objects.filter(farmer=farmer)
                # farmer = Farmer.objects.get(user=request.user)
                # products = Product.objects.filter(farmer=farmer)  # Products added by the logged-in farmer
            except Farmer.DoesNotExist:
                products = []

            
            products=None
            categories=Category.get_all_categories()
            category_name=request.GET.get('category')
            if category_name:
                products=Product.objects.filter(category__name=category_name, farmer=farmer)
            else:
                products=Product.objects.filter(farmer=farmer)
            data={}
            data['products']=products
            data['farmer']=farmer
            data['categories']=categories
            context = {**data, 'farmer_id': id}
            print('you are : ',request.session.get('email'))
            for product in Product.objects.all(): 
                 print(product.image.url)
            return render(request,'farmer_dashboard.html',context)
        
        
        
def farmer_profile(request,id):
    try:
            farmer = get_object_or_404(Farmer, id=id)
    except Farmer.DoesNotExist:
            farmer = None 
            return redirect('login')
        
    return render(request, 'farmer_profile.html', {'farmer': farmer})   

def edit_farmer_profile(request,id):
    farmer = get_object_or_404(Farmer, id=id)
    print(farmer)

    if request.method == 'POST':
        # Handle POST request when form is submitted
        # Update farmer's details from POST data and uploaded files
        if 'name' in request.POST:
            farmer.name = request.POST['name']
        if 'phone' in request.POST:
            farmer.phone = request.POST['phone']
        if 'email' in request.POST:
            farmer.email = request.POST['email']
        if 'location' in request.POST:
            farmer.location = request.POST['location']

        # Handle profile picture (if uploaded)
        if 'image' in request.FILES:
            farmer.image= request.FILES['image']

        # Save the updated farmer object to the database
        farmer.save()

        # Redirect to the farmer's profile page after saving
        return redirect('farmer_profile', id=farmer.id)
    return render(request, 'edit_farmer_profile.html', {'farmer':farmer})     

def add_product(request):
    farmer_id = request.session.get('farmer_id')
    categories=Category.objects.all()

    if not farmer_id:
        return redirect('login')

    try:
        farmer = Farmer.objects.get(id=farmer_id)
    except Farmer.DoesNotExist:
        return redirect('login')

    if request.method == 'GET':
        return render(request, 'add_product.html',{'farmer_id':farmer_id,'categories':categories})

    if request.method == 'POST':
        # Get data from POST
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category_name = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # File field requires request.FILE

        # if image:
        #         image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'products', image.name)
        #         # Save the image to the correct location
        #         with open(image_path, 'wb') as f:
        #             for chunk in image.chunks():
        #                 f.write(chunk)

        if not all([name, price, category_name, description, image]):
                return render(request, 'add_product.html', {'error': 'All fields are required', 'farmer_id': farmer_id})

        
        category_instance = Category.objects.get(name=category_name)
            # Create the product and associate it with the farmer
        product = Product.objects.create(
                farmer=farmer,
                name=name,
                price=price,
                quantity=quantity,
                category=category_instance,
                description=description,
                image=image,
            )
        print(product)
        return redirect('farmer_dashboard', id=farmer_id)  # Redirect to dashboard

    return render(request, 'add_product.html', {'farmer_id': farmer_id})
        

    return render(request, 'add_product.html',{'farmer_id':farmer_id}) 

def view_product(request,product_id):
    if product_id:
        # Fetch the product for the logged-in farmer
        product = get_object_or_404(Product, id=product_id)
        farmer_id = product.farmer.id
        return render(request, 'view_product.html', {'product_id': product_id,'product':product, 'farmer_id':farmer_id})
    


def update_product(request, product_id):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        farmer_id = product.farmer.id 

        if request.method == 'POST':
            # Retrieve form data
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.quantity = request.POST.get('quantity')
            product.description = request.POST.get('description')
            
            # Optional: Handle new image upload
            if request.FILES.get('image'):
                product.image = request.FILES.get('image')

            product.save()  # Save updated product to the database
            return redirect('view_product', product_id=product.id)  # Redirect to the updated product page

        # Render the form with the current product details
        return render(request,'update_product.html',{'product_id': product_id,'product':product,'farmer_id': farmer_id}) 

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    farmer_id=product.farmer.id
    if request.method == "POST":
        product.delete()
        return redirect('farmer_dashboard',id=farmer_id)
    return render(request, 'delete_product.html', {'product_id': product_id,'product': product,'farmer_id': farmer_id})

def view_orders(request,id):
    # Fetch the farmer by their ID
    farmer = Farmer.objects.get(id=id)
    
    # Fetch all orders related to the farmer
    orders = Order.objects.filter(farmer=farmer).order_by('-date')
    
    # Pass the orders to the orders.html template
    return render(request, 'farmer_orders.html', {'orders': orders,'farmer':farmer})

def accept_order(request, id):
    # Fetch the order
    order = get_object_or_404(Order, id=id)

    # Process POST request for acceptance or rejection
    if request.method == 'POST':
        if 'accept' in request.POST:
            product = order.product
            if product.quantity >= order.quantity:
                # Reduce product quantity
                product.quantity -= order.quantity
                product.save()

                # Mark order as accepted
                order.status = True
                order.save()
                return redirect('farmer_orders', id=order.product.farmer_id)
        elif 'reject' in request.POST:
            # Mark order as rejected
            order.status = False
            order.save()
            return redirect('farmer_dashboard', id=order.product.farmer_id)

    return render(request, 'accept_order.html', {'order': order})

    
def product_feedback_view(request, product_id):
    # Fetch the product or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    # Get all feedback associated with the product
    feedbacks = product.feedbacks.all()  # Use related_name from ForeignKey in Feedback model
    return render(request, 'product_feedback.html', {'product': product, 'feedbacks': feedbacks})