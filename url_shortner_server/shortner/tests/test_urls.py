from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shortner.views import (
    DeleteView, NewView, UpdateView, StubView, StatsView, ListUrlsView,
    signup, signout, signin, CustomView, home, delete_all_urls, about_us,
    create_url, login_test, homepage
)

class TestUrls(SimpleTestCase):
    def test_add_url_is_resolved(self):
        url = reverse('add_new')
        self.assertEqual(resolve(url).func.view_class, NewView)

    def test_delete_url_is_resolved(self):
        url = reverse('delete', args=['special'])
        self.assertEqual(resolve(url).func.view_class, DeleteView)

    def test_update_url_is_resolved(self):
        url = reverse('update')
        self.assertEqual(resolve(url).func.view_class, UpdateView)

    def test_stub_url_is_resolved(self):
        url = reverse('stub', args=['some-url'])
        self.assertEqual(resolve(url).func.view_class, StubView)

    def test_stats_url_is_resolved(self):
        url = reverse('stats')
        self.assertEqual(resolve(url).func.view_class, StatsView)

    def test_list_url_is_resolved(self):
        url = reverse('list')
        self.assertEqual(resolve(url).func.view_class, ListUrlsView)

    def test_signin_url_is_resolved(self):
        url = reverse('signin')
        self.assertEqual(resolve(url).func, signin)

    def test_signout_url_is_resolved(self):
        url = reverse('signout')
        self.assertEqual(resolve(url).func, signout)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup)

    def test_delete_all_url_is_resolved(self):
        url = reverse('delete_all_urls')
        self.assertEqual(resolve(url).func, delete_all_urls)

    def test_export_csv_url_is_resolved(self):
        url = reverse('export_csv')
        self.assertEqual(resolve(url).func.view_class, StatsView)

    def test_custom_url_is_resolved(self):
        url = reverse('custom')
        self.assertEqual(resolve(url).func.view_class, CustomView)

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_login_test_url_is_resolved(self):
        url = reverse('Test')
        self.assertEqual(resolve(url).func, login_test)

    def test_about_us_url_is_resolved(self):
        url = reverse('about_us')
        self.assertEqual(resolve(url).func, about_us)

    def test_create_url_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, create_url)

    def test_homepage_url_is_resolved(self):
        url = reverse('homepage', args=['testuser'])
        self.assertEqual(resolve(url).func, homepage)

    def test_admin_url_is_resolved(self):
        url = reverse('admin:index')
        self.assertEqual(url, '/admin/')

    def test_stats_export_csv_url_is_resolved(self):
        url = reverse('export_csv')
        self.assertEqual(resolve(url).func.view_class, StatsView)
    
    def test_stub_url_with_alphanumeric_characters_is_resolved(self):
        url = reverse('stub', args=['some-url-with-alphanumeric-123'])
        self.assertEqual(resolve(url).func.view_class, StubView)

    def test_update_url_without_args_is_resolved(self):
        url = reverse('update')
        self.assertEqual(resolve(url).func.view_class, UpdateView)

    def test_signin_url_is_resolved(self):
        url = reverse('signin')
        self.assertEqual(resolve(url).func, signin)

    def test_delete_all_urls_is_resolved(self):
        url = reverse('delete_all_urls')
        self.assertEqual(resolve(url).func, delete_all_urls)
    
    def test_custom_view_url_is_resolved(self):
        url = reverse('custom')
        self.assertEqual(resolve(url).func.view_class, CustomView)

    # def test_nonexistent_url_raises_404(self):
    #     with self.assertRaises(resolve.Resolver404):
    #         resolve('/nonexistent-url/')