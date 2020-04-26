from django.shortcuts import render
from videos.vimeo import Vimeo
import json
from django.http import HttpResponse


# def index(request):
#     v = Vimeo()
#     folder = v.get_folder_videos('fuchicorp')
#     return HttpResponse(json.dumps(folder), content_type="application/json")

def index(request):
    v = Vimeo()
    videos = v.get_folder_videos('fuchicorp')
    result = []
    for video in videos:
        result.append({
            "name": video['name'],
            "description": video["description"],
            "duration": video["duration"],
            "link": f"https://player.vimeo.com{video['uri'].replace('videos', 'video')}"
        })
    return render(request, 'videos.html', {'videos': result})
