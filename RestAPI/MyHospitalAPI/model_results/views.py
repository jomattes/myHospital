# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from model_results.models import Results
from model_results.serializers import ResultSerializer

# Create your views here.
@csrf_exempt
def result_list(request):
    """
    List all results, or create a new result.
    """

    if request.method == 'GET':
        result = Results.objects.all()
        serialzier = ResultSerializer(result, many=True)
        return JsonResponse(serialzier.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ResultSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def result_detail(request, pk):
    """
    Retrieve, update, or delete a single result.
    """

    try:
        result = Results.objects.get(pk=pk)
    except Results.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ResultSerializer(result)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ResultSerializer(result, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        result.delete()
        return HttpResponse(status=204)