# -*- coding: utf-8; mode: django -*-
from django.db import models
from django.test import TestCase
from django_any import any_model

class Good(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'django_any'

class TreeNode(models.Model):
    parent_node = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'django_any'

class TreeNodeWithGood(models.Model):
    parent_node = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=100)
    good = models.ForeignKey('Good')

    class Meta:
        app_label = 'django_any'

class TestRecursion(TestCase):
    def test_stop_recursion_for_model_with_one_foreign_field(self):
        try:
            tree_node = any_model(TreeNode)
        except RuntimeError:
            self.fail("Recursion is occured")

    def test_stop_recursion_for_model_with_another_foreign_field(self):
        tree_node = any_model(TreeNodeWithGood)

        self.assertEquals(tree_node.parent_node, None)
        self.assertTrue(bool(tree_node.good))

    def test_stop_recursion_should_not_erase_custom_values(self):
        tree_node = any_model(TreeNodeWithGood, name="Gena")

        self.assertEquals(tree_node.name, "Gena")

    def test_stop_recursion_should_not_erase_custom_values_for_recursive_model(self):
        tree_node = any_model(TreeNodeWithGood, parent_node=any_model(TreeNodeWithGood, name="Gena"))

        self.assertEquals(tree_node.parent_node.name, "Gena")