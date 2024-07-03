# -*- coding: utf-8 -*-

import pytest
from bakerydemo.breads.models import BreadType, BreadIngredient

@pytest.mark.django_db
def test_crud_bread_type():
    initial_count = BreadType.objects.count()
    
    # Création d'un article
    bread_type = BreadType.objects.create(title="Test Bread Type")
    
    # Vérification que l'article a été créé
    assert BreadType.objects.count() == initial_count + 1
    
    # Trouver l'article créé
    bread_type = BreadType.objects.get(title="Test Bread Type")
    
    # Vérification du titre
    assert bread_type.title == "Test Bread Type"
    
    # Vérification de la modification
    bread_type.title = "Test Bread Type Modified"
    bread_type.save()
    
    # Trouver l'article modifié
    bread_type = BreadType.objects.get(title="Test Bread Type Modified")
    
    # Vérification du titre
    assert bread_type.title == "Test Bread Type Modified"
    
    # Suppression de l'article
    bread_type.delete()
    
    # Vérification de la suppression
    assert BreadType.objects.count() == initial_count
    
@pytest.mark.django_db
def test_crud_bread_ingredient():
    initial_count = BreadIngredient.objects.count()
    
    # Création d'un article
    bread_ingredient = BreadIngredient.objects.create(name="Test Bread Ingredient")
    
    # Vérification que l'article a été créé
    assert BreadIngredient.objects.count() == initial_count + 1
    
    # Trouver l'article créé
    bread_ingredient = BreadIngredient.objects.get(name="Test Bread Ingredient")
    
    # Vérification du titre
    assert bread_ingredient.name == "Test Bread Ingredient"
    
    # Vérification de la modification
    bread_ingredient.name = "Test Bread Ingredient Modified"
    bread_ingredient.save()
    
    # Trouver l'article modifié
    bread_ingredient = BreadIngredient.objects.get(name="Test Bread Ingredient Modified")
    
    # Vérification du titre
    assert bread_ingredient.name == "Test Bread Ingredient Modified"
    
    # Suppression de l'article
    bread_ingredient.delete()
    
    # Vérification de la suppression
    assert BreadIngredient.objects.count() == initial_count
