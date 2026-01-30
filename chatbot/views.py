import json
from django.http import JsonResponse
from dashboard.decorators import role_base
from .utils import get_chatbot_answer

@role_base(required_role="student")
def chatbot_api(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("message")

            if not question:
                return JsonResponse({"reply": "Please ask a question."})

            answer = get_chatbot_answer(question)
            return JsonResponse({"reply": answer})

        except Exception as e:
            print("CHATBOT ERROR:", e)   # 👈 ADD THIS
            return JsonResponse(
                {"reply": f"Error: {str(e)}"},
            status=500
            )

    return JsonResponse(
        {"message": "Chatbot API endpoint. Use POST request."},
        status=405
    )
