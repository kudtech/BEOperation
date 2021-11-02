import requests
from django.contrib.auth.models import User
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.shortcuts import render, render_to_response,redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
import operator
from beapi.models import *
from .forms import *
import json 
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)
from rest_framework.response import Response
from django.contrib.auth.models import User
import posixpath
import os
import random
from . forms import NameForm, WorkOrderForm, JobForm, GeneralForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_tables2 import RequestConfig
from .tables import *
from rest_framework import viewsets
from beapi.serializers import *
from django.db.models import Q
from django.db import connection
from . beglobals import *
#graphQl Queries link
from .graphqlqueries import schema


# LIBRARIES FOR generating PDF
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
#
from django.core.mail import EmailMessage


def user_authenticate(username):
    users = User.objects.all()
    for user in users:
        if user.username == username:
            token, created = Token.objects.get_or_create(user=user)
            return user.username, token.key
    return None


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


def execsys(ecnum):
    URL = "http://" + beserver + ":8082/users/username/" + ecnum
    r = requests.get(url=URL)
    data = r.json()

    return data


def get_center(centre_code):
    if centre_code == "ER":
        centre = "Regional Office (ER)"
        return centre, centre_code
    if centre_code == "ERM":
        centre = "Eastern Maintenance"
        return centre, centre_code
    if centre_code == "END":
        centre = "Network Development"
        return centre, centre_code
    if centre_code == "MTD":
        centre = "Mutare District"
        return centre, centre_code
    if centre_code == "URB":
        centre = "Mutare Urban"
        return centre, centre_code
    if centre_code == "ENV":
        centre = "Mutare Environs"
        return centre, centre_code
    if centre_code == "MTG":
        centre = "Mutare Garage"
        return centre, centre_code
    if centre_code == "MND":
        centre = "Manicaland District"
        return centre, centre_code
    if centre_code == "NYA":
        centre = "Nyanga"
        return centre, centre_code
    if centre_code == "RSP":
        centre = "Rusape"
        return centre, centre_code
    if centre_code == "CHP":
        centre = "Chipinge"
        return centre, centre_code
    if centre_code == "CHM":
        centre = "Chimanimani"
        return centre, centre_code
    if centre_code == "MSB":
        centre = "Middle Sabi"
        return centre, centre_code
    if centre_code == "MSD":
        centre = "Masvingo District"
        return centre, centre_code
    if centre_code == "MSV":
        centre = "Masvingo Urban"
        return centre, centre_code
    if centre_code == "GUT":
        centre = "Gutu"
        return centre, centre_code
    if centre_code == "MAS":
        centre = "Mashava"
        return centre, centre_code
    if centre_code == "RUT":
        centre = "Rutenga"
        return centre, centre_code
    if centre_code == "CHR":
        centre = "Chiredzi"
        return centre, centre_code
    if centre_code == "MSG":
        centre = "Masvingo Garage"
        return centre, centre_code
    centre = "No Centre"
    centre_code = "No Centre Code"
    return centre, centre_code


class MyTeam(View):
    def get(self, request, *args, **kwargs):
        team_leaders = request.GET['leader']
        myteam, teams = artisan_team(team_leaders)
        data = ""
        team_leaders = []
        Teams = Team.objects.all()
        my_teams = dict()

        for teamleader in Teams:
            if teamleader.team_leader not in [member.team_leader for member in team_leaders]:
                team_leaders.append(teamleader)
                my_teams[teamleader.team_leader] = []

        for teamleader in team_leaders:
            teammembers = Team.objects.filter(team_leader=teamleader)
            if teammembers:
                for teammember in teammembers:
                    my_teams[teamleader.team_leader].append(
                        teammember.team_member)
        return render(request, 'beweb/wo.html', {
            'data': data, 'myteam': myteam, 'my_teams': my_teams, 'teams': teams, 'team_leaders': team_leaders
        })

    def post(self, request, *args, **kwargs):
        members = []
        members = request.POST.getlist('members')
        return HttpResponse('Are you sure you want to save data')


class MTeam(View):
    def get(self, request, *args, **kwargs):
        data = execsys(request.user.username)
        centre_code = data['section']
        username = data['username']
        centre, centre_code = get_center(centre_code)
        centre = request.GET['centre']
        date = datetime.now().strftime("%Y%m%d%H%M")
        centre_code = request.GET['centre_code']
        team_leaders = request.GET['leader']
        myteam = artisan_team(team_leaders)
        data = ""
        return render(request, 'beweb/job/create.html', {
            'data': data, 'myteam': myteam,  'team_leaders': team_leaders
        })


class MyAssets(View):
    def get(self, request, *args, **kwargs):
        data = execsys(request.user.username)
        centre = data['section']
        return render(request, 'beweb/assets.html', {'centre': centre
                                                     })


class WoSaveAsset(View):
    def post(self, request, *args, **kwargs):
        reference_number = None
        # IF WORKORDER DOES NOT EXIST, create workorder first
        assignee = request.session['assignee']
        team_members =request.session['teammembers']
        fleet = request.session['fleet']
        if not request.session['workorder_number']:
            username = request.session['username']
            description = request.session['description']
            supervisor = request.session['username']
            data = execsys(request.user.username)
            centre = data['section']
            section = request.session['section']
            centre_code = data['section']
            work_order_id = request.session['work_order']
            date = datetime.now().strftime("%Y%m%d%H%M")
            createdby = request.session['username']
            wo = request.session['work_order']
            job_description = request.session['job_description']
            expected_end_dt = request.session['expected_end_dt']
            section = request.session['section']
            job_number = request.session['job_number']
            trigger = request.session['trigger']
            start_date = request.session['start_date']
            asset_type = request.session['asset_type']
            job_type = request.session['job_type_id']
           

     
      
            if 'E50' in job_type:
                asset_id = request.POST['asset_id']
                asset_name = ''
                asset_number = ''
                asset_serial = ''
                e50_id = e50_id = "E50"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
                station_id = request.POST['asset_id']
            else:
                asset_id = None
                asset_name = None
                asset_number = None
                asset_serial = None

            if 'E60' in job_type:
                asset_id = request.POST['asset_id']
                district = data['centre']
                asset_name = ''
                asset_number = ''
                asset_serial = ''
                e60_id = e60_id = "E60"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
                transformer_id = request.POST['asset_id']
                work_type = request.POST['work_type']
            else:
                asset_id = None
                asset_name = None
                asset_number = None
                asset_serial = None

            wo = save_wo(username, description, supervisor,
                         centre, date, centre_code, work_order_id)
            joid = Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                            section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
             
            if 'E50' in job_type:
                save_e50(e50_id, job_number, createdby, station_id)
            else:
                pass

            if 'E60' in job_type:
                save_e60(e60_id, job_number, createdby,
                         transformer_id, work_type, district)
            else:
                pass
            jp = job_progress(job_number, createdby, fleet)
            a = save_team(username, assignee, jp, team_members)
            del request.session['description']
            del request.session['work_order']
            del request.session['job_description']
            del request.session['expected_end_dt']
            del request.session['section']
            del request.session['job_number']
            del request.session['trigger']
            del request.session['start_date']
            del request.session['asset_type']
            del request.session['job_type_id']
        else:
            wo = request.session['workorder_number']
            createdby = request.user.username
            username = request.user.username
            job_type = request.session['job_type_id']
            
            job_description = request.session['job_description']
            expected_end_dt = request.session['expected_end_dt']
            data = execsys(request.user.username)
            centre = data['section']
            section = request.session['section']
            job_number = request.session['job_number']
            trigger = request.session['trigger']
            start_date = request.session['start_date']
            asset_type = request.session['asset_type']
            if 'E50' in job_type:
                asset_id = request.POST['asset_id']
                asset_name = ''
                asset_number = ''
                asset_serial = ''
                e50_id = e50_id = "E50"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
                station_id = request.POST['asset_id']

            else:
                asset_id = None
                asset_name = None
                asset_number = None
                asset_serial = None
            if 'E60' in job_type:
                asset_id = request.POST['asset_id']
                district = data['centre']
                asset_name = ''
                asset_number = ''
                asset_serial = ''
                e60_id = e60_id = "E60"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
                transformer_id = request.POST['asset_id']
                work_type = request.POST['work_type']
            else:
                asset_id = None
                asset_name = None
                asset_number = None
                asset_serial = None

            joid = Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                            section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
            
            if 'E50' in job_type:
                save_e50(e50_id, job_number, createdby, station_id)
            else:
                pass

            if 'E60' in job_type:
                save_e60(e60_id, job_number, createdby,
                         transformer_id, work_type, district)
            else:
                pass

            jp = job_progress(job_number, createdby, fleet)
            a = save_team(username, assignee, jp, team_members)
              
            # del request.session['workorder_number']
            # del request.session['assignee']
            # del request.session['job_type_id']
            # del request.session['job_description']
            # del request.session['expected_end_dt']
            # del request.session['section']
            # del request.session['job_number']
            # del request.session['trigger']
            # del request.session['start_date']
            # del request.session['asset_type']
            # del request.session['fleet']
            # del request.session['team_members']

        joid = request.POST['joid']
        wo = request.POST['wo']
        url = 'http://' + beserver + ':8087/beapi/jobupdate/' + joid
        asset_sel = request.POST['asset_type']
        username = request.user.username
        selection = request.POST['asset_code_pk']
        usr, tkn = user_authenticate(username)
        data = {}
        if asset_sel == "transformer":
            t_pk = selection
            headers = {'Authorization': "Token "+tkn +
                       "", "Content-Type": "application/json"}
            URL = 'http://' + beserver + ':8089/gis/gistransformer/' + t_pk
            response = requests.get(url=URL, headers=headers)
            transformer = (response.json())[0]
            asset_id = transformer['transformerid']
            asset_name = transformer['name']
            asset_type = asset_sel
            asset_serial = transformer['serialno']
            asset_number = transformer['assetno']
            geom = transformer['geom2d']
            data = {
                "asset_id": asset_id,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "asset_number": asset_number,
                "asset_serial": asset_serial,
                "geom": geom
            }
            data = json.dumps(data)
            r = requests.patch(url=url, data=data, headers=headers)
        if asset_sel == "switchgear":
            swt_pk = selection
            headers = {'Authorization': "Token "+tkn +
                       "", "Content-Type": "application/json"}
            URL = 'http://' + beserver + ':8089/gis/gisswitchgear/' + swt_pk
            response = requests.get(url=URL, headers=headers)
            switchgear = (response.json())[0]
            asset_id = switchgear['switchgearid']
            asset_name = asset_sel
            asset_type = asset_sel
            asset_serial = switchgear['serialno']
            asset_number = switchgear['assetno']
            geom = switchgear['geom2d']
            data = {
                "asset_id": asset_id,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "asset_number": asset_number,
                "asset_serial": asset_serial,
                "geom": geom
            }
            data = json.dumps(data)
            r = requests.patch(url=url, data=data, headers=headers)
        if asset_sel == "meter":
            m_pk = selection
            headers = {'Authorization': "Token "+tkn +
                       "", "Content-Type": "application/json"}
            URL = 'http://' + beserver + ':8089/gis/gismeter/' + m_pk
            response = requests.get(url=URL, headers=headers)
            meter = (response.json())[0]
            asset_id = meter['meterid']
            asset_name = meter['make']
            asset_type = asset_sel
            asset_serial = ''
            asset_number = meter['meterno']
            geom = meter['geom2d']
            data = {
                "asset_id": asset_id,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "asset_number": asset_number,
                "asset_serial": asset_serial,
                "geom": geom
            }
            data = json.dumps(data)
            r = requests.patch(url=url, data=data, headers=headers)
        if asset_sel == "feeder":
            f_pk = selection
            headers = {'Authorization': "Token "+tkn +
                       "", "Content-Type": "application/json"}
            URL = 'http://' + beserver + ':8089/gis/gisfeeder/' + f_pk
            response = requests.get(url=URL, headers=headers)
            feeder = (response.json())[0]
            asset_id = feeder['feedercode']
            asset_name = feeder['name']
            asset_type = asset_sel
            asset_serial = ''
            asset_number = feeder['assetno']
            geom = feeder['geom2d']
            data = {
                "asset_id": asset_id,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "asset_number": asset_number,
                "asset_serial": asset_serial,
                "geom": geom
            }
            data = json.dumps(data)
            r = requests.patch(url=url, data=data, headers=headers)
        if asset_sel == "station":
            station_pk = selection
            headers = {'Authorization': "Token "+tkn +
                       "", "Content-Type": "application/json"}
            URL = 'http://' + beserver + ':8089/gis/gisstation/' + station_pk
            response = requests.get(url=URL, headers=headers)
            station = (response.json())[0]
            asset_id = station['stationid']
            asset_name = station['name']
            asset_type = asset_sel
            asset_serial = ''
            asset_number = station['assetno']
            geom = station['geom2d']
            data = {
                "asset_id": asset_id,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "asset_number": asset_number,
                "asset_serial": asset_serial,
            }
            data = json.dumps(data)
            r = requests.patch(url=url, data=data, headers=headers)
        if asset_sel == "pole":
            p_pk = selection
            headers = {'Authorization': "Token "+tkn +
                       "", "Content-Type": "application/json"}
            URL = 'http://' + beserver + ':8089/gis/gistransformer/' + p_pk
            response = requests.get(url=URL, headers=headers)
            pole = (response.json())[0]
            asset_id = pole['poleid']
            asset_name = asset_sel
            asset_type = asset_sel
            asset_serial = ''
            asset_number = pole['assetno']
            geom = pole['geom2d']
            data = {
                "asset_id": asset_id,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "asset_number": asset_number,
                "asset_serial": asset_serial,
            }
            data = json.dumps(data)
            r = requests.patch(url=url, data=data, headers=headers)
        my_work = Workorder.objects.filter(work_order_id=wo)
        my_jobs = Job.objects.filter(job_id=joid)
        my_progress = Jobprogress.objects.filter(job=joid)
        for jp in my_progress:
            my_team = Jobteam.objects.filter(job_progress=jp)

        return render(request, 'beweb/job/notification.html')


def workorder(request):
    work_order_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/single/workorder/" + work_order_id+"/"
    r = requests.get(url=url, headers=headers)
    data = r.json()
    num_jobs = len(data[0]['jobs'])
    employee_data = execsys(data[0]['created_by'])
    fullname = employee_data['firstname'] + " " + employee_data['surname']

    if data[0]['centre'] == "URB":
        data[0]['centre'] = "Mutare Urban"
    elif data[0]['centre'] == "ENV":
        data[0]['centre'] = "Mutare Environs"
    elif data[0]['centre'] == "RSP":
        data[0]['centre'] = "Rusape"
    elif data[0]['centre'] == "NYA":
        data[0]['centre'] = "Nyanga"
    elif data[0]['centre'] == "CHP":
        data[0]['centre'] = "Chipinge"
    elif data[0]['centre'] == "CHM":
        data[0]['centre'] = "Chimanimani"
    elif data[0]['centre'] == "MSB":
        data[0]['centre'] = "Middle Sabi"
    elif data[0]['centre'] == "RUT":
        data[0]['centre'] = "Rutenga"
    elif data[0]['centre'] == "GUT":
        data[0]['centre'] = "Gutu"
    elif data[0]['centre'] == "CHR":
        data[0]['centre'] = "Chiredzi"
    elif data[0]['centre'] == "MAS":
        data[0]['centre'] = "Mashava"
    elif data[0]['centre'] == "MSV":
        data[0]['centre'] = "Masvingo Urban"
    elif data[0]['centre'] == "MTD":
        data[0]['centre'] = "Mutare District"
    elif data[0]['centre'] == "MND":
        data[0]['centre'] = "Manicaland District"
    elif data[0]['centre'] == "MSD":
        data[0]['centre'] = "Masvingo District"
    elif data[0]['centre'] == "MTG":
        data[0]['centre'] = "Mutare Garage"
    elif data[0]['centre'] == "MSG":
        data[0]['centre'] = "Masvingo Garage"

    context = {
        "workorder": data[0],
        "number_of_jobs": num_jobs,
        "fullname": fullname
    }
    return render(request, 'beweb/workorder/workorder_view.html', context)


def job(request):
    job_id = request.GET.get('q', '')
    username = request.user.username
    decision = request.GET.get('decision', '')
    comments = request.GET.get('comments', '')

    e60_data = []
    try:
        job_workflow = Jobworkflow.objects.filter(
            job=job_id)[-0].workflow_id if Jobworkflow.objects.filter(job=job_id) else None
    except:
        job_workflow = None
    job_workflow_id = Jobworkflow.objects.filter(
        job=job_id)[-0].job_workflow_id
    workflow_code = Workflow.objects.filter(
        workflow_id=job_workflow)[0].workflow_code
    nextaction = Workflow.objects.filter(
        workflow_code=workflow_code)[0].role_code

    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    status = Job.objects.filter(job_id=job_id).values("status")[0]['status']
    role_name = ''
    approve = ''
    reject = ''

    if status == 4 or status == 5 or status == 6:
        url = "http://" + beserver + ":8087/beapi/job/awaiting/action/"+usr
        rs = requests.get(url=url, headers=headers)
        jobsdata = rs.json()

        role_name = jobsdata[0]["role_name"]
        approve = jobsdata[0]["approve"]
        reject = jobsdata[0]["reject"]
    else:
        pass

    url = "http://" + beserver + ":8087/beapi/job/" + job_id+"/"
    r = requests.get(url=url, headers=headers)
    data = r.json()
    
    jobtype = data[0]['type']
    contractor_data = []
    e117 = []
    client_data = []
    is_e117 = False
    is_e60 = False
    employee_data = []
    is_statutory = False

    if jobtype == 'E84':
        team_data = data[0]['job_progress'][0]['jobteam_members']
        end_date = data[0]['job_progress'][0]['end_dt']
        team_leader = data[0]['job_progress'][0]['jobteam_members'][0]['teamleader']
        employee_data = execsys(team_leader)
        fullname = employee_data['firstname'] + " " + employee_data['surname']
        data[0]['type'] = 'Line Inspection'

    elif jobtype == 'E117':
        team_data = data[0]['job_progress'][0]['jobteam_members']
        end_date = data[0]['job_progress'][0]['end_dt']
        team_leader = data[0]['job_progress'][0]['jobteam_members'][0]['teamleader']

        employee_data = execsys(team_leader)
        fullname = employee_data['firstname'] + " " + employee_data['surname']
        e117_url = "http://" + beserver + ":8087/beapi/e117/job/" + job_id+"/"
        e117_result = requests.get(url=e117_url, headers=headers)
        e117_data = e117_result.json()
        inspection_type = e117_data[0]['client_inspection_type']
        is_e117 = (str(inspection_type) == 'new_installation' or str(
            inspection_type) == 're_inspection' or str(inspection_type) == 'statutory')

        if str(e117_data[0]['client_inspection_type']) == 'statutory':
            e117_data[0]['client_inspection_type'] = 'Statutory'
            is_statutory = True
        elif str(e117_data[0]['client_inspection_type']) == 're_inspection':
            e117_data[0]['client_inspection_type'] = 'Re-inspection'
        elif str(e117_data[0]['client_inspection_type']) == 'new_installation':
            e117_data[0]['client_inspection_type'] = 'New Installation'

        if str(e117_data[0]['customer_type']) == 'domestic':
            e117_data[0]['customer_type'] = 'Domestic'
        elif str(e117_data[0]['customer_type']) == 'industrial':
            e117_data[0]['customer_type'] = 'Industrial'
        elif str(e117_data[0]['customer_type']) == 'farming':
            e117_data[0]['customer_type'] = 'Farming'
        elif str(e117_data[0]['customer_type']) == 'mining':
            e117_data[0]['customer_type'] = 'Mining'
        elif str(e117_data[0]['customer_type']) == 'institutions':
            e117_data[0]['customer_type'] = 'Institutions'

        e117 = e117_data[0]
        data[0]['type'] = 'Installation Inspection'

        if ((str(e117_data[0]['number_of_clients']) == 'multiple')):
            e117_data[0]['number_of_clients'] = 'Multiple'
            client_data = client_data
        else:
            client_url = "http://" + beserver + ":8087/beapi/client/" + \
                e117_data[0]['e117client']+"/"
            client_result = requests.get(url=client_url, headers=headers)
            c_data = client_result.json()
            client_data = c_data[0]

        if inspection_type == "new_installation" or inspection_type == "re_inspection":
            # GET CONTRACTOR DATA FROM THE CONTRACTOR ID FROM ABOVE REQUEST
            contractor_url = "http://" + beserver + ":8087/beapi/e117contractor/" + \
                e117_data[0]['client_contractor']+"/"
            contractor_result = requests.get(
                url=contractor_url, headers=headers)
            contractor_data = contractor_result.json()
        else:
            pass
    elif jobtype == 'E50':
        team_data = data[0]['job_progress'][0]['jobteam_members']
        end_date = data[0]['job_progress'][0]['end_dt']
        team_leader = data[0]['job_progress'][0]['jobteam_members'][0]['teamleader']
        employee_data = execsys(team_leader)
        fullname = employee_data['firstname'] + " " + employee_data['surname']
        data[0]['type'] = 'Primary Substation Maintenance'

    elif jobtype == 'E60':
        team_data = data[0]['job_progress'][0]['jobteam_members']
        end_date = data[0]['job_progress'][0]['end_dt']
        team_leader = data[0]['job_progress'][0]['jobteam_members'][0]['teamleader']
        employee_data = execsys(team_leader)
        fullname = employee_data['firstname'] + " " + employee_data['surname']
        data[0]['type'] = 'Consumer Substation Inspection'
        e60_url = "http://" + beserver + ":8087/beapi/e60job/" + job_id+"/"
        e60_response = requests.get(url=e60_url, headers=headers)
        e60_data = e60_response.json()
        type_of_work = e60_data[0]['type_of_work']
        is_e60 = type_of_work

    section = employee_data['section']
    try:
        start = datetime.strptime(
            data[0]['start_date'], "%Y-%m-%d") if data[0]['start_date'] else ''
        end = datetime.strptime(
            data[0]['expected_end_dt'], "%Y-%m-%d %H:%M:%S") if data[0]['expected_end_dt'] else ''
        delta = (datetime(end.year, end.month, end.day, end.hour, end.minute, end.second)-datetime(start.year,
                                                                                                   start.month, start.day, start.hour, start.minute, start.second)) if start and end else ''
    except:
        delta = ''

    if contractor_data:
        contractor = contractor_data[0]
    else:
        contractor = contractor_data

    context = {
        "job": data[0],
        "e117_data": e117,
        "client_data": client_data,
        "contractor_data": contractor,
        "section": section,
        "team_data": data[0]['job_progress'][0]['jobteam_members'],
        "team_members": len(team_data),
        "open_mileage": data[0]['job_progress'][0]['open_mileage'],
        "close_mileage": data[0]['job_progress'][0]['close_mileage'],
        "status": data[0]['job_progress'][0]['status'],
        "start_date": data[0]['start_date'],
        "expected_end_dt": data[0]['expected_end_dt'],
        "fleet": data[0]['job_progress'][0]['fleet_no'],
        "job_progress": data[0]['job_progress'],
        "trigger": data[0]['trigger'],
        "team_leader": fullname,
        "nextaction": nextaction,
        "status": status,
        "role_name": role_name,
        "approve": approve,
        "reject": reject,
        "job_description": data[0]['description'],
        "is_e117": is_e117,
        "is_e60": is_e60,
        "e60_data": e60_data,
        "is_statutory": is_statutory,
        "jobtype": jobtype
    }
    return render(request, 'beweb/job/jobview.html', context)


def get_team_progress():
    team_table = JobTeamTable(my_team)
    team_table.paginate(page=request.GET.get('page', 1), per_page=2)
    jobp_table = JobProgressTable(my_progress)
    jobp_table.paginate(page=request.GET.get('page', 1), per_page=2)
    return team_table, jobp_table


class MyAsset(View):
    def get(self, request, *args, **kwargs):
        transformers = Transformer.objects.all()
        switch = Switchgear.objects.all()
        submeter = Substationmeter.objects.all()
        feeder = Feeder.objects.all()
        pole = Pole.objects.all()
        selected = ""
        centre = ""
        centre_code = ""
        data = execsys(request.user.username)
        centre_code = data['section']
        centre, centre_code = get_center(centre_code)
        username = data['username']

        transformer_table = TransformerTable(
            Transformer.objects.filter(centre=centre))
        transformer_table.paginate(page=request.GET.get('page', 1), per_page=5)
        RequestConfig(request).configure(transformer_table)
        return render(request, 'beweb/asset.html', {
            'transformers': transformers, 'switch': switch, 'submeter': submeter, 'selected': selected, 'transformer_table': transformer_table, 'feeder': feeder, 'pole': pole, 'centre': centre, 'centre_code': centre_code
        })

    def post(self, request, *args, **kwargs):
        return HttpResponse('Are you sure you want to save data')


def get_user(request):
    username = request.user.username
    data = execsys(username)
    myteam = ""
    team_leaders = []
    Teams = Team.objects.all()
    for teamleader in Teams:
        if teamleader.team_leader not in [member.team_leader for member in team_leaders]:
            team_leaders.append(teamleader)
            # my_teams[teamleader.team_leader]=[]
    myteam = artisan_team(username)
    myteam = ""
    teams = ""
    return render(request, 'beweb/wo.html', {
        'data': data, 'myteam': myteam, 'teams': teams, 'team_leaders': team_leaders
    })


def artisan_team1(ecnum):
    leader = ecnum
    teams = Team.objects.all()
    myteam = Team.objects.filter(team_leader=leader)
    return myteam, teams


def artisan_team(ecnum):
    leader = ecnum
    teams = Team.objects.all()
    myteam = Team.objects.filter(team_leader=leader)
    return myteam


@login_required(login_url='/login')
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request, 'beweb/landing.html', {
            'titeam_leaderse': 'Home Page',
            'year': datetime.now().year,
        }
    )


def dashboard(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    data = execsys(request.user.username)
    centre = data["section"]
    jobtp = JobType.objects.filter(Q(job_type_id='E117') | Q(job_type_id='E50') | Q(
            job_type_id='E60') | Q(job_type_id='E84')).values("job_type_id", "type")
     
    return render(
        request, 'beweb/index.html', {
            'titeam_leaderse': 'Dashboard',
             'jobtp': jobtp,
            'year': datetime.now().year, 'centre': centre
        }
    )


@login_required(login_url='/login')
def landing(request):
    return render(
        request, 'beweb/landing.html', {
            'titeam_leaderse': 'Bussiness Apps',
            'year': datetime.now().year,
        }
    )


def viewJobs(request):
    return render(request, 'beweb/jobs.html')


class ListJobs(View):

    def get(self, request, *args, **kwargs):
        data = execsys(request.user.username)
        section = data["section"]
        return render(request, 'beweb/reports/mywork.html', {"section": section})


def workorder_jobs(request, workorder_id):
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}
    url = "http://" + beserver + ":8087/beapi/workorder/jobs/" + workorder_id
    r = requests.get(url=url, headers=headers)
    data = r.json()
    context = {
        "workorder_id": workorder_id,
        "jobs": data[0]['jobs'],
    }

    return render(request, 'beweb/job/workorder_jobs.html', context)


def jobprogress(request):
    job_progress_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/jobprogress/" + job_progress_id
    r = requests.get(url=url, headers=headers)
    data = r.json()
    teamleader = execsys(data[0]['jobteam_members'][0]['teamleader'])
    context = {
        "job_progress_id": data[0]['job_progress_id'],
        "jobteam": ',    '.join([MyTeam['description'] for MyTeam in data[0]['jobteam_members']]),
        "teamleader": teamleader['firstname']+" "+teamleader['surname'],
        "comments": data[0]['comments'],
        "status": data[0]['status'],
        "start_dt": (datetime.strptime(data[0]['start_dt'], "%Y-%m-%d %H:%M:%S") if data[0]['start_dt'] else ''),
        "end_dt": (datetime.strptime(data[0]['end_dt'], "%Y-%m-%d %H:%M:%S") if data[0]['end_dt'] else ''),
        "job": data[0]['job'],
        "fleet_no": data[0]['fleet_no'],
        "open_mileage": data[0]['open_mileage'],
        "dt":  datetime.now(),
        "close_mileage": data[0]['close_mileage']
    }
    return render(request, 'beweb/job/jobprogress.html', context)


def seejob(request):
    """Renders the jobs View page"""
    return render(
        request, 'beweb/view_job.html'
    )


def editjob(request):
    """Renders the job edit page"""
    job_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/job/" + job_id+"/"
    r = requests.get(url=url, headers=headers)
    data = r.json()
    team_data = data[0]['job_progress'][0]['jobteam_members']
    end_date = data[0]['job_progress'][0]['end_dt']
    team_leader = data[0]['job_progress'][0]['jobteam_members'][0]['teamleader']
    employee_data = execsys(team_leader)
    fullname = employee_data['firstname'] + " " + employee_data['surname']
    context = {
        "job": data[0],
        "team_data": data[0]['job_progress'][0]['jobteam_members'],
        "team_members": len(team_data),
        "open_mileage": data[0]['job_progress'][0]['open_mileage'],
        "close_mileage": data[0]['job_progress'][0]['close_mileage'],
        "status": data[0]['job_progress'][0]['status'],
        "start_date": data[0]['job_progress'][0]['start_dt'],
        "fleet": data[0]['job_progress'][0]['fleet_no'],
        "job_progress": data[0]['job_progress'],
        "team_leader": fullname
    }
    return render(request, 'beweb/job/jobedit.html', context)

# def reassignjob(request,job_number):
#     """Renders the reassign-job page"""
#     # old_job = request.GET.get('job_number')
#     job_id = "JO"+datetime.now().strftime("%Y%m%d%H%M") + \
#             str(random.randrange(000000, 100000))    
#     username = request.user.username
#     usr, tkn = user_authenticate(username)
#     headers = {'Authorization': "Token "+tkn +
#                "", "Content-Type": "application/json"}

#     url = "http://" + beserver + ":8087/beapi/job/" + job_number+"/"
#     r = requests.get(url=url, headers=headers)
#     job_data = r.json()
#     workorder_id = job_data[0]['work_order']
#     workorder_data = Workorder.objects.filter(
#             work_order_id=workorder_id).values()
#     code_centre = workorder_data[0]['centre']
#     users = requests.get(url="http://" + beserver + ":8082/users/").json()
#     team_leaders = TeamLeader.objects.filter(centre=code_centre).values('team_leader')
#     artisans = [user for user in users if ((user['designation'] == 'Artisan -' or 'Artisan') and user['status'] == 'active') and user['section'] == code_centre]
#     available_artisans=artisans
#     artisan_assistants = [assistant for assistant in users if assistant['section'] == code_centre and assistant['status'] == 'active']
#     teams = Team.objects.values('team_leader_id').distinct()
#     teams = {}
    
#     context = {
#         "job": job_data[0],
#         "job_id":job_id,
#         "Artisans":available_artisans,
#         "Artisan_Assistants":artisan_assistants,
#         "teams":teams,
#         "code_centre":code_centre,
#     }
#     return render(request, 'beweb/job/reassignjob.html', context)


class JobReassign(APIView):
    def post(self, request, *args, **kwargs):
        job_id = request.GET.get('q', '')
        username = request.user.username
        usr, tkn = user_authenticate(username)
        headers = {'Authorization': "Token "+tkn +
                   "", 'Content-Type': 'application/json'}
        url = "http://" + beserver + ":8087/beapi/jobupdate/" + job_id
        job_description = request.POST.get('description')
        job_number = request.POST.get('job_number')
        wo = request.POST.get('wo')
        start_date = request.POST.get('start_date')
        job_type = request.POST.get('type')
        assignee= request.POST.get('the_leader')
        # team_members= request.POST('second')
       #team_mmbr = request.POST['teammember']
        
        trigger = request.POST.get('trigger')
        fleet = request.POST.get('fleet')
        reference_number = request.POST.get('old_job')
        createdby = username
        # asset_type = request.GET.get('plant_equipment')
        expected_end_dt = request.POST.get('expected_end_dt')
        centre = request.POST.get('centre')
        section = centre
        asset_id = None
        asset_type=None

        new_job = Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                            section, job_number, trigger, start_date, asset_type, reference_number, asset_id)

                          
        new_jobprog = job_progress(job_number, createdby, fleet)
        new_team = save_team(username, assignee, new_jobprog, team_members)
        
        return render(request, 'beweb/job/notification.html')

class ChangeJob(APIView):
    def get(self, request, *args, **kwargs):
        job_id = request.GET['job_number']
        username = request.user.username
        usr, tkn = user_authenticate(username)
        headers = {'Authorization': "Token "+tkn +
                   "", 'Content-Type': 'application/json'}
        url = "http://" + beserver + ":8087/beapi/jobupdate/" + job_id
        description = request.GET['description']
        start_date = request.GET['start_date']
        type = request.GET['type']
        trigger = request.GET['trigger']
        fleet = request.GET['fleet']
        asset_type = request.GET['plant_equipment']
        expected_end_dt = request.GET['expected_end_dt']
        data = {
            "job_id": job_id,
            "description": description,
            # "job_progress":[
            #     {
            #     "fleet_no":fleet
            #     }
            # ],
            "type": type,
            "start_date": start_date,
            "expected_end_dt": expected_end_dt,
            "trigger": trigger,
            "asset_type": asset_type
        }
        data = json.dumps(data)

        r = requests.patch(url=url, data=data, headers=headers)

        URL = "http://" + beserver + ":8087/beapi/job/" + job_id+"/"
        r1 = requests.get(url=URL, headers=headers)
        data1 = r1.json()
        team_data = data1[0]['job_progress'][0]['jobteam_members']
        end_date = data1[0]['job_progress'][0]['end_dt']
        team_leader = data1[0]['job_progress'][0]['jobteam_members'][0]['teamleader']
        employee_data = execsys(team_leader)
        fullname = employee_data['firstname'] + " " + employee_data['surname']
        section = employee_data['section']
        status = data1[0]['status']
        description = data1[0]['description']
        try:
            start = datetime.strptime(
                data1[0]['job_progress'][0]['start_dt'],  "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(
                data1[0]['job_progress'][0]['end_dt'],  "%Y-%m-%d %H:%M:%S")
            delta = (datetime(end.year, end.month, end.day, end.hour, end.minute, end.second) -
                     datetime(start.year, start.month, start.day, start.hour, start.minute, start.second))
        except:
            delta = ''

        context = {
            "job": data1[0],
            "section": section,
            "team_data": data1[0]['job_progress'][0]['jobteam_members'],
            "team_members": len(team_data),
            "open_mileage": data1[0]['job_progress'][0]['open_mileage'],
            "close_mileage": data1[0]['job_progress'][0]['close_mileage'],
            "status": data1[0]['job_progress'][0]['status'],
            "start_date": data1[0]['job_progress'][0]['start_dt'],
            "start_dt": (datetime.strptime(data1[0]['job_progress'][0]['start_dt'], "%Y-%m-%d %H:%M:%S") if data1[0]['job_progress'][0]['start_dt'] else ''),
            "expected_end_dt": (datetime.strptime(data1[0]['expected_end_dt'], "%Y-%m-%d") if data1[0]['expected_end_dt'] else ''),
            "fleet": data1[0]['job_progress'][0]['fleet_no'],
            "job_progress": data1[0]['job_progress'],
            "team_leader": fullname,
            "hours": delta,
            "status": status,
            "description": description
        }
        jobprogress = data1[0]['job_progress']
        return render(request, 'beweb/job/jobview.html', context)


def wo(request):
    """Renders the E84 page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'beweb/wo.html',
        {
            'titeam_leaderse': 'E84 Page',
            'year': datetime.now().year,
        }
    )


def all_centres():
    url = "http://" + beserver + ":8082/centres/"
    r = requests.get(url=url)
    data = r.json()
    centres = {}

    for value in data:
        if value['scode'] == "URB":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "ENV":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "RSP":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "NYA":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "CHP":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "CHM":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MSB":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "RUT":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "GUT":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "CHR":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MAS":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MSV":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MTD":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MND":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MSD":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MTG":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
        elif value['scode'] == "MSG":
            centrecode = value['scode']
            centres[centrecode] = value['centrename']
    return centres


def create(request):
    data = execsys(request.user.username)
    centre_code = data['section']
    usr, tkn = user_authenticate(request.user.username)
    headers = {'Authorization': "Token "+tkn +
               "", 'Content-Type': 'application/json'}
    url = "http://" + beserver + ":8087/beapi/all_centres/"+centre_code
    all_parent_centres = requests.get(url=url, headers=headers)
    allcentres = all_parent_centres.json()
    jobtp = JobType.objects.filter(Q(job_type_id='E117') | Q(job_type_id='E50') | Q(
            job_type_id='E60') | Q(job_type_id='E84')).values("job_type_id", "type")
     
    work_order = "WO"+datetime.now().strftime("%Y%m%d%H%M") + \
        str(random.randrange(000000, 100000))
    username = data['username']
    centre, centre_code = get_center(centre_code)
    centres = all_centres()
    request.session['work_order'] = work_order
    request.session['centre'] = centre
    request.session['centre_code'] = centre_code
    request.session['centres'] = centres
    request.session['username'] = username
    request.session['year'] = (datetime.now()).isoformat()
    return render(
        request,
        'beweb/workorder/create.html',
        {
          'jobtp':jobtp,  'work_order': work_order, 'centre': centre, 'allcentres': allcentres, 'centre_code': centre_code, 'centres': centres, 'username': username,
            'year': datetime.now(),
        })


class Mywo(View):
    def post(self, request, *args, **kwargs):
        username = request.user.username
        data = execsys(username)
        username = data['username']
        description = request.POST['description']
        supervisor = request.POST['supervisor']
        date = datetime.now().strftime("%Y%m%d%H%M")
        centre_code = request.POST['centre_code']
        centre = centre_code
        work_order_id = request.POST['work_order_id']
        job_id = "JO"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        team_leaders = []
        jobtp = JobType.objects.filter(Q(job_type_id='E117') | Q(job_type_id='E50') | Q(
            job_type_id='E60') | Q(job_type_id='E84')).values("job_type_id", "type")
        Teams = Team.objects.values('team_leader_id').distinct()
        team_leaders = [team_leader['team_leader_id'] for team_leader in Teams]

        teams = {}
        for team_leader in team_leaders:
            team_members = [team_member['team_member'] for team_member in Teams.values(
            ) if team_member['team_leader_id'] == team_leader]
            data = execsys(team_leader)
            teamleader = {
                "ec_number": team_leader,
                "firstname": data['firstname'],
                "lastname": data['surname']
            }
            members = []
            for member in team_members:
                data1 = execsys(member)
                first_name = data1['firstname']
                last_name = data1['surname']
                our_team = {
                    "ec_number": member,
                    "firstname": first_name,
                    "lastname": last_name
                }
                members.append(our_team)
            team_sheet = []
            team_sheet.append(teamleader)
            team_sheet.append(members)
            teams[team_leader] = team_sheet
            team_leader = ''

        # variable declared to allow for creation of Job starting from a workorder (already created). Logic implemented in the SaveJob view`s if statement
        request.session['workorder_number'] = ''
        request.session['description'] = description
        request.session['teams'] = teams
        request.session['job_type_id'] = jobtp[0]['job_type_id']
        request.session['type'] = jobtp[0]['type']
        # request.session['_fleet'] = request.POST['_fleet']
        # request.session['teammembers'] = request.POST['teammembers']
        # request.session['job_assignee'] = request.POST['job_assignee']
       
        contractors = get_contractors(username)
        return render(request, 'beweb/job/createjob_workorder.html', {
            'wo': work_order_id, 'job_id': job_id, 'centre': centre, 'centre_code': centre_code, 'username': username, 'description': description,
            'year': datetime.now(), 'teams': teams, 'jobtp': jobtp, "contractors": contractors
        })


class Create_E117_Job(View):
    def get(self, request, *args, **kwargs):
        workorder_Id = request.GET.get('q', '')
        request.session['workorder_number'] = workorder_Id
        username = request.user.username
        data = execsys(username)
        centre_code = data['section']
        username = data['username']
        centre, centre_code = get_center(centre_code)
        jobtype = JobType.objects.filter(Q(type='Line Inspection') | Q(
            type='Installation Inspection')).values("job_type_id", "type")
        date = datetime.now()
        job_id = "JO"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        username = data['username']
        section = data['section']
        teams = {}
        return render(request, 'beweb/job/create_E117.html', {'work_order': workorder_Id, 'job_id': job_id, 'centre': centre, 'centre_code': centre_code, 'username': username,
                                                              'year': datetime.now(), 'jobtype': jobtype})

    def post(self, request, *args, **kwargs):
        return HttpResponse('Are you sure you want to save data')


class SaveJobandAddAsset(View):
    def post(self, request, *args, **kwargs):
        job_type = request.POST['jobtype']
        job_number = request.POST['job_number']
        wo = request.POST['workorder_number']
        username = request.user.username
        data = execsys(username)
        centre_code = data['section']
        username = data['username']
        fleet = request.POST['_fleet']
        assignee = request.POST['job_assignee']

        team_members = request.POST.getlist('teammembers')
        

        
        section = data['section']
        centre, centre_code = get_center(centre_code)
        user_centre = data['centre']

        if job_type == 'E84':
            team_members = []
            trigger = request.POST['trigger']
            start_date = request.POST['e84_start_date']
            asset_type = request.POST['asset_type']
            job_description = request.POST['description']
            expected_end_dt = request.POST['e84_expected_end_dt']
            createdby = request.user.username
            username = createdby
            jobtp = JobType.objects.filter(
                job_type_id='E84').values("job_type_id")
            request.session['assignee'] = assignee
            request.session['trigger'] = trigger
            request.session['fleet'] = fleet
            request.session['start_date'] = start_date
            request.session['asset_type'] = asset_type
            request.session['job_description'] = job_description
            request.session['team_members'] = team_members
            request.session['expected_end_dt'] = expected_end_dt
            request.session['section'] = section
            request.session['job_number'] = job_number
            request.session['job_type_id'] = job_type
            if asset_type == 'feeder':
                column_one = 'Feeder Id'
                column_two = 'Name'
                column_three = 'Voltage'
                column_four = 'Length'
                data_one = 'feedercode'
                data_two = 'name'
                data_three = 'voltagelevel'
                data_four = 'length'
            elif asset_type == 'station':
                column_one = 'Station Id'
                column_two = 'Name'
                column_three = 'Classification'
                column_four = 'Enclosure'
                data_one = 'stationid'
                data_two = 'name'
                data_three = 'classification'
                data_four = 'enclosure'
            elif asset_type == 'pole':
                column_one = "Pole Id"
                column_two = "Pole Material"
                column_three = "Feeder"
                column_four = "Position Type"
                data_one = 'poleid'
                data_two = 'material'
                data_three = 'feeder'
                data_four = 'positiontype'
            elif asset_type == 'meter':
                column_one = 'Meter Id'
                column_two = 'Meter No.'
                column_three = 'Make'
                column_four = 'Metering Type'
                data_one = 'meterid'
                data_two = 'meterno'
                data_three = 'make'
                data_four = 'meteringtype'
            elif asset_type == 'switchgear':
                column_one = 'Switchgear Id'
                column_two = 'Type'
                column_three = 'Voltage Rating'
                column_four = 'Feeder Code'
                data_one = 'switchgearid'
                data_two = 'type'
                data_three = 'voltagerating'
                data_four = 'feedercode'
            elif asset_type == 'transformer':
                column_one = 'Transformer Id'
                column_two = 'Make'
                column_three = 'Voltage Ratio'
                column_four = 'Name'
                data_one = 'transformerid'
                data_two = 'make'
                data_three = 'voltageratio'
                data_four = 'name'
            context = {
                'joid': job_number,
                'wo': wo,
                'centre': centre,
                'centre_code': centre_code,
                'username': username,
                'year': datetime.now(),
                'asset_type': asset_type,
                'column_one': column_one,
                'column_two': column_two,
                'column_three': column_three,
                'column_four': column_four,
                'data_one': data_one,
                'data_two': data_two,
                'data_three': data_three,
                'data_four': data_four,
                'job_type': job_type,
                'user_centre': user_centre
            }
        elif job_type == 'E50':
            asset_type = None
            column_one = None
            column_two = None
            column_three = None
            column_four = None
            data_one = None
            data_two = None
            data_three = None
            data_four = None
            trigger = None
            start_date = request.POST['e50_start_date']
            job_description = request.POST['e50_description']
            expected_end_dt = request.POST['e50_expected_end_dt']
            request.session['assignee'] = assignee
            request.session['trigger'] = trigger
            request.session['fleet'] = fleet
            request.session['start_date'] = start_date
            request.session['asset_type'] = asset_type
            request.session['job_description'] = job_description
            request.session['teammembers'] = team_members
            
            request.session['expected_end_dt'] = expected_end_dt
            request.session['section'] = section
            request.session['job_number'] = job_number
            request.session['job_type_id'] = job_type
            context = {
                'joid': job_number,
                'wo': wo,
                'centre': centre,
                'centre_code': centre_code,
                'username': username,
                'year': datetime.now(),
                'asset_type': asset_type,
                'column_one': column_one,
                'column_two': column_two,
                'column_three': column_three,
                'column_four': column_four,
                'data_one': data_one,
                'data_two': data_two,
                'data_three': data_three,
                'data_four': data_four,
                'job_type': job_type,
                'user_centre': user_centre
            }
        elif job_type == 'E60':
            asset_type = None
            column_one = None
            column_two = None
            column_three = None
            column_four = None
            data_one = None
            data_two = None
            data_three = None
            data_four = None
            trigger = None
            work_type = request.POST['work_type']
            start_date = request.POST['e60_start_date']
            job_description = request.POST['e60_description']
            expected_end_dt = request.POST['e60_expected_end_dt']
            request.session['assignee'] = assignee
            request.session['trigger'] = trigger
            request.session['fleet'] = fleet
            request.session['start_date'] = start_date
            request.session['asset_type'] = asset_type
            request.session['job_description'] = job_description
            request.session['second'] = team_members
            request.session['expected_end_dt'] = expected_end_dt
            request.session['section'] = section
            request.session['job_number'] = job_number
            request.session['job_type_id'] = job_type
            context = {
                'joid': job_number,
                'wo': wo,
                'centre': centre,
                'centre_code': centre_code,
                'username': username,
                'year': datetime.now(),
                'asset_type': asset_type,
                'column_one': column_one,
                'column_two': column_two,
                'column_three': column_three,
                'column_four': column_four,
                'data_one': data_one,
                'data_two': data_two,
                'data_three': data_three,
                'data_four': data_four,
                'job_type': job_type,
                'user_centre': user_centre,
                'work_type': work_type
            }

        return render(request, 'beweb/assets/assets.html', context)


class SaveJob(View):
    def post(self, request, *args, **kwargs):
        reference_number = None
        job_type = request.POST['jobtype']
        asset_id = None
        # IF WORKORDER DOES NOT EXIST, create workorder first
        if not request.session['workorder_number']:
            if job_type == 'E84':
                username = request.session['username']
                description = request.session['description']
                supervisor = request.session['username']
                centre = request.session['centre_code']
                centre_code = request.session['centre_code']
                work_order_id = request.session['work_order']
                date = datetime.now().strftime("%Y%m%d%H%M")
                createdby = request.session['username']
                wo = request.session['work_order']
                data = execsys(username)
                section = data['section']
                assignee = request.POST['assignee']
                job_number = request.POST['job_number']

                job_description = request.POST['description']
                
                
                start_date = request.POST['e84_start_date']
                trigger = request.POST['trigger']
                jobtp = JobType.objects.filter(
                    type='Line Inspection').values("job_type_id")
                fleet = request.POST['fleet']
                asset_type = request.POST['asset_type']
                expected_end_dt = request.POST['e84_expected_end_dt']

            elif job_type == 'E50':
                username = request.session['username']
                description = request.session['description']
                supervisor = request.session['username']
                centre = request.session['centre_code']
                centre_code = request.session['centre_code']
                work_order_id = request.session['work_order']
                date = datetime.now().strftime("%Y%m%d%H%M")
                createdby = request.session['username']
                wo = request.session['work_order']
                data = execsys(username)
                section = data['section']
                assignee = request.POST['job_assignee']
                team_members = request.POST['teammembers']
                job_number = request.POST['job_number']

                job_description = request.POST['e50_description']
               #team_mmbr = request.POST['e50_tnames']
                
                start_date = request.POST['e50_start_date']
                trigger = None
                jobtp = JobType.objects.filter(
                    job_type_id='E50').values("job_type_id")
                fleet = request.POST['_fleet']
                asset_type = None
                expected_end_dt = request.POST['e50_expected_end_dt']
                station_id = None
                e50_id = "E50"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))

            elif job_type == 'E60':
                username = request.session['username']
                description = request.session['description']
                supervisor = request.session['username']
                centre = request.session['centre_code']
                centre_code = request.session['centre_code']
                work_order_id = request.session['work_order']
                date = datetime.now().strftime("%Y%m%d%H%M")
                createdby = request.session['username']
                work_type = request.POST['work_type']
                wo = request.session['work_order']
                data = execsys(username)
                section = data['section']
                district = request.POST['section']
                assignee = request.POST['e60_assignee']
                job_number = request.POST['job_number']
                job_description = request.POST['e60_description']
               #team_mmbr = request.POST['e60_tnames']
                
                start_date = request.POST['e60_start_date']
                trigger = None
                jobtp = JobType.objects.filter(
                    job_type_id='E60').values("job_type_id")
                fleet = request.POST['_fleet']
                asset_type = None
                expected_end_dt = request.POST['e60_expected_end_dt']
                transformer_id = None
                e60_id = "E60"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))

            wo1 = save_wo(username, description, supervisor,
                          centre, date, centre_code, work_order_id)
            joid = Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                            section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
            if job_type == 'E50':
                save_e50(e50_id, job_number, createdby, station_id)
            elif job_type == 'E60':
                save_e60(e60_id, job_number, createdby,
                         transformer_id, work_type)
            else:
                pass
            jp = job_progress(job_number, createdby, fleet)
            a = save_team(username, assignee, jp, team_members)
            del request.session['description']
            del request.session['centre_code']
            del request.session['work_order']
            del request.session['workorder_number']
        else:
            if job_type == 'E84':
                wo = request.session['workorder_number']
                createdby = request.user.username
                username = request.user.username
                assignee = request.POST['assignee']
                job_description = request.POST['description']
                expected_end_dt = request.POST['e84_expected_end_dt']
                data = execsys(request.user.username)
                centre = data['section']
                section = data['section']
                job_number = request.POST['job_number']
                trigger = request.POST['trigger']
                start_date = request.POST['e84_start_date']
                asset_type = request.POST['asset_type']
                fleet = request.POST['fleet']
                
                
            elif job_type == 'E50':
                wo = request.session['workorder_number']
                createdby = request.user.username
                username = request.user.username
                assignee = request.POST['job_assignee']
                job_description = request.POST['e50_description']
                expected_end_dt = request.POST['e50_expected_end_dt']
                data = execsys(request.user.username)
                centre = data['section']
                section = data['section']
                job_number = request.POST['job_number']
                trigger = None
                start_date = request.POST['e50_start_date']
                asset_type = None
                fleet = request.POST['_fleet']
               #team_mmbr = request.POST['e50_tnames']
                
                e50_id = "E50"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
                station_id = None

            elif job_type == 'E60':
                wo = request.session['workorder_number']
                createdby = request.user.username
                username = request.user.username
                assignee = request.POST['e60_assignee']
                district = request.POST['section']
                work_type = request.POST['work_type']
                job_description = request.POST['e60_description']
                expected_end_dt = request.POST['e60_expected_end_dt']
                data = execsys(request.user.username)
                centre = data['section']
                section = data['section']
                job_number = request.POST['job_number']
                trigger = None
                start_date = request.POST['e60_start_date']
                asset_type = None
                fleet = request.POST['_fleet']
               #team_mmbr = request.POST['e60_tnames']
                
                e60_id = "E60"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
                transformer_id = None

            joid = Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                            section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
            if job_type == 'E50':
                save_e50(e50_id, job_number, createdby, station_id)
            elif job_type == 'E60':
                save_e60(e60_id, job_number, createdby,
                         transformer_id, work_type, district)
            else:
                pass
            jp = job_progress(job_number, createdby, fleet)
            a = save_team(username, assignee, jp, team_members)
            del request.session['workorder_number']
        return render(request, 'beweb/job/notification.html')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Are you sure you want to save data')


class Myjob(View):
    def get(self, request, *args, **kwargs):
        team_members = []
        username = request.user.username
        data = execsys(username)
        centre_code = data['section']
        username = data['username']
        section = data['section']
        centre, centre_code = get_center(centre_code)
        wo = request.GET['wo']
        assignee = request.GET['assignee']
        job_type = request.GET['jobtype']
        description = request.GET['description']
       #team_mmbr = request.GET['tnames']
        trigger = request.GET['trigger']
        fleet = request.GET['fleet']
        start_date = request.GET['e84_start_date']
        asset_type = request.GET['asset_type']
        
        expected_end_dt = request.GET['e84_expected_end_dt']
        createdby = request.user.username
        username = createdby
        jobtp = JobType.objects.filter(
            type='Line Inspection').values("job_type_id")
        joid = save_jobworkflow(createdby, assignee, job_type,
                                wo, description, expected_end_dt, centre, section)
        jp = job_progress(joid, createdby, fleet)
        a = save_team(username, assignee, jp, team_members)
        return render(request, 'beweb/assets/create.html', {
            'joid': joid, 'wo': wo, 'centre': centre, 'centre_code': centre_code, 'username': username,
            'year': datetime.now(), 'jobtp': jobtp, "a": a, 'jp': jp
        })


class MyjobAsset(View):
    def post(self, request, *args, **kwargs):
        username = request.user.username
        wo = request.form['wo']
        jobid = request.form['jobid']
        asset_id = request.form['equipment_id']
        asset_name = request.form['make']
        asset_type = request.form['asset_type']
        asset_number = request.form['asset_number']
        asset_serial = request.form['asset_serial']
        data = {
            "asset_id": asset_id,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "asset_number": asset_number,
            "asset_serial": asset_serial,
        }
        url = 'http://' + beserver + ':8087/beapi/jobupdate/' + str(jobid)
        usr, tkn = user_authenticate(username)
        headers = {'Authorization': "Token "+tkn +
                   "", "Content-Type": "application/json"}

        r = requests.patch(url=url, data=data, headers=headers)
        job = Job.objects.filter(job_id=jobid)
        return render(request, 'beweb/reports/mywork.html', {
            'job': job
        })


def generate_job_progress_id():
    jp_id = datetime.now().strftime("%Y%m%d%H%M") + \
        str(random.randrange(000000, 100000))
    return jp_id


def job_progress(job_id, createdby, fleet):
    jp_id = generate_job_progress_id()
    usr, tkn = user_authenticate(createdby)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/jobprogresspost"
    data = {
        "job_progress_id": "jp" + str(jp_id),
        "created_by": createdby,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comments": "",
        # "action": "",
        "status": 1,
        "fleet_no": fleet,
        "job": str(job_id)
    }
    data = json.dumps(data)

    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()
    jp_id = "jp" + str(jp_id)
    return jp_id


def save_jobworkflow(created_by, job_id, workflow_id, created_on):
    usr, tkn = user_authenticate(created_by)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}
    url = "http://" + beserver + ":8087/beapi/jobworkflowpost"
    data = {
        "workflow": workflow_id,
        "job_workflow_id": "jwf" + datetime.now().strftime("%Y%m%d%H%M") + str(random.randrange(000000, 100000)),
        "job": job_id,
        "created_by": created_by,
        "created_on": created_on,
    }
    data = json.dumps(data)

    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()


def generate_job_team_id():
    jt = datetime.now().strftime("%Y%m%d%H%M") + \
        str(random.randrange(000000, 100000))
    return jt


def save_team(username, assignee, jp_id, team_members):
    team_leaders = assignee
    
    for membr in team_members:
        member = membr.partition('%')[2]
        membername = membr.partition('%')[0]
        # if member:
        id = generate_job_team_id()
        
        usr, tkn = user_authenticate(username)
        url = "http://" + beserver + ":8087/beapi/jobteampost"
        headers = {'Authorization': "Token "+tkn +
                    "", "Content-Type": "application/json"}

        data = {
            "job_team_id": "jt" + id,
            "ec_num": member,
            "start_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_dt": "",
            "description": membername,
            "teamleader": team_leaders,
            "job_progress": jp_id
        }
        data = json.dumps(data)
        r = requests.post(url=url, data=data, headers=headers)
        response_data = r.json()
        
        member_id = member
    return team_leaders


def post_data(url, payload, headers):
    r = requests.request("POST", url, data=payload, headers=headers)
    response = r.json()
    return response


def generate_work_order_id():
    wo = datetime.now().strftime("%Y%m%d%H%M") + \
        str(random.randrange(000000, 100000))
    return wo


def save_wo(username, description, supervisor, centre, date, centre_code, work_order_id):
    wo = work_order_id
    usr, tkn = user_authenticate(username)
    url = 'http://' + beserver + ':8087/beapi/workorderpost'
    headers = {'Authorization': "Token "+tkn +
               "", 'Content-Type': 'application/json'}
    data = {
        "work_order_id": wo,
        "created_by": supervisor,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modified_by": "",
        "modified_on": None,
        "description": description,
        "centre": centre,
        "comments": None,
        "status": 1
    }
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()
    wo = response_data["work_order_id"]
    return wo


def generate_job_id():
    job_id = datetime.now().strftime("%Y%m%d%H%M") + \
        str(random.randrange(000000, 100000))
    return job_id


def Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre, section, job_number, trigger, start_date, asset_type, reference_number, asset_id):
    usr, tkn = user_authenticate(createdby)
    action_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    workflow_code, workflow_id = updateworkflow(section, job_type)
    url = 'http://' + beserver + ':8087/beapi/jobpost'
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"
               }

    data = {
        "job_id": job_number,
        "created_by": createdby,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": job_type,
        "description": job_description,
        "assignee": assignee,
        "start_date": start_date,
        "trigger": trigger,
        "expected_end_dt": expected_end_dt,
        "workflow": workflow_code,
        "status": 1,
        "work_order": wo,
        "asset_type": asset_type,
        "asset_id": asset_id

    }

    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()
    
    

    if reference_number is not None:
        patch_url = "http://" + beserver + ":8087/beapi/jobupdate/"+reference_number
        patch_data = {
            "reference_no": job_number
        }
        patch_data = json.dumps(patch_data)
        response = requests.patch(
            url=patch_url, data=patch_data, headers=headers)
    else:
        pass
    created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jo = job_number
    job_type = job_type
    save_jobworkflow(createdby, jo, workflow_id, created_on)
    return job_number


def updateworkflow(section, job_type):
    workflow_code = Appflow.objects.filter(section=section, app=job_type).values(
        'workflow_code')[0]['workflow_code']
    workflow_id = Workflow.objects.filter(
        workflow_code=workflow_code, step=1).values('workflow_id')[0]['workflow_id']
    return workflow_code, workflow_id

def get_workers():
    code_centre = workorder[0]['centre']
    #getting users from staff
    users = requests.get(url="http://" + beserver + ":8082/users/").json()
    # geting all artisans
    artisans = [user for user in users  if (user['designation'] == 'Artisan') and (user['status'] == 'active') and( user['section'] == code_centre)]
    # for artisan in artisans:
    #    data= schema.execute('{teamleders{teamLeader specialisation centre members{teamMember }}}').data['teamleders']
    workers= schema.execute('{teamleders{teamLeader specialisation centre members{teamMember }}}').data['teamleders']
    team_leaders = TeamLeader.objects.filter(centre=code_centre).values('team_leader')
    team_members = Team.objects.filter(centre=code_centre)
    artisan_assistants = [assistant for assistant in users if ((assistant['section'] == code_centre)and(assistant['designation'] == 'Artisan')  and( assistant['status'] == 'active'))]
    return workers
def get_depot_name(code):
    name=code
    if code == "URB":
        name = "Mutare Urban"
    elif code == "ENV":
        name = "Mutare Environs"
    elif code == "RSP":
        name = "Rusape"
    elif code == "NYA":
        name = "Nyanga"
    elif code == "CHP":
        name = "Chipinge"
    elif code == "CHM":
        name = "Chimanimani"
    elif code == "MSB":
        name = "Middle Sabi"
    elif code == "RUT":
        name = "Rutenga"
    elif code == "GUT":
        name = "Gutu"
    elif code == "CHR":
        name = "Chiredzi"
    elif code == "MAS":
        name = "Mashava"
    elif code == "MSV":
        name = "Masvingo Urban"
    elif code == "MTD":
        name = "Mutare District"
    elif code == "MND":
        name = "Manicaland District"
    elif code == "MSD":
        name = "Masvingo District"
    elif code == "MTG":
        name = "Mutare Garage"
    elif code == "MSG":
        name = "Masvingo Garage"

    return name
   
class AddJob(View):
     def get(self, request, *args, **kwargs):
        workorder_Id = request.GET.get('q')
        type=request.GET.get('jobtype')
        
        request.session['workorder_number'] = workorder_Id
        """get workers to associate with the job"""
        workers= schema.execute('{teamleders{teamLeader specialisation centre members{teamMember }}}').data['teamleders']
       
        workorder = Workorder.objects.filter(work_order_id=workorder_Id)
        print("__________________")
        print(workorder)
        print("__________________")


        job_id = "JO"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        code_centre = workorder[0]['centre']
        users = requests.get(url="http://" + beserver + ":8082/users/").json()
        artisans = [user for user in users if (('Assistant' not in user['designation']) and('Artisan' in user['designation']) and user['status'] == 'active')]
        artisan_assistants = [assistant for assistant in users if ((assistant['section'] == code_centre)and
        (assistant['designation'] == 'Artisan')  and( assistant['status'] == 'active'))]
        for artisan in artisans:
            for leader in workers:
                if (artisan['username']).lower()==(leader['teamLeader']).lower():
                    details= execsys(leader['teamLeader'])
                    depot= get_depot_name(details['section'])
                    leader['depot']=depot
                    leader['name'] = details['firstname'][0].upper() +' . ' + details['surname']
                    for member in leader['members']:
                        memberdetails= execsys(member['teamMember'])
                        memberdepot= get_depot_name(memberdetails['section'])
                        member['depot']=memberdepot
                        member['name'] = memberdetails['firstname'][0].upper() +' . ' + memberdetails['surname']
       
        return render(request, 'beweb/job/creation_forms/'+type.lower()+'.html', {
            'wo': workorder_Id,
            'artisan_assistants':artisan_assistants,
            'year': datetime.now(), 
            'teams': workers,
            'job_id':job_id,
            'type':type,
            "description": workorder[0]['description'],
            "contractors": get_contractors(request.user.username)
            })
       

def get_contractors(username):
    user, token = user_authenticate(username)
    headers = {'Authorization': "Token "+token +
               "", "Content-Type": "application/json"}
    url = "http://" + beserver + ":8087/beapi/e117contractor/all/"
    contractor = requests.get(url=url, headers=headers)
    contractors = contractor.json()
    return contractors


def get_available_artisans(workers, people):
    available_workers = workers
    for person in people:
        for worker in workers:
            if (person['onduty']==False):
                available_workers.remove(worker)
    return available_workers

def create_team(request):
    users = requests.get(url="http://" + beserver + ":8082/users/").json()
    username = request.user.username
    data = execsys(username)
    centre_code = data['section']
    username = data['username']
    centre, centre_code = get_center(centre_code)
    if("specialisation" in request.GET):
        specialisation = request.GET['specialisation']
        team_leaders = TeamLeader.objects.filter(
            specialisation=specialisation, centre=centre_code).values('team_leader')
        artisans = [user for user in users if ((user['designation'] == 'Artisan - ' + request.GET['specialisation'])
                                               and user['status'] == 'active') and user['section'] == centre_code]
        available_artisans = get_available_artisans(artisans, team_leaders)
        artisan_assistants = [user for user in users if (
            (user['designation'] == 'Artisan Assistant - '+request.GET['specialisation']) and user['status'] == 'active') and user['section'] == centre_code]
        return render(request, 'beweb/team/create.html', {
            'Artisans': available_artisans, 'ArtisanAssistants': artisan_assistants, 'specialisation': specialisation
        })
    else:
        return render(request, 'beweb/team/create.html', {
        })


def view_Teams(request):
    username = request.user.username
    usr, tkn = user_authenticate(username)
    data = execsys(username)
    centre_code = data['section']
    headers = {'Authorization': "Token "+tkn +
            "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/teams/" + centre_code
    teams = requests.get(url=url, headers=headers)
    team_d = teams.json()
    leaders = []

    for leader in team_d:
        team_data = execsys(leader['team_leader'])
        team = {
            'ec_number': leader['team_leader'],
            'fullname': team_data['firstname']+" "+team_data['surname'],
            'specialisation': leader['specialisation'],
            'members': len(leader['members'])
        }
        leaders.append(team)
    return render(request, 'beweb/team/teamsview.html', {'leaders': leaders})


def editTeam(self, request):
    return render(request, 'beweb/team/teamedit.html')


def view_Team(request, ec_number):
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
            "", "Content-Type": "application/json"}
    url = "http://" + beserver + ":8087/beapi/team/"+ ec_number
    teams = requests.get(url=url, headers=headers)
    team_data = teams.json()
    team_leader=[]
    specialisation=[]
    team_list=[]
    for team in team_data:
        leader_data = execsys(team['team_leader'])
        team_leader = leader_data['firstname']+" "+leader_data['surname']
        specialisation = team['specialisation']

        for member in team['members']:
            member_data = execsys(member['team_member'])
            team = {
                "team_members": member_data['firstname']+" "+member_data['surname']
            }
            team_list.append(team)
    return render(request, 'beweb/team/viewteam.html', {'team_list': team_list, 'team_leader': team_leader, 'specialisation': specialisation})


def addteam(request):
    url1 = "http://" + beserver + ":8087/beapi/teampost"
    createdby = request.user.username
    data = execsys(createdby)
    centre_code = data['section']
    username = data['username']
    centre, centre_code = get_center(centre_code)
    usr, tkn = user_authenticate(createdby)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}
    data = requests.get(url="http://" + beserver + ":8082/users/").json()
    tmbrs = (request.GET['teammember']).split(", ")
    tmbrs = tmbrs[:-1]
    tldr = (request.GET['teamleader']).split("  ")
    lecnums = [x['username'] for x in data if (
        (x['firstname'] == tldr[0])and (x['surname'] == tldr[1]))]
    if lecnums:
        tms = []
        for lecnum in lecnums:
            for member in tmbrs:
                tmbr = (member).split("  ")
                ecnums = [x['username'] for x in data if (
                    (x['firstname'] == tmbr[0])and (x['surname'] == tmbr[1]))]
                if ecnums:
                    for ecnum in ecnums:
                        tms.append({
                            "team_id": "tm" + datetime.now().strftime("%Y%m%d%H%M") + str(random.randrange(000000, 100000)),
                            "created_by": createdby,
                            "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "team_leader": lecnum,
                            "team_member": ecnum,
                            "centre": centre_code,
                            "specialisation": request.GET['teamspecialisation']
                        })
            data1 = {"team_leader": lecnum,
                     "team": tms,
                     "specialisation": request.GET['teamspecialisation'],
                     "centre": centre_code
                     }
            data1 = json.dumps(data1)
            r = requests.post(
                url="http://" + beserver + ":8087/beapi/teampost", data=data1, headers=headers)
            response_data = r.json()

    return render(request, 'beweb/team/notification.html', {
    })


def listForms(request):
    job_id = request.GET.get('job_id', '')
    context = {
        "job_id": job_id
    }
    return render(request, 'beweb/job/forms.html', context)


def displayE84Form(request):
    return render(request, 'beweb/job/e84.html')


def e117Form(request):
    e117_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}
    # GET E117 DATA
    url = "http://" + beserver + ":8087/beapi/e117/" + e117_id + "/"
    r = requests.get(url=url, headers=headers)
    data = r.json()
    employee_data = execsys(data[0]['created_by'])
    fullname = employee_data['firstname'] + " " + employee_data['surname']
    # GET CLIENT DATA USING CLIENT RETURNED FROM ABOVE REQUEST
    client_data = []
    if ((str(data[0]['number_of_clients']) == 'multiple')):
        data[0]['number_of_clients'] = 'Multiple'
        client_data = client_data
    else:
        client_url = "http://" + beserver + ":8087/beapi/client/" + \
            data[0]['e117client']+"/"
        client_result = requests.get(url=client_url, headers=headers)
        c_data = client_result.json()
        client_data = c_data[0]
    # GET CONTRACTOR DATA FROM THE CONTRACTOR ID FROM ABOVE REQUEST
    contractor = []
    inspection_type = data[0]['client_inspection_type']

    if inspection_type == "new_installation" or inspection_type == "re_inspection":
        contractor_url = "http://" + beserver + ":8087/beapi/e117contractor/" + \
            data[0]['client_contractor'] + "/"
        contractor_result = requests.get(url=contractor_url, headers=headers)
        contractor = contractor_result.json()
        contractor = contractor[0]
    else:
        pass
    # CHECK IF THERE IS A COMMENT
    insd_neutrals_fused = (str(data[0]['insd_neutrals_fused'])).lower() == "no"
    insd_block_fitted = (str(data[0]['insd_block_fitted'])).lower() == "no"
    insd_electrode_installed = (
        str(data[0]['insd_electrode_installed'])).lower() == "no"
    insd_bonded_earth = (str(data[0]['insd_bonded_earth'])).lower() == "no"
    insd_outlets_earthed = (
        str(data[0]['insd_outlets_earthed'])).lower() == "no"
    insd_conductors_size = (
        str(data[0]['insd_conductors_size'])).lower() == "no"
    insd_condition_wiring = (
        str(data[0]['insd_condition_wiring'])).lower() == "no"
    insd_bathroom_switch = (
        str(data[0]['insd_bathroom_switch'])).lower() == "no"
    conduits_conduits_bushed = (
        str(data[0]['conduits_conduits_bushed'])).lower() == "no"
    conduits_bonded = (str(data[0]['conduits_bonded'])).lower() == "no"
    conduits_correct_size = (
        str(data[0]['conduits_correct_size'])).lower() == "no"
    conduits_adequately_supported = (
        str(data[0]['conduits_adequately_supported'])).lower() == "no"
    conduits_suitable_type = (
        str(data[0]['conduits_suitable_type'])).lower() == "no"
    appliances_motor_installation = (
        str(data[0]['appliances_motor_installation'])).lower() == "no"
    appliances_outbuildings_switches = (
        str(data[0]['appliances_outbuildings_switches'])).lower() == "no"
    oh_height_satisfactory = (
        str(data[0]['oh_height_satisfactory'])).lower() == "no"
    oh_support_satisfactory = (
        str(data[0]['oh_support_satisfactory'])).lower() == "no"
    oh_condition_line = (str(data[0]['oh_condition_line'])).lower() == "bad"
    oh_earthwires_fitted = (
        str(data[0]['oh_earthwires_fitted'])).lower() == "no"
    defects_contractor = (str(data[0]['defects_contractor'])).lower() == "no"
    # Check whether there are quotations for materials or labour or vehicles or any combination of them
    is_material_quoted = len(data[0]['materials']) > 0
    is_labour_quoted = len(data[0]['labour']) > 0
    is_vehicle_quoted = len(data[0]['vehicles']) > 0
    is_quoted = is_labour_quoted or is_material_quoted or is_vehicle_quoted
    any_equipment = len(data[0]['equipment']) > 0
    is_statutory = False
    # Extract fullname and replace record creator`s ecnumber with his/her fullname
    if is_material_quoted:
        i = 1
        for material in data[0]['materials']:
            employee_data = execsys(material['created_by'])
            fullname = employee_data['firstname'] + \
                " " + employee_data['surname']
            material['created_by'] = fullname
            material['boq_id'] = i
            i = i+1

    if is_labour_quoted:
        i = 1
        for labour in data[0]['labour']:
            employee_data = execsys(labour['created_by'])
            fullname = employee_data['firstname'] + \
                " " + employee_data['surname']
            labour['created_by'] = fullname
            labour['boq_labour_id'] = i
            i = i+1

    if is_vehicle_quoted:
        i = 1
        for vehicle in data[0]['vehicles']:
            employee_data = execsys(vehicle['created_by'])
            fullname = employee_data['firstname'] + \
                " " + employee_data['surname']
            vehicle['created_by'] = fullname
            vehicle['boq_vehicle_id'] = i
            i = i+1

    if any_equipment:
        i = 1
        for equipment in data[0]['equipment']:
            employee_data = execsys(equipment['created_by'])
            fullname = employee_data['firstname'] + \
                " " + employee_data['surname']
            equipment['created_by'] = fullname
            equipment['equipment_id'] = i
            i = i+1

    # Get the Inspection type user-friendly name
    if data[0]['client_inspection_type'] == "new_installation":
        data[0]['client_inspection_type'] = "New Installation"
    elif data[0]['client_inspection_type'] == "statutory":
        data[0]['client_inspection_type'] = "Statutory"
        is_statutory = True
    elif data[0]['client_inspection_type'] == "re_inspection":
        data[0]['client_inspection_type'] = "Re-inspection"

    if data[0]['general_installation_status'] is None:
        installation_passed = False
    elif (data[0]['general_installation_status']).lower() == "failed":
        data[0]['general_installation_status'] = "Failed"
        installation_passed = False
    else:
        installation_passed = (
            data[0]['general_installation_status']).lower() == "passed"
        data[0]['general_installation_status'] = "Passed"

    artisan = execsys(data[0]['completed_by'])
    data[0]['completed_by'] = artisan['firstname'] + " " + artisan['surname']

    context = {
        "e117": data[0],
        "e117_id": data[0]['e117_id'],
        "installation_passed": installation_passed,
        "insd_neutrals_fused": insd_neutrals_fused,
        "insd_block_fitted": insd_block_fitted,
        "insd_electrode_installed": insd_electrode_installed,
        "insd_bonded_earth": insd_bonded_earth,
        "insd_outlets_earthed": insd_outlets_earthed,
        "insd_conductors_size": insd_conductors_size,
        "insd_condition_wiring": insd_condition_wiring,
        "insd_bathroom_switch": insd_bathroom_switch,
        "conduits_conduits_bushed": conduits_conduits_bushed,
        "conduits_bonded": conduits_bonded,
        "conduits_correct_size": conduits_correct_size,
        "conduits_adequately_supported": conduits_adequately_supported,
        "conduits_suitable_type": conduits_suitable_type,
        "appliances_motor_installation": appliances_motor_installation,
        "appliances_outbuildings_switches": appliances_outbuildings_switches,
        "oh_height_satisfactory": oh_height_satisfactory,
        "oh_support_satisfactory": oh_support_satisfactory,
        "oh_condition_line": oh_condition_line,
        "oh_earthwires_fitted": oh_earthwires_fitted,
        "defects_contractor": defects_contractor,
        "client": client_data,
        "contractor": contractor,
        "fullname": fullname,
        "materials": data[0]['materials'],
        "vehicles": data[0]['vehicles'],
        "labour": data[0]['labour'],
        "equipment": data[0]['equipment'],
        "is_labour_quoted": is_labour_quoted,
        "is_vehicle_quoted": is_vehicle_quoted,
        "is_material_quoted": is_material_quoted,
        "is_quoted": is_quoted,
        "any_equipment": any_equipment,
        "created_on": (str(data[0]['created_on']).split(' '))[0],
        "created_at": (str(data[0]['created_on']).split(' '))[1],
        "job_id": data[0]['job'],
        "is_statutory": is_statutory
    }
    return render(request, 'beweb/job/e117.html', context)


def e84Form(request):
    e84_general_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/e84general/" + e84_general_id
    r = requests.get(url=url, headers=headers)
    data = r.json()
    employee_data = execsys(data[0]['created_by'])

    fullname = employee_data['firstname'] + " " + employee_data['surname']
    created_on = (datetime.strptime(
        data[0]['created_on'], "%Y-%m-%d %H:%M:%S") if data[0]['created_on'] else '')

    context = {
        "e84_data": data[0],
        "inspections": data[0]['inspections'],
        "fullname": fullname,
        "created_on": created_on
    }
    return render(request, 'beweb/job/e84.html', context)


def e50Form(request):
    e50_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    # E50 GENERAL
    url = "http://" + beserver + ":8087/beapi/e50/" + e50_id
    response = requests.get(url=url, headers=headers)
    data = response.json()

    employee_data = execsys(data[0]['created_by'])
    fullname = employee_data['firstname'] + " " + employee_data['surname']
    created_on = (datetime.strptime(
        data[0]['created_on'], "%Y-%m-%d %H:%M:%S") if data[0]['created_on'] else '')
    # Separate created_on into two variables for date(created_on) and time(created_at)
    for value in data:
        formatted_date = (data[0]['created_on']).split(" ")
        data[0]['created_on'] = formatted_date[0]
        data[0]['created_at'] = formatted_date[1]

    # CHECK IF THERE IS A COMMENT & SAVE THE BOOLEAN RESULT IN A NEW VARIABLE
    relays_flags_reset_cmt = (
        str(data[0]['relays_flags_reset'])).lower() == "no"
    sef_uniselector_reset_cmt = (
        str(data[0]['sef_uniselector_reset'])).lower() == "no"
    fuses_links_position_cmt = (
        str(data[0]['fuses_links_position'])).lower() == "no"
    panels_wiring_order_cmt = (
        str(data[0]['panels_wiring_order'])).lower() == "no"
    apply_load_test_cmt = (str(data[0]['apply_load_test'])).lower() == "no"
    topup_cells_water_cmt = (str(data[0]['topup_cells_water'])).lower() == "no"
    clean_terminal_cases_cmt = (
        str(data[0]['clean_terminal_cases'])).lower() == "no"
    terminal_connections_cmt = (
        str(data[0]['terminal_connections'])).lower() == "no"
    float_voltage_cmt = (str(data[0]['float_voltage'])).lower() == "no"
    cubicle_lights_cmt = (str(data[0]['cubicle_lights'])).lower() == "bad"
    relays_clean_operate_cmt = (
        str(data[0]['relays_clean_operate'])).lower() == "no"
    cubicle_fuses_links_cmt = (
        str(data[0]['cubicle_fuses_links'])).lower() == "no"
    indicating_lamps_cmt = (str(data[0]['indicating_lamps'])).lower() == "no"
    panel_clean_wiring_cmt = (
        str(data[0]['panel_clean_wiring'])).lower() == "no"
    cubicle_lights_heaters_cmt = (
        str(data[0]['cubicle_lights_heaters'])).lower() == "no"
    insulators_arrestors_inorder_cmt = (
        str(data[0]['insulators_arrestors_inorder'])).lower() == "no"
    dfuse_isolators_inorder_cmt = (
        str(data[0]['dfuse_isolators_inorder'])).lower() == "no"
    busbars_jumpers_inorder_cmt = (
        str(data[0]['busbars_jumpers_inorder'])).lower() == "no"
    earthing_structure_fence_cmt = (
        str(data[0]['earthing_structure_fence'])).lower() == "no"
    cables_boxes_glands_cmt = (
        str(data[0]['cables_boxes_glands'])).lower() == "no"
    substation_surrounds_clean_cmt = (
        str(data[0]['substation_surrounds_clean'])).lower() == "no"
    paintwork_general_condition_cmt = (
        str(data[0]['paintwork_general_condition'])).lower() == "bad"

    # TRANSFORMERS
    transformers_url = "http://" + beserver + ":8087/beapi/transformer/e50/" + e50_id
    transformers_response = requests.get(url=transformers_url, headers=headers)
    transformers_data = transformers_response.json()
    new_transformers_data = list()
    for transformer in transformers_data:
        tx_url = "http://" + beserver + ":8087/beapi/transformer/" + \
            str(transformer['transformer'])
        tx_response = requests.get(url=tx_url, headers=headers)
        tx_data = tx_response.json()
        transformer['name'] = tx_data[0]['name']
        transformer['assetno'] = tx_data[0]['assetno']
        transformer['voltageratio'] = tx_data[0]['voltageratio']
        transformer['rating'] = tx_data[0]['capacity']
        # CHECK IF THERE IS A COMMENT & SAVE THE BOOLEAN RESULT IN A NEW VARIABLE
        transformer['tx_on_load_cmt'] = (
            str(transformer['tx_on_load'])).lower() == "no"
        transformer['ops_satisfactory_cmt'] = (
            str(transformer['ops_satisfactory'])).lower() == "no"
        transformer['oil_leaks_cmt'] = (
            str(transformer['oil_leaks'])).lower() == "yes"
        transformer['tank_oil_level_cmt'] = (
            str(transformer['tank_oil_level'])).lower() == "bad"
        transformer['diverter_tank_level_cmt'] = (
            str(transformer['diverter_tank_level'])).lower() == "bad"
        transformer['aux_tx_oil_cmt'] = (
            str(transformer['aux_tx_oil'])).lower() == "bad"
        transformer['main_tx_breather_cmt'] = (
            str(transformer['main_tx_breather'])).lower() == "bad"
        transformer['aux_tx_breather_cmt'] = (
            str(transformer['aux_tx_breather'])).lower() == "bad"
        transformer['diverter_switches_cmt'] = (
            str(transformer['diverter_switches'])).lower() == "bad"
        transformer['selector_switches_cmt'] = (
            str(transformer['selector_switches'])).lower() == "bad"
        transformer['mechanism_lubrication_cmt'] = (
            str(transformer['mechanism_lubrication'])).lower() == "bad"
        transformer['bushings_condition_cmt'] = (
            str(transformer['bushings_condition'])).lower() == "bad"
        transformer['sign_of_flashover_cmt'] = (
            str(transformer['sign_of_flashover'])).lower() == "no"
        transformer['buccholz_gas_cmt'] = (
            str(transformer['buccholz_gas'])).lower() == "no"
        transformer['tx_earthing_intact_cmt'] = (
            str(transformer['tx_earthing_intact'])).lower() == "no"
        new_transformers_data.append(transformer)

    # FEEDERS
    feeders_url = "http://" + beserver + ":8087/beapi/e50/feeder/" + e50_id
    feeders_response = requests.get(url=feeders_url, headers=headers)
    feeders_data = feeders_response.json()

    # CIRCUIT BREAKERS
    circuitbreakers_url = "http://" + beserver + ":8087/beapi/e50/circuitbreaker/" + e50_id
    circuitbreakers_response = requests.get(
        url=circuitbreakers_url, headers=headers)
    circuitbreakers_data = circuitbreakers_response.json()
    # CHECK IF THERE IS A COMMENT & SAVE THE BOOLEAN RESULT IN A NEW VARIABLE
    new_circuitbreakers_data = list()
    for circuitbreaker in circuitbreakers_data:
        circuitbreaker['bushings_condition_cmt'] = (
            str(circuitbreaker['bushings_condition'])).lower() == "bad"
        circuitbreaker['oil_leaks_cmt'] = (
            str(circuitbreaker['oil_leaks'])).lower() == "yes"
        circuitbreaker['eathing_intact_cmt'] = (
            str(circuitbreaker['eathing_intact'])).lower() == "no"
        circuitbreaker['tripping_circuit_healthy_cmt'] = (
            str(circuitbreaker['tripping_circuit_healthy'])).lower() == "no"
        new_circuitbreakers_data.append(circuitbreaker)

    # AUTODISCONNECT AND ISOLATORS
    autodisconnectors_url = "http://" + beserver + ":8087/beapi/e50/autodisconnectors/" + e50_id
    autodisconnectors_response = requests.get(
        url=autodisconnectors_url, headers=headers)
    autodisconnectors_data = autodisconnectors_response.json()
    # CHECK IF THERE IS A COMMENT & SAVE THE BOOLEAN RESULT IN A NEW VARIABLE
    new_autodisconnectors_data = list()
    for autodisconnector in autodisconnectors_data:
        autodisconnector['mechanism_operation_cmt'] = (
            str(autodisconnector['mechanism_operation'])).lower() == "bad"
        autodisconnector['bushing_condition_cmt'] = (
            str(autodisconnector['bushing_condition'])).lower() == "bad"
        autodisconnector['earthing_intact_cmt'] = (
            str(autodisconnector['earthing_intact'])).lower() == "no"
        autodisconnector['tripping_circuit_healthy_cmt'] = (
            str(autodisconnector['tripping_circuit_healthy'])).lower() == "no"
        new_autodisconnectors_data.append(autodisconnector)

    # STATION
    station_url = "http://" + beserver + ":8087/beapi/station/" + \
        str(data[0]['station'])
    station_response = requests.get(url=station_url, headers=headers)
    station_data = station_response.json()
    # Get District/Centre name, given district/centre id
    for station in station_data:
        centre_url = "http://" + beserver + ":8087/beapi/centre/" + \
            str(station['district']) + "/"
        centre_response = requests.get(url=centre_url, headers=headers)
        centre_data = centre_response.json()
        station_data[0]['district'] = centre_data[0]['centre_name']

    context = {
        "e50": data[0],
        "transformers": new_transformers_data,
        "feeders": feeders_data,
        "circuitbreakers": new_circuitbreakers_data,
        "autodisconnectors": new_autodisconnectors_data,
        "e50_general": data,
        "station": station_data[0],
        "fullname": fullname,
        "created_on": created_on
    }
    return render(request, 'beweb/job/e50.html', context)


def e60Form(request, **kwargs):
    e60_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}
    ctx_metering = []
    ctx_switchgears = []
    ctx_htlightings = []
    ctx_ltlightings = []
    ctx_dfuses = []
    # E60 DATA
    url = "http://" + beserver + ":8087/beapi/e60/" + e60_id
    response = requests.get(url=url, headers=headers)
    data = response.json()
    get_district= data[0]['district']
    centres_url = "http://" + beserver + ":8082/centres/"+get_district
    centres_response = requests.get(url=centres_url,headers=headers)
    centres_data = centres_response.json()
    district = centres_data[0]['centrename']

    employee_data = execsys(data[0]['created_by'])
    fullname = employee_data['firstname'] + " " + employee_data['surname']
    created_on = (datetime.strptime(
        data[0]['created_on'], "%Y-%m-%d %H:%M:%S") if data[0]['created_on'] else '')
    job_id = data[0]['job']

    # Function for Checking and Closing Job
    status = Job.objects.filter(job_id=job_id).values("status")[0]['status']
    role_name = ''
    approve = ''
    reject = ''
    if status >= 4:
        url = "http://" + beserver + ":8087/beapi/job/awaiting/action/"+usr
        rs = requests.get(url=url, headers=headers)
        jobsdata = rs.json()
        role_name = jobsdata[0]["role_name"]
        approve = jobsdata[0]["approve"]
        reject = jobsdata[0]["reject"]
    else:
        pass

    # Separate created_on into two variables for date(created_on) and time(created_at)
    for value in data:
        formatted_date = (data[0]['created_on']).split(" ")
        data[0]['created_on'] = formatted_date[0]
        data[0]['created_at'] = formatted_date[1]
    new_transformers_data = None

    if new_transformers_data == True:
        # TRANSFORMERS
        transformers_url = "http://" + beserver + ":8087/beapi/e60/transformer/" + e60_id
        transformers_response = requests.get(
            url=transformers_url, headers=headers)
        transformers_data = transformers_response.json()
        new_transformers_data = list()
        for transformer in transformers_data:
            tx_url = "http://" + beserver + ":8087/beapi/transformer/" + \
                str(transformer['transformer'])
            tx_response = requests.get(url=tx_url, headers=headers)
            tx_data = tx_response.json()
            transformer['name'] = tx_data[0]['name']
            transformer['assetno'] = tx_data[0]['assetno']
            transformer['voltageratio'] = tx_data[0]['voltageratio']
            transformer['rating'] = tx_data[0]['capacity']
            # CHECK IF THERE IS A COMMENT & SAVE THE BOOLEAN RESULT IN A NEW VARIABLE
            # transformer['tx_on_load_cmt']=(str(transformer['tx_on_load'])).lower() == "no"
            transformer['megger_ht_e'] = (
                str(transformer['megger_ht_e'])).lower() == "no"
            transformer['megger_ht_lt'] = (
                str(transformer['megger_ht_lt'])).lower() == "yes"
            transformer['megger_ht_lt_e'] = (
                str(transformer['megger_ht_lt_e'])).lower() == "bad"
            transformer['megger_lt_e'] = (
                str(transformer['megger_lt_e'])).lower() == "bad"
            transformer['oil_temp'] = (
                str(transformer['oil_temp'])).lower() == "bad"
            transformer['oil_dielectric_test'] = (
                str(transformer['oil_dielectric_test'])).lower() == "bad"
            transformer['tap_position'] = (
                str(transformer['tap_position'])).lower() == "bad"
            transformer['arcing_settings'] = (
                str(transformer['arcing_settings'])).lower() == "bad"
            transformer['tap_position'] = (
                str(transformer['tap_position'])).lower() == "bad"
            transformer['tap_position'] = (
                str(transformer['tap_position'])).lower() == "bad"

            new_transformers_data.append(transformer)
    else:
        pass

    asfound_switchgears_data={}
    y = 0
    switchgearasstate=[]
    switchgear_url = "http://" + beserver + ":8087/beapi/e60/switchgear/" + e60_id
    switchgear_response = requests.get(url=switchgear_url, headers=headers)
    asleft_switchgear_data = switchgear_response.json()
    if len(asleft_switchgear_data) == 0:
        asleft_switchgear_data = {}
    else:

        # SWITCHGEAR DATA FROM GIS  AS FOUND
        switchgears = []
        for asleft in asleft_switchgear_data:

            switchgears_url = "http://" + beserver + ":8087/beapi/switchgear/" + \
                asleft['switchgear']
            asfound_response = requests.get(
                url=switchgears_url, headers=headers)
            asfound_switchgeardata = asfound_response.json()
            switchgears.append(asfound_switchgeardata[0])
        asstates=[]
        y=0
        asleft_switchgear=[]
        for x in asleft_switchgear_data:

            asstate= asleft_switchgear_data[y]['as_state']
            asstates.append(asstate)
            asfound_switchgear=[]
            
            if asstate == 'As Found':
                    asfound_switchgear.append(asleft_switchgear_data[y])
            elif asstate == 'As Left':
                    asleft_switchgear.append(asleft_switchgear_data[y])
            else:
                None
            y+=1
        ctx_switchgears=[]
        switchgears_dict={}
        for asfound in asfound_switchgear:
            for asleft in asleft_switchgear:
                if len(asleft) == 0:
                    switchgears_dict={
                    "tripsetting":{
                        "asfound":asfound['trip_setting'],
                        "asleft":"None"
                    },
                    "oilcondition":{
                        "asfound":asfound['oil_condition'],
                        "asleft":"None"
                    },
                    "contacts_condition":{
                        "asfound":asfound['contacts_condition'],
                        "asleft":"None"
                    },
                    "conn_conditions":{
                        "asfound":asfound['conn_conditions'],
                        "asleft":"None"
                    },
                    "consumer_trip_setting":{
                        "asfound":asfound['consumer_trip_setting'],
                        "asleft":"None"
                    }
                }
                ctx_switchgears.append(switchgears_dict)
                
                # else:
                #     switchgears_dict={
                #         "tripsetting":{
                #             "asfound":asfound['trip_setting'],
                #             "asleft":asleft['trip_setting']
                #         },
                #         "oilcondition":{
                #             "asfound":asfound['oil_condition'],
                #             "asleft":asleft['oil_condition']
                #         },
                #         "contacts_condition":{
                #             "asfound":asfound['contacts_condition'],
                #             "asleft":asleft['contacts_condition']
                #         },
                #         "conn_conditions":{
                #             "asfound":asfound['conn_conditions'],
                #             "asleft":asleft['conn_conditions']
                #         },
                #         "consumer_trip_setting":{
                #             "asfound":asfound['consumer_trip_setting'],
                #             "asleft":asleft['consumer_trip_setting']
                #         }
                #     }
                #     ctx_switchgears.append(switchgears_dict)
                
       

    # e60 METERING
    asfound_metering_data = {}
    e60metering_url = "http://" + beserver + ":8087/beapi/e60/metering/" + e60_id
    e60metering_response = requests.get(url=e60metering_url, headers=headers)
    asleft_metering_data = e60metering_response.json()

    if len(asleft_metering_data) == 0:
        asleft_metering_data = {}
    else:
        # As Foundn Metering
        metering = []
        for asleft in asleft_metering_data:

            metering_url = "http://" + beserver + ":8087/beapi/meterings/" + \
                asleft['metering']
            metering_response = requests.get(url=metering_url, headers=headers)
            asfound_metering_data = metering_response.json()
            metering.append(asfound_metering_data[0])
        ctx_metering = []
        metering_dict = {}
        for asfound in metering:
            for asleft in asleft_metering_data:
                if asfound['metering_id'] == asleft['metering']:
                    metering_dict = {
                        "make": {
                            "asfound": asfound['make']
                        },
                        "amps": {
                            "asfound": asfound['amps']
                        },
                        "volts": {
                            "asfound": asfound['volts']

                        },
                        "maker_type": {
                            "asfound": asfound['maker_type']
                        },
                        "serial_number": {
                            "asfound": asfound['serial_number']
                        },
                        "zesa_number": {
                            "asfound": asfound['zesa_number']

                        },
                        "vad_transformer_no": {
                            "asfound": asfound['vad_transformer_no']

                        },
                        "ct_ratio": {
                            "asfound": asfound['ct_ratio']

                        },
                        "protection_type": {
                            "asfound": asfound['protection_type']

                        },
                        "meter_case_earthed": {
                            "asfound": "None",
                            "asleft": asleft['meter_case_earthed']
                        },
                        "fuses_condition": {
                            "asfound": "None",
                            "asleft": asleft['fuses_condition']
                        },
                        "phase_rotation": {
                            "asfound": "None",
                            "asleft": asleft['phase_rotation']
                        },
                        "connections_tight": {
                            "asfound": "None",
                            "asleft": asleft['connections_tight']
                        },
                        "metering_sealed": {
                            "asfound": "None",
                            "asleft": asleft['metering_sealed']
                        },
                        "cards_availabe": {
                            "asfound": "None",
                            "asleft": asleft['cards_available']
                        }


                    }
                    ctx_metering.append(metering_dict)

    # e60HOUSING
    e60housing_url = "http://" + beserver + ":8087/beapi/e60/housing/" + e60_id
    e60housing_response = requests.get(url=e60housing_url, headers=headers)
    e60housing_data = e60housing_response.json()
    if len(e60housing_data) == 0:
        e60housing_data = {}
    else:
        e60housing_data = e60housing_data[0]

# e60Safety
    e60safety_url = "http://" + beserver + ":8087/beapi/e60/safety/" + e60_id
    e60safety_response = requests.get(url=e60safety_url, headers=headers)
    e60safety_data = e60safety_response.json()
    if len(e60safety_data) == 0:
        e60safety_data = {}
    else:
        e60safety_data = e60safety_data[0]

    # e60SubGeneral
    e60subgeneral_url = "http://" + beserver + ":8087/beapi/e60/subgeneral/" + e60_id
    e60subgeneral_response = requests.get(
        url=e60subgeneral_url, headers=headers)
    e60subgeneral_data = e60subgeneral_response.json()
    for value in e60subgeneral_data:
        formatted_date=(e60subgeneral_data[0]['created_on']).split(" ")
        e60subgeneral_data[0]['created_on']=formatted_date[0]
        e60subgeneral_data[0]['created_at']=formatted_date[1]

    # E60 HT LIGHTING ARRESTOR
    asfound_lighting_data = {}
    e60htlighting_url = "http://" + beserver + ":8087/beapi/e60/htlightingarrester/" + e60_id
    e60htlighting_response = requests.get(
        url=e60htlighting_url, headers=headers)
    asleft_htlighting_data = e60htlighting_response.json()

    if len(asleft_htlighting_data) == 0:
        asleft_htlighting_data = {}
    else:
        # HT LIGHTING ARRESTOR
        htlighting = []
        for asleft in asleft_htlighting_data:
            lightingarrestor_url = "http://" + beserver + ":8087/beapi/lightningarrester/" + \
                asleft['lightningarrester_id']
            lighting_response = requests.get(
                url=lightingarrestor_url, headers=headers)
            asfound_lighting_data = lighting_response.json()
            htlighting.append(asfound_lighting_data[0])
        ctx_htlightings = []
        htlighting_dict = {}
        for asfound in htlighting:
            for asleft in asleft_htlighting_data:
                if asfound['lightningarrester_id'] == asleft['lightningarrester_id']:
                    htlighting_dict = {
                        "make": {
                            "asfound": asfound['make']
                        },
                        "voltage_rating": {
                            "asfound": asfound['voltage_rating']
                        },
                        "phase": {
                            "asfound": asfound['phase']
                        },
                        "kvar_rating": {
                            "asfound": asfound['kvar_rating']

                        },
                        "rails_connection": {
                            "asfound": 'None',
                            "asleft": asleft['rails_connection']
                        }
                    }
                    ctx_htlightings.append(htlighting_dict)

    # E60 LT LIGHTING ARRESTOR
    asfound_ltlighting_data = {}
    e60ltlighting_url = "http://" + beserver + ":8087/beapi/e60/ltlightingarrester/" + e60_id
    e60ltlighting_response = requests.get(
        url=e60ltlighting_url, headers=headers)
    asleft_ltlighting_data = e60ltlighting_response.json()
    if len(asleft_ltlighting_data) == 0:
        asleft_ltlighting_data = {}
    else:
        # LT LIGHTING ARRESTOR
        ltlighting = []
        for asleft in asleft_ltlighting_data:
            ltlightingarrestor_url = "http://" + beserver + ":8087/beapi/lightningarrester/" + \
                asleft['lightningarrester_id']
            ltlighting_response = requests.get(
                url=ltlightingarrestor_url, headers=headers)
            asfound_ltlighting_data = ltlighting_response.json()
            ltlighting.append(asfound_ltlighting_data[0])

        ctx_ltlightings = []
        ltlighting_dict = {}

        for asfound in ltlighting:
            for asleft in asleft_ltlighting_data:

                if asfound['lightningarrester_id'] == asleft['lightningarrester_id']:
                    ltlighting_dict = {
                        "make": {
                            "asfound": asfound['make']
                        },
                        "voltage_rating": {
                            "asfound": asfound['voltage_rating']
                        },
                        "phase": {
                            "asfound": asfound['phase']
                        },
                        "kvar_rating": {
                            "asfound": asfound['kvar_rating']

                        },
                        "rails_connection": {
                            "asfound": 'None',
                            "asleft": asleft['capacitor_satisfactory']
                        }
                    }
                    ctx_ltlightings.append(ltlighting_dict)
    # E60 DFUSES
    asfound_dfuse_data = {}
    e60dfuses_url = "http://" + beserver + ":8087/beapi/e60/dfuse/"+e60_id
    e60dfuses_response = requests.get(url=e60dfuses_url, headers=headers)
    asleft_dfuses_data = e60dfuses_response.json()

    if len(asleft_dfuses_data) == 0:
        asleft_dfuses_data = {}
    else:
        # DFUSES
        dfuses = []
        for asleft in asleft_dfuses_data:
            dfuses_url = "http://" + beserver + ":8087/beapi/dfuse/"+asleft['dfuse']
            dfuse_response = requests.get(url=dfuses_url, headers=headers)
            asfound_dfuse_data = dfuse_response.json()
            dfuses.append(asfound_dfuse_data[0])
        ctx_dfuses = []
        dfuses_dict = {}
        for asfound in dfuses:
            for asleft in asleft_dfuses_data:
                if asfound['dfuse_id'] == asleft['dfuse']:
                    dfuses_dict = {
                        "make": {
                            "asfound": 'None'
                        },
                        "rating": {
                            "asfound": asfound['rating']
                        },
                        "phase": {
                            "asfound": asfound['phase']
                        },
                        "kvar_rating": {
                            "asfound": 'None'

                        },
                        "as_state": {
                            "asfound": 'None',
                            "asleft": asleft['as_state']
                        }
                    }
                    ctx_dfuses.append(dfuses_dict)

    # TRANSFORMER DATA FROM GIS
    transformer_url = "http://" + beserver + ":8087/beapi/transformer/" + \
        str(data[0]['transformer'])
    station_response = requests.get(url=transformer_url, headers=headers)
    transformer_data = station_response.json()


    #E60 Transformer Data
    e60transformer_url = "http://" + beserver + ":8087/beapi/e60/transformer/" +e60_id
    e60t_response = requests.get(url=e60transformer_url,headers=headers)
    e60transformer_data = e60t_response.json()
    asstate = e60transformer_data[0]['as_state']
    
    asleft_transformer = {}
    if asstate == 'As Found':
        asfound_transfomer = e60transformer_data[0]
    elif asstate == 'As Left':
        asleft_transformer = e60transformer_data[0]
        
    #Get District/Centre name, given district/centre id
    for station in transformer_data:
        centre_url = "http://" + beserver + ":8087/beapi/centre/" + \
            str(station['district']) + "/"
        centre_response = requests.get(url=centre_url, headers=headers)
        centre_data = centre_response.json()
        transformer_data[0]['district'] = centre_data[0]['centre_name']

    context = {
        "e60": data[0],
        "asfoundtransfomer":asfound_transfomer,
        "asleft_transformer":asleft_transformer,
        # "asfound_switchgear":asfound_switchgear,
        # "asleft_switchgear":asleft_switchgear,
        # "e60_switchgear_data":e60_switchgear_data[0],
        # "switchgeardata":switchgeardata,
        "e60housing":e60housing_data,
        "e60safety_data":e60safety_data,
        "ctx_metering":ctx_metering,
        "ctx_htlightings":ctx_htlightings,
        "ctx_dfuses":ctx_dfuses,
        "ctx_ltlightings":ctx_ltlightings,
        "ctx_switchgears":ctx_switchgears,
        "e60_subgeneral":e60subgeneral_data[0],
        "transformr":transformer_data[0],
        "fullname": fullname,
        "created_on": created_on,
        "role_name":role_name,
        "approve":approve,
        "reject":reject,
        "district":district
    }
    return render(request, 'beweb/job/e60.html', context)


class FormsView(APIView):
    def get(self, request, job_id):
        forms = JobFormsModel.objects.filter(job_id=job_id)
        serializer = JobFormSerializer(forms, many=True).data
        return Response(serializer)


class TeamsByCentre(APIView):
    def get(self, request, team_leader, specialisation):

        teamsz = Team.objects.filter(
            team_leader=team_leader, specialisation=specialisation)
        serializer = TeamSerializers(teamsz, many=True).data
        return Response(serializer)


class JobsViewProcedure(APIView):
    '''
    Arguments:
        [username,section,status]
    Returns:
        Job id and Workorder id for the specified user
    '''

    def get(self, request, username, section, status):
        jobs = Job.objects.jobs_view_procedure(
            username=username, section=section, status=1)
        return Response(jobs)


class JobsViewSet(APIView):
    '''
    Returns a list of  jobs awaiting action in the system
    '''

    def get(self, request, ec_num):
        jobs = Jobworkflow.objects.job_awaiting_action_procedure(ec_num=ec_num)
        return Response(jobs)


class TeamsView(APIView):

    def get(self, request):
        username = request.user.username
        usr, tkn = user_authenticate(username)
        headers = {'Authorization': "Token "+tkn +
                   "", "Content-Type": "application/json"}
        url = "http://" + beserver + ":8087/beapi/teams"
        teams = requests.get(url=url, headers=headers)
        team_data = teams.json()
        employee_data = execsys(team_data[0]['team_leader'])
        fullname = employee_data['firstname'] + " " + employee_data['surname']

        return Response(team_data)


class ProgressJobs(APIView):
    '''
    Arguments:
        [username,section]
    Returns:
        Job id and Workorder id for the specified user
    '''

    def get(self, request, username, section, status):
        jobs = Job.objects.jobs_view_procedure(
            username=username, section=section, status=2)
        return Response(jobs)


class JobsReports(APIView):
    '''
    Arguments:
        [jobtype,section,centre,status,startdate,enddate]
    Returns:
        Jobs based on the given values
    '''

    def get(self, request, jobtype, centre, status, start_date, end_date):
        jobs = Job.objects.jobs_reports_view(
            jobtype=jobtype, centre=centre, status=status, start_date=start_date, end_date=end_date)
        return Response(jobs)


class ParentCentres(APIView):
    '''
    Arguments:
        [centreparent]
    Returns:
        All centres based on the given values(Parent centre)
    '''

    def get(self, request, centreparent):
        centres = Job.objects.all_parentcentres(centreparent)
        return Response(centres)


class WorkordersReports(APIView):
    '''
    Arguments:
        [jobtype,section,centre,status,startdate,enddate]
    Returns:
        Workorders based on the given values
    '''

    def get(self, request, workorder_centre, workorder_status, workorder_start_date, workorder_end_date):
        workorder = Job.objects.workorder_reports_view(
            workorder_centre=workorder_centre, workorder_status=workorder_status, workorder_start_date=workorder_start_date, workorder_end_date=workorder_end_date)
        return Response(workorder)


class ReinspectionJobs(APIView):
    '''
    Arguments:
        [username,section]
    Returns:
        Job id and Workorder id for the specified user
    '''

    def get(self, request):
        username = request.user.username
        usr, tkn = user_authenticate(username)
        user_data = execsys(username)
        section = user_data['section']
        headers = {'Authorization': "Token "+tkn +
                   "", "Content-Type": "application/json"}
        url = "http://" + beserver + ":8087/beapi/jobs/reinspection/"
        reinspection = requests.get(url=url, headers=headers)
        reinspection_data = reinspection.json()

        return Response(reinspection_data)


class SuspendedJobs(APIView):
    '''
    Arguments:
        [username,section]
    Returns:
        Job id and Workorder id for the specified user
    '''

    def get(self, request, username, section, status):
        jobs = Job.objects.jobs_view_procedure(
            username=username, section=section, status=3)
        return Response(jobs)


class WorkorderViewSet(APIView):
    def get(self, request, centre):
        if centre == 'MSD':
            workorder = Workorder.objects.filter(Q(centre='MSV') | Q(centre='GUT') | Q(
                centre='RUT') | Q(centre='MAS') | Q(centre='CHR') | Q(centre='MSG') | Q(centre='MSD'))
            serializer = WorkorderSerializers(workorder, many=True).data
        elif centre == 'MND':
            workorder = Workorder.objects.filter(Q(centre='CHM') | Q(centre='MSB') | Q(
                centre='CHP') | Q(centre='NYA') | Q(centre='RSP') | Q(centre='MND'))
            serializer = WorkorderSerializers(workorder, many=True).data
        elif centre == 'MTD':
            workorder = Workorder.objects.filter(Q(centre='ENV') | Q(
                centre='URB') | Q(centre='MTG') | Q(centre='MTD'))
            serializer = WorkorderSerializers(workorder, many=True).data
        else:
            workorder = Workorder.objects.filter(Q(centre=centre))
            serializer = WorkorderSerializers(workorder, many=True).data
        return Response(serializer)


class OnlySaveWorkorder(View):
    def post(self, request, *args, **kwargs):
        username = request.user.username
        data = execsys(username)
        username = data['username']
        description = request.POST['description']
        supervisor = request.POST['supervisor']
        date = datetime.now().strftime("%Y%m%d%H%M")
        centre_code = request.POST['centre_code']
        centre = centre_code
        work_order_id = request.POST['work_order_id']
        wo = save_wo(username, description, supervisor,
                     centre, date, centre_code, work_order_id)
        my_work = Workorder.objects.filter(work_order_id=wo)

        workorder_table = WorkorderTable1(my_work)
        workorder_table.paginate(page=request.POST.get('page', 1), per_page=2)
        RequestConfig(request).configure(workorder_table)
        return render(request, 'beweb/workorder/notification.html', {'workorder_table': workorder_table})


def editwork(request):
    work_order_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/single/workorder/" + work_order_id+"/"
    r = requests.get(url=url, headers=headers)
    data = r.json()
    num_jobs = len(data[0]['jobs'])
    context = {
        "workorder": data[0],
        "number_of_jobs": num_jobs
    }
    return render(request, 'beweb/workorder/workorder_edit.html', context)


class SaveEditedWorkorder(View):
    def post(self, request, *args, **kwargs):
        wo = request.POST['work_order_id']
        description = request.POST['description']
        username = request.user.username
        usr, tkn = user_authenticate(username)
        url = 'http://' + beserver + ':8087/beapi/workorderpatch/'+wo
        headers = {'Authorization': "Token "+tkn +
                   "", 'Content-Type': 'application/json'}
        data = {
            "description": description
        }
        data = json.dumps(data)
        r = requests.patch(url=url, data=data, headers=headers)
        response_data = r.json()
        url = "http://" + beserver + ":8087/beapi/single/workorder/" + wo
        rs = requests.get(url=url, headers=headers)
        data1 = rs.json()
        num_jobs = len(data1[0]['jobs'])
        employee_data = execsys(data1[0]['created_by'])
        fullname = employee_data['firstname'] + " " + employee_data['surname']
        context = {
            "workorder": data1[0],
            "fullname": fullname,
            "number_of_jobs": num_jobs
        }
        return render(request, 'beweb/workorder/workorder_view.html', context)


def Job_workflow(request):
    job_id = request.GET.get('job_id', '')
    username = request.user.username
    status = request.GET.get('status', 0)
    opt = request.GET.get('opt', '0')
    wkf_id = 0
    decision = request.GET.get('decision', '0')
    apv = 1
    # if decision == "8":
    #     apv = -1

    comments = request.GET.get('comments', '')
    actioner, tkn = user_authenticate(username)
    job_workflow = Jobworkflow.objects.filter(
        job=job_id).values("workflow_id")[0]['workflow_id']
    job_workflow_id = Jobworkflow.objects.filter(
        job=job_id).values("job_workflow_id")[0]['job_workflow_id']
    jobworkflow = Jobworkflow.objects.filter(job_workflow_id=job_workflow_id).select_related(
        'workflow').values('workflow__workflow_code', 'workflow__step').first()
    step = jobworkflow['workflow__step']
    next_step = step + apv
    workflow_cd = jobworkflow['workflow__workflow_code']
    workflowid = Workflow.objects.filter(
        workflow_code=workflow_cd, step=next_step).values('workflow_id').first()
    if workflowid:
        wkf_id = workflowid['workflow_id']

    jobworkflowpatch_url = 'http://' + beserver + ':8087/beapi/jobworkflowpatch/'+job_workflow_id
    headers = {'Authorization': "Token "+tkn +
               "", 'Content-Type': 'application/json'}
    data = {
        "ec_num": actioner,
        "action": decision,
        "action_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comments": comments
    }
    data = json.dumps(data)

    r = requests.patch(url=jobworkflowpatch_url, data=data, headers=headers)
    response_data = r.json()

    url = "http://" + beserver + ":8087/beapi/jobworkflowpost"
    data = {
        "workflow": wkf_id,
        "job_workflow_id": "jwf" + datetime.now().strftime("%Y%m%d%H%M") + str(random.randrange(000000, 100000)),
        "job": job_id,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data = json.dumps(data)

    if wkf_id > 0:
        r = requests.post(url=url, data=data, headers=headers)
        response_data = r.json()

    data = execsys(request.user.username)
    section = data['section']
    jobupdate_url = 'http://' + beserver + ':8087/beapi/jobupdate/'+job_id
    jobupdate_data = {"status": decision}
    jobupdate_data = json.dumps(jobupdate_data)
    jobupdate_r = requests.patch(
        url=jobupdate_url, data=jobupdate_data, headers=headers)
    jobupdate_response_data = jobupdate_r.json()
    return render(request, 'beweb/reports/mywork.html', {"section": section})


def myjobs(request):
    usr, tkn = user_authenticate(request.user.username)
    headers = {'Authorization': "Token "+tkn +
               "", 'Content-Type': 'application/json'}
    url = "http://" + beserver + ":8087/beapi/job/awaiting/action/"+usr
    rs = requests.get(url=url, headers=headers)
    jobsdata = rs.json()
    data = execsys(request.user.username)
    section = data['section']
    jobs_records = []
    for job in jobsdata:
        job_id = job["job_id"]
        approve = job["approve"]
        role_name = job["role_name"]
        url1 = "http://" + beserver + ":8087/beapi/job/" + job_id+"/"
        r = requests.get(url=url1, headers=headers)
        jobdata = r.json()
        assignee = jobdata[0]['assignee']
        description = jobdata[0]['description']
        data = execsys(assignee)
        artisan = data['surname']+" "+data['firstname']
        jobs_records.append({"job_id": job_id, "approve": approve, "artisan": artisan,
                             "description": description, "nextaction": role_name})
    return render(request, 'beweb/reports/mywork.html', {'data': jobs_records, "section": section})


def reports(request):
    data = execsys(request.user.username)
    centre_code = data['section']
    # centres= {}

    usr, tkn = user_authenticate(request.user.username)
    headers = {'Authorization': "Token "+tkn +
               "", 'Content-Type': 'application/json'}
    url = "http://" + beserver + ":8087/beapi/all_centres/"+centre_code
    all_parent_centres = requests.get(url=url, headers=headers)
    allcentres = all_parent_centres.json()

    username = data['username']
    centre, centre_code = get_center(centre_code)
    job_type = JobType.objects.filter(Q(job_type_id='E117') | Q(job_type_id='E50') | Q(
        job_type_id='E60') | Q(job_type_id='E84')).values("job_type_id", "type")
    context = {'centre': centre,
               'centre_code': centre_code,
               #   'centres': centres,
               'job_type': job_type,
               'allcentres': allcentres
               }

    return render(request, 'beweb/reports/reports.html', context)


class SaveE117Job(APIView):
    def post(self, request, *args, **kwargs):
        # The below variables apply to all E117 inspections regardless of inspection type
        job_id = request.POST.get('job_number')
        created_by = request.user.username
        username = request.user.username
        data = execsys(request.user.username)
        section = data['section']
        workorder_number = request.POST.get('workorder_number')
        job_type = request.POST.get('jobtype')
        wo = request.POST.get('workorder_number')
        centre = data['section']
        job_description = request.POST.get('description')
        job_number = request.POST.get('job_number')
        createdby = created_by
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        e117_id = "E117"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        inspection_type = request.POST.get('inspection_type')
        reference_number = None
        team_members = request.POST.getlist('teammembers')
        asset_id = None
        # IF WORKORDER DOES NOT EXIST, create workorder first
        if not request.session['workorder_number']:
            username = request.session['username']
            description = request.session['description']
            supervisor = request.session['username']
            centre = request.session['centre_code']
            centre_code = request.session['centre_code']
            work_order_id = request.session['work_order']
            date = datetime.now().strftime("%Y%m%d%H%M")
            save_wo(username, description, supervisor,
                    centre, date, centre_code, work_order_id)
        # NEW INSTALLATION
        if inspection_type == "new_installation":
            client_id = "ci"+datetime.now().strftime("%Y%m%d%H%M") + \
                str(random.randrange(000000, 100000))
            client_name = str(request.POST.get('customer_name'))
            property_address = request.POST.get('property_address')
            client_phone = request.POST.get('customer_phone', '')
            owner_name = str(request.POST.get(
                'new_installation_property_owner_name'))
            owner_address = str(request.POST.get(
                'new_installation_property_owner_address'))
            assignee = request.POST['job_assignee']
            fleet = request.POST.get('new_installation_fleet')
            job_description = request.POST.get('description')
            print("___________________")
            print(job_description)
            print("___________________")
            expected_end_dt = request.POST.get(
                'new_installation_expected_end_dt')
            trigger = None
            start_date = request.POST.get('new_installation_start_date')
            asset_type = None
            number_of_clients = None
            customer_type = None
            # e117contractor_id="con"+datetime.now().strftime("%Y%m%d%H%M") + str(random.randrange(000000, 100000))
            e117contractor_id = request.POST.get(
                'new_installation_contractor_name')
            # contractor_name=request.POST.get('new_installation_contractor_name')
            # contractor_address=request.POST.get('new_installation_contractor_address')
            # contractor_phone=request.POST.get('new_installation_contractor_phone')
           #team_mmbr = request.POST['e117_tnames']
            
            # Method Calls to save job, job progress, job team, client, contractor and e117 record
            jo=Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                     section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
            
            jp = job_progress(job_id, createdby, fleet)
            save_team(username, assignee, jp, team_members)
            save_client(client_id, client_name, property_address, client_phone,
                        owner_name, owner_address, created_by, number_of_clients, customer_type)
            # save_contractor(created_by,created_on,e117contractor_id,contractor_name,contractor_address,contractor_phone)
            save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                      inspection_type, number_of_clients, customer_type)
        # STATUTORY INSPECTION
        elif inspection_type == "statutory":
            number_of_clients = request.POST.get('statutory_number_of_clients')
            customer_type = request.POST.get('statutory_customer_type')
            if number_of_clients == "single":
                inspection_type = request.POST.get('inspection_type')
                trigger = None
                asset_type = None
                client_id = "ci"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
                job_description = request.POST.get('description')
                client_name = str(request.POST.get(
                    'e117_statutory_customer_name'))
                client_phone = request.POST.get(
                    'e117_statutory_customer_phone')
                property_address = request.POST.get(
                    'statutory_single_property_address')
                owner_name = request.POST.get(
                    'statutory_single_property_owner_name')
                owner_address = request.POST.get(
                    'statutory_single_property_owner_address')
                start_date = request.POST.get('statutory_single_start_date')
                expected_end_dt = request.POST.get(
                    'statutory_single_expected_end_dt')
                assignee = request.POST['job_assignee']
                customer_type = request.POST.get('statutory_customer_type')
               #team_mmbr = request.POST['e117_tnames']
                
                fleet = request.POST.get('statutory_single_fleet')
                e117contractor_id = None
                # Method Calls to save job, job progress, job team, client and e117 record
                Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                         section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
                jp = job_progress(job_id, createdby, fleet)
                save_team(username, assignee, jp, team_members)
                save_client(client_id, client_name, property_address, client_phone,
                            owner_name, owner_address, created_by, number_of_clients, customer_type)
                save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                          inspection_type, number_of_clients, customer_type)
            elif number_of_clients == "multiple":
                statutory_number_of_clients = request.POST.get(
                    'statutory_number_of_clients')
                statutory_customer_type = request.POST.get(
                    'statutory_customer_type')
                job_description = request.POST.get(
                    'e117_statutory_description')
                start_date = request.POST.get('statutory_multiple_start_date')
                expected_end_dt = request.POST.get(
                    'statutory_multiple_expected_end_dt')
                assignee = request.POST['job_assignee']
                statutory_multiple_assistants = request.POST.get(
                    'statutory_multiple_assistants')
                fleet = request.POST.get('statutory_multiple_fleet')
               #team_mmbr = request.POST['e117_tnames']
                
                trigger = None
                asset_type = None
                client_id = None
                e117contractor_id = None
                # Method Calls to save job, job progress, job team and e117 record
                Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                         section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
                jp = job_progress(job_id, createdby, fleet)
                save_team(username, assignee, jp, team_members)
                save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                          inspection_type, number_of_clients, customer_type)
            else:
                pass
        # RE-INSPECTION
        elif inspection_type == "re_inspection":
            client_id = "ci"+datetime.now().strftime("%Y%m%d%H%M") + \
                str(random.randrange(000000, 100000))
            e117contractor_id = request.POST.get(
                're_inspection_contractor_name')
            re_inspection_service_number = request.POST.get(
                're_inspection_service_number')
            re_inspection_receipt_number = request.POST.get(
                're_inspection_receipt_number')
            re_inspection_fee = request.POST.get('re_inspection_fee')
            re_inspection_date_paid = request.POST.get(
                're_inspection_date_paid')
            client_name = request.POST.get('re_inspection_customer_name')
            client_phone = request.POST.get('re_inspection_customer_phone')
            property_address = request.POST.get(
                're_inspection_property_address')
            owner_name = request.POST.get('re_inspection_property_owner_name')
            owner_address = request.POST.get(
                're_inspection_property_owner_address')
            # contractor_name=request.POST.get('re_inspection_contractor_name')
            # contractor_phone=request.POST.get('re_inspection_contractor_phone')
            # contractor_address=request.POST.get('re_inspection_contractor_address')
            job_description = request.POST.get('description')
            start_date = request.POST.get('re_inspection_start_date')
            expected_end_dt = request.POST.get('re_inspection_expected_end_dt')
            assignee = request.POST['job_assignee']
           #team_mmbr = request.POST['e117_tnames']
            
            fleet = request.POST.get('re_inspection_fleet')
            trigger = None
            asset_type = None
            number_of_clients = None
            customer_type = None
            reinspection_id = "re"+datetime.now().strftime("%Y%m%d%H%M") + \
                str(random.randrange(000000, 100000))
            service_number = request.POST.get('re_inspection_service_number')
            re_inspection_fee = request.POST.get('re_inspection_fee')
            receipt_no = request.POST.get('re_inspection_receipt_number')
            e117 = e117_id
            date_paid = request.POST.get('re_inspection_date_paid')
            Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                     section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
            jp = job_progress(job_id, createdby, fleet)
            save_team(username, assignee, jp, team_members)
            save_client(client_id, client_name, property_address, client_phone,
                        owner_name, owner_address, created_by, number_of_clients, customer_type)
            # save_contractor(created_by,created_on,e117contractor_id,contractor_name,contractor_address,contractor_phone)
            save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                      inspection_type, number_of_clients, customer_type)
            save_reinspection(reinspection_id, receipt_no, re_inspection_fee,
                              e117, date_paid, service_number, created_by, created_on)
        return render(request, 'beweb/job/notification.html')

# Reinspection Function after the Job has been rejected


def ReInspection(request):
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}
    data = execsys(username)
    centre_code = data['section']
    username = data['username']
    section = data['section']
    centre, centre_code = get_center(centre_code)
    date = datetime.now()
    job_id = "JO"+datetime.now().strftime("%Y%m%d%H%M") + \
        str(random.randrange(000000, 100000))
    service_number = "SN"+datetime.now().strftime("%Y%m%d%H%M") + \
        str(random.randrange(000000, 100000))
    team_leaders = []
    jobtp = JobType.objects.filter(
        Q(type='Installation Inspection')).values("job_type_id", "type")
    Teams = Team.objects.values('team_leader_id').distinct()
    team_leaders = [team_leader['team_leader_id'] for team_leader in Teams]

    re_inspection_job_id = request.GET.get('q', '')
    url = "http://" + beserver + ":8087/beapi/job/" + re_inspection_job_id+"/"
    reinspection_job = requests.get(url=url, headers=headers)
    reinspection_data = reinspection_job.json()
    workorder = reinspection_data[0]['work_order']
    workorder_description = reinspection_data[0]['description']

    e117_url = "http://" + beserver + ":8087/beapi/e117/job/"+re_inspection_job_id+"/"
    e117_result = requests.get(url=e117_url, headers=headers)
    e117_data = e117_result.json()
    e117_id = e117_data[0]['e117_id']
    client_url = "http://" + beserver + ":8087/beapi/client/" + \
        e117_data[0]['e117client']+"/"
    client_result = requests.get(url=client_url, headers=headers)
    client_data = client_result.json()
    # GET CONTRACTOR DATA FROM THE CONTRACTOR ID FROM ABOVE REQUEST
    contractor_url = "http://" + beserver + ":8087/beapi/e117contractor/" + \
        e117_data[0]['client_contractor']+"/"
    contractor_result = requests.get(url=contractor_url, headers=headers)
    contractor_data = contractor_result.json()

    teams = {}
    for team_leader in team_leaders:
        team_members = [team_member['team_member'] for team_member in Teams.values(
        ) if team_member['team_leader_id'] == team_leader]
        data = execsys(team_leader)
        teamleader = {
            "ec_number": team_leader,
            "firstname": data['firstname'],
            "lastname": data['surname']
        }
        members = []
        for member in team_members:
            data1 = execsys(member)
            first_name = data1['firstname']
            last_name = data1['surname']
            our_team = {
                "ec_number": member,
                "firstname": first_name,
                "lastname": last_name
            }
            members.append(our_team)

        team_sheet = []
        team_sheet.append(teamleader)
        team_sheet.append(members)
        teams[team_leader] = team_sheet
        team_leader = ''
    return render(request, 'beweb/job/reinspection.html', {
        'workorder': workorder, 'job_id': job_id, 'centre': centre, 'centre_code': centre_code, 'username': username,
        'jobtp': jobtp, 'client_data': client_data[0], 'e117_data': e117_data[0], 'e117_id': e117_id, 'old_job_number': re_inspection_job_id,
        'contractor_data': contractor_data[0], 'teams': teams, 'service_number': service_number, 'workorder_description': workorder_description
    })


class SaveReinspection(APIView):
    def get(self, request, *args, **kwargs):
        asset_id = None
        job_id = request.GET.get('job_number')
        reference_number = request.GET.get('old_job_number')
        created_by = request.user.username
        username = request.user.username
        data = execsys(request.user.username)
        section = data['section']
        workorder_number = request.GET.get('workorder_number')
        job_type = request.GET.get('jobtype')
        wo = request.GET.get('workorder_number')
        centre = data['section']
        job_number = request.GET.get('job_number')
        createdby = created_by
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        e117_id = "e"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        inspection_type = request.GET.get('inspection_type')
        client_id = "ci"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        e117contractor_id = "con"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        re_inspection_service_number = request.GET.get(
            're_inspection_service_number')
        re_inspection_receipt_number = request.GET.get(
            're_inspection_receipt_number')
        re_inspection_fee = request.GET.get('re_inspection_fee')
        re_inspection_date_paid = request.GET.get('re_inspection_date_paid')
        client_name = request.GET.get('re_inspection_customer_name')
        client_phone = request.GET.get('re_inspection_customer_phone')
        property_address = request.GET.get('re_inspection_property_address')
        owner_name = request.GET.get('re_inspection_property_owner_name')
        owner_address = request.GET.get('re_inspection_property_owner_address')
        contractor_name = request.GET.get('re_inspection_contractor_name')
        contractor_phone = request.GET.get('re_inspection_contractor_phone')
        contractor_address = request.GET.get(
            're_inspection_contractor_address')
        job_description = request.GET.get('workorder_description')
        start_date = request.GET.get('re_inspection_start_date')
        expected_end_dt = request.GET.get('re_inspection_expected_end_dt')
        assignee = request.GET.get('re_inspection_assignee')
       #team_mmbr = request.GET['e117_tnames']
        
        fleet = request.GET.get('re_inspection_fleet')
        trigger = None
        asset_type = None
        number_of_clients = None
        customer_type = None
        reinspection_id = "re"+datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        service_number = request.GET.get('re_inspection_service_number')
        re_inspection_fee = request.GET.get('re_inspection_fee')
        receipt_no = request.GET.get('re_inspection_receipt_number')
        e117 = e117_id
        date_paid = request.GET.get('re_inspection_date_paid')
        Save_Job(createdby, assignee, job_type, wo, job_description, expected_end_dt, centre,
                 section, job_number, trigger, start_date, asset_type, reference_number, asset_id)
        jp = job_progress(job_id, createdby, fleet)
        save_team(username, assignee, jp, team_members)
        save_client(client_id, client_name, property_address, client_phone,
                    owner_name, owner_address, created_by, number_of_clients, customer_type)
        save_contractor(created_by, created_on, e117contractor_id,
                        contractor_name, contractor_address, contractor_phone)
        save_e117(e117_id, job_id, created_by, section, workorder_number,
                  client_id, e117contractor_id, inspection_type)
        save_reinspection(reinspection_id, receipt_no, re_inspection_fee,
                          e117, date_paid, service_number, created_by, created_on)
        return render(request, 'beweb/job/notification.html')


def save_contractor(created_by, created_on, e117contractor_id, contractor_name, contractor_address, contractor_phone):
    user, token = user_authenticate(created_by)
    url = 'http://' + beserver + ':8087/beapi/e117contractorpost/'
    headers = {'Authorization': "Token "+token + "", "Content-Type": "application/json"
               }
    data = {
        "created_by": created_by,
        "created_on": created_on,
        "e117contractor_id": e117contractor_id,
        "contractor_name": contractor_name,
        "contractor_address": contractor_address,
        "contractor_phone": contractor_phone
    }
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()
    return


def save_client(client_id, client_name, property_address, client_phone, owner_name, owner_address, created_by, number_of_clients, customer_type):
    user, token = user_authenticate(created_by)
    url = 'http://' + beserver + ':8087/beapi/clientpost/'
    headers = {'Authorization': "Token "+token + "", "Content-Type": "application/json"
               }

    data = {
        "client_id": client_id,
        "client_name": client_name,
        "property_address": property_address,
        "client_phone": client_phone,
        "owner_name": owner_name,
        "owner_address": owner_address,
        "customer_type": customer_type,
        "number_of_clients": number_of_clients
    }
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()
    client_name = client_name
    return client_name


def save_e117(e117_id, job_id, created_by, client_id, e117contractor_id, inspection_type, number_of_clients, customer_type):
    user, token = user_authenticate(created_by)
    created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = 'http://' + beserver + ':8087/beapi/e117post/'
    headers = {'Authorization': "Token "+token +
               "", "Content-Type": "application/json"}
    data = {
        "e117_id": e117_id,
        "created_by": created_by,
        "job": job_id,
        "number_of_clients": number_of_clients,
        "customer_type": customer_type,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "client_inspection_type": inspection_type,
        "e117client": client_id,
        "client_contractor": e117contractor_id
    }
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()
    createdby = created_by
    return createdby


def save_e50(e50_id, job_number, createdby, station_id):
    user, token = user_authenticate(createdby)
    created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = 'http://' + beserver + ':8087/beapi/e50post'
    headers = {'Authorization': "Token "+token +
               "", "Content-Type": "application/json"}
    data = {
        "e50_id": e50_id,
        "job": job_number,
        "station": station_id,
        "created_by": createdby,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data = json.dumps(data)
    response = requests.post(url=url, data=data, headers=headers)
    response_data = response.json()
    return response_data


def save_e60(e60_id, job_number, createdby, transformer_id, work_type, district):
    user, token = user_authenticate(createdby)
    created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = 'http://' + beserver + ':8087/beapi/e60post'
    headers = {'Authorization': "Token "+token +
               "", "Content-Type": "application/json"}
    data = {
        "e60_id": e60_id,
        "job": job_number,
        "district": district,
        "transformer": transformer_id,
        "created_by": createdby,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type_of_work": work_type
    }
    data = json.dumps(data)
    response = requests.post(url=url, data=data, headers=headers)
    response_data = response.json()
    return response_data


def save_reinspection(reinspection_id, receipt_no, re_inspection_fee, e117, date_paid, service_number, created_by, created_on):
    user, token = user_authenticate(created_by)
    headers = {'Authorization': "Token "+token + "", "Content-Type": "application/json"
               }
    url = "http://" + beserver + ":8087/beapi/e117reinspectionpost/"
    data = {
        "reinspection_id": reinspection_id,
        "receipt_no": receipt_no,
        "e117": e117,
        "amount": re_inspection_fee,
        "date_paid": date_paid,
        "service_number": service_number,
        "created_by": created_by,
        "created_on": created_on
    }
    data = json.dumps(data)
    r = requests.post(url=url, data=data, headers=headers)
    response_data = r.json()
    createdby = created_by
    return createdby


def reject_job(request, job_id):
    user, token = user_authenticate(request.user.username)
    headers = {'Authorization': "Token "+token +
               "", "Content-Type": "application/json"}
    data = {
        "job_id": job_id,
        "status": 8
    }
    job_workflow_id = "jwf" + datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
    actioner = request.user.username

    job_number = request.POST.get('job') or job_id
    comment = request.POST.get('comments')
    decision = 8
    createdby = request.user.username
    #REASSIGN JOB TO ANOTHER ARTISAN
    if request.POST.get('reassign_button'):
            with connection.cursor() as cursor:
                cursor.execute("CALL core.approve_job(%s, %s, %s, %s,%s);",
                               (job_workflow_id, job_id, actioner,decision, comment))
                connection.commit()

            """Renders the reassign-job page"""
            job_id = "JO"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))    
            username = request.user.username
            usr, tkn = user_authenticate(username)
            headers = {'Authorization': "Token "+tkn +
                    "", "Content-Type": "application/json"}

            url = "http://" + beserver + ":8087/beapi/job/" + job_number+"/"
            r = requests.get(url=url, headers=headers)
            job_data = r.json()
            workorder_id = job_data[0]['work_order']
            workorder_data = Workorder.objects.filter(
                    work_order_id=workorder_id).values()
            code_centre = workorder_data[0]['centre']
            users = requests.get(url="http://" + beserver + ":8082/users/").json()
            team_leaders = TeamLeader.objects.filter(centre=code_centre).values('team_leader')
            artisans = [user for user in users if ((user['designation'] == 'Artisan -' or 'Artisan') and user['status'] == 'active') and user['section'] == code_centre]
            available_artisans=artisans
            artisan_assistants = [assistant for assistant in users if assistant['section'] == code_centre and assistant['status'] == 'active']
            teams = Team.objects.values('team_leader_id').distinct()
            teams = {}
            
            context = {
                "job": job_data[0],
                "job_id":job_id,
                "Artisans":available_artisans,
                "Artisan_Assistants":artisan_assistants,
                "teams":teams,
                "code_centre":code_centre,
            }
            return render(request, 'beweb/job/reassignjob.html', context)
                    # return render(request, 'beweb/job/close.html', {})

    # REDO (GIVE THE SAME ARTISAN)
    elif request.POST.get('redo_button'):
        with connection.cursor() as cursor:
            cursor.execute("CALL core.approve_job(%s, %s, %s, %s,%s);",
                            (job_workflow_id, job_id, actioner,decision, comment))
            connection.commit()
        action = 10
        username = request.user.username
        usr, tkn = user_authenticate(username)
        headers = {'Authorization': "Token "+tkn +
                "", "Content-Type": "application/json"}

        url = "http://" + beserver + ":8087/beapi/job/" + job_number+"/"
        r = requests.get(url=url, headers=headers)
        job_data = r.json()
        assignee = job_data[0]['assignee']
        with connection.cursor() as cursor:
            cursor.execute("CALL core.redo_job(%s, %s, %s, %s);",
                            (job_workflow_id, job_id, assignee, comment))
            connection.commit()
        return render(request, 'beweb/job/reject.html', {})
        job_type = job_data[0]['type']
        fleet = job_data[0]['fleet_no']
        if job_type == 'E50':
            url = "http://" + beserver + ":8087/beapi/e50/job/" + job_number
            response = requests.get(url=url, headers=headers)
            e50_data = response.json()
            station_id = e50_data[0]['station']
            e50_id = "E50"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))

            save_e50(e50_id, job_number, createdby, station_id)

        elif job_type == 'E60':
            e60_id = "E60"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
            url = "http://" + beserver + ":8087/beapi/e60job/" + job_number
            response = requests.get(url=url, headers=headers)
            e60_data = response.json()
            transformer_id = e60_data[0]['transformer']
            work_type = e60_data[0]['type_of_work']
            district = e60_data[0]['district']

            save_e60(e60_id, job_number, createdby,
                        transformer_id, work_type, district)

        elif job_type == 'E117':
            e117_id = "E117"+datetime.now().strftime("%Y%m%d%H%M") + \
                    str(random.randrange(000000, 100000))
            url = "http://" + beserver + ":8087/beapi/e117/job/" + job_number
            response = requests.get(url=url, headers=headers)
            e117_data = response.json()
            inspection_type = e117_data[0]['client_inspection_type']
            created_by = request.user.username
            client_id = e117_data[0]['e117client']
            e117contractor_id= e117_data[0]['client_contractor']
            customer_type = e117_data[0]['customer_type']
            number_of_clients = e117_data[0]['number_of_clients']

            if inspection_type == "new_installation":
                trigger = None
                asset_type = None
                number_of_clients = None
                customer_type = None
                
                # Method Calls to save job, job progress, job team, client, contractor and e117 record
                jp = job_progress(job_id, createdby, fleet)

                save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                        inspection_type, number_of_clients, customer_type)
        # STATUTORY INSPECTION
            elif inspection_type == "statutory":
                if number_of_clients == "single":
                    trigger = None
                    asset_type = None
                    e117contractor_id = None
                    # Method Calls to save job, job progress, job team, client and e117 record
                    jp = job_progress(job_id, createdby, fleet)
                    save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                            inspection_type, number_of_clients, customer_type)
                elif number_of_clients == "multiple":
                    trigger = None
                    asset_type = None
                    client_id = None
                    e117contractor_id = None
                    # Method Calls to save job, job progress, job team and e117 record
                    jp = job_progress(job_id, createdby, fleet)
                    save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                            inspection_type, number_of_clients, customer_type)
            # RE-INSPECTION
            elif inspection_type == "re_inspection":
                trigger = None
                asset_type = None
                number_of_clients = None
                customer_type = None
                e117 = e117_id
                jp = job_progress(job_id, createdby, fleet)
                save_e117(e117_id, job_id, created_by, client_id, e117contractor_id,
                        inspection_type, number_of_clients, customer_type)

        else:
            pass
    data = json.dumps(data)
    url = "http://" + beserver + ":8087/beapi/jobupdate/"+job_id
    job = requests.patch(url=url, data=data, headers=headers)
    response = job.json()
    return render(request, 'beweb/job/reject.html')


def generate_pdf(request, e117_id):
    user, token = user_authenticate(request.user.username)
    headers = {'Authorization': "Token "+token +
               "", "Content-Type": "application/json"}
    # GET E117 data
    url = "http://" + beserver + ":8087/beapi/e117/"+e117_id+"/"
    e117 = requests.get(url=url, headers=headers)
    data = e117.json()
    # GET CLIENT DATA USING CLIENT RETURNED FROM ABOVE REQUEST
    client_url = "http://" + beserver + ":8087/beapi/client/" + \
        data[0]['e117client']+"/"
    client_result = requests.get(url=client_url, headers=headers)
    client_data = client_result.json()
    stand_plot_number = client_data[0]['property_address']
    client_email = client_data[0]['email_address']
    date_created = client_data[0]['e117'][0]['created_on']
    employee_data = execsys(client_data[0]['e117'][0]['created_by'])
    signed = employee_data['firstname'] + " " + employee_data['surname']
    designation = employee_data['designation']

    # GET THE COMMENTS OTHERWISE SET COMMENT FIELD TO EMPTY
    defects = []
    if ((str(data[0]['insd_neutrals_fused'])).lower() == "no" or (str(data[0]['insd_neutrals_fused'])).lower() == "0"):
        defects.append("Neutrals Fused? "+data[0]['insd_neutrals_fused_cmt'])
    else:
        insd_neutrals_fused_cmt = ''
    if ((str(data[0]['insd_block_fitted'])).lower() == "no" or (str(data[0]['insd_block_fitted'])).lower() == "0"):
        defects.append("Neutrals block fitted? " +
                       data[0]['insd_block_fitted_cmt'])
    else:
        insd_block_fitted_cmt = ''
    if ((str(data[0]['insd_electrode_installed'])).lower() == "no" or (str(data[0]['insd_electrode_installed'])).lower() == "0"):
        defects.append("Customer`s electrode installed? " +
                       data[0]['insd_electrode_installed_cmt'])
    else:
        insd_electrode_installed_cmt = ''
    if ((str(data[0]['insd_bonded_earth'])).lower() == "no" or (str(data[0]['insd_bonded_earth'])).lower() == "0"):
        defects.append("Structures bonded to earth? " +
                       data[0]['insd_bonded_earth_cmt'])
    else:
        insd_bonded_earth_cmt = ''
    if ((str(data[0]['insd_outlets_earthed'])).lower() == "no" or (str(data[0]['insd_outlets_earthed'])).lower() == "0"):
        defects.append("Earthing pin of socket outlets earthed? " +
                       data[0]['insd_outlets_earthed_cmt'])
    else:
        insd_outlets_earthed_cmt = ''
    if ((str(data[0]['insd_conductors_size'])).lower() == "no" or (str(data[0]['insd_conductors_size'])).lower() == "0"):
        defects.append("Circuit conductors of correct size? " +
                       data[0]['insd_conductors_size_cmt'])
    else:
        insd_conductors_size_cmt = ''
    if ((str(data[0]['insd_condition_wiring'])).lower() == "bad" or (str(data[0]['insd_condition_wiring'])).lower() == "0"):
        defects.append("Condition of wiring? " +
                       data[0]['insd_condition_wiring_cmt'])
    else:
        insd_condition_wiring_cmt = ''
    if ((str(data[0]['insd_bathroom_switch'])).lower() == "no" or (str(data[0]['insd_bathroom_switch'])).lower() == "0"):
        defects.append("Bathroon switch accessible from bath? " +
                       data[0]['insd_bathroom_switch_cmt'])
    else:
        insd_bathroom_switch_cmt = ''
    if ((str(data[0]['conduits_conduits_bushed'])).lower() == "no" or (str(data[0]['conduits_conduits_bushed'])).lower() == "0"):
        defects.append("Are conduits bushed? " +
                       data[0]['conduits_conduits_bushed_cmt'])
    else:
        conduits_conduits_bushed_cmt = ''
    if ((str(data[0]['conduits_bonded'])).lower() == "no" or (str(data[0]['conduits_bonded'])).lower() == "0"):
        defects.append("Are conduits bonded to earth? " +
                       data[0]['conduits_bonded_cmt'])
    else:
        conduits_bonded_cmt = ''
    if ((str(data[0]['conduits_correct_size'])).lower() == "no" or (str(data[0]['conduits_correct_size'])).lower() == "0"):
        defects.append("Are conduits of correct size? " +
                       data[0]['conduits_correct_size_cmt'])
    else:
        conduits_correct_size_cmt = ''
    if ((str(data[0]['conduits_adequately_supported'])).lower() == "no" or (str(data[0]['conduits_adequately_supported'])).lower() == "0"):
        defects.append("Are conduits adequately supported? " +
                       data[0]['conduits_adequately_supported_cmt'])
    else:
        conduits_adequately_supported_cmt = ''
    if ((str(data[0]['conduits_suitable_type'])).lower() == "no" or (str(data[0]['conduits_suitable_type'])).lower() == "0"):
        conduits_suitable_type_cmt = data[0]['conduits_suitable_type_cmt']
        defects.append("Are conduits of suitable type? " +
                       data[0]['conduits_suitable_type_cmt'])
    else:
        conduits_suitable_type_cmt = ''
    if ((str(data[0]['appliances_motor_installation'])).lower() == "no" or (str(data[0]['appliances_motor_installation'])).lower() == "0"):
        defects.append("Motor installation suitably protected? " +
                       data[0]['appliances_motor_installation_cmt'])
    else:
        appliances_motor_installation_cmt = ''
    if ((str(data[0]['appliances_outbuildings_switches'])).lower() == "no" or (str(data[0]['appliances_outbuildings_switches'])).lower() == "0"):
        defects.append("Outbuildings protected by main switches? " +
                       data[0]['appliances_outbuildings_switches_cmt'])
    else:
        appliances_outbuildings_switches_cmt = ''
    if ((str(data[0]['oh_height_satisfactory'])).lower() == "no" or (str(data[0]['oh_height_satisfactory'])).lower() == "0"):
        defects.append("Overhead lines height satisfactory? " +
                       data[0]['oh_height_satisfactory_cmt'])
    else:
        oh_height_satisfactory_cmt = ''
    if ((str(data[0]['oh_support_satisfactory'])).lower() == "no" or (str(data[0]['oh_support_satisfactory'])).lower() == "0"):
        defects.append("Overhead lines support satisfactory? " +
                       data[0]['oh_support_satisfactory_cmt'])
    else:
        oh_support_satisfactory_cmt = ''
    if ((str(data[0]['oh_condition_line'])).lower() == "bad" or (str(data[0]['oh_condition_line'])).lower() == "0"):
        defects.append("Condition of overhead lines? " +
                       data[0]['oh_condition_line_cmt'])
    else:
        oh_condition_line_cmt = ''
    if ((str(data[0]['oh_earthwires_fitted'])).lower() == "no" or (str(data[0]['oh_earthwires_fitted'])).lower() == "0"):
        defects.append("Earthwires fitted to lines? " +
                       data[0]['oh_earthwires_fitted_cmt'])
    else:
        oh_earthwires_fitted_cmt = ''
    if ((str(data[0]['defects_contractor'])).lower() == "no" or (str(data[0]['defects_contractor'])).lower() == "0"):
        defects.append("Contractor notified of defects? " +
                       data[0]['defects_contractor_cmt'])
    else:
        defects_contractor_cmt = ''
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Times-Roman', 12)
    p.drawString(
        100, 800, "ZIMBABWE ELECTRICITY TRANSMISSION AND DISTRIBUTION COMPANY")
    p.drawString(200, 780, "E1: INSPECTION OF INSTALLATION")
    p.drawString(20, 750, "TO: 1. CUSTOMER")
    p.drawString(350, 750, "SERVICE NUMBER SN: ....")
    p.drawString(45, 730, "2. CONTRACTOR")
    p.drawString(45, 710, "3. DISTRICT MANAGER")
    p.drawString(45, 690, "4. SENIOR CUSTOMER SERVICES OFFICER")
    p.drawString(20, 650, "Sir/Madam,")
    p.drawString(
        20, 610, "You are Hereby notified that the electrical installation on")
    p.setFont('Times-Bold', 12)
    p.drawString(300, 610, "STAND/PLOT No: ")
    p.setFont('Times-Italic', 12)
    if len(stand_plot_number) > 30:
        p.drawString(400, 610, stand_plot_number[:30])
        p.drawString(20, 590, stand_plot_number[30:])
    else:
        p.drawString(400, 610, stand_plot_number)
    p.setFont('Times-Bold', 12)
    p.drawString(20, 570, "SUB. DIV. NO.")
    p.drawString(250, 570, "FARM/MINE:")
    p.drawString(20, 550, "DISTRICT:")
    p.drawString(250, 550, "TOWNSHIP:")
    p.setFont('Times-Roman', 12)
    p.drawString(
        20, 530, "has been inspected and that certain defects, a list of which is given below, require your attention.")
    p.drawString(
        20, 510, "This installation will be reinspected in receipt of a Notification of Completion of Wiring Form E. 38 ")
    p.drawString(20, 490, " and the reinspection fee of $420.00")
    p.drawString(195, 490, "due in terms of the Authority General Conditions,")
    p.drawString(20, 470, "of Supply, Schedule of prescribed Fees.")
    p.setFont('Times-Bold', 12)
    p.drawString(20, 450, "DATE: ")
    p.setFont('Times-Roman', 12)
    p.drawString(60, 450, datetime.now().strftime("%Y%m%d%H%M"))
    p.setFont('Times-Bold', 12)
    p.drawString(250, 450, "SIGNED: ")
    p.setFont('Times-Roman', 12)
    p.drawString(310, 450, signed)
    p.setFont('Times-Bold', 12)
    p.drawString(20, 430, "REF: ")
    p.setFont('Times-Roman', 12)
    p.drawString(55, 430, (e117_id).capitalize())
    p.setFont('Times-Bold', 12)
    p.drawString(250, 430, "DESIGNATION: ")
    p.setFont('Times-Roman', 12)
    p.drawString(340, 430, designation)
    p.setFont('Times-Bold', 12)
    p.drawString(20, 400, "LIST OF DEFECTS REQUIRING ATTENTION:")
    p.setFont('Times-Italic', 12)
    if len(defects) > 0:
        x = 40
        y = 370
        counter = 1
        for defect in defects:
            if len(defect) > 100:
                p.drawString(x, y, str(counter) + ". " + defect[:100])
                y = y - 20
                p.drawString(x, y, defect[101:])
                y = y - 20
            else:
                p.drawString(x, y, str(counter) + ". " + defect)
                y = y - 20
            counter = counter + 1
    p.setFont('Times-Roman', 12)
    p.drawString(
        20, 41, "N.B: After connection to the Mains the tests and inspections made by the Authority in no way relieve")
    p.drawString(
        45, 21, "the Consumer of any responsibility in regards its subsequent maintenance of his electrical installation.")
    p.showPage()
    p.save()
    buffer.seek(0)
    attachment = e117_id + '.pdf'
    message = ''
    if client_email is None:
        message = "Client Email Address Not Found!"
    else:
        send_email(attachment, buffer, client_email)
    job_id = data[0]['job']
    patch_data = {
        "job_id": job_id,
        "status": 7
    }
    patch_data = json.dumps(patch_data)
    patch_url = "http://" + beserver + ":8087/beapi/jobupdate/"+job_id
    patch_response = requests.patch(
        url=patch_url, data=patch_data, headers=headers)
    response = patch_response.json()
    context = {
        "message": message
    }
    return render(request, 'beweb/job/close.html', context)


def send_email(attachment, buffer, client_email):
    subject = "Inspection of Installation Report"
    message = "Dear Sir/Madam,\n\nPlease find attached report for the inspection carried out at your property.\n\nRegards,\n\n ZETDC\n Eastern Region\n\n"
    sender = "eastsupport@zetdc.co.zw"
    to = client_email
    email = EmailMessage(
        subject,
        message,
        sender,
        [to]
    )
    email.attach(attachment, buffer.read(), 'application/pdf')
    email.send()
    return


class Stations(APIView):
    '''
    Returns a list of stations for a particular centre
    '''

    def get(self, request, depot):
        station = Station.objects.filter(depot=depot)
        serializer = StationSerializer(station, many=True).data
        return Response(serializer)


class Transformers(APIView):
    '''
    Returns a list of transformers for a particular centre
    '''

    def get(self, request, depot):
        station = Transformer.objects.filter(depot=depot)
        serializer = TransformersSerializer(station, many=True).data
        return Response(serializer)


class ApproveE50(View):
    def post(self, request, *args, **kwargs):
        username = request.user.username
        data = execsys(username)
        username = data['username']
        job_workflow_id = "jwf" + datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        job_id = request.POST.get('job_id')
        actioner = request.user.username
        comment = request.POST.get('reject_reason')
        # CHECK i.e close E50 job
        if request.POST.get('check'):
            job_id = request.POST.get('job')
            job_workflow_id = None
            decision = 7
            comment = None
            with connection.cursor() as cursor:
                cursor.execute("CALL core.approve_job(%s, %s, %s, %s, %s);",
                               (job_workflow_id, job_id, actioner, decision, comment))
                connection.commit()
            return render(request, 'beweb/job/close.html', {})
        # REJECT E50 job
        elif request.POST.get('send'):
            decision = 8
            with connection.cursor() as cursor:
                cursor.execute("CALL core.approve_job(%s, %s, %s, %s, %s);",
                               (job_workflow_id, job_id, actioner, decision, comment))
                connection.commit()
            return render(request, 'beweb/job/reject.html', {})


class ApproveE60(View):
    def post(self, request, *args, **kwargs):
        username = request.user.username
        data = execsys(username)
        username = data['username']
        job_workflow_id = "jwf" + datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        job_id = request.POST.get('job_id')
        actioner = request.user.username
        comment = request.POST.get('reject_reason')
        # CHECK i.e close E60 job
        if request.POST.get('check'):
            job_id = request.POST.get('job')
            job_workflow_id = "jwf" + datetime.now().strftime("%Y%m%d%H%M") + \
                str(random.randrange(000000, 100000))
            decision = 7
            comment = None
            with connection.cursor() as cursor:
                cursor.execute("CALL core.approve_job(%s, %s, %s, %s, %s);",
                               (job_workflow_id, job_id, actioner, decision, comment))
                connection.commit()
            return render(request, 'beweb/job/close.html', {})
        # REJECT E60 job
        elif request.POST.get('send'):
            decision = 8
            with connection.cursor() as cursor:
                cursor.execute("CALL core.approve_job(%s, %s, %s, %s, %s);",
                               (job_workflow_id, job_id, actioner, decision, comment))
                connection.commit()
            return render(request, 'beweb/job/reject.html', {})

class ApproveE117(View):
    def post(self, request, *args, **kwargs):
        username = request.user.username
        data = execsys(username)
        username = data['username']
        job_workflow_id = "jwf" + datetime.now().strftime("%Y%m%d%H%M") + \
            str(random.randrange(000000, 100000))
        job_id = request.POST.get('job_id')
        actioner = request.user.username
        comment = request.POST.get('reject_reason')
        # CHECK i.e close E117 job
        if request.POST.get('check'):
            job_id = request.POST.get('job')
            job_workflow_id = "jwf" + datetime.now().strftime("%Y%m%d%H%M") + \
                str(random.randrange(000000, 100000))
            decision = 7
            comment = None
            with connection.cursor() as cursor:
                cursor.execute("CALL core.approve_job(%s, %s, %s, %s, %s);",
                               (job_workflow_id, job_id, actioner, decision, comment))
                connection.commit()
            return render(request, 'beweb/job/close.html', {})
        # REJECT E117 job
        elif request.POST.get('send'):
            decision = 8
            with connection.cursor() as cursor:
                cursor.execute("CALL core.approve_job(%s, %s, %s, %s, %s);",
                               (job_workflow_id, job_id, actioner, decision, comment))
                connection.commit()
            return render(request, 'beweb/job/reject.html', {})

class ViewReport(View):
    def post(self, request):
        report_type = request.POST.get('report_type')
        jobtype = request.POST.get('jobtype')
        centres = request.POST.get('centres')
        centre_code = request.POST.get('centre_code')
        centre = request.POST.get('centre')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')
        pagetype = "reports"
        context={
            "report_type":report_type,
            "jobtype":jobtype,
            "centre":centre,
            "centre_code":centre_code,
            "start_date":start_date,
            "end_date":end_date,
            "status":status,
            "pagetype":pagetype
        }
        return render(request, 'beweb/reports/view_report.html', context)


def delworkOrder(self,request):
    work_order_id = request.GET.get('q', '')
    username = request.user.username
    usr, tkn = user_authenticate(username)
    headers = {'Authorization': "Token "+tkn +
               "", "Content-Type": "application/json"}

    url = "http://" + beserver + ":8087/beapi/single/workorder/" + work_order_id+"/"
    r = requests.get(url=url, headers=headers)
    data = r.json()
    num_jobs = len(data[0]['jobs'])
    # if num_jobs == 0:
    #     url = "http://" + beserver + ":8087/beapi/workorderdelete/" + work_order_id+"/"
    #     r = requests.get(url=url, headers=headers)
    #     data = r.json()

    context = {
        "workorder": data[0],
        "number_of_jobs": num_jobs
    }
    return render(request, 'beweb/workorder/delete_workorder.html', context)

class Worksdelete(View):
    def delete(self, request):
        work_order_id = request.GET.get('q', '')
        username = request.user.username
        usr, tkn = user_authenticate(username)
        headers = {'Authorization': "Token "+tkn +
                "", 'Content-Type': 'application/json'}

        url = "http://" + beserver + ":8087/beapi/single/workorder/" + work_order_id+"/"
        workorder_response = requests.get(url=url, headers=headers)
        data = workorder_response.json()

        url = 'http://' + beserver + ':8087/beapi/workorderdelete/'+work_order_id+"/"
        data = json.dumps(data)
        delete_response = requests.delete(url=url, data=data, headers=headers)
        # response_data = delete_response.json()
        context = {
            "work_order_id": work_order_id
        }
        return render(request, 'beweb/dashboard.html', context)
