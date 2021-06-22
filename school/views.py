from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from site_utility.models import Counties, Cities
from prof.models import Profesori
from site_utility.useful_functions import query_to_json_obj
from school.models import Facultati
from prof.views import get_stars

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