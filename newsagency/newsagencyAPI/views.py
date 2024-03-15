import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date
from urllib.parse import parse_qs
from .models import Story



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
    if not request.user.is_authenticated:
        return HttpResponse('Not logged in', content_type='text/plain', status=401)

    logout(request)
    return HttpResponse('Logout successful', content_type='text/plain', status=200)

@method_decorator(csrf_exempt, name='dispatch') 
class StoriesView(View):


    def get(self, request):
        if not request.method == 'GET':
            return HttpResponse('Method not allowed', content_type='text/plain', status=503)
        
        if request.body:
        
            bodyUnicode = request.body.decode('utf-8')
            requestBody=parse_qs(bodyUnicode)

            requestedCategory = requestBody['story_cat'][0]
            requestedRegion = requestBody['story_region'][0]
            requestedDate = requestBody['story_date'][0]
        else:
            requestedCategory = '*'
            requestedRegion = '*'
            requestedDate = '*'

        storySet = Story.objects.all()

        if(requestedCategory != '*'):
            storySet = storySet.filter(category=requestedCategory)

        if(requestedRegion != '*'):
            storySet = storySet.filter(region=requestedRegion)
        
        if(requestedDate != '*'):
            try:
                requestedDate = parse_date(requestedDate)
                storySet = storySet.filter(date__gte=requestedDate)
            except Exception as e:
                return HttpResponse('Invalid date format', content_type='text/plain', status=503)
        

        if(len(storySet) == 0):
            return HttpResponse('No stories matching your parameters were found', content_type='text/plain', status=404)
        
        outputSet = []

        for story in storySet:
            storyDict = {
                'key': str(story.id),
                'headline' : str(story.headline),
                'story_cat' : str(story.category),
                'story_region' : str(story.region),
                'author' : str(story.author.name),
                'story_date' : str(story.date),
                'story_details' : str(story.details)
            }

            outputSet.append(storyDict)
                

        return JsonResponse({'stories' : outputSet}, status=200, safe=False)
        
    def post(self, request):

        if not request.method == 'POST':
            return HttpResponse('Method not allowed', content_type='text/plain', status=405)

        if not request.user.is_authenticated:
            return HttpResponse('Unauthenticated Author.  Not logged in', content_type='text/plain', status=503)
        
        if not request.content_type == 'application/json':
            return HttpResponse('Invalid Content Type', content_type='text/plain', status=503)
        
        
        try:
            data = json.loads(request.body)

            headline = data['headline']
            category = data['category']
            region = data['region']
            details = data['details']

            if(headline == None or category == None or region == None or details == None):
                return HttpResponse('Missing Fields', content_type='text/plain', status=503)
            
            if(len(headline) > 64):
                return HttpResponse('Headline exceeds maximum length', content_type='text/plain', status=503)

            if(len(details) > 256):
                return HttpResponse('Details exceeds maximum length', content_type='text/plain', status=503)
            
            regions = ['uk', 'eu', 'w']
            categories = ['pol', 'art', 'tech', 'trivia']

            if region not in regions:
                return HttpResponse('Invalid region', content_type='text/plain', status=503)
            
            if category not in categories:
                return HttpResponse('Invalid category', content_type='text/plain', status=503)
            
            Story.objects.create(headline=headline, 
                                    category=category, 
                                    region=region, 
                                    author=request.user.author, 
                                    details=details)
            
            return HttpResponse('CREATED', content_type='text/plain', status=201)

        except Exception as e:
            return HttpResponse('Bad Request ' + str(e), content_type='text/plain', status=503)


    def delete(self, request, storyID):

        if not request.method == 'DELETE':
            return HttpResponse('Method not allowed', content_type='text/plain', status=503)
        
        if not request.user.is_authenticated:
            return HttpResponse('Unauthenticated Author.  Not logged in', content_type='text/plain', status=503)
        
        try:
            story = Story.objects.get(id=storyID)
            if story.author.user != request.user:
                return HttpResponse('Unauthorised. Only Author of a story can delete it', content_type='text/plain', status=503)
            story.delete()
            return HttpResponse('OK', content_type='text/plain', status=200)
        
        except Exception as e:
            return HttpResponse('Story not found', content_type='text/plain', status=503)