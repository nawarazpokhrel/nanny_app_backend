from django import forms

from django.core.exceptions import ValidationError


def validate_file_size(value):
    if value:
        filesize = value.size
        print(value.size)
        if filesize > 2097152:  # 2MB in bytes
            raise ValidationError("The maximum file size that can be uploaded is 2MB.")
    else:
        return value
