from PIL import Image, ImageChops


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
