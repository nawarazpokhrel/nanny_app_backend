from django.contrib.auth import get_user_model

from apps.common.usecases import BaseUseCase
User=get_user_model()

class CreateUserUseCase(BaseUseCase):
    def __init__(self, serializer):
        super().__init__(serializer)

    def _factory(self):
        password = self._data.pop('password')
        user = User(**self._data)
        user.save()
        user.set_password(password)
        user.save()