from django.shortcuts import render
from models import Dispense_Drug_List

# Create your views here.

def demo_dashboard(request):

	render(request, 'demo_dashboard.html')

