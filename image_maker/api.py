from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from django.conf import settings
import urllib
import cStringIO
import os


class ImagesMaker(object):
    @classmethod
    def create_top_ten_picture(cls, top_likers):
        top_im = Image.open(settings.IMAGES['top_ten'])
        for liker in top_likers:
            l
    @classmethod
    def create_small_stat_image(cls, info):
        """
            Creating Small Box Of Statistics
            params:
                info = {
                    'title' -> Top Title Naming,
                    'image_profile' -> Image Profile Of User
                    'font_icon' -> Icon To Write. like : unichr(0x087d)
                    'value' -> Stats Number
                    'file_name' -> file name
                }
        """
        font_dejavu = ImageFont.truetype(settings.FONTS['dejavu'], 35)
        font_awsome = ImageFont.truetype(settings.FONTS['awesome'], 35)

        back_im = Image.open(settings.IMAGES['small'])

        file_ = cStringIO.StringIO(
            urllib.urlopen(info['image_profile']).read())
        back_im.paste(Image.open(file_), (25, 90))

        draw = ImageDraw.Draw(back_im)

        draw.text((25, 20), info['title'], (51, 51, 51), font=font_dejavu)
        draw.text((100, 100), info['font_icon'], (0, 0, 0), font=font_awsome)
        size = draw.textsize(info['font_icon'], font=font_awsome)
        draw.text(
            (size[0] + 100, 100), info['value'], (0, 0, 0), font=font_dejavu)

        draw = ImageDraw.Draw(back_im)
        back_im.save(
            os.path.join(settings.STATICFILES_DIRS[0], 'images', '{}.png'.format(info['file_name'])))

    @classmethod
    def create_stats_images(cls, user):
        """
            get User object and 
            creating all photos for this user
        """
        if 'total' in user['stats']:
            cls.create_small_stat_image({
                'font_icon': unichr(0xF087),
                'title': 'My Total Like',
                'value': user['stats']['total'],
                'image_profile': user['stats']['profile_photo']['data']['url'],
                'file_name': '1'
            })
        if 'photos' in user['stats']:
            cls.create_small_stat_image({
                'font_icon': unichr(0xF087),
                'title': 'My Total Like',
                'value': user['stats']['total'],
                'image_profile': user['stats']['profile_photo']['data']['url'],
                'file_name': '1'
            })
        if 'videos' in user['stats']:
            pass
        if 'posts' in user['stats']:
            pass
        if 'top_likers' in user['stats']:
            pass

