from django.shortcuts import render
from django.http import HttpResponse



def homepage(request):
   
   return render(request,'templates\home.html')

def about(request):
   
   return render(request,'about.html')


   