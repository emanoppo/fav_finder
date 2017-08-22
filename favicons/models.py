"""Favicon model."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
import requests

from django.db import models


class Favicon(models.Model):
    """Favicon model."""

    # If I were collecting more information related to a given URL, I would
    # most likely want to pull out URL into its own model and the url field here
    # would be a ForeignKey to that model.
    url = models.CharField(max_length=255, unique=True)
    fav_url = models.CharField(max_length=255, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_favicon_for_url(self, url):
        """Extract favicon URL from a given URL.

        Standardize URL format to http://www.website.com/favicon.ico
        """
        headers = {'User-Agent': 'Chrome/2.18.4'}

        try:
            request = requests.get(url, headers=headers)
        except Exception:
            return None

        if request.status_code != 200:
            return None

        content = BeautifulSoup(request.content, 'html.parser')

        try:
            favicon_url = content.find('link', attrs={'rel': 'shortcut icon'})['href']
        except Exception:
            try:
                favicon_url = content.find('link', attrs={'rel': 'icon'})['href']
            except Exception:
                try:
                    favicon_url = url + '/favicon.ico'
                except Exception:
                    return None

        if not favicon_url.startswith('http'):
            if favicon_url.startswith('//'):
                favicon_url = 'http:' + favicon_url
            elif favicon_url.startswith('/'):
                favicon_url = url + favicon_url
            else:
                return None

        try:
            fav_request = requests.get(favicon_url, headers=headers)
        except Exception:
            return None

        if fav_request.status_code != 200:
            return None

        return favicon_url
