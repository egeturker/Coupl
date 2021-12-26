from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from coupl.serializers import UserSerializer, EventSerializer
from coupl.models import Event, Profile


# todo
class UserLoginView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class EventListView(APIView):
    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventGetView(APIView):
    def get(self, request, format=None):
        event_id = request.query_params.get('event_id')
        event = Event.objects.get(pk=event_id)

        print(event)
        serializer = EventSerializer(event)

        return Response(serializer.data, status=201)


class EventAddView(APIView):
    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class EventJoinView(APIView):
    def post(self, request, format=None):
        event_id = request.query_params.get('eventId')
        print(event_id)
        user_id = request.query_params.get('userId')
        try:
            event = Event.objects.get(pk=event_id)
        except ObjectDoesNotExist:
            return JsonResponse('Event with the given id is not found.', status=400, safe=False)
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return JsonResponse('User with the given id is not found.', status=400, safe=False)
        event.eventAttendees.add(user)
        return JsonResponse('Successfully joined the event', status=201, safe=False)


class EventLeaveView(APIView):
    def post(self, request, format=None):
        event_id = request.query_params.get('eventId')
        user_id = request.query_params.get('userId')
        try:
            event = Event.objects.get(pk=event_id)
        except ObjectDoesNotExist:
            return JsonResponse('Event with the given id is not found.', status=400, safe=False)
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return JsonResponse('User with the given id is not found.', status=400, safe=False)
        if event.eventAttendees.contains(user):
            event.eventAttendees.remove(user)
            return JsonResponse('Successfully left event', status=201, safe=False)
        else:
            return JsonResponse('User is not in the event', status=400, safe=False)

class UserGetMatches(APIView):
    def get(self, request, format=None):
        event_id = request.query_params.get('eventId')
        user_id = request.query_params.get('userId')
        try:
            event = Event.objects.get(pk=event_id)
        except ObjectDoesNotExist:
            return JsonResponse('Event with the given id is not found.', status=400, safe=False)
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return JsonResponse('User with the given id is not found.', status=400, safe=False)
        if event.eventAttendees.contains(user):
            possibleMatches = []
            for attendee in event.eventAttendees.all().exclude(user):
                if attendee.profile.gender in Profile.preferenceList[user.profile.preference]:
                    possibleMatches.append(attendee)
            return possibleMatches
        else:
            return JsonResponse('User is not in the event', status=400, safe=False)
