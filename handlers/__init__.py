from .admins import dp
from .users import dp

from .errors import dp # Ловит все текстовые сообщения поэтому мы импортируем этот хендлер последним

__all__ = ['dp'] # Список параметров которые можно импортировать из папки users