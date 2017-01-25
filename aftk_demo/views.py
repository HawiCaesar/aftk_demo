from django.shortcuts import render
from django.http import HttpResponse
from models import Dispense_Drug_List
from django.template import loader
from datetime import date
import datetime
#from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from django.http import JsonResponse
import urllib, urllib2
import requests


# Create your views here.

def index(request):

	list_of_persons = Dispense_Drug_List.objects.all()

	message_counter = 0

	
	for person in list_of_persons:

		total = person.next_pick_date - datetime.date.today()

		print total.days

		if total.days == 7:

			#send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, person.mobile_number, person.next_pick_date ) # Send One Week Reminder

			person.weeks_reminder = 1
			person.save()
			message_counter+=1

		elif total.days == 2:

			#send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, person.mobile_number, person.next_pick_date ) # Send 2 day Reminder

			person.two_day_reminder = 1
			person.save()
			message_counter+=1

		else:

			print "Out of reminder period"

			

	return render(request, 'index.html', {'sms_list': list_of_persons, 'message_count':message_counter})

def demo_dashboard(request):

	return render(request, 'demo_dashboard.html')


def send_sms(no_of_days, first_name, last_name, mobile_number, date):

	if no_of_days == 7:

		message = "Dear "+first_name+last_name+". Kindly remember to come for a drug refill on "+date+". This is a one week reminder"

	elif no_of_days == 2:

		message = "Dear "+first_name+last_name+". Kindly remember to come for a drug refill on "+date+". This us a two day reminder"

	elif no_of_days == -1:

		message = "Dear "



	# Dealing with the days



	headers = {"apikey":"bd32556c91e9968fd079957eaf9aa55f6b4f971fbe0bf0e8571699ea32c8f793"}

	values = {"username": "hawi_caesar",
				"to":"+254733806122", # for purposes of demo, this number is used
				"message":message}

	response = requests.post('http://api.sandbox.africastalking.com/version1/messaging', headers=headers, data = values)

	content = response.content

	return HttpResponse(content)
	

