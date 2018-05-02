from django.http import HttpResponse, JsonResponse
from django.utils.encoding import smart_str
from django.conf import settings
from django.http import Http404
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from Lugdunum.models import Place, RecentPhoto, OldPhoto
from Lugdunum.serializers import PlaceSerializer, RecentPhotoSerializer, OldPhotoSerializer
import os
import json
import base64
from Lugdunum.forms import UploadFileForm
from Lugdunum.utils import handle_uploaded_file

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class RecentPhotoViewSet(viewsets.ModelViewSet):
    queryset = RecentPhoto.objects.all()
    serializer_class = RecentPhotoSerializer

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

def recentPhotoList(request, id_place):
    if request.method == 'GET':
        images = Place.objects.get(pk=id_place).recentphoto_set.order_by('-note')
        serializer = RecentPhotoSerializer(images, many=True)
        for image in serializer.data:
            try:
                image['image'] = image['image'].replace('/media','')
                file_as_b64 = base64.b64encode(open(os.path.join(settings.MEDIA_ROOT,image['image']),'rb').read())
                image['file'] = file_as_b64.decode('ascii')
            except:
                raise ValueError('Tried to encode base64 string by joining',settings.MEDIA_ROOT, image['image'])
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def photoUpload(request):
    if request.method == 'POST':
        response = '<h1>File uploaded</h1>'
        file_uploaded = json.loads(request.body.decode())
        response += '<p>' + file_uploaded['description'] + "</p>"
        place = Place.create(
            latitude = file_uploaded['latitude'],
            longitude = file_uploaded['longitude'],
            description = file_uploaded['description']
            )
        place.save()
        oldphoto = OldPhoto.create(
            name=file_uploaded['name'],
            description=file_uploaded['descriptionPhoto'],
            date=file_uploaded['date'],
            infoLink=file_uploaded['infoLink'],
            file_string=file_uploaded['file'],
            place=place,
        )
        try:
            oldphoto.save()
        except:
            raise ValueError('impossible de créer')
        return HttpResponse(response)
    if request.method == 'GET':
        response = '<h1>Oops, wrong request</h1>'
        response += str(request.body)
        return HttpResponse(response)

def placeList(request, id = "all"):
    if request.method == 'GET':
        if id=="all":
            places = Place.objects.all()
            serializer = PlaceSerializer(places, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            place = Place.objects.get(pk = id)
            serializer = PlaceSerializer(place)
            return JsonResponse([serializer.data], safe=False)

@csrf_exempt
def voteUpload(request, id):
    if request.method == 'POST':
        photo = RecentPhoto.objects.get(pk = id)
        data = json.loads(request.body.decode())
        response = '<p>Your vote has been submitted. Have a nice day :)<p>'
        new_note = (float(data['note']) + photo.noteNumber * photo.note) / (photo.noteNumber + 1)
        response += '<p> noteNumber : ' + str(photo.noteNumber) + '</p>'
        response += '<p> note : ' + str(photo.note) + '</p>'
        response += '<p> data[note] : ' + str(float(data['note'])) + '</p>'
        photo.note = new_note
        photo.noteNumber += 1
        photo.save()
        return HttpResponse(response)

def index(request):
    response = HttpResponse('<p>Have a nice day :)</p>')
    return response