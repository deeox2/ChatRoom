"""
This test suite is setup for the Django development environment and not for the Heroku production environment. 
The current app's settings (as of Mary 18, 2015) are set up for the heroku production environment, as such these test suites cannot be run.
To run these tests, revert the setttings back to dev: 
1) Remove the configurations listed at the end of Settings. They are labeled 'Heroku Prod Settings'
2) Reconfigure the server URL in static/js/chatApiClient.js. This variable is listed at the top
OR
1) Follow these instructions and set this app up to run tests on Heroku: http://stackoverflow.com/questions/13705328/how-to-run-django-tests-on-heroku
"""

from django.test import TestCase, Client
from chatRoomApi.models import Messages
import json
from django.core.urlresolvers import reverse
from chatRoomApi.views import query

class TestHelperFunctionQueryWithTwentyRowDB(TestCase):
    """
    This will test suite will test the helper function, query(), ability to make accurate DB queries with a 20 Row DB
    Purpose: to make sure query can pull the LATEST 'n' DB objects when there are more than 'n' objects in the DB
    """
    def setUp(self):
        # POPULATE DB WITH 20 MESSAGES
        self.mockTwentyMessages = [{'username': 'testUser', 'message': str(num)} for num in range(1, 21)]
        for message in self.mockTwentyMessages:
            foo = Messages(username=message['username'], message= message['message'])
            foo.save()

    def testCanDBQueryHandleTwentyMessages(self):
        tenMessages = query(10)
        self.assertEqual(tenMessages, self.mockTwentyMessages[-10:])

class TestHelperFunctionQueryWithTwoRowDB(TestCase):
    """
    This will test suite will test the helper function, query(), ability to make accurate DB queries with a 2 Row DB
    Purpose: to make sure query can pull the LATEST 'n' DB objects when number of objects in DB < n
    """
    def setUp(self):
        # POPULATE DB WITH 2 MESSAGES
        self.mockTwoMessages = [{'username': 'testUser', 'message': str(num)} for num in range(1, 3)]
        for message in self.mockTwoMessages:
            foo = Messages(username=message['username'], message= message['message'])
            foo.save()

    def testCanDBQueryHandleMoreQueriesThanThereAreObjectsInTheDB(self):
        tenMessages = query(10)
        self.assertEqual(tenMessages, self.mockTwoMessages[-10:])

class TestHelperFunctionQueryWithEmptyDB(TestCase):
    """
    This will test suite will test the helper function, query(), ability to make accurate DB queries with a 0 Row (empty) DB
    Purpose: Intercept "model.DoesNotExist" exception. Return this dictionary: {"username": "none", "message": "none"}. Client will know what to do.
    """

    def testCanDBQueryHandleMoreQueriesThanThereAreObjectsInTheDB(self):
        tenMessages = query(10)
        self.assertEqual(tenMessages, "none")

class TestChatApiView(TestCase):

    def testPostRequestToView(self):
        """
        Test that view correctly reads the json object sent through POST and writes the information to the DB.
        """
        c = Client()
        chatPOST = json.dumps( {"username": "testUser", "message": "test"} )
        c.post(reverse('chatApi'), data=chatPOST, content_type='application/json')
        self.assertEqual(Messages.objects.get(username='testUser').message, "test")

    def testGetRequestToView(self):
        """
        Test that view correctly queries the DB for chat log (10 latest chat messages) and returns chat log as JSON 
        """
        ### POPULATE DB WITH 20 MESSAGE OBJECTS ###
        mockTwentyMessages = [{'username': 'testUser', 'message': str(num)} for num in range(1, 21)]
        for message in mockTwentyMessages:
            foo = Messages(username=message['username'], message= message['message'])
            foo.save()
        ###

        expectedChatLog = json.dumps( {"chatLog": [ {"username": "testUser", "message": "11"}, 
            {"username": "testUser", "message": "12"},
            {"username": "testUser", "message": "13"},
            {"username": "testUser", "message": "14"},
            {"username": "testUser", "message": "15"},
            {"username": "testUser", "message": "16"},
            {"username": "testUser", "message": "17"},
            {"username": "testUser", "message": "18"},
            {"username": "testUser", "message": "19"},
            {"username": "testUser", "message": "20"} ] } )

        c = Client()
        response = c.get(reverse('chatApi') )

        self.assertEqual(response.content, expectedChatLog)

