from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from django.conf import settings
import urllib
import cStringIO
import os


class ImagesMaker(object):

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
                }
        """
        font_dejavu = ImageFont.truetype(settings.FONTS['dejavu'], 35)
        font_awsome = ImageFont.truetype(settings.FONTS['awesome'], 35)
        back_im = Image.open(settings.IMAGES['small'])

        file_ = cStringIO.StringIO(
            urllib.urlopen(info['image_profile']).read())
        back_im.paste(Image.open(file_), (90, 100))
        draw = ImageDraw.Draw(back_im)  

        draw.text((20, 10), info['title'], (0, 0, 0), font=font_dejavu)

        draw.text((70, 100), info['font_icon'], (0, 0, 0), font=font_awsome)
        size = draw.textsize(info['font_icon'], font=font_awsome)
        draw.text(
            (size[0] + 70, 100), info['value'], (0, 0, 0), font=font_dejavu)

        draw = ImageDraw.Draw(back_im)
        back_im.save(
            os.path.join(settings.STATICFILES_DIRS[0], 'images', '1.png'))
