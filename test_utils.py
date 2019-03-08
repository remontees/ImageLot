#!/usr/bin/env python3
#coding: utf8
"""
Module de test de la classe Utils
"""
from utils import calcul_bordure

def test_calcul_bordure():
    """
    Classe de test de la classe Photo
    """
    assert calcul_bordure(0, 0) == 0
    assert calcul_bordure(200, 2) == 204
