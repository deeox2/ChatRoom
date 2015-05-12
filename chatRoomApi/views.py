from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from chatRoomApi.models import Messages
import json

def index(request):
    return HttpResponse("Yo what is up?")

def query(r):
    """ 
    query performs a DB query on chatRoomApi.models.Messages
    It returns a list with a dictionary stored in each index. Each dictionary contains the username and message field values for the latest 'r' object. 
    Each dictionary follows this template: {'username': <fieldValue>, 'message': <fieldValue>}
    The length of the list is defined as the function's argument. This function will query the latest 'r' objects.
    For example, r = 5 will return the 5 latest chat messages saved to the DB. These dictionary items are ordered from oldest to earliest within the list. 
    """
    lastMessagesObject = Messages.objects.latest('pk')
    lastPk = lastMessagesObject.pk
    usernamesAndMessages = []
    rFirst = r -1
    rLast = r + 1
    for pkNum in range(lastPk -rFirst, lastPk+rLast):
        try:
            messageObject = Messages.objects.get(pk= pkNum)
            usernameMessageDictionary = {'username': messageObject.username,
             'message': messageObject.message}
            usernamesAndMessages.append(usernameMessageDictionary)
        except Messages.DoesNotExist:
            continue
    return usernamesAndMessages

def chatApi(request):
    """
    This view handles the POST and GET requests from the Chat Client.
    GET : this view will query the DB for the 10 latest chat logs and will return a JSON object containing those logs
        format of JSON return object: '{"chatLog": [{"username": <FieldValue>, "message":<FieldValue>}, {...}, ...] }'
    POST : this view will read a JSON object that contains a username and message that will be saved to the DB.
        format: '{"username": <Value>, "message": <Value>}'
    """
    #handles POST and GET requests from Chat Client
    if request.method == 'POST':
        # parse JSON object and write to database
        chatMessage = json.loads(request.body)
        messageDB = Messages(username= chatMessage['username'], message= chatMessage['message'] )
        messageDB.save()
        return HttpResponse("message uploaded")

    elif request.method == 'GET':
        chatLog = {"chatLog": query(10)}
        chatLogJSON = json.dumps(chatLog)
        return HttpResponse(chatLogJSON, content_type='application/json')
    else:
        return HttpResponseBadRequest("Request method must be either POST or GET")
