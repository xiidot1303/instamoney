from django.http import HttpResponse, FileResponse
def get_photos(request, folder, file):
    f = open('files/photos/{}/{}'.format(folder, file), 'rb')
    return FileResponse(f)