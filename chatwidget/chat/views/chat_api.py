from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .langchain import chat

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])  # Allow POST and OPTIONS methods
def chat_api(request):
    if request.method == 'OPTIONS':
        # Handle the preflight CORS request
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'  # Adjust this as necessary for your setup
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if request.method == 'POST':
        # Directly pass the request to the langchain chat function
        response = chat(request)
        #print('Chat Response:', response.content)  
        return response
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



