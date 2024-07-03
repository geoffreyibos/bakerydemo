from django.contrib.auth import get_user_model
from django.test import TestCase
from wagtail.models import Page, Collection, Site

from bakerydemo.base.models import (
    Person,
    FooterText,
    StandardPage,
    HomePage,
    GalleryPage,
    FormPage,
    GenericSettings,
    SiteSettings,
    UserApprovalTask,
)


class PersonModelTests(TestCase):

    def test_create_person_with_image(self):
        person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            job_title="Developer",
            image=<your_image_instance_here>,
        )
        self.assertEqual(str(person), "John Doe")
        self.assertEqual(person.thumb_image, "")

    def test_person_preview_modes(self):
        person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            job_title="Developer",
        )
        self.assertIn(("blog_post", "Blog post"), person.preview_modes)

    def test_person_get_preview_template(self):
        person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            job_title="Developer",
        )
        request = None  # Mock request if needed
        self.assertEqual(person.get_preview_template(request, "blog_post"), "base.html")

    def test_person_get_preview_context(self):
        person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            job_title="Developer",
        )
        request = None  # Mock request if needed
        context = person.get_preview_context(request, "blog_post")
        self.assertIn("page", context)


class FooterTextModelTests(TestCase):

    def test_create_footer_text(self):
        footer_text = FooterText.objects.create(body="Test Footer Text")
        self.assertEqual(str(footer_text), "Footer text")
        self.assertEqual(footer_text.body, "Test Footer Text")

    def test_footer_text_get_preview_template(self):
        footer_text = FooterText.objects.create(body="Test Footer Text")
        request = None  # Mock request if needed
        self.assertEqual(footer_text.get_preview_template(request, ""), "base.html")

    def test_footer_text_get_preview_context(self):
        footer_text = FooterText.objects.create(body="Test Footer Text")
        request = None  # Mock request if needed
        context = footer_text.get_preview_context(request, "")
        self.assertEqual(context["footer_text"], "Test Footer Text")


class StandardPageModelTests(TestCase):

    def test_create_standard_page(self):
        homepage = Page.objects.get(pk=1)
        standard_page = StandardPage(
            title="About Us",
            introduction="Introduction text",
            body='[{"type": "paragraph", "value": "Body text"}]',
        )
        homepage.add_child(instance=standard_page)
        self.assertEqual(standard_page.title, "About Us")

    def test_create_standard_page_invalid_body(self):
        homepage = Page.objects.get(pk=1)
        standard_page = StandardPage(
            title="About Us",
            introduction="Introduction text",
            body=None,  # Invalid body value
        )
        with self.assertRaises(ValueError):
            homepage.add_child(instance=standard_page)


class HomePageModelTests(TestCase):

    def test_create_home_page(self):
        homepage = Page.objects.get(pk=1)
        home_page = HomePage(
            title="Home",
            hero_text="Welcome to our site",
            hero_cta="Learn more",
            hero_cta_link=homepage,
        )
        homepage.add_child(instance=home_page)
        self.assertEqual(home_page.title, "Home")

    def test_create_home_page_missing_hero_text(self):
        homepage = Page.objects.get(pk=1)
        home_page = HomePage(
            title="Home",
            hero_cta="Learn more",
            hero_cta_link=homepage,
        )
        with self.assertRaises(ValueError):
            homepage.add_child(instance=home_page)


class GalleryPageModelTests(TestCase):

    def setUp(self):
        self.root_collection = Collection.get_first_root_node()
        self.collection = self.root_collection.add_child(name="Test Collection")

    def test_create_gallery_page(self):
        homepage = Page.objects.get(pk=1)
        gallery_page = GalleryPage(
            title="Gallery",
            introduction="Introduction text",
            collection=self.collection,
        )
        homepage.add_child(instance=gallery_page)
        self.assertEqual(gallery_page.title, "Gallery")

    def test_create_gallery_page_invalid_collection(self):
        homepage = Page.objects.get(pk=1)
        gallery_page = GalleryPage(
            title="Gallery",
            introduction="Introduction text",
            collection=None,  # Invalid collection value
        )
        with self.assertRaises(ValueError):
            homepage.add_child(instance=gallery_page)


class FormPageModelTests(TestCase):

    def test_create_form_page(self):
        homepage = Page.objects.get(pk=1)
        form_page = FormPage(
            title="Contact Form",
            body='[{"type": "paragraph", "value": "Form Body"}]',
        )
        homepage.add_child(instance=form_page)
        self.assertEqual(form_page.title, "Contact Form")

    def test_create_form_page_missing_body(self):
        homepage = Page.objects.get(pk=1)
        form_page = FormPage(
            title="Contact Form",
        )
        with self.assertRaises(ValueError):
            homepage.add_child(instance=form_page)


class GenericSettingsModelTests(TestCase):

    def test_create_generic_settings(self):
        settings = GenericSettings.objects.create(
            twitter_url="https://twitter.com/example",
            github_url="https://github.com/example",
        )
        self.assertEqual(settings.twitter_url, "https://twitter.com/example")


class SiteSettingsModelTests(TestCase):

    def test_create_site_settings(self):
        site = Site.objects.create(hostname="example.com", root_page=Page.objects.get(pk=1))
        settings = SiteSettings.objects.create(
            site=site,
            title_suffix=" | The Wagtail Bakery",
        )
        self.assertEqual(settings.title_suffix, " | The Wagtail Bakery")


class UserApprovalTaskModelTests(TestCase):

    def test_create_user_approval_task(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="password")
        user_approval_task = UserApprovalTask.objects.create(
            name="User Approval",
            user=user,
        )
        self.assertEqual(user_approval_task.name, "User Approval")
