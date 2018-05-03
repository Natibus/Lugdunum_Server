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
                image['image'] = image['image'].replace('/media', '')
                file_as_b64 = base64.b64encode(
                    open(os.path.join(settings.MEDIA_ROOT, image['image']), 'rb').read())
                image['file'] = file_as_b64.decode('ascii')
            except:
                raise ValueError(
                    'Tried to encode base64 string by joining', settings.MEDIA_ROOT, image['image'])
        return JsonResponse(serializer.data, safe=False)


def recentPhotoList(request, id_place):
    if request.method == 'GET':
        images = Place.objects.get(
            pk=id_place).recentphoto_set.order_by('-note')
        serializer = RecentPhotoSerializer(images, many=True)
        for image in serializer.data:
            try:
                image['image'] = image['image'].replace('/media', '')
                file_as_b64 = base64.b64encode(
                    open(os.path.join(settings.MEDIA_ROOT, image['image']), 'rb').read())
                image['file'] = file_as_b64.decode('ascii')
            except:
                raise ValueError(
                    'Tried to encode base64 string by joining', settings.MEDIA_ROOT, image['image'])
        return JsonResponse(serializer.data, safe=False)


def jsonOldPhotoUploadIsValid(jsonData):
    latitudeFlag = True if "latitude" in jsonData else False
    longitudeFlag = True if "longitude" in jsonData else False
    descriptionFlag = True if "description" in jsonData else False
    nameFlag = True if "name" in jsonData else False
    descriptionPhotoFlag = True if "descriptionPhoto" in jsonData else False
    dateFlag = True if "date" in jsonData else False
    infoLinkFlag = True if "infoLink" in jsonData else False
    fileStringFlag = True if "file" in jsonData else False
    # if some informations are not given, fill them out
    if not(descriptionFlag):
        jsonData['description'] = "Pas de description"
    if not(descriptionPhotoFlag):
        jsonData['descriptionPhoto'] = "Pas de description"
    if not(dateFlag):
        jsonData['date'] = "Pas de date"
    if not(infoLinkFlag):
        jsonData['infoLink'] = "Pas de lien d'informations"
    return (latitudeFlag and longitudeFlag and nameFlag and fileStringFlag)

def jsonRecentPhotoUploadIsValid(jsonData):
    nameFlag = True if "name" in jsonData else False
    fileStringFlag = True if "file" in jsonData else False
    return (nameFlag and fileStringFlag)

def createOldPhoto(requestData):
    place = Place.create(
            latitude=requestData['latitude'],
            longitude=requestData['longitude'],
            description=requestData['description']
        )
    place.save()
    oldphoto = OldPhoto.create(
        name=requestData['name'],
        description=requestData['descriptionPhoto'],
        date=requestData['date'],
        infoLink=requestData['infoLink'],
        file_string=requestData['file'],
        place=place,
    )
    try:
        oldphoto.save()
    except:
        raise ValueError("can't create old photo")

@csrf_exempt
def photoUpload(request):
    if request.method == 'POST':
        response = '<p>Your old photo has been submitted. Have a nice day :)<p>'
        requestData = json.loads(request.body.decode())
        if jsonOldPhotoUploadIsValid(requestData):
            response = [{
                    "response":"c'est validé ^.^",
                    "request":requestData
                }]
            createOldPhoto(requestData)
        else :
            response = [{
                    "response":"il manque des données",
                    "request":requestData
                }]
        return JsonResponse(response, safe=False)
    if request.method == 'GET':
        response = '<h1>Oops, wrong request</h1>'
        return HttpResponse(response)

def createRecentPhoto(requestData, id_place):
    place = Place.objects.get(pk=id_place)
    recentPhoto = RecentPhoto.create(
        name=requestData['name'],
        file_string=requestData['file'],
        place=place,
    )
    try:
        recentPhoto.save()
    except:
        raise ValueError("can't create recent photo")
@csrf_exempt
def recentPhotoUpload(request, id_place):
    if request.method == 'POST':
        requestData = json.loads(request.body.decode())
        if jsonRecentPhotoUploadIsValid(requestData):
            response = [{
                    "response":"requete valide",
                    "request":requestData
                }]
            createRecentPhoto(requestData, id_place)
        else:
            response = [{
                "response":"requete non valide",
                "request":requestData
            }]
        return JsonResponse(response, safe = False)
    if request.method == 'GET':
        response = '<h1>Oops, wrong request</h1>'
        return HttpResponse(response)


def placeList(request, id="all"):
    if request.method == 'GET':
        if id == "all":
            places = Place.objects.all()
            serializer = PlaceSerializer(places, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            place = Place.objects.get(pk=id)
            serializer = PlaceSerializer(place)
            return JsonResponse([serializer.data], safe=False)


@csrf_exempt
def voteUpload(request, id_recentPhoto):
    if request.method == 'POST':
        photo = RecentPhoto.objects.get(pk=id_recentPhoto)
        data = json.loads(request.body.decode())
        response = '<p>Your vote has been submitted. Have a nice day :)<p>'
        new_note = (float(data['note']) + photo.noteNumber *
                    photo.note) / (photo.noteNumber + 1)
        photo.note = new_note
        photo.noteNumber += 1
        photo.save()
        return HttpResponse(response)


def index(request):
    response = '<h1> Welcome to Lugdunum </h1>'
    response += '<p>To access places, see <a href="http://51.254.118.174:8080/Lugdunum/places/">here</a></p>'
    response += '<p>To access one place with its id, see, or example, here <a href="http://51.254.118.174:8080/Lugdunum/places/106/">here</a></p>'
    response += '<p>To access old photos for a place with id, see <a href="http://51.254.118.174:8080/Lugdunum/photoList/106/">here</a></p>'
    response += '<p>To access recent photos for a place with id, see <a href="http://51.254.118.174:8080/Lugdunum/recentPhotoList/106/">here</a></p>'
    response += '<p>To upload an old photo, post to http://51.254.118.174:8080/Lugdunum/photoUpload/">here</a></p>'
    response += '<p>To upload a recent photo for a place with id, post to http://51.254.118.174:8080/Lugdunum/recentPhotoUpload/106/">here</a></p>'
    response += '<p>Have a nice day :)</p>'
    return HttpResponse(response)