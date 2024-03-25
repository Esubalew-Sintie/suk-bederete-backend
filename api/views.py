from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
routes =  [
      {
          'Endpoint': '/template/getTemplate',
          'method': 'GET',
          'body': None,
          'description': 'Return a Template object'
      },
      {
          'Endpoint': '/stores/',
          'method': 'GET',
          'body': None,
          'description': 'Return an arry of notes'
      }
    ]
@api_view(['GET'])
def getroutes(request):
    return Response(routes)
