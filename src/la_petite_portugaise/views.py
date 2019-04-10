from django.shortcuts import redirect
#from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


# def handler503(request, exception):
#     return render(request, '503.html', locals())

def page_redirect(request):
	print(request.LANGUAGE_CODE)
	if request.LANGUAGE_CODE == 'en':
		return redirect('en/posts/')
	elif request.LANGUAGE_CODE == 'fr':
		return redirect('fr/articles/')
	elif request.LANGUAGE_CODE == 'de':
		return redirect('de/nachrichten/')