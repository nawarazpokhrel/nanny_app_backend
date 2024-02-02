from django import forms

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_file_size(value):
    if value:
        filesize = value.size
        print(value.size)
        if filesize > 2097152:  # 2MB in bytes
            raise ValidationError("The maximum file size that can be uploaded is 2MB.")
    else:
        return value


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)
