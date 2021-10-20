from django.shortcuts import render
import requests

# Create your views here.
def home(request):
    response = requests.get('http://127.0.0.1:8000/api/posts').json()
    return render(request,'reddit/home.html',{'response':response})
