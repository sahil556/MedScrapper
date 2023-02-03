from django.shortcuts import render
from django.http import HttpResponse
import json 
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from medicine_class import MedicineDetails
# Create your views here.



def home(request):
    return HttpResponse("Welcome to MedScrapper")


def medicine_from_1mg(request):
    medicine_name = json.loads(request.body)['name']
    return HttpResponse("1mg link")

def medicine_from_pharmeasy(request):
    medicine_name = json.loads(request.body)['name']
    return HttpResponse("pharmeasy link")

def medicine_from_netmeds(request):
    medicine_name = json.loads(request.body)['name']
    return HttpResponse("netmeds link")