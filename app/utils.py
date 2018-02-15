import logging
import random
import string

import requests
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


def generate_random_key(length=4):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def load_remote_m3u8(link, playlist, remove_existed=False):
    from app.models import Channel, Upload

    r = requests.get(link)
    if not r.ok:
        return

    upload = Upload(
        user=playlist.user,
        info=link
    )
    upload.file.save('requests.m3u8', ContentFile(r.content))
    upload.save()

    if remove_existed:
        playlist.channels.all().delete()

    duration = title = group = path = None
    for line in r.iter_lines(decode_unicode=True):
        line = line.decode("utf-8")

        if line == '#EXTM3U':
            continue

        if line.startswith('#EXTINF:'):
            duration, title = line[8:].split(',')
            continue

        if line.startswith('#EXTGRP:'):
            group = line[8:]
            continue

        if line.startswith('#'):
            logger.warning('Unsupported line skipped: {}'.format(line))
            continue

        if line:
            path = line

            Channel.objects.create(
                playlist=playlist,
                title=title,
                duration=duration,
                group=group,
                path=path
            )


def load_m3u8_from_file(fo, playlist, remove_existed=False):
    from app.models import Channel, Upload

    Upload.objects.create(
        user=playlist.user,
        info=fo.name,
        file=fo
    )

    if remove_existed:
        playlist.channels.all().delete()

    duration = title = group = path = None
    for line in fo.read().splitlines():
        line = line.decode("utf-8")

        if line == '#EXTM3U':
            continue

        if line.startswith('#EXTINF:'):
            duration, title = line[8:].split(',')
            continue

        if line.startswith('#EXTGRP:'):
            group = line[8:]
            continue

        if line.startswith('#'):
            logger.warning('Unsupported line skipped: {}'.format(line))
            continue

        if line:
            path = line

            Channel.objects.create(
                playlist=playlist,
                title=title,
                duration=duration,
                group=group,
                path=path
            )
