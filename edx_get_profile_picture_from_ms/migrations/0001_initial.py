# -*- coding: utf-8 -*-
from django.db import migrations
from django.conf import settings
import logging

SECRET_KEY=settings.SOCIAL_AUTH_OAUTH_SECRETS.get("azuread-oauth2", "")
AZURE_CLIENT_ID=settings.AZURE_CLIENT_ID[0]

def create_provider_record(apps, schema_editor):
    OAuth2ProviderConfig = apps.get_model("third_party_auth", "OAuth2ProviderConfig")
    OAuth2ProviderConfig.objects.create(
        name="Microsoft",
        slug="azuread-oauth2",
        visible=True,
        enabled=True,
        backend_name="azuread-oauth2",
        key=AZURE_CLIENT_ID,
        secret=SECRET_KEY,
    )
    logging.info("Created Provider Configuration (OAuth) for Microsoft")


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(create_provider_record, reverse_code=migrations.RunPython.noop),
    ]
