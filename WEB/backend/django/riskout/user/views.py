from django.shortcuts import render

# Create your views here.

def main_html(requests):
    return render(requests, 'index.html')
