from django.http import HttpResponse, JsonResponse
from django.utils.encoding import smart_str
from django.conf import settings
from django.http import Http404
from rest_framework import viewsets
from Lugdunum.models import Place, RecentPhoto, OldPhoto, Image
from Lugdunum.serializers import PlaceSerializer, RecentPhotoSerializer, ImageSerializer, OldPhotoSerializer
import os
import json
import base64

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class RecentPhotoViewSet(viewsets.ModelViewSet):
    queryset = RecentPhoto.objects.all()
    serializer_class = RecentPhotoSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class=ImageSerializer

def photoList(request, id_place):
    if request.method == 'GET':
        images = Place.objects.get(pk=id_place).oldphoto_set.all()
        serializer = OldPhotoSerializer(images, many=True)
        for image in serializer.data:
            try:
                image['image'] = image['image'].replace('/media','')
                file_as_b64 = base64.b64encode(open(os.path.join(settings.MEDIA_ROOT,image['image']),'rb').read())
                image['file'] = file_as_b64.decode('ascii')
            except:
                raise ValueError('Tried to encode base64 string by joining',settings.MEDIA_ROOT, image['image'])
        return JsonResponse(serializer.data, safe=False)
def placeList(request):
    if request.method == 'GET':
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return JsonResponse(serializer.data, safe=False)
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def index(request):
    response = HttpResponse('<p>Have a nice day :)</p>')
    return response