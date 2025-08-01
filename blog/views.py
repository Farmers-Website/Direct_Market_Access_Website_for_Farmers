from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


from .models import Product

def register(request):
    if request.method=="POST":
        form =UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:product_list')  # Redirect to product list after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('blog:login')

# Product list view (only accessible if logged in)
@login_required
def product_list(request):
    # Replace this with actual product logic
    products = [
        {'name': 'Product 1', 'price': 100},
        {'name': 'Product 2', 'price': 200},
    ]
    return render(request, 'blog/product_list.html', {'products':products})







































#             return redirect('market:pro')
#     else:
#         form=UserCreationForm()
#     return render(request,'blog/register.html',{'form':form})


# def Homepage(request):
#     return render(request,"product_list.html")

# def LoginPage(request):

#     return render(request,"blog/login.html")

# def post_product(request):
#     if request.method =="POST":
#         title=request.POST['title']
#         description =request.POST['description']
#         price=request.POST['price']
#         product = Product(vendor =request.user,title=title,description=description,price=price)
#         product.save()
#         return redirect('market:product_list')
#     return render(request,'blog/post_product.html')


# def product_list(request):
#     products=Product.objects.all()
#     return render(request,'blog/product_list.html',{'products':products})