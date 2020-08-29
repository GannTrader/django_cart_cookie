from django.shortcuts import render
from django.http import HttpResponse
from django.utils.crypto import get_random_string

def test_cookie(request):
	if not request.COOKIES.get('random'):
		response = HttpResponse('first visiting')
		lstring = get_random_string(length = 20)
		response.set_cookie('random', lstring, 60*60*24*30)
		return response
	else:
		return HttpResponse('your random cookie is ' + str(request.COOKIES['random']))

def random_string(request):
	s = get_random_string(length = 20)
	return HttpResponse(s)

def test_session(request):
	if not request.session.get('fruit'):
		request.session['fruit'] = 'banana'
		return HttpResponse('create session success')
	else:
		return HttpResponse('your session is ' + request.session['fruit'])


