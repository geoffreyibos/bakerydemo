from django.contrib.auth import get_user_model
from django.test import TestCase
from wagtail.models import Page, Collection, Site
from django.urls import reverse
from rest_framework.test import APIClient

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
import requests

BASE = "http://localhost:8000"
BASE_API = BASE + "/api/v2/"

class ApiTests(TestCase):

    def test_pages_listing(self):
        url = BASE_API + "pages/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        
        self.assertTrue("total_count" in response.json()["meta"].keys())
        self.assertTrue("items" in response.json().keys())
        
        for value in response.json()["items"]:
            self.assertTrue("id" in value.keys())
            self.assertTrue("meta" in value.keys())
            self.assertTrue("title" in value.keys())
            
            self.assertTrue("type" in value["meta"].keys())
            self.assertTrue("detail_url" in value["meta"].keys())
            self.assertTrue("html_url" in value["meta"].keys())
            self.assertTrue("slug" in value["meta"].keys())
            self.assertTrue("first_published_at" in value["meta"].keys())
            self.assertTrue("locale" in value["meta"].keys())
            
    def test_pages_detail(self):
        url = BASE_API + "pages/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        
        # Testing on the first 5 items
        for value in response.json()["items"][::5]:
            detail_url = value["meta"]["detail_url"]
            response = requests.get(detail_url)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue("id" in response.json().keys())
            self.assertTrue("meta" in response.json().keys())
            self.assertTrue("title" in response.json().keys())
            self.assertTrue("type" in response.json()["meta"].keys())
            self.assertTrue("detail_url" in response.json()["meta"].keys())
            self.assertTrue("html_url" in response.json()["meta"].keys())
            self.assertTrue("slug" in response.json()["meta"].keys())
            self.assertTrue("first_published_at" in response.json()["meta"].keys())
            self.assertTrue("locale" in response.json()["meta"].keys())
            self.assertTrue("show_in_menus" in response.json()["meta"].keys())
            self.assertTrue("seo_title" in response.json()["meta"].keys())
            self.assertTrue("search_description" in response.json()["meta"].keys())
            self.assertTrue("alias_of" in response.json()["meta"].keys())
            self.assertTrue("parent" in response.json()["meta"].keys())
            self.assertTrue("locale" in response.json()["meta"].keys())
            
    def test_pages_detail_not_found(self):
        url = BASE_API + "pages/100000/"
        response = requests.get(url)
        
        self.assertEqual(response.status_code, 404)
        
    def test_images_listing(self):
        url = BASE_API + "images/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        
        self.assertTrue("total_count" in response.json()["meta"].keys())
        self.assertTrue("items" in response.json().keys())
        
        for value in response.json()["items"]:
            self.assertTrue("id" in value.keys())
            self.assertTrue("meta" in value.keys())
            self.assertTrue("title" in value.keys())
            
            #  "id": 9,
            # "meta": {
            #     "type": "wagtailimages.Image",
            #     "detail_url": "http://127.0.0.1:8000/api/v2/images/9/",
            #     "tags": [],
            #     "download_url": "/media/original_images/breads1.jpg"
            # },
            # "title": "Breads 1"
            
            self.assertTrue("type" in value["meta"].keys())
            self.assertTrue("detail_url" in value["meta"].keys())
            self.assertTrue("tags" in value["meta"].keys())
            self.assertTrue("download_url" in value["meta"].keys())
            
    def test_images_detail(self):
        url = BASE_API + "images/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        
        # Testing on the first 5 items
        for value in response.json()["items"][::5]:
            detail_url = value["meta"]["detail_url"]
            response = requests.get(detail_url)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue("id" in response.json().keys())
            self.assertTrue("meta" in response.json().keys())
            self.assertTrue("title" in response.json().keys())
            self.assertTrue("width" in response.json().keys())
            self.assertTrue("height" in response.json().keys())
            self.assertTrue("type" in response.json()["meta"].keys())
            self.assertTrue("detail_url" in response.json()["meta"].keys())
            self.assertTrue("tags" in response.json()["meta"].keys())
            self.assertTrue("download_url" in response.json()["meta"].keys())
            
            download_url = response.json()["meta"]["download_url"]
            response = requests.get(BASE + download_url)
            self.assertEqual(response.status_code, 200)
            
    def test_images_detail_not_found(self):
        url = BASE_API + "images/100000/"
        response = requests.get(url)
        
        self.assertEqual(response.status_code, 404)
        
    def test_documents_listing(self):
        url = BASE_API + "documents/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        
        self.assertTrue("total_count" in response.json()["meta"].keys())
        self.assertTrue("items" in response.json().keys())
        
        for value in response.json()["items"]:
            self.assertTrue("id" in value.keys())
            self.assertTrue("meta" in value.keys())
            self.assertTrue("title" in value.keys())
            
            self.assertTrue("type" in value["meta"].keys())
            self.assertTrue("tags" in value["meta"].keys())
            self.assertTrue("detail_url" in value["meta"].keys())
            self.assertTrue("download_url" in value["meta"].keys())
            
    def test_documents_detail(self):
        url = BASE_API + "documents/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        
        # Testing on the first 5 items
        for value in response.json()["items"][::5]:
            detail_url = value["meta"]["detail_url"]
            response = requests.get(detail_url)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue("id" in response.json().keys())
            self.assertTrue("meta" in response.json().keys())
            self.assertTrue("title" in response.json().keys())
            self.assertTrue("type" in response.json()["meta"].keys())
            self.assertTrue("detail_url" in response.json()["meta"].keys())
            self.assertTrue("tags" in response.json()["meta"].keys())
            self.assertTrue("download_url" in response.json()["meta"].keys())
            
            download_url = response.json()["meta"]["download_url"]
            response = requests.get(download_url)
            self.assertEqual(response.status_code, 200)
            
    def test_documents_detail_not_found(self):
        url = BASE_API + "documents/100000/"
        response = requests.get(url)
        
        self.assertEqual(response.status_code, 404)