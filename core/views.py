from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def dashboard_callback(request, context):
    current_tab = request.session.get('current_tab', 'overview')
    context.update({
        "tabs": ["Overview", "Chatbots", "Subscriptions"],
        "current_tab": current_tab,
        "chatbots": range(9),
        "subscriptions": range(9),
    })

    return context

@csrf_exempt
def set_tab_session(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tab = data.get("tab")
        request.session["current_tab"] = tab
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "invalid method"}, status=405)
