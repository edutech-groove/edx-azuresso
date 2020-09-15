import logging
from io import BytesIO

import urllib2
from django.core import files
from django.utils.timezone import now
from openedx.core.djangoapps.profile_images.images import create_profile_images
from openedx.core.djangoapps.user_api.accounts.image_helpers import get_profile_image_names, set_has_profile_image

log = logging.getLogger(__name__)

def download_profile_image(user=None, *args, **kwargs):
    if user and not user.profile.profile_image_uploaded_at:
        try:
            username = user.username

            req = urllib2.Request('https://graph.microsoft.com/v1.0/me/photo/$value')
            req.add_header('Authorization', 'Bearer {0}'.format(kwargs['response']['access_token']))
            resp = urllib2.urlopen(req)
            content = resp.read()

            fp = BytesIO()
            fp.write(content)
            image_file = files.File(fp)
            profile_image_names = get_profile_image_names(user.username)

            create_profile_images(image_file, profile_image_names)
            user.profile.profile_image_uploaded_at = now()
            user.save()
            log.info(
                LOG_MESSAGE_CREATE,
                {'image_names': profile_image_names.values(), 'user_id': user.id}
            )
        except Exception as e:
            log.exception('Error when downloading user image from Microsoft API', exc_info=True)
