import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Reply
from django.contrib.auth.models import User
# Create your tests here.

'''
Comprehensive user authentication checks for form posting and
correct cascade deletion of object verifications.
'''

class Helper:

    @staticmethod
    def create_and_login_user(
            username="abcd1234", 
            email="abcd@gmail.com", 
            password="pass12345"):
        
        client = Client()
        user = User.objects.create_user(
            username=username, 
            email=email,
            password=password,
            )
        
        client.login(username=username, password=password)
        return user

    @staticmethod
    def create_question(user, question_text, days):
        """
        Create a question with the given `question_text` and published 
        the given number of `days` offset to now (negative for questions 
        published in the past, positive for questions that have yet to be 
        published).
        """

        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(
            question_text=question_text, 
            pub_date=time, 
            user=user)

    @staticmethod
    def create_reply(user, reply_text, days):
        """
        Create a reply tied to a question with the given `reply_text` 
        and published the given number of `days` offset to now 
        (negative for replies published in the past, positive for 
        replies that have yet to be published).
        """

        time = timezone.now() + datetime.timedelta(days=days)
        op_user = Helper.create_and_login_user("1234abcd", "user@example.com", "1234pass")
        question = Helper.create_question(
            user=op_user,
            question_text="test question for replies",
            days=-5,
            )
        return Reply.objects.create(
            user=user,
            reply_text=reply_text,
            pub_date=time,
            question=question)

    @staticmethod
    def create_replies_to_single_question_id(user, question, reply_text, days):
        """
        Allows the ability to create multiple replies tied to a 
        single question with the given `reply_text` and published the 
        given number of `days` offset to now (negative for replies published
        in the past, positive for replies that have yet to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Reply.objects.create(
            user=user,
            reply_text=reply_text,
            pub_date=time,
            question=question)


class FormPostAuthenticationCheck(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_credentials = {
            'username': 'testuser',
            'password': 'secretpass123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_credentials)


    def test_logged_user_question_post(self):
        '''
        This test checks for successful question post from a logged in user.
        '''
        login = self.client.login(
            username=self.user_credentials['username'],
            password=self.user_credentials['password']
        )
        self.assertTrue(login)

        # check Question post (logged in)
        response = self.client.post(
            reverse('polls:create_question'),
            data={
                'question_text':'Test?',
                'pub_date':timezone.now()
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Question.objects.filter(question_text="Test?").exists())
        self.assertContains(response, "Test?")


    def test_logged_user_reply_post(self):
        '''
        This test checks for successful reply post from a logged in user.
        '''
        login = self.client.login(
            username=self.user_credentials['username'],
            password=self.user_credentials['password']
        )
        self.assertTrue(login)
        
        question = Helper.create_question(
            user=self.user, 
            question_text="Hello?", 
            days=-1)

        # check Reply post (logged in)
        response = self.client.post(
            reverse('polls:create_reply', args=(question.id,)),
            data={
                'reply_text':'Test?',
                'pub_date':timezone.now()
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Question.objects.filter(question_text="Hello?").exists())
        self.assertTrue(Reply.objects.filter(reply_text="Test?").exists())
        self.assertContains(response, "Test?")


    def test_logged_out_user_question_post(self):
        '''
        This test checks for unsuccessful question posts from a non-logged in user.
        Additionally checks for redirect to login page.
        '''
        response = self.client.post(
            reverse('polls:create_question'),
            data={
                'question_text':'Test?',
                'pub_date':timezone.now()
            }
        )

        # Assertions for redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, 
            f"{reverse('accounts:login')}?next={reverse('polls:create_question')}")
        
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'], [],
        )
        
    
    def test_logged_out_user_reply_post(self):
        '''
        This test checks for unsuccessful reply posts from a non-logged in user.
        Additionally checks for redirect to login page.
        '''
        question = Helper.create_question(
            user=self.user, 
            question_text="Hello?", 
            days=-1)

        response = self.client.post(
            reverse('polls:create_reply', args=(question.id,)),
            data={
                'reply_text':'Test?',
                'pub_date':timezone.now()
            }
        )

        # Assertions for redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, 
            f"{reverse('accounts:login')}?next={reverse('polls:create_reply', args=(question.id,))}")
        
        self.assertTrue(Question.objects.filter(question_text="Hello?").exists())
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertQuerySetEqual(
            response.context['latest_reply_list'], [],
        )


class CheckDeletionOfObjects(TestCase):
    def test_question_deletion(self):
        '''
        Creates a question then deletes it to verify deletion.
        '''
        user = Helper.create_and_login_user()
        question = Helper.create_question(
            user=user,
            question_text="Test Question",
            days=-1
        )
        # verify existence of question object
        self.assertTrue(Question.objects.filter(id=question.id).exists())
        # delete question
        question.delete()
        # verify existence of question object is false
        self.assertFalse(Question.objects.filter(id=question.id).exists())


    def test_question_deletion_reply_cascade(self):
        '''
        Deletes a created question with three replies to test deletion
        of those three replies.
        '''
        user = Helper.create_and_login_user()
        question = Helper.create_question(
            user=user,
            question_text="Test Question with Replies",
            days=-1
        )

        # add 3 replies to created question
        for i in range(3):
            Helper.create_replies_to_single_question_id(
                user=user, 
                question=question, 
                reply_text=f"Reply {i+1}", 
                days=-1
                )
        
        # verify replies exist
        self.assertEqual(Reply.objects.filter(question=question).count(), 3)
        # delete question
        question.delete()
        # verify question deletion
        self.assertFalse(Question.objects.filter(id=question.id).exists())
        # verify replies have also deleted due to cascade delete
        self.assertEqual(Reply.objects.filter(question=question).count(), 0)


    def test_other_question_deletion_no_reply_cascade(self):
        '''
        Creates two questions -- question1 with replies and question2 without 
        and verifies replies to question1 don't get deleted when 
        question2 gets deleted'''
        user = Helper.create_and_login_user()
        question1 = Helper.create_question(
            user=user,
            question_text="Test Question with Replies",
            days=-1
        )
        question2 = Helper.create_question(
            user=user,
            question_text="Test Question w/o Replies",
            days=-1
        )
        # add 3 replies to created question
        for i in range(3):
            Helper.create_replies_to_single_question_id(
                user=user, 
                question=question1, 
                reply_text=f"Reply {i+1}", 
                days=-1
                )    
        # delete question2
        question2.delete()
        # verify deletion of question2
        self.assertFalse(Question.objects.filter(id=question2.id).exists())
        # verify question1 still exists
        self.assertTrue(Question.objects.filter(id=question1.id).exists())
        # verify replies to question1 still exist
        self.assertEqual(Reply.objects.filter(question=question1.id).count(), 3)


    def test_reply_deletion_no_question_cascade(self):
        '''
        Creates a reply to a question then deletes the reply to verify
        that question did not get deleted.
        '''
        user = Helper.create_and_login_user()
        question = Helper.create_question(
            user=user,
            question_text="Test Question with Reply",
            days=-1
        )
        reply = Helper.create_replies_to_single_question_id(
                user=user, 
                question=question, 
                reply_text="Reply", 
                days=-1
            )
        # check reply exists
        self.assertTrue(Reply.objects.filter(id=reply.id, question=question).exists())
        self.assertEqual(Reply.objects.filter(question=question.id).count(), 1)
        # delete reply
        reply.delete()
        # verify reply deletion
        self.assertEqual(Reply.objects.filter(question=question.id).count(), 0)
        # check question exists
        self.assertTrue(Question.objects.filter(id=question.id).exists())


    def test_user_deletion(self):
        '''
        Creates and deletes a user to verify successful deletion of user.
        '''
        user = Helper.create_and_login_user()
        # verify existence of user
        self.assertTrue(User.objects.filter(id=user.id).exists())
        # delete user
        user.delete()
        # verify existence of user is false
        self.assertFalse(User.objects.filter(id=user.id).exists())


    def test_user_deletion_question_cascade(self):
        '''
        Creates a user that creates a question then deletes user
        to verify the question are also deleted
        '''
        user = Helper.create_and_login_user()
        question = Helper.create_question(
            user=user,
            question_text="Test Question",
            days=-1
        )
        # verify existence of question
        self.assertTrue(Question.objects.filter(id=question.id).exists())
        # delete user
        user.delete()
        # verify deletion of user
        self.assertFalse(User.objects.filter(id=user.id).exists())
        # verify existence of question is false
        self.assertFalse(Question.objects.filter(id=question.id).exists())


    def test_user_deletion_reply_cascade(self):
        '''
        Creates a user1 that creates replies to another user's question 
        then deletes user1 to verify only user1's replies are deleted and
        not the other user's question.
        '''
        user = Helper.create_and_login_user()
        question = Helper.create_question(
            user=user,
            question_text="Test Question",
            days=-1
        )
        user1 = Helper.create_and_login_user(
            username="1234abcd", 
            email="abcdefg@gmail.com", 
            password="pass12345"
        )
        # add 3 replies from user1 to user's question
        for i in range(3):
            Helper.create_replies_to_single_question_id(
                user=user1, 
                question=question, 
                reply_text=f"Reply {i+1}", 
                days=-1
                )
        # delete user1
        user1.delete()
        # verify deletion of user1
        self.assertFalse(User.objects.filter(id=user1.id).exists())
        # verify existence of question
        self.assertTrue(Question.objects.filter(id=question.id).exists())
        # verify existence of user1's replies are false
        self.assertEqual(Reply.objects.filter(question=question.id).count(), 0)


    def test_user_deletion_question_and_reply_cascade(self):
        '''
        Creates a user that creates a question with replies then
        deletes the user to verify that the question and replies are also
        deleted.
        '''
        user = Helper.create_and_login_user()
        question = Helper.create_question(
            user=user,
            question_text="Test Question",
            days=-1
        )
        # add 3 replies from user
        for i in range(3):
            Helper.create_replies_to_single_question_id(
                user=user, 
                question=question, 
                reply_text=f"Reply {i+1}", 
                days=-1
                )
            
        # delete user
        user.delete()
        # verify deletion of user
        self.assertFalse(User.objects.filter(id=user.id).exists())
        # verify user's replies are deleted
        self.assertEqual(Reply.objects.filter(question=question.id).count(), 0)
        # verify user's question is also deleted
        self.assertFalse(Question.objects.filter(id=question.id).exists())


    def test_user1_cannot_delete_user2_question(self):
        '''
        Creates user1 and user2 where user2 creates a question then
        verifies that user1 cannot delete user2's question.
        '''

    def test_user1_cannot_delete_user2_reply(self):
        '''
        Creates user1 and user2 where user2 creates a reply to
        user1's question then verifies that user1 cannot delete
        user2's reply.
        '''
        
        
