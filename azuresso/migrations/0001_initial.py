# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-03 08:18
from django.db import migrations
from django.conf import settings
from django.contrib.sites.models import Site
import logging

AZURE_CLIENT_ID=settings.AZURE_CLIENT_ID
LMS_HOST = settings.ENV_TOKENS.get("LMS_BASE")

def _get_or_create_site():
    site_lms = Site.objects.filter(name=LMS_HOST)
    if not site_lms:
        site_lms = Site.objects.create(name=LMS_HOST, domain=LMS_HOST)
        return site_lms.id
    else:
        return site_lms[0].id

def create_provider_record(apps, schema_editor):
    OAuth2ProviderConfig = apps.get_model("third_party_auth", "OAuth2ProviderConfig")
    OAuth2ProviderConfig.objects.create(
        name="Microsoft",
        slug="azuread-oauth2",
        visible=True,
        enabled=True,
        backend_name="azuread-oauth2",
        site_id=_get_or_create_site(),
        key=AZURE_CLIENT_ID,
    )
    logging.info("Created Provider Configuration (OAuth) for Microsoft")


class Migration(migrations.Migration):

    dependencies = [
        ('third_party_auth', '0022_auto_20181012_0307'),
    ]

    operations = [
        migrations.RunPython(create_provider_record, reverse_code=migrations.RunPython.noop),
    ]
