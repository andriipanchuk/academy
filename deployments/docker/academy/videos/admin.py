from django.contrib import admin
from videos.models import Video, VideoTopic
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
        """
        Function to sync all videos from vimeo to database
        """

        ## Getting vimeo client 
        vimeo_cleint = Vimeo()  

        ## Getting all folders from vimeo 
        vimeo_folders = vimeo_cleint.get_folders()

        ## list to store all topics which is already in database 
        db_topics = []

        ## Looping all folders in vimeo 
        for vimeo_folder in vimeo_folders:
            ## Getting only fuchicorp folders
            if 'fuchicorp' in vimeo_folder['name']:
                ## If folder does not exist in database as topic
                if not VideoTopic.objects.filter(name=vimeo_folder['name']).exists():
                    ## Creating topic in database and saving to database 
                    db_topic = VideoTopic(
                            name=vimeo_folder['name']
                        )
                    db_topic.save()
                ## Storing db instances to loop it later
                db_topics.append(db_topic)
            
        
        ## looping topics only 
        for topic in db_topics:
            ## Getting all videos based on topics
            videos = vimeo_cleint.get_folder_videos(topic.name)
            ## looping each videos
            for video in videos:
                ## if video does not have name will add 
                if not video['name']:
                    video['name'] = 'video does not have name'
                ## if video does not have description will add 
                if not video["description"]:
                    video["description"] = 'No description'

                ## if video does not exist in database 
                if not Video.objects.filter(name=video['name']).exists():
                    ## Create instance of the video and store in database with proper topic
                    video = Video(
                        name=video['name'],
                        description=video["description"],
                        duration=video["duration"],
                        link=f"https://player.vimeo.com{video['uri'].replace('videos', 'video')}",
                        topic=topic
                    )
                    video.save()

        self.message_user = 'Videos are synced'
        return HttpResponseRedirect("../")
            

admin.site.register(Video, VideoAdmin)
admin.site.register(VideoTopic)
