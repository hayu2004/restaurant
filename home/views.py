from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def home(request):
    template = loader.get_template('home.html')
    context = {}  # Bạn có thể truyền dữ liệu sang template nếu cần
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('kabout.html')
    context = {}  # Bạn có thể truyền dữ liệu sang template nếu cần
    return HttpResponse(template.render(context, request))

def review(request):
    template = loader.get_template('review.html')
    context = {}  # Bạn có thể truyền dữ liệu sang template nếu cần
    return HttpResponse(template.render(context, request))

def user(request):
    template = loader.get_template('user.html')
    context = {}  # Bạn có thể truyền dữ liệu sang template nếu cần
    return HttpResponse(template.render(context, request))
