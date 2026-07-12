from django.conf import settings


def settings_flags(request):
    """Expone banderas de settings a todas las plantillas.

    `DEBUG` se usa para no cargar el script de estadísticas (Umami) durante
    el desarrollo local, de forma que el tráfico de desarrollo no ensucie las
    métricas. El script solo se incluye cuando DEBUG es False (producción).
    """
    return {'DEBUG': settings.DEBUG}