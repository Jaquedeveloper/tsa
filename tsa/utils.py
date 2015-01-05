from django.http import HttpResponse
import json

def json_response(data=None):
    return HttpResponse(json.dumps(data), content_type='text/json')