from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import *
from django.template import RequestContext
from django.contrib.auth import logout as django_logout

from bashoneliners.main.models import HackerProfile, OneLiner, User
from bashoneliners.main.forms import PostOneLinerForm, EditOneLinerForm, SearchOneLinerForm

from datetime import datetime


''' constants '''

#


''' helper methods '''

def get_common_params(request):
    if request.method == 'GET':
	searchform = SearchOneLinerForm(request.GET)
    else:
	searchform = SearchOneLinerForm()

    params = {
	    'user': request.user,
	    'searchform': searchform,
	    }

    try:
	if request.META['HTTP_USER_AGENT'].startswith('W3C_Validator'):
	    params['w3c'] = True
    except: 
	pass

    return params

def tweet(oneliner, test=False, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
    if not oneliner.was_tweeted:
	if oneliner.is_published:
	    try:
		import tweepy # 3rd party lib, install with: easy_install tweepy
		import settings
		if consumer_key is None:
		    consumer_key = settings.TWITTER.get('consumer_key')
		if consumer_secret is None:
		    consumer_secret = settings.TWITTER.get('consumer_secret')
		if access_token is None:
		    access_token = settings.TWITTER.get('access_token')
		if access_token_secret is None:
		    access_token_secret = settings.TWITTER.get('access_token_secret')

		# set up credentials to use Twitter api.
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)

		tweetmsg = 'http://bashoneliners.com/main/oneliner/%d %s: %s # posted by %s' % (
			oneliner.pk,
			oneliner.summary,
			oneliner.line,
			oneliner.user.username,
			)
		if len(tweetmsg) > 160:
		    tweetmsg = tweetmsg[:156] + ' ...'
		
		if test:
		    print tweetmsg
		    print
		    return True
		else:
		    oneliner.was_tweeted = True
		    oneliner.save()
		    return api.update_status(tweetmsg)
	    except:
		pass


''' url handlers '''

def index(request):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(is_published=True).order_by('-pk')
    return render_to_response('main/index.html', params)

def top_n(request, num):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.top()
    return render_to_response('main/top_n.html', params)

def oneliner(request, pk):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(pk=pk)
    return render_to_response('main/oneliner.html', params)

@login_required
def post(request):
    params = get_common_params(request)

    if request.method == 'POST':
	form = PostOneLinerForm(request.user, request.POST)
	if form.is_valid():
	    new_oneliner = form.save()
	    tweet(new_oneliner)
	    return redirect(index)
    else:
	form = PostOneLinerForm(request.user)

    params['form'] = form

    return render_to_response('main/post.html', params, context_instance=RequestContext(request))

@login_required
def edit_oneliner(request, pk):
    params = get_common_params(request)

    try:
	oneliner0 = OneLiner.objects.get(pk=pk, user=request.user)
    except:
	return render_to_response('main/access-error.html')

    if request.method == 'POST':
	form = EditOneLinerForm(request.user, request.POST, instance=oneliner0)
	if form.is_valid():
	    if form.is_save:
		oneliner1 = form.save()
		tweet(oneliner1)
		return redirect(oneliner, oneliner1.pk)
	    elif form.is_delete:
		oneliner0.delete()
		return redirect(profile)
    else:
	form = EditOneLinerForm(request.user, instance=oneliner0)

    params['form'] = form

    return render_to_response('main/post.html', params, context_instance=RequestContext(request))

def sourcecode(request):
    params = get_common_params(request)
    return render_to_response('main/sourcecode.html', params)

def mission(request):
    params = get_common_params(request)
    return render_to_response('main/mission.html', params)

def profile(request, user_id=None):
    params = get_common_params(request)

    if user_id is None:
	user_id = request.user.pk

    user = User.objects.get(pk=user_id)

    params['hacker'] = user
    params['oneliners'] = OneLiner.objects.filter(user=user).order_by('-pk')
    if user == request.user:
	params['owner'] = True

    return render_to_response('main/profile.html', params)

def wishlist(request):
    params = get_common_params(request)
    params['oneliners'] = OneLiner.objects.filter(is_published=True).order_by('-pk')
    return render_to_response('main/index.html', params)

def search(request):
    params = get_common_params(request)
    form = params['searchform']

    if form.is_valid():
	params['oneliners'] = OneLiner.search(form.cleaned_data.get('query'))

    return render_to_response('main/search.html', params)

def search_ajax(request):
    params = {}

    if request.method == 'GET':
	form = SearchOneLinerForm(request.GET)
    else:
	form = None

    if form is not None:
	if form.is_valid():
	    params['oneliners'] = OneLiner.search(form.cleaned_data.get('query'))

    return render_to_response('main/oneliners.html', params)

def login(request):
    params = get_common_params(request)
    return render_to_response('main/login.html', params, context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return index(request)

# eof
