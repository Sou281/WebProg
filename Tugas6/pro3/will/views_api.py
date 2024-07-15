from django.shortcuts import render
from django.http import JsonResponse
from will.models import Course
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json ,requests

@csrf_exempt
def consumeApiGet(request):
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    data = response.json()
    return render(request, "api-get.html", {'data': data})

@csrf_exempt
def apiCourse(request):
    if request.method == "GET":
        # Serialize the data into json
        data = serializers.serialize("json", Course.objects.all())
        # Turn the JSON data into a dict and send as JSON response
        return JsonResponse(json.loads(data), safe=False)

    if request.method == "POST":
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        # filter data
        if not body:
            data = '{"message": "data is not json type!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)
        else:
            created = Course.objects.create(
                course_name=body['course_name']
            )
            data = '{"message": "data successfully created!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)

    if request.method == "PUT":
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        # filter data
        if not body:
            data = '{"message": "data is not json type!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)
        else:
            try:
                course = Course.objects.get(pk=body['id'])
                course.course_name = body['course_name']
                course.save()
                data = '{"message": "data successfully updated!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)
            except Course.DoesNotExist:
                data = '{"message": "course not found!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)

    if request.method == "DELETE":
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        # filter data
        if not body:
            data = '{"message": "data is not json type!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)
        else:
            try:
                course = Course.objects.get(pk=body['id'])
                course.delete()
                data = '{"message": "data successfully deleted!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)
            except Course.DoesNotExist:
                data = '{"message": "course not found!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)