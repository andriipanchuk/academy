from django.shortcuts import render
from videos.vimeo import Vimeo
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from videos.models import Video, VideoTopic


# def index(request):
#     v = Vimeo()
#     folder = v.get_folder_videos('fuchicorp')
#     return HttpResponse(json.dumps(folder), content_type="application/json")

# @login_required
def index(request):
    result = Video.objects.all()
    return render(request, 'videos.html', {'videos': result})


# @login_required
def topics(request, topic=None):
    topics = VideoTopic.objects.all()

    if topic is not None:
        
        videos = Video.objects.filter(topic__id=topic)
        if not Video.objects.filter(topic__id=topic).exists():

            if Video.objects.filter(id=topic).exists():
                single_video = Video.objects.get(id=topic)
                return render(request, 'one-video.html', {'video': single_video})
            
        return render(request, 'topics.html', {'table_data': videos})
    
    

    return render(request, 'topics.html', {'table_data': topics})
