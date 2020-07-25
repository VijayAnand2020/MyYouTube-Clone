import json,os
import requests
from django.shortcuts import render
from . import models

# Create your views here.
API_KEY = os.environ.get('api')
BASE_VIDEO_API_URL = "https://www.googleapis.com/youtube/v3/search?&part=snippet&maxResults=50&q={}&key=%s"%API_KEY


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'home/Aboutpage.html')

def search(request):
    return render(request, 'home/search.html')

def newsearch(request):
    search = request.POST.get('search')
    search_new = search
    models.Search.objects.create(search=search)
    search_new = search_new.replace(" ","+")
    final_url = BASE_VIDEO_API_URL.format(search_new)
    json_file = requests.get(final_url)

    COMPLETE_VIDEO_INFORMATION = []

    data = json.loads(json_file.text)['items']

    for part in data:
        try:
            vid_link = part['id']['videoId']
            vid_link = 'https://youtube.com/watch?v=' + vid_link
            titles = part['snippet']['title']
            channel_name = part['snippet']['channelTitle']
            description = part['snippet']['description']
            images_url = part['snippet']['thumbnails']['medium']['url']
            COMPLETE_VIDEO_INFORMATION.append((titles,description,images_url,vid_link,channel_name))
        except KeyError:
            print('Error due to key error')

    stuff_for_frontend = {
        'search':search,
        'complete_information':COMPLETE_VIDEO_INFORMATION,
    }

    return render(request, 'home/newsearch.html', stuff_for_frontend)
