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
                settings.SOCIAL_AUTH_PIPELINE = [
                    'third_party_auth.pipeline.parse_query_params',
                    'social_core.pipeline.social_auth.social_details',
                    'social_core.pipeline.social_auth.social_uid',
                    'social_core.pipeline.social_auth.auth_allowed',
                    'social_core.pipeline.social_auth.social_user',
                    'third_party_auth.pipeline.associate_by_email_if_login_api',
                    'social_core.pipeline.user.get_username',
                    'third_party_auth.pipeline.set_pipeline_timeout',
                    'third_party_auth.pipeline.ensure_user_information',
                    'social_core.pipeline.user.create_user',
                    'social_core.pipeline.social_auth.associate_user',
                    'social_core.pipeline.social_auth.load_extra_data',
                    'social_core.pipeline.user.user_details',
                    'third_party_auth.pipeline.user_details_force_sync',
                    'third_party_auth.pipeline.set_id_verification_status',
                    'third_party_auth.pipeline.set_logged_in_cookies',
                    'third_party_auth.pipeline.login_analytics',
                    'azure_picture_profile.pipeline.download_profile_image',
                ]
                settings.SOCIAL_AUTH_AZUREAD_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'
