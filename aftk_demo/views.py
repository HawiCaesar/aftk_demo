from django.shortcuts import render
from django.http import HttpResponse
from models import Dispense_Drug_List
from django.template import loader
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from django.http import JsonResponse

# Create your views here.

def index(request):

	list_of_persons = Dispense_Drug_List.objects.all()

	return render(request, 'index.html', {'sms_list': list_of_persons})

def demo_dashboard(request):

	return render(request, 'demo_dashboard.html')


def send_sms(request):

	username = "XXXXXXXXXXXXXXXXXX"
	apikey   = "XXXXXXXXXXXXXXXXXX"

	to = "+254XXXXXXXX"

	message = "I'm a lumberjack and it's ok, I sleep all night and I work all day"

	gateway = AfricasTalkingGateway(username, apikey)

	try:
		results = gateway.sendMessage(to2, message)

		for recipient in results:

		 	print 'number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
	                                                            recipient['status'],
	                                                            recipient['messageId'],
	                                                            recipient['cost'])

		response = JsonResponse({'sms_status': 'sms sent to ' + str(to2)})

		return HttpResponse(response, content_type='application/json')

	except AfricasTalkingGatewayException, e:

		error = 'Encountered an error while sending: %s' % str(e)

	 	return HttpResponse(error, content_type='application/json')

	

