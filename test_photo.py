#!/usr/bin/env python3
#coding: utf8
"""
Module de test de la classe Photo
"""
from photo import Photo

class TestPhoto:
    """
    Classe de test de la classe Photo
    """
    photo_jpg = Photo("test.jpg", "test")
    photo_bmp = None

    def test_attr(self):
        """
        Teste les attributs de l'objet
        """
        assert self.photo_jpg.name == "test.jpg"
        assert self.photo_jpg.taille[0] == 3072
        assert self.photo_jpg.taille[1] == 2304

    def test_str(self):
        """
        Tester la méthode magique __str__
        """
        assert str(self.photo_jpg) == "test.jpg"

    def test_false_format(self):
        """
        Tester si une erreur est renvoyée lorsqu'on essaye de lire une image
        qui n'est ni au format JPEG, ni au format PNG, ni au format GIF.
        """
        erreur = False
        try:
            self.photo_bmp = Photo("test.bmp", "test")
        except TypeError:
            erreur = True
        finally:
            assert erreur
