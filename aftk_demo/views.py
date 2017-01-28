from django.shortcuts import render
from django.http import HttpResponse
from models import Dispense_Drug_List
from django.template import loader
from datetime import date
import datetime
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from django.http import JsonResponse
import urllib, urllib2
import requests


# Create your views here.

def index(request):

	list_of_persons = Dispense_Drug_List.objects.all()

	message_counter = 0

	
	for person in list_of_persons:

		total = person.next_pick_date - datetime.date.today()

		striped_number = person.mobile_number[1:]

		final_mobile_number = ''.join(('+254', striped_number))

		print total.days

		if total.days == 7:

			send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, final_mobile_number, person.next_pick_date.strftime("%A %d, %B %Y") ) # Send One Week Reminder

			person.weeks_reminder = 1
			person.save()
			message_counter+=1

		elif total.days == 2:

			send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, final_mobile_number, person.next_pick_date.strftime("%A %d, %B %Y") ) # Send 2 day Reminder

			person.two_day_reminder = 1
			person.save()
			message_counter+=1

		else:

			print "Out of reminder period"


	return render(request, 'index.html', {'sms_list': list_of_persons, 'message_count': message_counter})

def demo_dashboard(request):

	return render(request, 'demo_dashboard.html')


def send_sms_reminder(no_of_days, first_name, last_name, mobile_number, the_date):

	#content based on the days

	if no_of_days == 7:

		message = "Dear "+first_name+" "+last_name+". Kindly remember to come for a drug refill on "+the_date+". This is a one week reminder"

	elif no_of_days == 2:

		message = "Dear "+first_name+" "+last_name+". Kindly remember to come for a drug refill on "+the_date+". This is a two day reminder"

	elif no_of_days == -1:

		message = "Dear "

	#sending the sms	

	username = "MY SANDBOX USERNAME"
	apiKey   = "MY APIKEY"


	to = mobile_number

	gateway = AfricasTalkingGateway(username, apiKey, "sandbox")


	try:
    # Thats it, hit send and we'll take care of the rest.
    
	    results = gateway.sendMessage(to, message)
	    
	    for recipient in results:
	        # status is either "Success" or "error message"
	        print 'number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                            recipient['status'],
                                                            recipient['messageId'],
                                                            recipient['cost'])

	except AfricasTalkingGatewayException, e:
	    print 'Encountered an error while sending: %s' % str(e)
	
	

