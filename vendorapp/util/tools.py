from PIL import Image, ImageChops
from django.core.mail import send_mail


def resize_image(input_file_path, output_file_path, size=(200, 200)):
    # Keeping aspect ratio intact the missing areas
    # are compensated by white color.

    image = Image.open(input_file_path)
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size

    thumb = image.crop((0, 0, size[0], size[1]))

    offset_x = max((size[0] - image_size[0]) // 2, 0)
    offset_y = max((size[1] - image_size[1]) // 2, 0)

    thumb = ImageChops.offset(thumb, offset_x, offset_y)
    thumb.save(output_file_path)


def welcome_notification(user):

    subject = 'Zoobaay registration successful. '
    message = 'Hello {} welcome to ZooBaay. Your {} account has'
    'been created.'.format(user.username, user.user_type)

    send_mail(
        subject,
        message,
        'zoobaay@gmail.com',
        user.email
    )
