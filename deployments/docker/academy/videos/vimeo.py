from django.conf import settings
from vimeo import VimeoClient


class Vimeo():
    """
    Vimeo class is using VimeoClient to able to work with Vimeo apis.
    <token> Vimeo token 
    <key> Key of the vimeo app
    <secret> secret of the vimeo app
    """
    def __init__(self):
        self.vimeo = VimeoClient(
            token=getattr(settings, 'VIMEO_ACCESS_TOKEN', None),
            key=getattr(settings, 'VIMEO_CLIENT_ID', None), 
            secret=getattr(settings, 'VIMEO_CLIENT_SECRET', None)
            )

    def get_folder_videos(self, folder_name):
        ## Function is resposible to find all videos from the folder 
        response_data = self.vimeo.get('/me/folders').json()
        ## Looping all folders in vimeo
        for folder in response_data['data']:
            ## if folder is matching with <folder_name> 
            if folder_name.lower() == folder['name'].lower():
                ## Getting link of the videos as 
                link = str(folder['metadata']['connections']['videos']['uri'])
        if link:
            ## Getting all videos and returning data
            video_resononse = self.vimeo.get(link).json()
            return video_resononse['data']
        else:
            return {'message': 'function can not find link'}
