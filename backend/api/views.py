from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..langgraph_workflow import handle_query
import json

@csrf_exempt
def query_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query")
        result = handle_query(query)
        return JsonResponse(result)
    return JsonResponse({"error": "Invalid request method"}, status=400)
