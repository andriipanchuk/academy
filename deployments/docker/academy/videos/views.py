from django.shortcuts import render
from videos.vimeo import Vimeo
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from videos.models import Video


# def index(request):
#     v = Vimeo()
#     folder = v.get_folder_videos('fuchicorp')
#     return HttpResponse(json.dumps(folder), content_type="application/json")

@login_required
def index(request):
    result = Video.objects.all()
    return render(request, 'videos.html', {'videos': result})
