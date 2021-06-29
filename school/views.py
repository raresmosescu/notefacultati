from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from site_utility.models import Counties, Cities
from prof.models import Profesori, Pareri
from site_utility.useful_functions import query_to_json_obj
from school.models import Facultati
from prof.views import get_stars
import statistics, math


counties = {county.name:county.id for county in Counties.objects.all().order_by('name_simple')}
first_county_id = list(counties.values())[0]
cities = {city.name:city.id for city in Cities.objects.filter(county_id = first_county_id).order_by('name_simple')}

# Create your views here.
def school_view(request, school_id):
	school_data = Facultati.objects.get(id_facultate = school_id)
	# # school_data['profesori'] = es_search.professors_by_school_id(school_id)
	# prof_data = query_to_json_obj(Profesori.objects.filter(id_facultate = school_id).order_by('-numarul_notelor'))

	prof_data = Profesori.objects.filter(id_facultate = school_id).order_by('-numarul_notelor')[:15]

	context = {'profs': prof_data, 'school': school_data}
	return render(request, 'school_view.html', context=context)

def school_add(request):
	if request.POST:
		data = request.POST
		print(data)
		return HttpResponse('success adding school')
	else:
		return render(request, "errors/not_available_yet.html")
		# # Disabled feature
		# return render(request, 'school_add.html', {'counties': counties, 'cities': cities})


def school_ranking(request):
	context = {'ranked_schools': generate_ranking_data()}
	return render(request, template_name="school_ranking.html", context = context)


def generate_ranking_data():

    rated_schools = Facultati.objects.filter(numar_pareri__gte = 1)
    rs_medie_note = [n.medie_note for n in rated_schools]
    rs_numar_pareri = [n.numar_pareri for n in rated_schools]

    output = []
    for school in rated_schools:

    	
    	data = {
    	'id_facultate': school.id_facultate,
    	'scor': calculate_rank(school.medie_note, school.numar_pareri, rs_numar_pareri),
    	'facultate': school.facultate,
    	'numar_pareri': school.numar_pareri,
    	'medie_note': school.medie_note
    	}

    	output.append(data)

    return sorted(output, key=lambda x:x['scor'], reverse=True)

def calculate_rank(r, n, number_of_ratings):
	'''
	number_of_ratings = list containing the ratings count for all objects
	r = average rating of object 
	n = sum total # of ratings of object
	m = average # of ratings for all objects
	w = weight - calculated by the formula n/(n+m)
	s = final score as a exponential function mapped from 0 to 1
	'''
	m = sum(number_of_ratings)/len(number_of_ratings)
	w = n/(n+m)
	s = 1 - 1/math.exp(w*r)
	return float(f'{s*100:.2f}')