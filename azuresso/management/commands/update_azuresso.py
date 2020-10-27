from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
import logging

AZURE_CLIENT_ID=settings.AZURE_CLIENT_ID
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update Client ID for Microsoft'


    def handle(self, *args, **options):
        try:
            OAuth2ProviderConfig = apps.get_model('third_party_auth', 'OAuth2ProviderConfig')
            microsoft = OAuth2ProviderConfig.objects.filter(name='Microsoft').latest('id')
            if microsoft.key == "": 
                microsoft.key = AZURE_CLIENT_ID
                microsoft.save()
                self.stdout.write(self.style.SUCCESS('Updated Provider Configuration (OAuth) for Microsoft with key %s' % AZURE_CLIENT_ID))
            else:
                self.stdout.write(self.style.WARNING('Exist Client ID: %s' % microsoft.key))
        except Exception as e:
            log.exception('Error when updating Client ID from Microsoft', exc_info=True)
