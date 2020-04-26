from django.conf import settings
from vimeo import VimeoClient


class Vimeo():
    def __init__(self):
        self.vimeo = VimeoClient(
            token=getattr(settings, 'VIMEO_ACCESS_TOKEN', None),
            key=getattr(settings, 'VIMEO_CLIENT_ID', None), 
            secret=getattr(settings, 'VIMEO_CLIENT_SECRET', None)
            )

    def get_folder_videos(self, folder_name):
        response_data = self.vimeo.get('/me/folders').json()
        for folder in response_data['data']:
            if folder_name.lower() == folder['name'].lower():
                vifeos_uri = folder['metadata']['connections']['videos']['uri']
        if vifeos_uri:
            video_resononse = self.vimeo.get(vifeos_uri).json()
            return video_resononse['data']
        else:
            return {'message': 'can not find images'}
