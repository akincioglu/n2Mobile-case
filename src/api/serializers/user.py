from rest_framework import serializers
from ..models.user import User, Address, Geo, Company

class GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geo
        fields = ['lat', 'lng']

class AddressSerializer(serializers.ModelSerializer):
    geo = GeoSerializer()

    class Meta:
        model = Address
        fields = ['street', 'suite', 'city', 'zipcode', 'geo']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        company_data = validated_data.pop('company')

        geo_data = address_data.pop('geo')
        geo_instance = Geo.objects.create(**geo_data)

        address_instance = Address.objects.create(geo=geo_instance, **address_data)
        company_instance = Company.objects.create(**company_data)

        user_instance = User.objects.create(address=address_instance, company=company_instance, **validated_data)
        return user_instance
    
    def update(self, instance, validated_data):
      address_data = validated_data.pop('address', None)
      if address_data:
          instance.address.street = address_data.get('street', instance.address.street)
          instance.address.suite = address_data.get('suite', instance.address.suite)
          instance.address.city = address_data.get('city', instance.address.city)
          instance.address.zipcode = address_data.get('zipcode', instance.address.zipcode)

          geo_data = address_data.get('geo', {})
          instance.address.geo.lat = geo_data.get('lat', instance.address.geo.lat)
          instance.address.geo.lng = geo_data.get('lng', instance.address.geo.lng)

      company_data = validated_data.get('company', {})
      if company_data:
          instance.company.name = company_data.get('name', instance.company.name)

      instance.name = validated_data.get('name', instance.name)
      instance.username = validated_data.get('username', instance.username)
      instance.phone = validated_data.get('phone', instance.phone)
      instance.website = validated_data.get('website', instance.website)

      try:
          if address_data:
              instance.address.save()
              if geo_data:
                instance.address.geo.save()
          if company_data:
              instance.company.save()
          instance.save()
      except Exception as e:
          print(f"Error while saving instance: {e}")

      return instance