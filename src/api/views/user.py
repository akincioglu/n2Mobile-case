from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models.user import User
from ..serializers.user import UserSerializer
import requests
from decouple import config

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        data = request.data

        name = data.get('name', '')
        username = data.get('username', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        website = data.get('website', '')
        company_name = data.get('company', {}).get('name')
        location = self.get_location_from_ip(request)

        user_data = {
            'name': name,
            'username': username,
            'email': email,
            'address': {
                'suite': "None",
                'street': location.get('region', ''),
                'city': location.get('city', ''),
                'zipcode': location.get('postal', ''),
                'geo': {
                    'lat': float(location.get('loc', '').split(",")[0]),
                    'lng': float(location.get('loc', '').split(",")[1])
                }
            },
            'phone': phone,
            'website': website,
            'company': {
                'name': company_name
            }
        }

        serializer = self.get_serializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @action(detail=False, methods=['GET'])
    def get_user_by_username(self, request):
        username = request.query_params.get('username', None)
        if username is None:
            return Response({'error': 'Username parameter is required'}, status=400)

        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def get_user_by_email(self, request):
        email = request.query_params.get('email', None)
        if email is None:
            return Response({'error': 'Email parameter is required'}, status=400)

        user = get_object_or_404(User, email=email)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location_from_ip(self, request):
        # ip_address = self.get_client_ip(request)
        ip_address = config('IP_ADDRESS') 
        api_endpoint = f"https://ipinfo.io/{ip_address}/json"
        api_key = config('IPINFO_API_KEY')

        response = requests.get(api_endpoint, headers={"Authorization": f"Bearer {api_key}"})
        data = response.json()

        return data
