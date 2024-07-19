from django.shortcuts import render

import requests
from django.http import JsonResponse

# Create your views here.
from account.models import Account
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from django.contrib.auth.models import User

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

class VerifyTokenView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        refresh = request.data.get('refresh')
        print(token)

        try:
            # Manually verify the token
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = Account.objects.get(id=user_id)
            role = user.role

            return Response({'user_id': user_id, 'role': role})
        except TokenError as e:
            if isinstance(e, InvalidToken) and refresh:
                try:
                    refresh_token = RefreshToken(refresh)
                    new_access_token = str(refresh_token.access_token)
                    return Response({'access': new_access_token})
                except TokenError:
                    return Response({'error': 'Invalid refresh token'}, status=400)
            return Response({'error': str(e)}, status=400)

def update_clerk_user_metadata(request, user_id, role):
    clerk_api_key = "sk_test_hqvJsTDARJZewKOibkM6auiWzDKDafHMMOVqAlgtHi"  # Replace with your actual Clerk API key
    url = f"https://api.clerk.com/v1/users/{user_id}/metadata"

    headers = {
        'Authorization': f'Bearer {clerk_api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        "public_metadata": {
            "role": role
        }
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        print(response)
        response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful
        return JsonResponse({"message": "User metadata updated successfully."}, safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": f"Failed to update user metadata. Error: {str(e)}"}, safe=False)
