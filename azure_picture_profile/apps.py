"""
App configuration for azure_picture_profile.
"""

from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings


class EdxAzureSSOConfig(AppConfig):
    """
    azure_picture_profile configuration.
    """
    name = 'azure_picture_profile'
    verbose_name = 'azure_picture_profile'

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'aws': {'relative_path': 'settings.aws'},
                'production': {'relative_path': 'settings.production'},
                'devstack': {'relative_path': 'settings.devstack_docker'}
            }
        }
    }

    def ready(self):
        if settings.FEATURES.get('ENABLE_AZURE_PICTURE_PROFILE', False):
            if settings.FEATURES.get('ENABLE_THIRD_PARTY_AUTH', False):
                settings.SOCIAL_AUTH_PIPELINE += [
                    'azure_picture_profile.pipeline.download_profile_image',
                ]
                settings.SOCIAL_AUTH_AZUREAD_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'
