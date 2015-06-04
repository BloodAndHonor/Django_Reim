#encoding: utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from reimsite.models import Application, Detail, Funds, Item, Reim, Config
from django.utils import timezone
import hashlib
from datetime import *
import csv

def index(request):
	return render(request,'reimsite/road.html',None)

def apply(request):
	return render(request,'reimsite/index.html',None)

def msg(request,msg,retlink):
	a = { 'msgtext':msg, 'retlink': retlink}
	return render(request,'reimsite/message.html',a)

def add_record(request):
	if request.method == "GET":
		return msg(request,'该页面不存在','apply')
	else:
		name = request.POST['name']
		category = request.POST['category']
		days = request.POST['days']
		others = request.POST['others']
		remain = request.POST['remain']
		if days == "":
			days = "0"
		total = 180* int(days.encode('ascii'))

		app = Application.objects.create(name=name, category=category, days=days, others=others, date=timezone.now(), remain=remain, total=total)
		items = app.item_set.all()
		res = {'application':app, 'items':items, 'details': Detail.objects.all()}

		return render(request,'reimsite/index.html', res)

def rm_record(request):
	if request.method == "GET":
		return msg(request,'该页面不存在','apply')
	else:
		appid = request.POST['appid']
		app = Application.objects.get(pk=appid)

		app.item_set.all().delete()
		app.delete()

		return render(request,'reimsite/index.html',None)

def adminrm_record(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	if request.method == "GET":
		return msg(request,'该页面不存在','backend')
	else:
		appid = request.POST['appid']
		app = Application.objects.get(pk=appid)

		app.item_set.all().delete()
		app.delete()

		return render(request,'backend/index.html',None)

def add_item(request):
	if request.method == "GET":
		return msg(request,'该页面不存在','apply')
	else:
		app = Application.objects.get(pk=request.POST['appid'])

		detail=Detail.objects.get(id=request.POST['detail'])
		money=request.POST['money']

		app.item_set.create(detail=detail, money=money)
		app.total = app.total + int(money.encode('ascii'))
		# application status   0--abandon 1--waiting for deal 2--dealt
		app.status = 1
		app.save()

		items = app.item_set.all()
		res = {'application':app, 'items':items, 'details': Detail.objects.all()}

		return render(request,'reimsite/index.html', res)

def rm_item(request):
	if request.method == "GET":
		return msg(request,'该页面不存在','apply')
	else:
		appid = request.POST['appid']
		itemid = request.POST['itemid']
		app = Application.objects.get(pk=appid)
		tmp = app.item_set.get(id=itemid)

		app.total = app.total - tmp.money
		if len(app.item_set.all()) == 0:
			app.status = 0
		app.save()
		tmp.delete()

		items = app.item_set.all()
		res = {'application':app, 'items':items, 'details': Detail.objects.all()}

		return render(request,'reimsite/index.html', res)

def show_applications(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	a ={"applications": Application.objects.order_by('status')}
	return render(request,'backend/application.html',a)

def deal_application(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	a ={"applications": Application.objects.filter(status=1), "funds": Funds.objects.all()}
	return render(request,'backend/deal.html',a)

def login(request):
	if request.method == "GET":
		return render(request, 'backend/login.html')
	else:
		username = request.POST['username']
		passwd = request.POST['passwd']

		adm = Config.objects.get(name=username)
		if hashlib.md5(passwd).hexdigest() == adm.value:
			request.session['token'] = 'allowed'
			return HttpResponseRedirect('/reim/backend/')
		else:
			return msg(request,'用户名或密码错误','login')

def backend(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	return render(request, 'backend/index.html', None)
	
def add_reim(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	if request.method == "GET":
		return msg(request,'该页面不存在','deal_app')
	else:
		appid = request.POST['appid']
		fundid = request.POST['fundid']
		number = request.POST['number']

		app = Application.objects.get(pk=appid)
		fund = Funds.objects.get(id=fundid)
		app.status = 2
		app.save()

		Reim.objects.create(record=app, funds=fund, number=number)

		a ={"applications": Application.objects.order_by('status'), "funds": Funds.objects.all()}
		return render(request,'backend/deal.html',a)

def init(request):
	if len(Config.objects.filter(name="lyp")) == 0:
		Config.objects.create(name="lyp", value=hashlib.md5("123").hexdigest())
	return HttpResponse("Init successfully")

def search(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	if request.method == "GET":
		return msg(request,'该页面不存在','search')
	else:
		sdate = request.POST['sdate']
		tdate = request.POST['tdate']
		res = Application.objects.filter(date__gte=sdate, date__lte=tdate)

		a = { "applications":res, "sdate":sdate, "tdate":tdate, "flag":True}
		return render(request,'backend/index.html', a)

def export(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	if request.method == "GET":
		return msg(request,'该页面不存在','backend')
	else:
		sdate = request.POST['sdate']
		tdate = request.POST['tdate']
		res = Application.objects.filter(date__gte=sdate, date__lte=tdate, status=2)

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
		writer = csv.writer(response)

		writer.writerow(['序号', '报销人', '科目', '经费卡号', '单据数目', '报账额度','备注'])
		i = 1
		for item in res:
			writer.writerow([i, item.name, item.category, item.reim.funds.credit, item.remain, item.total, item.others])
			i = i + 1

		return response

def detail(request):
	if request.method == "GET":
		return render(request,'backend/detail.html', None)
	else:
		sdate = request.POST['sdate']
		tmp = sdate.split('-')
		sobj = date(int(tmp[0]),int(tmp[1]),int(tmp[2]))
		tdate = request.POST['tdate']
		tmp = tdate.split('-')
		tobj = date(int(tmp[0]),int(tmp[1]),int(tmp[2]))

		number = request.POST['number']
		collection = Reim.objects.filter(number=number)
		res = None
		for i in collection:
			if i.record.date >= sobj and i.record.date <= tobj:
				res = i

		items = None
		if res != None:
			items = res.record.item_set.all()

		a = { "reim": res,"items":items, "sdate":sdate, "tdate":tdate, "number":number}
		return render(request,'backend/detail.html', a)

def chpass(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	if request.method == "GET":
		return render(request, 'backend/passwd.html', None)
	else:
		newpwd = request.POST['newpwd']
		username = request.POST['username']

		pwd = hashlib.md5(newpwd).hexdigest()
		tmp = Config.objects.get(name=username)
		if tmp == None:
			return HttpResponse("hehe")
		else:
			tmp.value = pwd
			tmp.save()
		return msg(request, '修改成功','backend')

def logout(request):
	if request.session['token'] == 'allowed':
		del request.session['token']
		return HttpResponseRedirect('/reim/login/')
	else:
		return msg(request, '未登录','login')

def source(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	if request.method == "GET":
		a = {
		"funds": Funds.objects.all(),
		"detail": Detail.objects.all(),
		}
		return render(request, 'backend/soucre.html', a)
	else:
		source = request.POST['source']
		Detail.objects.create(source=source)

		a = {
		"funds": Funds.objects.all(),
		"detail": Detail.objects.all(),
		}
		return render(request, 'backend/soucre.html', a)

def credit(request):
	if request.session['token'] != 'allowed':
		return HttpResponseRedirect('/reim/login/')
	if request.method == "GET":
		a = {
		"funds": Funds.objects.all(),
		"detail": Detail.objects.all(),
		}
		return render(request, 'backend/soucre.html', a)
	else:
		credit = request.POST['credit']
		Detail.objects.create(credit=credit)
		a = {
		"funds": Funds.objects.all(),
		"detail": Detail.objects.all(),
		}
		return render(request, 'backend/soucre.html', a)