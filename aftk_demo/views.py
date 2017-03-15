from django.shortcuts import render
from django.http import HttpResponse
from models import Dispense_Drug_List
from django.template import loader
from datetime import date
import datetime
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from django.http import JsonResponse
#import urllib, urllib2
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

			if person.weeks_reminder == 0:

				send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, final_mobile_number, person.next_pick_date.strftime("%A %d, %B %Y") ) # Send One Week Reminder

				person.weeks_reminder = 1
				person.save()
				message_counter+=1

			else:

				print "Already sent 1 week SMS reminder"

		elif total.days == 2:

			if person.two_day_reminder == 0:

				send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, final_mobile_number, person.next_pick_date.strftime("%A %d, %B %Y") ) # Send 2 day Reminder

				person.two_day_reminder = 1
				person.save()
				message_counter+=1

			else:

				print "Already sent 2 day SMS reminder"

		elif total.days <= 0:

			if person.one_day_later_reminder == 0:

				send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, final_mobile_number, person.next_pick_date.strftime("%A %d, %B %Y") ) # Send 2 day Reminder

				person.one_day_later_reminder = 1
				person.save()
				message_counter+=1

			elif person.one_day_later_reminder == 1:

				send_sms_reminder(total.days, person.patient_first_name, person.patient_last_name, final_mobile_number, person.next_pick_date.strftime("%A %d, %B %Y") ) # Send one day later Reminder
				message_counter+=1
				#print "Out of reminder period "+str(total.days)

		else:

				print "Not 7days, 2days or later than drug refill date"


	return render(request, 'index.html', {'sms_list': list_of_persons, 'message_count': message_counter})


def send_sms_reminder(no_of_days, first_name, last_name, mobile_number, the_date):

	#content based on the days

	if no_of_days == 7:

		message = "Dear "+first_name+" "+last_name+", kindly remember to come for a drug refill on "+the_date+". This is a one week reminder"

	elif no_of_days == 2:

		message = "Dear "+first_name+" "+last_name+", kindly remember to come for a drug refill on "+the_date+". This is a two day reminder"

	elif no_of_days <= 0:

		message = "Dear "+first_name+" "+last_name+", You drug refill was yesterday on "+the_date+". Please make a point of visiting the Hospital immediately!"

	#sending the sms	

	username = ""
	apiKey   = "bd32556c91e9968fd079957eaf9aa55f6b4f971fbe0bf0e8571699ea32c8f793"


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
	
	

