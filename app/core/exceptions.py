"""
Exceções customizadas para a lógica de negócio da aplicação.
"""

class MiteScanError(Exception):
    """Classe base para exceções da aplicação."""
    detail: str = "Um erro interno ocorreu."
    status_code: int = 500

class ResourceNotFoundError(MiteScanError):
    """Lançado quando um recurso não é encontrado no banco de dados."""
    status_code = 404
    def __init__(self, resource_name: str = "Recurso"):
        self.detail = f"{resource_name} não encontrado."

class DuplicateEntryError(MiteScanError):
    """Lançado quando uma tentativa de criar uma entrada duplicada é feita."""
    status_code = 400
    def __init__(self, field_name: str = "Entrada"):
        self.detail = f"{field_name} já cadastrado."
