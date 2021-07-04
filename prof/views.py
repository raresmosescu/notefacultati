from django.shortcuts import render, redirect
from django.http import HttpResponse
from search.elastic_search_utils import es_search
from .models import Profesori, Pareri, Taguri
from user.models import AuthUser
from school.models import Facultati
from site_utility.useful_functions import query_to_json_obj, json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from collections import defaultdict
from django.contrib import messages
import requests
from django.db import connection


# Create your views here.
def prof_view(request, prof_id=0):
	if prof_id != 0:
		prof_data = query_to_json_obj(Profesori.objects.filter(id_profesor = prof_id))[0]['fields']
		school_data = query_to_json_obj(Facultati.objects.filter(id_facultate = prof_data['id_facultate']))[0]['fields']
		reviews = Pareri.objects.filter(profesor = prof_id).order_by('-id_parere')
		tags_data = Taguri.objects.all()

		aggregated_tag_names, aggregated_tag_ids = aggregate_tags(reviews, tags_data)
		# print({t.id_tag:t.nume for t in tags_data})
		context = {'prof': prof_data, 
		'agg_tag_names': {k:v for k,v in sorted(dict(aggregated_tag_names).items(), key=lambda x: x[1], reverse=True)},
		'all_tags': {t.id_tag:t.nume for t in tags_data},
		'school': school_data, 
		'reviews': reviews, 
		'grades_avg': prof_data['media_notelor'], 
		'grades_count': prof_data['numarul_notelor'], 
		'stars': get_stars(rounded_average=prof_data['media_rotunjita'])}

		# update_school_ranking(prof_data['id_facultate'])

		return render(request, "prof_view.html", context)
	else:
		return HttpResponse('<h2>Pagina pe care o cauti nu exista. Incearca alta.</h2>')



def prof_add(request):

	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path))

	if request.POST:
		r = request.POST

		print(r)

		if not captcha(request, settings.CAPTCHA_SECRET):
			return redirect('%s?next=%s' % (request.path, request.GET.get('next')))
		
		nume = r['prof_first_name'] + ' ' + r['prof_last_name']
		id_fac = r['school_id']
		dep = r['prof_department']
		if 'prof_class' in r:
			discip = r['prof_class']
		if 'prof_directory_link' in r:
			dir_link = r['prof_directory_link']
		prof = Profesori(
			nume=nume,
			id_facultate = Facultati.objects.get(id_facultate=id_fac),
			departament = dep,
			disciplina = discip,
			id_creator = AuthUser.objects.get(id = request.user.id),
			timestamp = timezone.now()
			)
		prof.save()
		messages.success(request, 'Profesor adaugat. Poti sa-ti spui parerea despre el.')
		return redirect("prof:prof_view", prof.id_profesor)
	else:
		return render(request, "prof_add.html", context={'captcha_key': settings.CAPTCHA_SITE_KEY})



def review_add(request, prof_id=0):
	if prof_id != 0:

		if not request.user.is_authenticated:
			return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), request.path))
		elif Pareri.objects.filter(id_user = request.user.id, profesor = prof_id):
			return render(request, "review_failed.html", {'id_profesor': prof_id})

		if request.POST:
			
			# Limit one review per professor per session
			if 'rated_professors' not in request.session:
				print('CLEARED')
				request.session['rated_professors'] = []
			if prof_id in request.session.get('rated_professors'):
				print('FAILED')
				return render(request, "review_failed.html", {'id_profesor': prof_id})

			save_review_in_db(request, prof_id)

			request.session['rated_professors'] += [prof_id]

			return redirect(to='prof:prof_view', prof_id = prof_id)
		
		prof_data = query_to_json_obj(Profesori.objects.filter(id_profesor = prof_id))
		tags = Taguri.objects.all()
		return render(request, "review_add.html", {'prof': prof_data[0]['fields'], 'tags': tags}) 
	else:
		return HttpResponse('<h2>Pagina pe care o cauti nu exista. Incearca alta.</h2>')



def prof_rating_data(prof_id):
	reviews = Pareri.objects.filter(profesor = prof_id)
	grades = [r.nota_generala for r in reviews]
	grades_count = len(grades)
	grades_avg = 0
	if grades_count:
		grades_avg = float("{:.1f}".format( sum(grades)/grades_count )) # get the 1 point floating number of the average grades
	return {'grades_count': grades_count, 'grades_avg': grades_avg}



def get_stars(rounded_average:int):
	if rounded_average:
		return [1] * rounded_average + [0] * (5-rounded_average)
	else:
		return [0,0,0,0,0]



def save_review_in_db(request, prof_id):
	
	r = request.POST
	tags = []
	for t in r.getlist('tags'):
		if t:
			tags.append(t)
		else:
			tags.append(None)
	grade = r['grade']
	message = r['message']

	if not grade:
		grade = None
	if not message:
		message = None
	if not tags:
		tags = None

	prof = Profesori.objects.get(id_profesor=prof_id)


	parere = Pareri(
		id_user = AuthUser.objects.get(id=request.user.id),
		profesor = prof,
		nota_generala = r['star-rating'],
		dificultate = r['fire-rating'],
		as_repeta = r['would-repeat'],
		tag1 = tags[0],
		tag2 = tags[1],
		tag3 = tags[2],
		mesaj = message,
		nota_primita_student = grade,
		timestamp = timezone.now(),
		ip = request.META.get("REMOTE_ADDR")
		)

	parere.save()

	rdata = prof_rating_data(prof_id)

	prof.numarul_notelor = rdata['grades_count']
	prof.media_notelor = rdata['grades_avg']
	prof.media_rotunjita = round(rdata['grades_avg'])

	prof.save()
	update_school_ranking(id_fac = prof.id_facultate.id_facultate)



def update_school_ranking(id_fac:int):
    with connection.cursor() as cursor:
        cursor.execute('SELECT p.nota_generala FROM pareri AS p INNER JOIN profesori AS prof ON p.profesor = prof.id_profesor INNER JOIN facultati AS f ON f.id_facultate = prof.id_facultate WHERE f.id_facultate = %d;' % id_fac)
        data = cursor.fetchall()
        note = [f[0] for f in data]
        print(note)

    # ranking score algorithm (bayesian average)

    avg = float(f'{sum(note)/len(note):.1f}')

    # updating the database    
    f = Facultati.objects.get(id_facultate=id_fac)
    f.medie_note = avg
    f.numar_pareri = len(note)
    f.save()



def aggregate_tags(reviews, tags_data):
	tags_ids = defaultdict(int)
	tags_names = defaultdict(int)

	# get tag id : aggregate number
	for r in reviews:
		if r.tag1:
			if r.tag1 in tags_ids:
				tags_ids[r.tag1] += 1
			else:
				tags_ids[r.tag1] = 1
		if r.tag2:
			if r.tag2 in tags_ids:
				tags_ids[r.tag2] += 1
			else:
				tags_ids[r.tag2] = 1
		if r.tag3:
			if r.tag3 in tags_ids:
				tags_ids[r.tag3] += 1
			else:
				tags_ids[r.tag3] = 1

	# get tag name : aggregate number
	for tag_data in tags_data:
		tid = tag_data.id_tag
		tname = tag_data.nume
		if tid in tags_ids:
			tags_names[tname] += tags_ids[tid]
	return tags_names, tags_ids


def captcha(request, secret):
	r = request.POST
	if r['g-recaptcha-response']:
		response = r['g-recaptcha-response']
		success = requests.get(url=f'https://www.google.com/recaptcha/api/siteverify?secret={secret}&response={response}').json()['success']
		if not success:
			messages.warning(request, message="Challenge-ul captcha a esuat. Incearca din nou.")
			return False
	else:
		messages.warning(request, message="Trebuie sa completezi challenge-ul captcha.")
		return False
	return True



        