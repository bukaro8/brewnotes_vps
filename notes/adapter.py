from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse


class SocialOnlySignupAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Only allow signups coming from social accounts
        return bool(request.session.get('socialaccount_sociallogin'))
