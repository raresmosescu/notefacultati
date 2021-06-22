from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from site_utility.models import Counties, Cities
from school.models import Facultati, Specializari
from prof.models import Profesori
from school.views import counties
from django.http import HttpResponse, JsonResponse


# Create your views here.
@csrf_exempt
def ajax_cities(request):
	county_name = request.POST['selected_county']
	county_id = counties[county_name]
	cities = {city.name:city.id for city in Cities.objects.filter(county_id = county_id).order_by('name_simple')}
	return JsonResponse(cities)


# Create your views here.
@csrf_exempt
def ajax_departments(request):
	school_id = request.POST['school_id']
	departments = {department.specializare : department.id_specializare for department in Specializari.objects.filter(id_facultate = school_id).order_by('specializare')}
	return JsonResponse(departments)


# @csrf_exempt
# def ajax_load_professors(request):
# 	school_id = request.POST['school_id']
# 	departments = {department.specializare : department.id_specializare for department in Specializari.objects.filter(id_facultate = school_id).order_by('specializare')}
# 	return JsonResponse(departments)

