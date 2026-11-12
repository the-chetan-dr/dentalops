from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def healthz(request):
    """Lightweight Render health check; verifies the app and database are reachable."""
    try:
        connection.ensure_connection()
    except Exception:  # noqa: BLE001 - health endpoint must report dependency failure.
        return JsonResponse({"status": "unhealthy"}, status=503)
    return JsonResponse({"status": "ok"})
