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
        """Clean, format, and validate URL field.

        Here we remove any path or querystring on the URL. This assumes we're
        only interested in the favicon for a site's main page. E.g. we're happy
        with the favicon for www.target.com, and don't need to separately save
        the favicon for www.target.com/some-other-page.
        """
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
        """Save form.

        This assumes we want to update the existing Favicon record if there's a
        new favicon URL, rather than creating a new record for the new favicon
        URL.
        """
        url = self.cleaned_data.get('url')
        favicon, created = Favicon.objects.get_or_create(url=url)
        favicon_url = favicon.get_favicon_for_url(url)

        if favicon.fav_url != favicon_url:
            favicon.fav_url = favicon_url
            favicon.modified = datetime.datetime.now()
            favicon.save()

        return favicon.fav_url
