from queue import Queue
from django.http import HttpResponse,Http404
import random
import string
from datetime import datetime
import time
from threading import Thread

q = set()
blocked_q=set()
assigned_q=set()
#already_freed=set()
d={}


def free_token_after_60(token):
	time.sleep(60)
	try:
		d[token]['free']=True
		d[token]['blocked']=False
		q.add(int(token))
		print("added token again and freed")
	except KeyError :
		print("problem occured")
	except ValueError :
		print("value error occured")

def create_token(request):
	#N=10
	try:
		token = random.randint(500,5000000)
		q.add(token)
		d[str(token)]={'free':True,'blocked':False,
		'created':datetime.now()}
	#print(q.get())
		return HttpResponse(f"created token {str(token)}")
	except:
		pass

def assign_token(request):
	#print(f"now q is {q}")
	if len(q) > 0:
		random_token=q.pop()
		#print(f"random {random_token}")
		key = str(random_token)
		diff=datetime.now()-d[key]['created'] 
		if diff.total_seconds() > 5*60:
			print(f"token will be deleted as {diff.total_seconds()}")
			assign_token(request)
		if d[key]['blocked'] == False and d[key]['free']==True:
			#assigned_q.add(random_token)
			d[key]['free'] = False
			process = Thread(target=free_token_after_60, args=(key,))
			process.start()
			return HttpResponse(f"assigned {random_token} to request")
		elif d[key]['blocked'] == True:
			blocked_q.add(random_token)
			assign_token(request)
		else:
			#already_freed.add(random_token)
			assign_token(request)
	raise Http404("No token available")

def unblock_token(request,token):
	try:
		t=blocked_q.remove(token)
		q.add(t)
		d[t]['blocked']=False
		d[t]['free']=True
		return HttpResponse("unblocked token",token)
	except KeyError as e:
		return HttpResponse("no token found")

def delete_token(request,token):
	try:
		q.remove(token)
		del d[str(token)]
		import json
		return HttpResponse(json.dumps({"deleted":token}))
	except KeyError as e:
		return HttpResponse("no token found")

def keep_pool_token_alive(request,token):
	if request.headers.get('Keep-Alive',None) is not None:
		try:
			d[str(token)]['created']=datetime.now()
			return HttpResponse(f"{token} alive for more 5 minutes")
		except KeyError as e:
			return HttpResponse("no token found")
	return HttpResponse("header should have keep alive")
