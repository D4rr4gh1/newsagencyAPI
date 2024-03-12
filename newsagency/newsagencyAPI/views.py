from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@require_POST
def loginView(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('Login Successful. Welcome ' + username, content_type='text/plain', status=200)
    
    return HttpResponse('Login Failed. Your username or password were incorrect.', content_type='text/plain', status=401)
    
@csrf_exempt
@require_POST
def logoutView(request):
    print(request.user)
    if not request.user.is_authenticated:
        return HttpResponse('Not logged in', content_type='text/plain', status=401)

    logout(request)
    return HttpResponse('Logout successful', content_type='text/plain', status=200)


class StoriesView(View):

    @csrf_exempt
    @require_GET
    def get(self, request):
        return HttpResponse('Stories view', content_type='text/plain', status=200)
    
    @csrf_exempt
    @require_POST
    def post(self, request):
        return HttpResponse('Stories view', content_type='text/plain', status=200)
    

    def delete(self, request):
        return HttpResponse('Stories view', content_type='text/plain', status=200)