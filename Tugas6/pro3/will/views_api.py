from django.shortcuts import render
from django.http import JsonResponse
from will.models import Course
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
# GET TEST METHODS
# 
def apiCourse(request):
    if (request.method == "GET"):
        # Serialize the data into json        
        data = serializers.serialize("json", Course.objects.all())
        # Turn the JSON data into a dict and send as JSON response             
        return JsonResponse(json.loads(data), safe=False)

    if (request.method == "POST"):
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
        
    # PUT TEST METHODS
    # curl http://127.0.0.1:8000/api/course -X PUT --header "Content-Type: application/json" --data "{\"id\": 1,\"course_name\": \"perbarui course\"}"
    if request.method == "PUT":
        try:
            body = json.loads(request.body.decode("utf-8"))
            # Check if JSON data exists
            if not body:
                data = '{"message": "data is not json type!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)
            
            # Update an existing course
            course_id = body.get('id', None)
            if course_id is None:
                data = '{"message": "id is required!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)

            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                data = '{"message": "course does not exist!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)

            course.course_name = body['course_name']
            course.save()
            data = '{"message": "data successfully updated!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)

        except json.JSONDecodeError:
            data = '{"message": "invalid json data!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)
        
    if request.method == "DELETE":
        try:
            body = json.loads(request.body.decode("utf-8"))
            # Check if JSON data exists
            if not body:
                data = '{"message": "data is not json type!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)
            
            # Delete an existing course
            course_id = body.get('id', None)
            if course_id is None:
                data = '{"message": "id is required!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)

            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                data = '{"message": "course does not exist!"}'
                dumps = json.loads(data)
                return JsonResponse(dumps, safe=False)

            course.delete()
            data = '{"message": "data successfully deleted!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)

        except json.JSONDecodeError:
            data = '{"message": "invalid json data!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)
