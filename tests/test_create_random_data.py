from django.test import TestCase
from django.core.management import call_command
from wagtail.images.models import Image
from wagtail.models import Page
from bakerydemo.base.models import FooterText, HomePage, Person, StandardPage
from bakerydemo.blog.models import BlogIndexPage, BlogPage
from bakerydemo.breads.models import BreadIngredient, BreadPage, BreadsIndexPage, BreadType, Country
from bakerydemo.locations.models import LocationPage, LocationsIndexPage

class CreateRandomDataCommandTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Obtenir la racine de la hiérarchie des pages
        root = Page.get_first_root_node()

        # Créer la page d'accueil (HomePage)
        homepage = HomePage(
            title='Home',
            slug='homeSlug',  # Slug unique pour éviter les conflits
            live=True,
            hero_text='Welcome to the Home Page',
            hero_cta='Learn more',
            depth=root.depth + 1,  # Profondeur relative à la racine
            path=root.path + '0001',  # Chemin basé sur le chemin de la racine
        )
        root.add_child(instance=homepage)  # Ajouter la page d'accueil à la racine
        homepage.save_revision().publish()

        # Créer BreadsIndexPage s'il n'existe pas
        if not BreadsIndexPage.objects.exists():
            breads_index = BreadsIndexPage(
                title='Breads',
                slug='breads',
                live=True,
                introduction='Introduction to breads',
                depth=homepage.depth + 1,
                path=homepage.path + '0001',
            )
            homepage.add_child(instance=breads_index)  # Ajouter BreadsIndexPage comme enfant de HomePage
            breads_index.save_revision().publish()

        # Créer LocationsIndexPage s'il n'existe pas
        if not LocationsIndexPage.objects.exists():
            locations_index = LocationsIndexPage(
                title='Locations',
                slug='locations',
                live=True,
                introduction='Introduction to locations',
                depth=homepage.depth + 1,
                path=homepage.path + '0002',
            )
            homepage.add_child(instance=locations_index)  # Ajouter LocationsIndexPage comme enfant de HomePage
            locations_index.save_revision().publish()

        # Créer BlogIndexPage s'il n'existe pas
        if not BlogIndexPage.objects.exists():
            blog_index = BlogIndexPage(
                title='Blog',
                slug='blog',
                live=True,
                introduction='Introduction to blog',
                depth=homepage.depth + 1,
                path=homepage.path + '0003',
            )
            homepage.add_child(instance=blog_index)  # Ajouter BlogIndexPage comme enfant de HomePage
            blog_index.save_revision().publish()

    def test_create_random_data(self):
        page_count = 5
        snippet_count = 5
        image_count = 5

        call_command('create_random_data', page_count, snippet_count, image_count)

        # Vérifier le nombre d'images créées
        self.assertEqual(Image.objects.count(), image_count)

        # Vérifier le nombre de snippets créés
        self.assertEqual(Country.objects.count(), snippet_count)
        self.assertEqual(BreadIngredient.objects.count(), snippet_count)
        self.assertEqual(BreadType.objects.count(), snippet_count)
        self.assertEqual(Person.objects.count(), snippet_count)
        self.assertEqual(FooterText.objects.count(), snippet_count)

        # Vérifier le nombre de pages créées
        self.assertEqual(BreadPage.objects.count(), page_count)
        self.assertEqual(LocationPage.objects.count(), page_count)
        self.assertEqual(BlogPage.objects.count(), page_count)

        # Les pages Standard sont imbriquées sous une page de niveau supérieur, donc elles sont page_count + 1
        self.assertEqual(StandardPage.objects.count(), page_count + 1)
