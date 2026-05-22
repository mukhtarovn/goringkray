from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Product
class ProductModelSerializer(HyperlinkedModelSerializer):
   class Meta:
       model = Product
       fields = '__all__'