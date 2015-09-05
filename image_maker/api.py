from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from django.conf import settings
import urllib
import cStringIO
import os


class ImagesMaker(object):

    @classmethod
    def create_top_ten_picture(cls, top_likers, name):

        top_im = Image.open(settings.IMAGES['top_ten'])
        images_index = (
            (225, 30),
            (140, 110),
            (330, 110),
            (30, 175),
            (90, 175),
            (150, 175),
            (210, 175),
            (270, 175),
            (330, 175),
            (390, 175),
        )

        for index, liker in enumerate(top_likers):
            file_ = cStringIO.StringIO(
                urllib.urlopen(liker['pic_small']).read())
            top_im.paste(Image.open(file_), images_index[index])

        draw = ImageDraw.Draw(top_im)
        top_im.save(
            os.path.join(settings.STATICFILES_DIRS[0], 'images', '{}_{}.png'.format(name,'top_likers')))

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
        back_im.paste(Image.open(file_), (105, 90))

        draw = ImageDraw.Draw(back_im)
        font_dejavu.size = 20

        draw.text((75, 20), info['title'], (8, 102, 198), font=font_dejavu)
        draw.text((190, 100), info['font_icon'], (0, 0, 0), font=font_awsome)
        size = draw.textsize(info['font_icon'], font=font_awsome)
        draw.text(
            (size[0] + 190, 100), str(info['value']), (0, 0, 0), font=font_dejavu)

        draw = ImageDraw.Draw(back_im)
        back_im.save(
            os.path.join(settings.STATICFILES_DIRS[0], 'images', '{}.png'.format(info['file_name'])))

    @classmethod
    def create_stats_images(cls, user):
        """
            get User object and 
            creating all photos for this user
        """
        image_base_name = user['fb_id']
        if 'total' in user['stats']:
            cls.create_small_stat_image({
                'font_icon': unichr(0xF087),
                'title': 'I Worth ',
                'value': user['stats']['total'],
                'image_profile': user['profile_photo']['data']['url'],
                'file_name': '{}_{}'.format(image_base_name,'total')
            })
        if 'photos' in user['stats']:
            cls.create_small_stat_image({
                'font_icon': unichr(0xF087),
                'title': 'My Total Like On Photos',
                'value': user['stats']['total'],
                'image_profile': user['profile_photo']['data']['url'],
                'file_name': '{}_{}'.format(image_base_name,'photos')
            })

        if 'videos' in user['stats']:
            cls.create_small_stat_image({
                'font_icon': unichr(0xF087),
                'title': 'My Total Like On Videos',
                'value': user['stats']['videos'],
                'image_profile': user['profile_photo']['data']['url'],
                'file_name': '{}_{}'.format(image_base_name,'videos')
            })
        if 'posts' in user['stats']:
            cls.create_small_stat_image({
                'font_icon': unichr(0xF087),
                'title': 'My Total Like On Photos',
                'value': user['stats']['posts'],
                'image_profile': user['profile_photo']['data']['url'],
                'file_name': '{}_{}'.format(image_base_name,'posts')
            })
        if 'top_likers' in user['stats']:
            cls.create_top_ten_picture(user['stats']['top_likers'],image_base_name)
