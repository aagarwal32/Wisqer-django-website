import datetime
from urllib.parse import quote
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from .models import Question, Reply
from django.contrib.auth.models import User
# Create your tests here.


def create_and_login_user(username="abcd1234", 
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


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions
        whose pub_date is in the future.
        """

        user = create_and_login_user()
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time, user=user)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions
        whose pub_date is older than 1 day.
        """
        user = create_and_login_user()
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time, user=user)
        self.assertIs(old_question.was_published_recently(), False)
    

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions 
        whose pub_date is within the last day.
        """
        user = create_and_login_user()
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time, user=user)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(user, question_text, days):
    """
    Create a question with the given `question_text` and published 
    the given number of `days` offset to now (negative for questions 
    published in the past, positive for questions that have yet to be 
    published).
    """

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, 
                                    pub_date=time, user=user)
    

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],[],
            )
        

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on
        the index page.
        """
        user = create_and_login_user()
        question = create_question(user, question_text="Past question.",
                                   days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question],
        )


    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed
        on the index page.
        """
        user = create_and_login_user()
        create_question(user, question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No questions are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [],
        )


    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past
        questions are displayed.
        """
        user1 = create_and_login_user()
        user2 = create_and_login_user("1234abcd", "user@example.com", "1234pass")
        question = create_question(user1, question_text="Past question.",
                                   days=-30)
        create_question(user2, question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question],
            )
        

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""

        user1 = create_and_login_user()
        user2 = create_and_login_user("1234abcd", "user@example.com", "1234pass")
        question1 = create_question(user1, question_text="Past question 1.",
                                    days=-30)
        question2 = create_question(user2, question_text="Past question 2.",
                                    days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        user = create_and_login_user()
        future_question = create_question(
            user,
            question_text="Future question.",
            days=5)
        
        encoded_question = quote(future_question.question_text)
        url = reverse("polls:detail", args=(future_question.id, encoded_question))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        user = create_and_login_user()
        past_question = create_question(
            user,
            question_text="Past question.",
            days=-5
        )
        encoded_question = quote(past_question.question_text)
        url = reverse("polls:detail", args=(past_question.id, encoded_question,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


def create_reply(user, reply_text, days):
    """
    Create a reply tied to a question with the given `reply_text` 
    and published the given number of `days` offset to now 
    (negative for replies published in the past, positive for 
    replies that have yet to be published).
    """

    time = timezone.now() + datetime.timedelta(days=days)
    op_user = create_and_login_user("1234abcd", "user@example.com", "1234pass")
    question = create_question(
        user=op_user,
        question_text="test question for replies",
        days=-5,
        )
    return Reply.objects.create(
        user=user,
        reply_text=reply_text,
        pub_date=time,
        question=question)


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


class ReplyDetailViewTests(TestCase):
    def test_no_replies(self):
        '''
        If no replies exist, an appropriate message is displayed.
        '''
        user = create_and_login_user()
        question = create_question(user, question_text="test", days=-5)
        encoded_question = quote(question.question_text)
        response = self.client.get(reverse('polls:detail', args=(question.id, encoded_question,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No replies yet...")
        self.assertQuerySetEqual(response.context["latest_reply_list"], [],)


    def test_past_reply(self):
        '''
        Replies with a pub_date in the past are displayed on the question
        detail page.
        '''
        user = create_and_login_user()
        reply = create_reply(user, reply_text="Past Reply.", days=-5)
        encoded_question = quote(reply.question.question_text)
        response = self.client.get(reverse('polls:detail', args=(reply.question.id, encoded_question)))
        self.assertQuerySetEqual(
            response.context["latest_reply_list"], [reply],
        )


    def test_future_reply(self):
        '''
        Replies with a pub_date in the future are not displayed on the 
        question detail page.
        '''
        user = create_and_login_user()
        reply = create_reply(user, reply_text="Future Reply.", days=5)
        encoded_question = quote(reply.question.question_text)
        response = self.client.get(reverse('polls:detail', args=(reply.question.id, encoded_question)))
        self.assertQuerySetEqual(
            response.context["latest_reply_list"], [],
        )


    def test_past_and_future_replies(self):
        '''
        Even if both past and future replies exist, only past replies are
        displayed.
        '''
        user1 = create_and_login_user()
        user2 = create_and_login_user("1234abcd", "user2@example.com", "1234pass")
        user3 = create_and_login_user("5678abcd", "user3@example.com", "5678pass")

        question = create_question(user1, question_text="Test Question", days=-5)
        encoded_question = quote(question.question_text)
        reply = create_replies_to_single_question_id(
            user2, question=question, reply_text="Past Reply.", days=-5)
        create_replies_to_single_question_id(
            user3, question=question, reply_text="Future Reply.", days=5)
        
        response = self.client.get(reverse('polls:detail', args=(question.id, encoded_question,)))
        self.assertQuerySetEqual(
            response.context['latest_reply_list'], [reply],
        )
        

    def test_two_past_replies(self):
        '''
        If two replies are in the past, both replies are displayed.
        '''
        user1 = create_and_login_user()
        user2 = create_and_login_user("1234abcd", "user2@example.com", "1234pass")
        user3 = create_and_login_user("5678abcd", "user3@example.com", "5678pass")
        question = create_question(user1, question_text="Test Question", days=-5)
        encoded_question = quote(question.question_text)
        reply1 = create_replies_to_single_question_id(
            user2, question=question, reply_text="Past Reply 1.", days=-3)
        reply2 = create_replies_to_single_question_id(
            user3, question=question, reply_text="Past Reply 2.", days=-5)
        
        response = self.client.get(reverse('polls:detail', args=(question.id, encoded_question)))
        self.assertQuerySetEqual(
            response.context['latest_reply_list'], [reply1, reply2],
        )
    

class QuestionFormValidationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="secretpass123",
            email="testuser@example.com"
        )

    def test_user_create_question_with_no_text(self):
        self.client.login(username='testuser', password='secretpass123')
        url = reverse('polls:index')
        form = {
            'question_text': "",
            'pub_date': timezone.now()
        }
        response = self.client.post(url, form)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'], [],
        )

    def test_user_create_question_with_text(self):
        self.client.login(username='testuser', password='secretpass123')
        url = reverse('polls:create_question')
        form = {
            'question_text': "test",
            'pub_date': timezone.now() + datetime.timedelta(days=-1)
        }
        response = self.client.post(url, form, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Question.objects.filter(question_text="test").exists())
        self.assertContains(response, "test")


# class RatingValidationTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username="testuser",
#             password="secretpass123",
#             email="testuser@example.com"
#         )
#         self.user2 = User.objects.create_user(
#             username="testuser2",
#             password="secretpass123",
#             email="testuser2@example.com"
#         )
#         self.create_question_url = reverse('polls:create_question')

#     def test_add_rating_to_own_question_ajax(self):
#         '''
#         A user can add an up-rating to their own question via an AJAX request.
#         '''
#         self.client.login(username='testuser', password='secretpass123')
        
#         # Create a question
#         form = {
#             'question_text': "test",
#             'pub_date': timezone.now() + datetime.timedelta(days=-1)
#         }
#         response = self.client.post(self.create_question_url, form)
#         self.assertEqual(response.status_code, 201)  # Assuming 201 for successful creation
        
#         # Retrieve the created question
#         question = Question.objects.last()
#         self.assertEqual(question.question_text, "test")
        
#         # Add rating via AJAX
#         question_rating_url = reverse('polls:question_rating', args=[question.id])
#         response = self.client.post(
#             question_rating_url,
#             {'action': 'like'},
#             HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # Simulate an AJAX request
#         )
        
#         # Check the JSON response
#         self.assertEqual(response.status_code, 200)
#         json_response = response.json()
#         self.assertEqual(json_response['status'], 'success')
#         self.assertEqual(json_response['message'], 'Rating updated successfully.')
#         self.assertIn(self.user, question.likes.all())

#     def test_add_rating_to_another_question_ajax(self):
#         '''
#         A user can add an up-rating to another user's question via an AJAX request.
#         '''
#         self.client.login(username='testuser', password='secretpass123')
        
#         # Create a question
#         form = {
#             'question_text': "test",
#             'pub_date': timezone.now() + datetime.timedelta(days=-1)
#         }
#         response = self.client.post(self.create_question_url, form)
#         self.assertEqual(response.status_code, 201)  # Assuming 201 for successful creation
        
#         # Retrieve the created question
#         question = Question.objects.last()
#         self.assertEqual(question.question_text, "test")
        
#         self.client.logout()
#         self.client.login(username='testuser2', password='secretpass123')
        
#         # Add rating via AJAX
#         question_rating_url = reverse('polls:question_rating', args=[question.id])
#         response = self.client.post(
#             question_rating_url,
#             {'action': 'like'},
#             HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # Simulate an AJAX request
#         )
        
#         # Check the JSON response
#         self.assertEqual(response.status_code, 200)
#         json_response = response.json()
#         self.assertEqual(json_response['status'], 'success')
#         self.assertEqual(json_response['message'], 'Rating updated successfully.')
#         self.assertIn(self.user2, question.likes.all())


    
