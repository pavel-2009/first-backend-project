from datetime import datetime


def current_year(request):
    """Добавляет в контекст переменную с текущим годомо."""
    year = datetime.now().year
    return {
        'year': year,
    }
