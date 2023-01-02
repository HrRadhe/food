from django.core.exceptions import ValidationError
import os

def allow_only_images(value):               #   0 .  1
    ext =  os.path.splitext(value.name)[1] #cover-im.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('This is not valid file')