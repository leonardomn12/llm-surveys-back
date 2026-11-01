class AIServiceException(Exception):
    """Excepción al comunicarse con el servicio de IA"""

    def __init__(self, message: str, status_code: int):
        super().__init__()
        self.message = message
        self.status_code = status_code


class NotItemException(Exception):
    """Excepción cuando el cuestionario no tiene items"""

    def __init__(self, message: str, status_code: int):
        super().__init__()
        self.message = message
        self.status_code = status_code
