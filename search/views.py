from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from collections import defaultdict
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .elastic_search_utils import es_search
from prof.models import Profesori
from school.models import Facultati
from django.db.models import Q
from django.urls import reverse


def search_page(request):
	return render(request, 'search.html', {})

def search(request):
	if request.method == "GET":
		if 'query' in request.GET:
			query = request.GET['query']
			schools = es_search.schools(query, limit=20)
			return render(request, 'results_schools.html', {'schools': schools})
	return redirect('/')
			

# Create your views here.
def results(request):
	if request.method == "GET":
		if 'query' in request.GET:
			query = request.GET['query']
			schools = es_search.schools(query, limit=20)
			return render(request, 'results_schools.html', {'schools': schools})

def school_profs(request, id_facultate):
	query = request.GET['query']
	
	profs = search_name(query, id_facultate)
	fac = Facultati.objects.get(id_facultate=id_facultate)
			 
	return render(request, 'school_profs_results.html', {'profs': profs, 'fac': fac, 'query': query})


@csrf_exempt
def ajax_school(request):
	query = request.POST['school']	
	results = es_search.schools(query, limit=5)
	print(results)
	return JsonResponse(json.dumps(results),safe=False)


# @csrf_exempt
# def ajax_professor(request):
# 	query = request.POST['school']	
# 	results = es_search.professors(query, limit=5)
# 	# print(results)
# 	return JsonResponse(json.dumps(results), safe=False)


def tokenize_query(query:str):
	names = [n for n in query.split() if len(n) > 2]
	return names

def search_name(query, id_facultate):
	names = tokenize_query(query)
	if len(names) == 1:
		profs = Profesori.objects.filter(id_facultate=id_facultate).filter(Q(nume__icontains=names[0]))[:15]
	if len(names) == 2:
		profs = Profesori.objects.filter(id_facultate=id_facultate).filter(Q(nume__icontains=names[0]) & Q(nume__icontains=names[1]))[:15]
	if len(names) > 2:
		profs = []
	if not query:
		profs = []
	return profs