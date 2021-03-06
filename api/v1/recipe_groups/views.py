#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from django.db.models import Q
from django.db.models import Count
from v1.recipe_groups.models import Cuisine, Course, Tag
from v1.recipe.models import Recipe
from v1.recipe_groups import serializers
from rest_framework import permissions
from rest_framework import viewsets
from v1.common.permissions import IsOwnerOrReadOnly
from v1.common.recipe_search import get_search_results


class CuisineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    queryset = Cuisine.objects.all()
    serializer_class = serializers.CuisineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'


class CuisineCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    serializer_class = serializers.CuisineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects

        filter_set = {}
        if 'course' in self.request.query_params:
            try:
                filter_set['course'] = Course.objects.get(
                    slug=self.request.query_params.get('course')
                )
            except:
                return []

        if 'rating' in self.request.query_params:
            filter_set['rating'] = self.request.query_params.get('rating')

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)

        return Cuisine.objects.filter(recipe__in=query).annotate(total=Count('recipe', distinct=True))


class CourseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'


class CourseCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    serializer_class = serializers.CourseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects

        filter_set = {}
        if 'cuisine' in self.request.query_params:
            try:
                filter_set['cuisine'] = Cuisine.objects.get(
                    slug=self.request.query_params.get('cuisine')
                )
            except:
                return []

        if 'rating' in self.request.query_params:
            filter_set['rating'] = self.request.query_params.get('rating')

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)

        return Course.objects.filter(recipe__in=query).annotate(total=Count('recipe', distinct=True))


class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    lookup_field = 'title'
