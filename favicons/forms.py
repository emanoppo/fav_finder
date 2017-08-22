"""Forms for favicon finder."""
import datetime
import requests
from urlparse import urlparse

from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from models import Favicon


class FavFinderForm(forms.Form):
    """Favicon finder form."""

    url = forms.CharField(required=True)

    def clean_url(self):
        """Clean, format, and validate URL field."""
        url = self.cleaned_data.get('url')
        url = url.strip()

        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        validate = URLValidator()

        try:
            validate(url)
        except ValidationError, e:
            raise forms.ValidationError('Invalid URL %s: %s' % (url, str(e)))

        # follow redirect, strip any path or querystring
        try:
            request = requests.get(url, headers={'User-Agent': 'Chrome/2.18.4'})
        except Exception:
            raise forms.ValidationError('Sorry, there was an error connecting to that website!')

        parsed_url = urlparse(request.url)
        url = parsed_url.scheme + '://' + parsed_url.netloc

        return url

    def save(self):
        """Save form."""
        url = self.cleaned_data.get('url')
        favicon, created = Favicon.objects.get_or_create(url=url)
        favicon_url = favicon.get_favicon_for_url(url)

        if favicon.fav_url != favicon_url:
            favicon.fav_url = favicon_url
            favicon.modified = datetime.datetime.now()
            favicon.save()

        return favicon.fav_url
