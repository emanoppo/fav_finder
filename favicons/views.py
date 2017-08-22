"""Favicon views."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View

from forms import FavFinderForm


class FavFinder(View):
    """Favicon finder view."""

    form_class = FavFinderForm
    initial = {}
    template_name = 'fav_finder.html'

    def get(self, request):
        """Handle GET request for favicon finder."""
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handle POST request for favicon finder."""
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        favicon_url = form.save()

        if favicon_url:
            return render(request, self.template_name, {'form': form, 'favicon_url': favicon_url})
        else:
            return render(request, self.template_name, {'form': form, 'favicon_url': 'https://media.giphy.com/media/AYKv7lXcZSJig/giphy.gif', 'error': 'Oh no, we couldn\'t find a favicon for this site!'})
