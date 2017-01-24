from django.shortcuts import render
from django.http import HttpResponse
from models import Dispense_Drug_List
from django.template import loader
from datetime import date, datetime
#from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from django.http import JsonResponse
import urllib, urllib2
import requests


# Create your views here.

def index(request):

	list_of_persons = Dispense_Drug_List.objects.all()

	for person in list_of_persons:

		total = person.next_pick_date - datetime.date()

		total_days = total.days


	return render(request, 'index.html', {'sms_list': list_of_persons,'one_week_list': total_days})

def demo_dashboard(request):

	return render(request, 'demo_dashboard.html')


def send_sms(request):

	headers = {"apikey":"bd32556c91e9968fd079957eaf9aa55f6b4f971fbe0bf0e8571699ea32c8f793"}

	values = {"username": "hawi_caesar",
				"to":"+254733806122",
				"message":"Another JSON response?"}

	response = requests.post('http://api.sandbox.africastalking.com/version1/messaging', headers=headers, data = values)

	content = response.content

	return HttpResponse(content)
	

