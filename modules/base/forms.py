from typing import Any, Optional

from django.db.models import Model
from django.utils.translation import get_language

from modules.store.models import Store


def get_field_from_info(obj: Model, related_name: str, field_name: str) -> Optional[Any]:
    current_language = get_language()
    store = Store.get_by_code_or_default(current_language)

    related_obj = getattr(obj, related_name).filter(store=store).first()
    if not related_obj:
        return None

    return getattr(related_obj, field_name, None)
