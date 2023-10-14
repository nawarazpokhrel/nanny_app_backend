class BaseUseCase:
    def __init__(self, serializer):
        self._serializer = serializer
        self._data = serializer.validated_data if self._serializer else None

    def execute(self):
        self._is_valid()
        return self._factory()

    def _is_valid(self):
        return True

    def _factory(self):
        raise NotImplementedError("Sub class must override this class.")
