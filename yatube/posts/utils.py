from django.core.paginator import Paginator

from yatube.settings import POSTS_PER_PAGE


def get_paginator(items_list):
    return Paginator(items_list, POSTS_PER_PAGE)
