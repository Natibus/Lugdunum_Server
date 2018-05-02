import base64
def handle_uploaded_file(path,f):
    with open(path, 'wb+') as destination:
        destination.write(base64.decodestring(f.encode()))