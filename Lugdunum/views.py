from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.conf import settings
from django.http import Http404
import os
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def index(request):
    
    response = HttpResponse('<p>Hey</p>') # mimetype is replaced by content_type for django 1.7
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response