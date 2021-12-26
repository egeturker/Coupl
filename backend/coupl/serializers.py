from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework import serializers
from coupl.models import Profile, Event


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create(username=validated_data.get('username'), password=validated_data.get('password'))

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.password = validated_data.get('password')
        instance.save()
        return instance


class UserDisplaySerializer(serializers.RelatedField):
    def to_representation(self, value):
        username = value.username
        pk = value.pk
        return {"pk": pk, "username": username}


class EventSerializer(serializers.ModelSerializer):
    eventAttendees = UserDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['pk', 'eventName', 'eventDescription', 'eventCreator', 'eventStartTime', 'eventFinishTime',
                  'eventAttendees']

    def create(self, validated_data):
        print(validated_data)
        return Event.objects.create(eventName=validated_data.get('eventName'),
                                    eventDescription=validated_data.get('eventDescription'),
                                    eventCreator=validated_data.get('eventCreator'),
                                    eventStartTime=validated_data.get('eventStartTime'),
                                    eventFinishTime=validated_data.get('eventFinishTime'))
