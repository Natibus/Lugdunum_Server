from django.http import HttpResponse
from django.utils.encoding import smart_str

def index(request):
    response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str("zbra.jpg")
    response['X-Sendfile'] = smart_str("media/")
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response