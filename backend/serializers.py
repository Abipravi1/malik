from rest_framework import serializers
from .models import *

class Tokensserializers(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = '__all__'