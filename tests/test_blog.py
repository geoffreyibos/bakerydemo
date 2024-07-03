from django.test import TestCase
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.images.tests.utils import get_test_image_file
from bakerydemo.blog.models import BlogPage, BlogIndexPage, BlogPersonRelationship
from bakerydemo.base.models import Person
from taggit.models import Tag
from datetime import datetime

class BlogPageModelTests(TestCase):

    def setUp(self):
        # Crée une instance d'image pour les tests
        self.image = Image.objects.create(
            title="Test Image",
            file=get_test_image_file(),
            width=100,
            height=100
        )
        self.root_page = Page.objects.get(pk=1)

    def test_create_blog_page(self):
        blog_page = BlogPage(
            title="Test Blog Page",
            introduction="Introduction text",
            image=self.image,
            body='[{"type": "paragraph", "value": "Body text"}]',
            subtitle="Test subtitle",
            date_published="2024-07-05",
        )
        self.root_page.add_child(instance=blog_page)

        # Vérifie que la création s'est déroulée correctement
        self.assertEqual(blog_page.title, "Test Blog Page")
        self.assertEqual(blog_page.authors(), [])
        self.assertEqual(blog_page.subtitle, "Test subtitle")
        self.assertEqual(blog_page.image, self.image)
        date_str = '2024-07-05'
        expected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        self.assertEqual(blog_page.date_published, expected_date)

    def test_blog_index_page_children(self):
        blog_index_page = BlogIndexPage(
            title="Test Blog Index Page",
            introduction="Introduction text",
            image=self.image,
            slug="test-blog-index-page",
        )
        self.root_page.add_child(instance=blog_index_page)

        blog_page = BlogPage(
            title="Test Blog Page 1",
            introduction="Introduction text",
            image=self.image,
            body='[{"type": "paragraph", "value": "Body text"}]',
            subtitle="Test subtitle",
            date_published="2024-07-05",
        )
        blog_index_page.add_child(instance=blog_page)

        # Vérifie que la méthode children retourne les pages enfants
        children = blog_index_page.get_children()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].title, "Test Blog Page 1")

    def test_blog_index_page_get_context(self):
        blog_index_page = BlogIndexPage(
            title="Test Blog Index Page",
            introduction="Introduction text",
            image=self.image,
            slug="test-blog-index-page",
        )
        self.root_page.add_child(instance=blog_index_page)

        blog_page_1 = BlogPage(
            title="Test Blog Page 1",
            introduction="Introduction text",
            image=self.image,
            body='[{"type": "paragraph", "value": "Body text"}]',
            subtitle="Test subtitle",
            date_published="2024-07-05",
        )
        blog_index_page.add_child(instance=blog_page_1)

        blog_page_2 = BlogPage(
            title="Test Blog Page 2",
            introduction="Introduction text",
            image=self.image,
            body='[{"type": "paragraph", "value": "Body text"}]',
            subtitle="Test subtitle",
            date_published="2024-07-04",
        )
        blog_index_page.add_child(instance=blog_page_2)

        # Vérifie que la méthode get_context retourne les articles triés par date de publication
        context = blog_index_page.get_context(None)
        posts = context.get("posts")
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].title, "Test Blog Page 1")
        self.assertEqual(posts[1].title, "Test Blog Page 2")


class BlogPersonRelationshipModelTests(TestCase):

    def setUp(self):
        # Crée une instance de BlogPage et une instance de Person pour les tests
        self.root_page = Page.objects.get(pk=1)
        self.blog_page = BlogPage(
            title="Test Blog Page",
            introduction="Introduction text",
            body='[{"type": "paragraph", "value": "Body text"}]',
            subtitle="Test subtitle",
            date_published="2024-07-05",
        )
        self.root_page.add_child(instance=self.blog_page)
        self.person = Person.objects.create(first_name="John", last_name="Doe")

    def test_create_blog_person_relationship(self):
        blog_person_relationship = BlogPersonRelationship.objects.create(
            page=self.blog_page,
            person=self.person,
        )

        self.assertEqual(blog_person_relationship.page, self.blog_page)
        self.assertEqual(blog_person_relationship.person, self.person)
