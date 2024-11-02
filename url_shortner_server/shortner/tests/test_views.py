
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shortner.models import Link
import csv
import io

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_new_url = reverse("add_new")
        self.update_url = reverse("update")

    def tearDown(self):
        User.objects.all().delete()
        Link.objects.all().delete()

    def test_stats_view_authenticated(self):
        self.client.post(reverse('signup'), {'username': 'newuser123', 'pass1': 'password123', 'pass2': 'password123', 'fname': 'John', 'lname': 'Doe', 'email': 'john.doe@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser123', 'pass1': 'password123'})
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepages/urlstats.html')

    def test_stats_view_unauthenticated(self):
        response = self.client.get(reverse('stats'))
        self.assertRedirects(response, reverse('signin'))

    def test_stats_view_empty_links(self):
        self.client.post(reverse('signup'), {'username': 'newuser123', 'pass1': 'password123', 'pass2': 'password123', 'fname': 'John', 'lname': 'Doe', 'email': 'john.doe@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser123', 'pass1': 'password123'})
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['list_of_links']), 0)

    def test_stats_view_multiple_links(self):
        self.client.post(reverse('signup'), {'username': 'newuser123', 'pass1': 'password123', 'pass2': 'password123', 'fname': 'John', 'lname': 'Doe', 'email': 'john.doe@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser123', 'pass1': 'password123'})
        self.client.post(reverse('add_new'), {"long-url": "https://www.example1.com"})
        self.client.post(reverse('add_new'), {"long-url": "https://www.example2.com"})
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['list_of_links']), 2)

    def test_stats_view_sorting(self):
        self.client.post(reverse('signup'), {'username': 'newuser123', 'pass1': 'password123', 'pass2': 'password123', 'fname': 'John', 'lname': 'Doe', 'email': 'john.doe@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser123', 'pass1': 'password123'})
        
        # Add two links
        self.client.post(reverse('add_new'), {"long-url": "https://www.example1.com"})
        self.client.post(reverse('add_new'), {"long-url": "https://www.example2.com"})
        
        # Get the links and update CTR
        link1 = Link.objects.get(long_url="https://www.example1.com")
        link2 = Link.objects.get(long_url="https://www.example2.com")
        
        # Simulate clicks by visiting the stub URLs
        for _ in range(5):
            self.client.get(reverse('stub', args=[link1.stub]))
        for _ in range(3):
            self.client.get(reverse('stub', args=[link2.stub]))
        
        # Refresh the link objects from the database
        link1.refresh_from_db()
        link2.refresh_from_db()
        
        # Get the stats view
        response = self.client.get(reverse('stats'))
        
        # Check if the links are sorted by CTR (descending order)
        self.assertEqual(response.context['list_of_links'][0]['ctr'], 5)
        self.assertEqual(response.context['list_of_links'][1]['ctr'], 3)
        
        # Ensure the links are in the correct order
        self.assertEqual(response.context['list_of_links'][0]['long_url'], "https://www.example1.com")
        self.assertEqual(response.context['list_of_links'][1]['long_url'], "https://www.example2.com")

    def test_export_csv_authenticated(self):
        self.client.post(reverse('signup'), {'username': 'newuser123', 'pass1': 'password123', 'pass2': 'password123', 'fname': 'John', 'lname': 'Doe', 'email': 'john.doe@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser123', 'pass1': 'password123'})
        self.client.post(reverse('add_new'), {"long-url": "https://www.example.com"})
        response = self.client.get(reverse('export_csv'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename="link_statistics_'))

    def test_export_csv_unauthenticated(self):
        response = self.client.get(reverse('export_csv'))
        self.assertRedirects(response, reverse('signin'))

    def test_export_csv_content(self):
        self.client.post(reverse('signup'), {'username': 'newuser123', 'pass1': 'password123', 'pass2': 'password123', 'fname': 'John', 'lname': 'Doe', 'email': 'john.doe@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser123', 'pass1': 'password123'})
        long_url = "https://www.example.com"
        self.client.post(reverse('add_new'), {"long-url": long_url})
        
        response = self.client.get(reverse('export_csv'))
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ['Long URL', 'Short URL', 'CTR'])

    def test_export_csv_multiple_links(self):
        self.client.post(reverse('signup'), {'username': 'newuser456', 'pass1': 'mypassword', 'pass2': 'mypassword', 'fname': 'Alice', 'lname': 'Smith', 'email': 'alice.smith@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser456', 'pass1': 'mypassword'})
        
        long_url_1 = "https://www.example1.com"
        long_url_2 = "https://www.example2.com"
        long_url_3 = "https://www.example3.com"
        for url in [long_url_1, long_url_2, long_url_3]:
            self.client.post(reverse('add_new'), {"long-url": url})
        
        response = self.client.get(reverse('export_csv'))
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        
        self.assertEqual(len(rows), 4)
        urls_in_csv = [row[0] for row in rows[1:]]
        expected_urls = [long_url_1, long_url_2, long_url_3]
        for url in expected_urls:
            self.assertIn(url, urls_in_csv)

    def test_export_csv_empty_links(self):
        self.client.post(reverse('signup'), {'username': 'newuser789', 'pass1': 'mypassword', 'pass2': 'mypassword', 'fname': 'Bob', 'lname': 'Johnson', 'email': 'bob.johnson@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser789', 'pass1': 'mypassword'})
        response = self.client.get(reverse('export_csv'))
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        self.assertEqual(len(rows), 1)

    def test_stats_view_context(self):
        self.client.post(reverse('signup'), {'username': 'newuser321', 'pass1': 'mypassword', 'pass2': 'mypassword', 'fname': 'Charlie', 'lname': 'Brown', 'email': 'charlie.brown@example.com'})
        self.client.post(reverse('signin'), {'username': 'newuser321', 'pass1': 'mypassword'})
        long_url = "https://www.example.com"
        self.client.post(reverse('add_new'), {"long-url": long_url})
        
        response = self.client.get(reverse('stats'))
        
        self.assertIn('csv_export_url', response.context)
        expected_csv_export_url = reverse('export_csv')
        actual_csv_export_url = response.context['csv_export_url']
        self.assertEqual(expected_csv_export_url, actual_csv_export_url)

    def test_stats_view_link_details(self):
        username = 'test_user456'
        email = 'test.user456@example.com'
        
        signup_data = {
            'username': username,
            "pass1": "securePass!234",
            "pass2": "securePass!234",
            "fname": "Test",
            "lname": "User",
            "email": email
        }
        
        self.client.post(reverse("signup"), signup_data)
        self.client.post(reverse("signin"), {"username": username, "pass1": signup_data["pass1"]})
        
        long_url = "https://www.testurl.com"
        self.client.post(reverse("add_new"), {"long-url": long_url})
        
        stats_response = self.client.get(reverse("stats"))
        link = stats_response.context["list_of_links"][0]
        
        self.assertEqual(link["long_url"], long_url)

    def test_stats_view_multiple_users(self):
        usernames_and_emails = [
            ('first_user111', 'first.user111@example.com'),
            ('second_user222', 'second.user222@example.com')
        ]
        
        for username, email in usernames_and_emails:
            signup_data = {
                "username": username,
                "pass1": "mypassword",
                "pass2": "mypassword",
                "fname": username.split('_')[0].capitalize(),
                "lname": username.split('_')[1].capitalize(),
                "email": email,
            }
            
            self.client.post(reverse("signup"), signup_data)
            self.client.post(reverse("signin"), {"username": username, "pass1": signup_data["pass1"]})
            
            for i in range(3):
                long_url = f"https://www.link{i}.com"
                self.client.post(reverse("add_new"), {"long-url": long_url})
            
            stats_response = self.client.get(reverse("stats"))
            self.assertEqual(len(stats_response.context["list_of_links"]), 3)
            
            self.client.post(reverse("signout"))

    def test_export_csv_filename(self):
        username = 'unique_user999'
        email = 'unique.user999@example.com'
        
        signup_data = {
            "username": username,
            "pass1": "mypassword",
            "pass2": "mypassword",
            "fname": "Unique",
            "lname": "User",
            "email": email,
        }
        
        self.client.post(reverse("signup"), signup_data)
        self.client.post(reverse("signin"), {"username": username, "pass1": "mypassword"})
        
        response = self.client.get(reverse("export_csv"))
        
        content_disposition = response['Content-Disposition']
        self.assertTrue(content_disposition.startswith("attachment; filename=\"link_statistics_"))

    def test_stats_view_ctr_update(self):
        username = 'ctr_user555'
        email = 'ctr.user555@example.com'
        
        signup_data = {
            "username": username,
            "pass1": "mypassword",
            "pass2": "mypassword",
            "fname": "CTR",
            "lname": "User",
            "email": email,
        }
        
        self.client.post(reverse("signup"), signup_data)
        self.client.post(reverse("signin"), {"username": username, "pass1": "mypassword"})
        self.client.post(reverse("add_new"), {"long-url": "https://www.ctrtesturl.com"})
        
        link = Link.objects.get(long_url="https://www.ctrtesturl.com")
        self.client.get(reverse("stub", args=[link.stub]))
        
        stats_response = self.client.get(reverse("stats"))
        self.assertEqual(stats_response.context["list_of_links"][0]["ctr"], 1)

    def test_stats_view_no_session(self):
        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 302)

    def test_export_csv_no_session(self):
        response = self.client.get(reverse("export_csv"))
        self.assertEqual(response.status_code, 302)