from django.contrib import admin
from videos.models import Video
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from videos.vimeo import Vimeo
from django.urls import path

admin.site.site_header = "Academy Admin dashboard"
class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duration')
    
    list_filter = ('name', 'duration')
    
    change_list_template = 'admin/videos/sync.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync/', self.sync_vimeo_videos)
        ]
        return custom_urls + urls

    def sync_vimeo_videos(self, request):
        v = Vimeo()
        videos = v.get_folder_videos('fuchicorp')

        for video in videos:

            if not video['name']:
                video['name'] = 'video does not have name'

            if not video["description"]:
                video["description"] = 'No description'
            
            if not Video.objects.filter(name=video['name']).exists():
                video = Video(
                    name=video['name'],
                    description=video["description"],
                    duration=video["duration"],
                    link=f"https://player.vimeo.com{video['uri'].replace('videos', 'video')}"
                )
                video.save()
        self.message_user = 'Videos are synced'
        return HttpResponseRedirect("../")
            


admin.site.register(Video, VideoAdmin)