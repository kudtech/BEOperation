from .models import Workorder
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .serializers import *
from .models import *

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND, HTTP_200_OK)

from django.contrib.auth.models import User
from django.db.models import Count




################################################################################
import select
import errno
import sys
from datetime import datetime
from django.http import HttpResponse
from django.views import View
###############################################################################

class Appflows(APIView):
    """[Workflow for Apps View]
    
    Arguments:
        APIView {[GET Method]} -- [description]
    
    Returns:
        [type] -- [Returns Appflow Data]
    """
    permission_classes = (IsAuthenticated,) 
    def get(self, request, format=None):
        appflow = Appflow.objects.prefetch_related().all()
        serializer=AppFlowSerializer(appflow,many=True).data
        return Response(serializer)



class AppflowsPost(APIView):
     """[Add New App workflow]
     
     Arguments:
         APIView {[POST Method]} -- [description]
     
     Returns:
         [type] -- [posts Appflow Data]
     """
     permission_classes = (IsAuthenticated,)
     def post(self, request):
         serializer = AppflowSerializers(data = request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED) 
         else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppflowDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,pk):
        appflow = Appflow.objects.all()
        serializerFlow = AppflowSerializers(appflow,many=True).data
        return Response(serializerFlow)
    def delete(self,request,pk):
        appflow = Appflow.objects.filter(appflow_id=pk)
        appflow.delete()
        return Response("Content deleted successfully",status=status.HTTP_204_NO_CONTENT)



class AppflowModify(APIView):
    def get_object(self, pk):
        try:
            return Appflow.objects.get(pk=pk)
        except Appflow.DoesNotExist:
            raise Http404
    def get(self,request,pk,format=None):
        appflows= self.get_object(pk)
        serializerapp=AppflowSerializers(appflows)
        return Response(serializerapp.data)

    def put(self, request, pk, format=None):
        appflowmodify = self.get_object(pk)
        serializer = AppflowSerializers(appflowmodify, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppflowUpdate(APIView):
    def get_object(self,pk):
        try:
            return Appflow.objects.get(pk=pk)
        except Appflow.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        appflow = self.get_object(pk)
        serializerap = AppflowSerializers(appflow)
        return Response(serializerap.data)

    def patch(self, request, pk):
        appflowz = self.get_object(pk)
        serializer = AppflowSerializers(appflowz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class Workorders(APIView):
    '''
    Returns a list of all workorders created in the system
    '''
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        workorder = Workorder.objects.all()
        serializer = WorkorderSerializers(workorder, many=True).data
        return Response(serializer)


class SingleWorkorder(APIView):
    '''
    Returns a list of all jobs associated with the specified workorder 
    '''
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Workorder.objects.get(pk=pk)
        except Workorder.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        workorder=self.get_object(pk)
        serializer = WorkorderSerializers([workorder], many=True).data
        return Response(serializer)


class WorkorderJobs(APIView):
    '''
    Returns a list of all jobs associated with the specified workorder 
    '''
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Workorder.objects.get(pk=pk)
        except Workorder.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        workorder=self.get_object(pk)
        serializer = WorkorderJobsSerializers([workorder], many=True).data
        return Response(serializer)


class JobsWorkorder(APIView):
    '''
    Returns a list of all jobs associated with the specified workorder 
    '''
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Workorder.objects.get(pk=pk)
        except Workorder.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        workorder=self.get_object(pk)
        serializer = WorkorderSerializer([workorder], many=True).data
        return Response(serializer)


class WorkordersPost(APIView):
    
    def post(self, request):
        serializer = WorkorderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkorderDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self,pk):
        try:
            return Workorder.objects.get(pk=pk)
        except Workorder.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        wkorder = self.get_object(pk)
        serializer = WorkorderSerializers([wkorder], many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        wkorder = self.get_object(pk)
        wkorder.delete()
        return Response("Work Order deleted successfully", status=status.HTTP_204_NO_CONTENT)


class WorkorderModify(APIView):
    def get_object(self, pk):
        try:
            return Workorder.objects.get(pk=pk)
        except Workorder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns a single workorder with a specified id.
        '''
        workorder = self.get_object(pk)
        serializer = WorkorderSerializers(workorder)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        '''
        Updates a single workorder with a specified id.
        '''
        workorder = self.get_object(pk)
        serializer = WorkorderSerializers(workorder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkOrderUpdate(APIView):
    def get_object(self, pk):
        try:
            return Workorder.objects.get(pk=pk)
        except Workorder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns a single workorder with a specified id.
        '''
        workorder = self.get_object(pk)
        serializer = WorkorderSerializers(workorder)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates a single workorder with a specified id.
        '''
        workorder = self.get_object(pk)
        serializer = WorkorderSerializers(
            workorder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



 #
 # JOB
 # 


class JobGet(APIView):
    
    def get_object(self,pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns a single job. User should specify the id.
        '''
        job = self.get_object(pk)
        serializer = JobSerializer([job], many=True).data
        return Response(serializer)   



class Jobs(APIView):

    '''
    Returns a list of all jobs created in the system
    '''
    def get(self, request, format=None):
        jobs = Job.objects.all()       
        serializer = JobSerializer(jobs, many=True).data
        return Response(serializer)


class AssignedJobs(APIView):

    '''
    Returns a list of all jobs assigned to a specified user
    ''' 
    def get(self, request, assignee):        
        jobs = Job.objects.filter(assignee=assignee).filter(sync_status=0)           
        serializer = JobSerializer(jobs, many=True).data
        return Response(serializer) 


class JobCreate(APIView):
    '''
    Enables the creation of a job
    '''
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDelete(APIView):  
    def get(self, request, pk):

        '''
        Returns details of the job with the specified id
        '''
        job = Job.objects.filter(job_id=pk)
        serializer = JobSerializer(job, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes job with the specified id
        '''
        job = Job.objects.filter(job_id=pk)
        job.delete()
        return Response("Job deleted successfully", status=status.HTTP_204_NO_CONTENT)


class JobUpdate(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of the job with the specified id
        '''
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)


    def patch(self, request, pk):

        '''
        Updates a job with the specified id
        '''
        if 'sync_status' in request.data:
            if request.data['sync_status'] is not None and request.data['sync_status'] !='':           
                sync_status = request.data['sync_status']
        else:
            sync_status=0        
        job = self.get_object(pk)
        serializer = JobSerializer(
            job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(sync_status=sync_status)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
#CLIENT
#


class ClientGet(APIView):  

    def get_object(self, pk):
        try:
            return E117Client.objects.get(pk=pk)
        except E117Client.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single client with the specified id
        '''
        client = self.get_object(pk)
        serializer = ClientSerializer([client], many=True).data
        return Response(serializer)

class Clients(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all clients in the system
        '''
        client = E117Client.objects.all()
        serializer = ClientSerializer(client, many=True).data
        return Response(serializer)

class ClientCreate(APIView):
    def post(self, request):
        '''
        Enables the creation of a client
        '''
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDelete(APIView):
    def get_object(self, pk):
        try:
            return E117Client.objects.get(pk=pk)
        except E117Client.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single client with the specified id
        '''
        client = self.get_object(pk)
        serializer = ClientSerializer([client], many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a client account  with the specified id
        '''
        client = self.get_object(pk)
        client.delete()
        return Response("Client deleted successfully", status=status.HTTP_204_NO_CONTENT)

class ClientUpdate(APIView):
    def get_object(self, pk):
        try:
            return E117Client.objects.get(pk=pk)
        except E117Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single client with the specified id
        '''
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def patch(self, request, pk):

        '''
        Updates details of a client with the specified id
        '''
        client = self.get_object(pk)
        serializer = ClientSerializer(
            client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#FEEDER
class FeederGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single feeder with the specified id
        '''
        feeder=get_object_or_404(Feeder,feedercode=pk)
        serializer = FeederSerializer([feeder], many=True).data
        return Response(serializer)


class Feeders(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all feeders in the system
        '''
        feeder = Feeder.objects.all()
        serializer = FeederSerializer(feeder, many=True).data
        return Response(serializer)

class FeederCreate(APIView):
    def post(self, request):
        '''
        Enables creation of a feeder
        '''
        serializer = FeederSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeederDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single feeder with the specified id
        '''
        feeder = Feeder.objects.filter(feedercode=pk)
        serializer = FeederSerializer(feeder, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single feeder with the specified id
        '''
        feeder = Feeder.objects.filter(feedercode=pk)
        feeder.delete()
        return Response("Feeder deleted successfully", status=status.HTTP_204_NO_CONTENT)


class FeederUpdate(APIView):
    def get_object(self, pk):
        try:
            return Feeder.objects.get(pk=pk)
        except Feeder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single feeder with the specified id
        '''
        feeder = self.get_object(pk)
        serializer = FeederSerializer(feeder)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a feeder with the specified id
        '''
        feeder = self.get_object(pk)
        serializer = FeederSerializer(
            feeder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LIGHTNING ARRESTERS
class LightningArresterGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Lightning Arrester with the specified id
        '''
        lightningarrester = Lightningarrester.objects.filter(lightningarrester_id=pk)
        serializer = LightningArresterSerializer(lightningarrester, many=True).data
        return Response(serializer)

    
class LightningArresters(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Lightning Arresters
        '''
        lightningarrester = Lightningarrester.objects.all()
        serializer = LightningArresterSerializer(lightningarrester, many=True).data
        return Response(serializer)


class LightningArresterCreate(APIView):
    def post(self, request):
        '''
        Creates a single Lightning Arrester
        '''
        serializer = LightningArresterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LightningArresterDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Lightning Arrester with the specified id
        '''
        lightningarrester = Lightningarrester.objects.filter(lightningarrester_id=pk)
        serializer = LightningArresterSerializer(lightningarrester, many=True).data
        return Response(serializer)

    def delete(self, request, pk):

        '''
        Deletes a single Lightning Arrester with the specified id
        '''
        lightningarrester = Lightningarrester.objects.filter(lightningarrester_id=pk)
        lightningarrester.delete()
        return Response("Lightning Arrester deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  LightningArresterUpdate(APIView):
    def get_object(self, pk):
        try:
            return Lightningarrester.objects.get(pk=pk)
        except Lightningarrester.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single lightningarrester with the specified id
        '''
        lightningarrester = self.get_object(pk)
        serializer = LightningArresterSerializer(lightningarrester)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single lightningarrester with the specified id
        '''
        lightningarrester = self.get_object(pk)
        serializer = LightningArresterSerializer(
            lightningarrester, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 
# SUBSTATION METER
# 

class SubstationMeterGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Substation Meter with the specified id
        '''
        substationmeter = Substationmeter.objects.filter(meter_id=pk)
        serializer = SubstationMeterSerializer(substationmeter, many=True).data
        return Response(serializer)

    
class SubstationMeters(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Substation Meters
        '''
        substationmeter = Substationmeter.objects.all()
        serializer = SubstationMeterSerializer(substationmeter, many=True).data
        return Response(serializer)


class SubstationMeterCreate(APIView):
    def post(self, request):
        '''
        Creates a single Substation Meter in the system
        '''
        serializer = SubstationMeterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubstationMeterDelete(APIView):
    def get(self, request, pk):
        '''
        Gets details of a single Substation Meter with the specified id
        '''
        substationmeter = Substationmeter.objects.filter(meter_id=pk)
        serializer = SubstationMeterSerializer(substationmeter, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single Substation Meter with the specified id
        '''
        substationmeter = Substationmeter.objects.filter(meter_id=pk)
        substationmeter.delete()
        return Response("Substation Meter deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  SubstationMeterUpdate(APIView):
    def get_object(self, pk):
        try:
            return Substationmeter.objects.get(pk=pk)
        except Substationmeter.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a  single Substation Meter  with the specified id
        '''
        substationmeter = self.get_object(pk)
        serializer = SubstationMeterSerializer(substationmeter)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Substation Meter with the specified id
        '''
        substationmeter = self.get_object(pk)
        serializer = SubstationMeterSerializer(
            substationmeter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 
# SWITCHGEAR
# 

class SwitchgearGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Switchgear with the specified id
        '''
        switchgear = Switchgear.objects.filter(switchgearid=pk)
        serializer = SwitchgearSerializer(switchgear, many=True).data
        return Response(serializer)

    
class Switchgears(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Switchgears in the system
        '''
        switchgear = Switchgear.objects.all()
        serializer = SwitchgearSerializer(switchgear, many=True).data
        return Response(serializer)


class SwitchgearCreate(APIView):
    def post(self, request):
        '''
        Creates a Switchgear record in the system
        '''
        serializer = SwitchgearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SwitchgearDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Switchgear with the specified id
        '''
        switchgear = Switchgear.objects.filter(switchgearid=pk)
        serializer = SwitchgearSerializer(switchgear, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        switchgear = Switchgear.objects.filter(switchgearid=pk)
        switchgear.delete()
        return Response("Switchgear deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  SwitchgearUpdate(APIView):
    def get_object(self, pk):
        try:
            return Switchgear.objects.get(pk=pk)
        except Switchgear.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Switchgear with the specified id
        '''
        switchgear = self.get_object(pk)
        serializer = SwitchgearSerializer(switchgear)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Switchgear with the specified id
        '''
        switchgear = self.get_object(pk)
        serializer = SwitchgearSerializer(
            switchgear, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 
# TRANSFORMER
# 

class TransformerGet(APIView):
    def get(self, request, pk):
        '''
        Returns details ofStation with the specified id
        '''
        transformer = Transformer.objects.filter(transformerid=pk)
        serializer = TransformerSerializer(transformer, many=True).data
        return Response(serializer)

    
class Transformers(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Transformers in the system
        '''
        transformer = Transformer.objects.all()
        serializer = TransformerSerializer(transformer, many=True).data
        return Response(serializer)



class TransformerCreate(APIView):
    def post(self, request):
        '''
        Creates a single Transformer record
        '''
        serializer = TransformerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransformerDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Transformer with the specified id
        '''
        transformer = Transformer.objects.filter(transformerid=pk)
        serializer = TransformerSerializer(transformer, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single transformer with the specified id
        '''
        transformer = Transformer.objects.filter(transformerid=pk)
        transformer.delete()
        return Response("Transformer deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  TransformerUpdate(APIView):
    def get_object(self, pk):
        try:
            return Transformer.objects.get(pk=pk)
        except Transformer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Transformer with the specified id
        '''
        transformer = self.get_object(pk)
        serializer = TransformerSerializer(transformer)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Transformer with the specified id
        '''
        transformer = self.get_object(pk)
        serializer = TransformerSerializer(
            transformer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# 
# BOQLABOUR
# 

class BoqLabourGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Bill of Quantities- Labour with the specified id
        '''
        boqlabour = Boqlabour.objects.filter(boq_labour_id=pk)
        serializer = BoqLabourSerializer(boqlabour, many=True).data
        return Response(serializer)

    
class BoqsLabour(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Labour Bill of Quantities in the system
        '''
        boqlabour = Boqlabour.objects.all()
        serializer = BoqLabourSerializer(boqlabour, many=True).data
        return Response(serializer)


class BoqLabourCreate(APIView):
    def post(self, request):
        '''
        Creates a single Bill of Quantities for Labour record
        '''
        serializer = BoqLabourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoqLabourDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Bill of Quantities for Labour with the specified id
        '''
        boqlabour = Boqlabour.objects.filter(boq_labour_id=pk)
        serializer = BoqLabourSerializer(boqlabour, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single Bill of Quantities for Labour record with the specified id
        '''
        boqlabour = Boqlabour.objects.filter(boq_labour_id=pk)
        boqlabour.delete()
        return Response("BOQ for Labour deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  BoqLabourUpdate(APIView):
    def get_object(self, pk):
        try:
            return Boqlabour.objects.get(pk=pk)
        except Boqlabour.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Bill of Quantities for Labour with the specified id
        '''
        boqlabour = self.get_object(pk)
        serializer = BoqLabourSerializer(boqlabour)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Bill of Quantities - Labour with the specified id
        '''
        boqlabour = self.get_object(pk)
        serializer = BoqLabourSerializer(
            boqlabour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# 
# BOQMATERIAL
# 

class BoqMaterialGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Materials Bill of Quantities with the specified id
        '''
        boqmaterial = Boqmaterial.objects.filter(boq_id=pk)
        serializer = BoqMaterialSerializer(boqmaterial, many=True).data
        return Response(serializer)

    
class BoqMaterial(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Bill of Quantities -  Materials in the system
        '''
        boqmaterial = Boqmaterial.objects.all()
        serializer = BoqMaterialSerializer(boqmaterial, many=True).data
        return Response(serializer)


class BoqMaterialCreate(APIView):
    def post(self, request):
        '''
        Creates a single Materials Bill of Quantities record in the system
        '''
        serializer = BoqMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoqMaterialDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Materials Bill of Quantities with the specified id
        '''
        boqmaterial = Boqmaterial.objects.filter(boq_id=pk)
        serializer = BoqMaterialSerializer(boqmaterial, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single Materials Bill of quantities record with the specified id
        '''
        boqmaterial = Boqmaterial.objects.filter(boq_id=pk)
        boqmaterial.delete()
        return Response("BOQ for Material deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  BoqMaterialUpdate(APIView):
    def get_object(self, pk):
        try:
            return Boqmaterial.objects.get(pk=pk)
        except Boqmaterial.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Materials Bill of Quantities with the specified id
        '''
        boqmaterial = self.get_object(pk)
        serializer = BoqMaterialSerializer(boqmaterial)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Materials Bill of Quantities with the specified id
        '''
        boqmaterial = self.get_object(pk)
        serializer = BoqMaterialSerializer(
            boqmaterial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# 
# BOQVEHICLE
# 

class BoqVehicleGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Vehicle`s Bill of Quantities with the specified id
        '''
        boqvehicle = Boqvehicle.objects.filter(boq_vehicle_id=pk)
        serializer = BoqVehicleSerializer(boqvehicle, many=True).data
        return Response(serializer)

    
class BoqVehicle(APIView):
    def get(self, request, format=None):
        '''
        Returns details of all Vehicles` Bill of Quantities with the specified id
        '''
        boqvehicle = Boqvehicle.objects.all()
        serializer = BoqVehicleSerializer(boqvehicle, many=True).data
        return Response(serializer)


class BoqVehicleCreate(APIView):
    def post(self, request):
        '''
        Returns details of a single Materials Bill of Quantities with the specified id
        '''
        serializer = BoqVehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BoqVehicleDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Vehicle`s Bill of Quantities with the specified id
        '''
        boqvehicle = Boqvehicle.objects.filter(boq_vehicle_id=pk)
        serializer = BoqVehicleSerializer(boqvehicle, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single Vehicle`s Bill of Quantities record with the specified id
        '''
        boqvehicle = Boqvehicle.objects.filter(boq_vehicle_id=pk)
        boqvehicle.delete()
        return Response("BOQ for Vehicle deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  BoqVehicleUpdate(APIView):
    def get_object(self, pk):
        try:
            return Boqvehicle.objects.get(pk=pk)
        except Boqvehicle.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Vehicle`s Bill of Quantities with the specified id
        '''
        boqvehicle = self.get_object(pk)
        serializer = BoqVehicleSerializer(boqvehicle)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Vehicle`s Bill of Quantities with the specified id
        '''
        boqvehicle = self.get_object(pk)
        serializer = BoqVehicleSerializer(
            boqvehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WorkOrderUpdate(APIView):
    def get_object(self, pk):
        try:
            return Workorder.objects.get(pk=pk)
        except Workorder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        workorder = self.get_object(pk)
        serializer = WorkorderSerializers(workorder)
        return Response(serializer.data)

    def patch(self, request, pk):
        workorder = self.get_object(pk)
        serializer = WorkorderSerializers(
            workorder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Workflows(APIView):
    def get(self, request, format=None):
        workflows=Workflow.objects.prefetch_related('job_workflows').all() 
        serializer=WorkflowSerializer(workflows,many=True).data
        return Response(serializer)


class WorkflowsPost(APIView):
    def post(self, request):
        serializer = WorkflowSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkflowDelete(APIView):

    def get(self, request, pk):
        wkflow = Workflow.objects.filter(workflow_id=pk)
        serializer = WorkflowSerializer(wkflow, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        wkorder = Workflow.objects.filter(work_order_id=pk)
        wkorder.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class WorkflowUpdate(APIView):
    def get_object(self, pk):
        try:
            return Workflow.objects.get(pk=pk)
        except Workflow.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        workflows = self.get_object(pk)
        serializer = WorkflowSerializer(workflows)
        return Response(serializer.data)

    def patch(self, request, pk):
        workflows = self.get_object(pk)
        serializer = WorkflowSerializer(
            workflows, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#User Role Trail methods


class  UserRoleTrails(APIView):
    def get(self, request, format=None):
        user_role_trails = Userroletrail.objects.all()
        serializer = UserroletrailSerializers(user_role_trails, many=True).data
        return Response(serializer)
    

class UserRoleTrailsPost(APIView):
    def post(self, request):
        serializer = UserroletrailSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRoleTrailDelete(APIView):

    def get(self, request, pk):
        user_role_trail = Userroletrail.objects.filter(user_role_trail_id=pk)
        serializer = UserroletrailSerializers(user_role_trail, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        user_role_trail = Userroletrail.objects.filter(user_role_trail_id=pk)
        user_role_trail.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class UserRoleTrailUpdate(APIView):
    def get_object(self, pk):
        try:
            return Userroletrail.objects.get(pk=pk)
        except Userroletrail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        userroletrails = self.get_object(pk)
        serializer = UserroletrailSerializers(userroletrails)
        return Response(serializer.data)

    def patch(self, request, pk):
        userroletrails = self.get_object(pk)
        serializer =UserroletrailSerializers(
           userroletrails, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#User Role Views
class  UserRoles(APIView):
    def get(self, request, format=None):
        user_role_ = Userroletrail.objects.all()
        serializer = UserroleSerializers(user_role_, many=True).data
        return Response(serializer)
    

class UserRolePost(APIView):
    def post(self, request):
        serializer = UserroleSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRoleDelete(APIView):

    def get(self, request, pk):
        user_role = Userrole.objects.filter(user_role_id=pk)
        serializer = UserroleSerializers(user_role, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        user_role = Userrole.objects.filter(user_role_id=pk)
        user_role.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class UserRoleUpdate(APIView):
    def get_object(self, pk):
        try:
            return Userroletrail.objects.get(pk=pk)
        except Userroletrail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        userrole = self.get_object(pk)
        serializer = UserroleSerializers(userrole)
        return Response(serializer.data)

    def patch(self, request, pk):
        userrole = self.get_object(pk)
        serializer =UserroleSerializers(
           userrole, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class Teams(APIView):
    def get(self, request):
        team = TeamLeader.objects.all()
        serializer = TeamLeaderSerializer(team, many=True)
        return Response(serializer.data)

class TeamLeaders(APIView):
    def get(self, request):
        team = TeamLeader.objects.all()
        serializer = TeamLeaderSerializer(team, many=True)
        return Response(serializer.data)


class TeamGet(APIView):
    def get(self, request, team_leader):
        team = TeamLeader.objects.filter(team_leader=team_leader)
        serializer = TeamLeaderSerializer(team, many=True)
        return Response(serializer.data)


class TeamView(APIView):
    def get(self, request):
        teammember = Team.objects.all()
        serializer = TeamSerializers(teammember, many=True)
        return Response(serializer.data)

class TeamPost(APIView): 
    def post(self,request):
        serializer=TeamLeaderSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)


class TeamDelete(APIView):

    def get(self, request, pk):
        team = Team.objects.filter(team_id=pk)
        serializer = TeamSerializers(team, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        user_role = Team.objects.filter(team_id=pk)
        user_role.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class TeamUpdate(APIView):
    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = TeamSerializers(team)
        return Response(serializer.data)

    def patch(self, request, pk):
        team = self.get_object(pk)
        serializer = TeamSerializers(
           team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#Role Permision Views
class  RolePermissions(APIView):
    def get(self, request, format=None):
        role_permission = Rolepermission.objects.all()
        serializer = RolePermissionSerializers(role_permission, many=True).data
        return Response(serializer)
    

class RolePermissionPost(APIView):
    def post(self, request):
        serializer = RolePermissionSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RolePermissionDelete(APIView):
    
    def get(self, request, pk):
        role_permission = Rolepermission.objects.filter(role_permission_id=pk)
        serializer = RolePermissionSerializers(role_permission, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        role_permission = Rolepermission.objects.filter(role_permission_id=pk)
        role_permission.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class RolePermissionUpdate(APIView):
    def get_object(self, pk):
        try:
            return Rolepermission.objects.get(pk=pk)
        except Rolepermission.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        role_permission = self.get_object(pk)
        serializer = RolePermissionSerializers(role_permission)
        return Response(serializer.data)

    def patch(self, request, pk):
        role_permission = self.get_object(pk)
        serializer =RolePermissionSerializers(
           role_permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#Role Views
class Roles(APIView):
    def get(self, request, format=None):
        roles = Role.objects.all().prefetch_related('workflows')
        serializer=RoleSerializers(roles,many=True).data
        return Response(serializer)
    

class RolePost(APIView):
    def post(self, request):
        serializer = RoleSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleDelete(APIView):
    
    def get(self, request, pk):
        role = Role.objects.filter(role_id=pk)
        serializer = RoleSerializers(role, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        role = Role.objects.filter(role_id=pk)
        role.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class RoleUpdate(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        role_ = self.get_object(pk)
        serializer = RoleSerializers(role)
        return Response(serializer.data)

    def patch(self, request, pk):
        role = self.get_object(pk)
        serializer =RoleSerializers(
           role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#Pole Views
class  Poles(APIView):
    def get(self, request, format=None):
        pole = Pole.objects.all()
        serializer = PoleSerializers(pole, many=True).data
        return Response(serializer)
    

class PolePost(APIView):
    def post(self, request):
        serializer = PoleSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PoleDelete(APIView):

    def get(self, request, pk):
        pole = Pole.objects.filter(pole_id=pk)
        serializer = PoleSerializers(pole, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        pole = Pole.objects.filter(pole_id=pk)
        pole.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class PoleUpdate(APIView):
    def get_object(self, pk):
        try:
            return Pole.objects.get(pk=pk)
        except Pole.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pole_ = self.get_object(pk)
        serializer = PoleSerializers(pole)
        return Response(serializer.data)

    def patch(self, request, pk):
        pole = self.get_object(pk)
        serializer =PoleSerializers(
           pole, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#Permission Views
class  Permissions(APIView):
    def get(self, request, format=None):
        permission = Permission.objects.all()
        serializer = PermissionSerializers(permission, many=True).data
        return Response(serializer)
    

class PermissionPost(APIView):
    def post(self, request):
        serializer = PermissionSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionDelete(APIView):
    
    def get(self, request, pk):
        permission = Permission.objects.filter(perm_id=pk)
        serializer = PermissionSerializers(permission, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        permission = Permission.objects.filter(perm_id=pk)
        permission.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class PermissionUpdate(APIView):
    def get_object(self, pk):
        try:
            return Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        permission = self.get_object(pk)
        serializer = PermissionSerializers(permission)
        return Response(serializer.data)

    def patch(self, request, pk):
        permission = self.get_object(pk)
        serializer = PermissionSerializers(
           permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#Office Views
class  Offices(APIView):
    def get(self, request, format=None):
        office = Office.objects.all()
        serializer = OfficeSerializers(office, many=True).data
        return Response(serializer)
    

class OfficePost(APIView):
    def post(self, request):
        serializer = OfficeSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfficeDelete(APIView):
    
    def get(self, request, pk):
        office = Office.objects.filter(office_id=pk)
        serializer = OfficeSerializers(office, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        office = Office.objects.filter(office_id=pk)
        office.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class OfficeUpdate(APIView):
    def get_object(self, pk):
        try:
            return Office.objects.get(pk=pk)
        except Office.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        office = self.get_object(pk)
        serializer = OfficeSerializers(office)
        return Response(serializer.data)

    def patch(self, request, pk):
        office = self.get_object(pk)
        serializer = OfficeSerializers(
           office, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#Jobworkflow Views
class  Jobworkflows(APIView):
    def get(self, request, format=None):
        # jobworkflow=Jobworkflow.objects.select_related('workflow')
        jobworkflow = Jobworkflow.objects.all()
        serializer = JobworkflowSerializers(jobworkflow, many=True).data
        return Response(serializer)
    

class JobworkflowPost(APIView):
    def post(self, request):
        serializer = JobworkflowSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JobworkflowDelete(APIView):

    def get(self, request, pk):
        jobworkflow = Jobworkflow.objects.filter(workflow_id=pk)
        serializer = JobworkflowSerializers(jobworkflow, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        jobworkflow = Jobworkflow.objects.filter(workflow_id=pk)
        jobworkflow.delete()
        return Response("content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class JobworkflowUpdate(APIView):
    def get_object(self, pk):
        try:
            return Jobworkflow.objects.get(pk=pk)
        except Jobworkflow.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobworkflow = self.get_object(pk)
        serializer = JobworkflowSerializers(jobworkflow)
        return Response(serializer.data)

    def patch(self, request, pk):
        jobworkflow = self.get_object(pk)
        serializer = JobworkflowSerializers(
           jobworkflow, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#following views were written by tsitsi

########################
#JOBTEAM
########################

class JobTeam(APIView):
    def get(self, request, pk):
        jobteam = Jobteam.objects.filter(pk=pk)
        serializer = JobteamSerializers(jobteam, many=True).data
        return Response(serializer)


class SpecificJobTeam(APIView):
    def get(self, request,job_progress):
        jobteam = Jobteam.objects.filter(job_progress=job_progress)
        serializer = JobteamSerializers(jobteam, many=True).data
        return Response(serializer)


class JobteamGet(APIView):
    def get(self, request, format=None):
        jobteam = Jobteam.objects.all()
        serializer = JobteamSerializers(jobteam, many=True).data
        return Response(serializer)


class JobteamPost(APIView):
    def post(self, request):
        serializer = JobteamSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobteamDelete(APIView):

    def get_object(self, pk):
        try:
            return Jobteam.objects.get(pk=pk)
        except Jobteam.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobteam = self.get_object(pk)
        serializer = JobteamSerializers(jobteam, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        jobteam = self.get_object(pk)
        jobteam.delete()
        return Response('content deleted successfully', status=status.HTTP_204_NO_CONTENT)


class JobteamUpdate(APIView):

    def get_object(self, pk):
        try:
            return Jobteam.objects.get(pk=pk)
        except Jobteam.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobteam = self.get_object(pk)
        serializer = JobteamSerializers([jobteam], many=True).data
        return Response(serializer)

    def patch(self,request,pk):
        if 'sync_status' in request.data:
            if request.data['sync_status'] is not None and request.data['sync_status'] !='':           
                sync_status = request.data['sync_status']
        else:
            sync_status=0 
        jobteam = self.get_object(pk)
        serializer = JobteamSerializers(
            jobteam, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save(sync_status=sync_status)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#######################
#JOBSYNC
#######################


class Jobsync(APIView):
    def get(self, request, pk):
        jobsync = Jobsync.objects.filter(pk=pk)
        serializer = JobsyncSerializers(jobsync, many=True).data
        return Response(serializer)


class JobsyncGet(APIView):
    def get(self, request, format=None):
        jobsync = Jobsync.objects.all()
        serializer = JobsyncSerializers(jobsync, many=True).data
        return Response(serializer)


class JobsyncPost(APIView):
    def post(self, request):
        serializer = JobsyncSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobsyncDelete(APIView):

    def get_object(self, pk):
        try:
            return Jobsync.objects.get(pk=pk)
        except Jobsync.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobsync = self.get_object(pk)
        serializer = JobsyncSerializers(jobsync, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        jobsync = self.get_object(pk)
        jobsync.delete()
        return Response('content deleted successfully', status=status.HTTP_204_NO_CONTENT)


class JobsyncUpdate(APIView):

    def get_object(self, pk):
        try:
            return Jobsync.objects.get(pk=pk)
        except Jobsync.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobsync = self.get_object(pk)
        serializer = JobsyncSerializers(jobsync, many=True).data
        return Response(serializer)

    def patch(self, pk, request):
        jobsync = self.get_object(pk)
        serializer = JobsyncSerializers(
            jobsync, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

####################
#JOBPROGRESS
####################

class SingleJobProgress(APIView):

    '''
    Returns job progress details for a single job
    ''' 
    def get(self, request, job_id):        
        jobprogress = Jobprogress.objects.filter(job_id=job_id)           
        serializer = JobprogressSerializers(jobprogress, many=True).data
        return Response(serializer)

class JobProgress(APIView):
    def get(self, request, pk):
        jobprogress = Jobprogress.objects.filter(pk=pk).prefetch_related('job')
        serializer = JobprogressSerializers(jobprogress, many=True).data
        return Response(serializer)


class JobProgress(APIView):
    def get(self, request, pk):
        jobprogress = Jobprogress.objects.filter(pk=pk)
        serializer = JobprogressSerializers(jobprogress, many=True).data
        return Response(serializer)

class JobprogressGet(APIView):
    def get(self, request, format=None):
        jobprogress = Jobprogress.objects.all()
        serializer = JobprogressSerializers(jobprogress, many=True).data
        return Response(serializer)


class JobprogressPost(APIView):
    def post(self, request):
        serializer = JobprogressSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobprogressDelete(APIView):

    def get_object(self, pk):
        try:
            return Jobprogress.objects.get(pk=pk)
        except Jobprogress.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobprogress = self.get_object(pk)
        serializer = JobprogressSerializers(jobprogress, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        jobprogress = self.get_object(pk)
        jobprogress.delete()
        return Response('content deleted successfully', status=status.HTTP_204_NO_CONTENT)


class JobprogressUpdate(APIView):

    def get_object(self, pk):
        try:
            return Jobprogress.objects.get(pk=pk)
        except Jobprogress.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobprogress = self.get_object(pk)
        serializer = JobprogressUpdateSerializer([jobprogress], many=True).data
        return Response(serializer)

    def patch(self,request,pk):
        if 'sync_status' in request.data:
            if request.data['sync_status'] is not None and request.data['sync_status'] !='':           
                sync_status = request.data['sync_status']
        else:
            sync_status=0 
        jobprogress = self.get_object(pk)
        serializer = JobprogressUpdateSerializer(
            jobprogress, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save(sync_status=sync_status)
            return Response(serializer.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

####################
#JOBATTACHMENT
####################


class Jobattachment(APIView):
    def get(self, request, pk):
        jobattach = Jobattachment.objects.filter(pk=pk)
        serializer = JobattachmentSerializers(jobattach, many=True).data
        return Response(serializer)

class JobattachmentGet(APIView):
    def get(self, request, format=None):
        jobattachment = Jobattachment.objects.all()
        serializer = JobattachmentSerializers(jobattachment, many=True).data
        return Response(serializer)


class JobattahmentPost(APIView):
    def post(self, request):
        serializer = JobattachmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobattachmentDelete(APIView):

    def get_object(self, pk):
        try:
            return Jobattachment.objects.get(pk=pk)
        except Jobattachment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        jobattachment = self.get_object(pk)
        serializer = JobattachmentSerializers(jobattachment, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        jobattachment = self.get_object(pk)
        jobattachment.delete()
        return Response('content deleted successfully', status=status.HTTP_204_NO_CONTENT)


class JobattachmentUpdate(APIView):

    def get_object(self, pk):
        try:
            return Jobattachment.objects.get(pk=pk)
        except Jobattachment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        jobattachment = self.get_object(pk)
        serializer = JobattachmentSerializers(jobattachment, many=True).data
        return Response(serializer)

    def patch(self,request, pk ):
        jobattachment = self.get_object(pk)
        serializer = JobattachmentSerializers(
            jobattachment, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

########################
#E84LineInspection
########################


class E84LineInspection(APIView):
    def get(self, request, pk):
        e84line = E84Lineinspection.objects.filter(pk=pk)
        serializer = E84LineinspectionSerializers(e84line, many=True).data
        return Response(serializer)
    
class E84LineinspectionGet(APIView):
    def get(self, request, format=None):
        e84line = E84Lineinspection.objects.all()
        serializer = E84LineinspectionSerializers(e84line, many=True).data
        return Response(serializer)


class E84LineinspectionPost(APIView):
    def post(self, request):
        serializer = E84LineinspectionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E84LineinspectionDelete(APIView):

    def get_object(self, pk):
        try:
            return E84Lineinspection.objects.get(pk=pk)
        except E84Lineinspection.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        e84line = self.get_object(pk)
        serializer = E84LineinspectionSerializers(e84line, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        e84line = self.get_object(pk)
        e84line.delete()
        return Response('content deleted successfully', status=status.HTTP_204_NO_CONTENT)


class E84LineinspectionUpdate(APIView):

    def get_object(self, pk):
        try:
            return E84Lineinspection.objects.get(pk=pk)
        except E84Lineinspection.DoesNotExist:
            raise Http404

    def get(self, request,pk,format=None):
        e84line = self.get_object(pk)
        serializer = E84LineinspectionSerializers([e84line], many=True).data
        return Response(serializer)

    def patch(self, request, pk):
        e84line = self.get_object(pk)
        serializer = E84LineinspectionSerializers(
            e84line, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#####################
#E84General
#####################


class E84general(APIView):
    def get(self, request, pk):
        e84general = E84General.objects.filter(pk=pk).prefetch_related('inspections')
        serializer = E84GeneralSerializers(e84general, many=True).data
        return Response(serializer)

class E84GeneralGet(APIView):
    def get(self, request, format=None):
        e84general = E84General.objects.all()
        serializer = E84GeneralSerializers(e84general, many=True).data
        return Response(serializer)


class E84GeneralPost(APIView):
    def post(self, request):
        serializer = E84GeneralSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E84GeneralDelete(APIView):

    def get_object(self, pk):
        try:
            return E84General.objects.get(pk=pk)
        except E84General.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        e84general = self.get_object(pk)
        serializer = E84GeneralSerializers(e84general, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        e84general = self.get_object(pk)
        e84general.delete()
        return Response('content deleted successfully', status=status.HTTP_204_NO_CONTENT)


class E84GeneralUpdate(APIView):

    def get_object(self, pk):
        try:
            return E84General.objects.get(pk=pk)
        except E84General.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        e84general = self.get_object(pk)
        serializer = E84GeneralSerializers([e84general], many=True).data
        return Response(serializer)

    def patch(self, request, pk):
        e84general = self.get_object(pk)
        serializer = E84GeneralSerializers(
            e84general, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#####################
#E60
#####################
class E60s(APIView):
    def get(self, request, pk):
        e60s = E60.objects.filter(pk=pk)
        serializer = E60Serializer(e60s, many=True).data
        return Response(serializer)
    
class E60sGet(APIView):
    def get(self, request, format=None):
        e60s = E60.objects.all()
        serializer = E60Serializer(e60s, many=True).data
        return Response(serializer)


class E60Post(APIView):
    def post(self, request):
        serializer = E60Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E60Delete(APIView):

    def get(self, request, pk):
        '''
        Returns details of a single E60 the specified id
        '''
        e60s = E60.objects.filter(e60_id=pk)
        serializer = E60Serializer(e60s, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E60 with the specified id
        '''
        e60s = E60.objects.filter(e60_id=pk)
        e60s.delete()
        return Response("E60 deleted successfully", status=status.HTTP_204_NO_CONTENT)


class E60Update(APIView):

    def get_object(self, pk):
        try:
            return E60.objects.get(pk=pk)
        except E60.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60 with the specified id
        '''
        e60s = self.get_object(pk)
        serializer = E60Serializer(e60s)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E60 with the specified id
        '''
        e60s = self.get_object(pk)
        serializer = E60Serializer(
            e60s, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#####################
#E60TRANSFORMER
####################
class E60TransformersByE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all E60Transformers for a particular e60 form with the specified id
        '''
        e60transformer= E60Transformer.objects.filter(e60_id=e60_id)
        serializer = E60TransformerSerializers( e60transformer, many=True).data
        return Response(serializer)


class E60Transformers(APIView):
    def get(self, request, pk):
        e60transformer = E60Transformer.objects.filter(pk=pk)
        serializer = E60TransformerSerializers(e60transformer, many=True).data
        return Response(serializer)


class E60TransformerGet(APIView):
    def get(self, request, format=None):
        e60transformer = E60Transformer.objects.all()
        serializer = E60TransformerSerializers(e60transformer, many=True).data
        return Response(serializer)



class E60TransformerPost(APIView):
    def post(self, request):
        serializer = E60TransformerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E60TransformerDelete(APIView):

    def get(self, request, pk):
        '''
        Returns details of a single E60transformer the specified id
        '''
        e60transformer = E60Transformer.objects.filter(e60transformer_id=pk)
        serializer = E60TransformerSerializers(e60transformer, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E60 with the specified id
        '''
        e60transformer = E60Transformer.objects.filter(e60transformer_id=pk)
        e60transformer.delete()
        return Response("E60transformer deleted successfully", status=status.HTTP_204_NO_CONTENT)


class E60TransformerUpdate(APIView):
    def get_object(self, pk):
        try:
            return E60Transformer.objects.get(pk=pk)
        except E60Transformer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60transformer with the specified id
        '''
        e60transformer = self.get_object(pk)
        serializer = E60TransformerSerializers(e60transformer)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E60transformer with the specified id
        '''
        e60transformer = self.get_object(pk)
        serializer = E60TransformerSerializers(
            e60transformer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#########################
#E60SWITCHGEAR
#########################
class E60SwitchgearByE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all E60Switchgear for a particular e60 form with the specified id
        '''
        e60switch= E60Switchgear.objects.filter(e60_id=e60_id)
        serializer = E60SwitchgearSerializers( e60switch, many=True).data
        return Response(serializer)

class E60Switchgears(APIView):
    def get(self, request, pk):
        e60switch = E60Switchgear.objects.filter(pk=pk)
        serializer = E60SwitchgearSerializers(e60switch, many=True).data
        return Response(serializer)
    
class E60SwitchgearGet(APIView):
    def get(self, request, format=None):
        e60switch = E60Switchgear.objects.all()
        serializer = E60SwitchgearSerializers(e60switch, many=True).data
        return Response(serializer)


class E60SwitchgearPost(APIView):
    def post(self, request):
        serializer = E60SwitchgearSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E60SwitchgearDelete(APIView):

    def get(self, request, pk):
        '''
        Returns details of a single E60switch the specified id
        '''
        e60switchdel = E60Switchgear.objects.filter(e60switchgear_id=pk)
        serializer = E60SwitchgearSerializers(e60switchdel, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50 with the specified id
        '''
        e60switchdel = E60Switchgear.objects.filter(e60switchgear_id=pk)
        e60switchdel.delete()
        return Response("E50 deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E60SwitchgearUpdate(APIView):

    def get_object(self, pk):
        try:
            return E60Switchgear.objects.get(pk=pk)
        except E60Switchgear.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50 with the specified id
        '''
        eswitchupd = self.get_object(pk)
        serializer = E60SwitchgearSerializers(eswitchupd)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50 with the specified id
        '''
        eswitchupd = self.get_object(pk)
        serializer = E60SwitchgearSerializers(
            eswitchupd, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#######################
#E60SUBSTATIONGENERAL
#######################
class E60SubstationgeneralE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all E60Switchgear for a particular e60 form with the specified id
        '''
        e60substation= E60Subgeneral.objects.filter(e60_id=e60_id)
        serializer = E60SubgeneralSerializer( e60substation, many=True).data
        return Response(serializer)
        
class E60Substationgenerals(APIView):
    def get(self, request, pk):
        e60substation = E60Subgeneral.objects.filter(pk=pk)
        serializer = E60SubgeneralSerializer(e60substation, many=True).data
        return Response(serializer)
    
class E60SubstationgeneralGet(APIView):
    def get(self, request, format=None):
        e60substation = E60Subgeneral.objects.all()
        serializer = E60SubgeneralSerializer(
            e60substation, many=True).data
        return Response(serializer)


class E60SubstationgeneralPost(APIView):
    def post(self, request):
        serializer = E60SubgeneralSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E60SubstationgeneralDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E60sub general with the specified id
        '''
        e60substationdel = E60Subgeneral.objects.filter(e60subgeneral_id=pk)
        serializer = E60SubgeneralSerializer(e60substationdel, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E60sub general with the specified id
        '''
        e60substation = E60Subgeneral.objects.filter(e60subgeneral_id=pk)
        e60substation.delete()
        return Response("E60sub general deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E60SubstationgeneralUpdate(APIView):

    def get_object(self, pk):
        try:
            return E60Subgeneral.objects.get(pk=pk)
        except E60Subgeneral.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60subgen with the specified id
        '''
        e60substation = self.get_object(pk)
        serializer = E60SubgeneralSerializer(e60substation)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E60subgen with the specified id
        '''
        e60substation = self.get_object(pk)
        serializer = E60SubgeneralSerializer(
            e60substation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#####################################
#E60Safety
#####################################
class E60SafetysE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all e60safety for a particular e60 form with the specified id
        '''
        e60safety= E60Safety.objects.filter(e60_id=e60_id)
        serializer = E60SafetySerializers( e60safety, many=True).data
        return Response(serializer)
class E60Safetys(APIView):
    def get(self,request,pk):
        e60safety = E60Safety.objects.filter(pk=pk)
        serializer = E60SafetySerializers(e60safety,many=True).data
        return Response (serializer)

class E60SafetyGet(APIView):
    def get(self, request, format=None):
        e60safety = E60Safety.objects.all()
        serializer = E60SafetySerializers(
            e60safety, many=True).data
        return Response(serializer)

class E60SafetyPost(APIView):
    def post(self, request):
        serializer = E60SafetySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E60SafetyDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E60Safety with the specified id
        '''
        e60safety = E60Safety.objects.filter(e60safety_id=pk)
        serializer = E60SafetySerializers(e60safety, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E60Safety with the specified id
        '''
        e60safety = E60Safety.objects.filter(e60safety_id=pk)
        e60safety.delete()
        return Response(" E60Safety deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E60SafetyUpdate(APIView):

    def get_object(self, pk):
        try:
            return E60Safety.objects.get(pk=pk)
        except E60Safety.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60Safety with the specified id
        '''
        e60safety = self.get_object(pk)
        serializer = E60SafetySerializers(e60safety)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E60Safety with the specified id
        '''
        e60safety = self.get_object(pk)
        serializer = E60SafetySerializers(
            e60safety, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

######################################
#E60HOUSING
######################################
class E60HousingE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all e60housing for a particular e60 form with the specified id
        '''
        e60housing= E60Housing.objects.filter(e60_id=e60_id)
        serializer = E60HousingSerializers( e60housing, many=True).data
        return Response(serializer)
class E60Housings(APIView):
    def get(self, request, pk):
        e60housing = E60Housing.objects.filter(pk=pk)
        serializer = E60HousingSerializers(e60housing, many=True).data
        return Response(serializer)
    
class E60HousingGet(APIView):
    def get(self, request, format=None):
        e60housing = E60Housing.objects.all()
        serializer = E60HousingSerializers(
            e60housing, many=True).data
        return Response(serializer)


class E60HousingsPost(APIView):
    def post(self, request):
        serializer = E60HousingSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E60HousingDelete(APIView):

    def get(self, request, pk):
        '''
        Returns details of a single E60Housing with the specified id
        '''
        e60housing = E60Housing.objects.filter(e60housing_id=pk)
        serializer = E60HousingSerializers(e60housing, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E60Housing with the specified id
        '''
        e60housing = E60Housing.objects.filter(e60housing_id=pk)
        e60housing.delete()
        return Response(" E60Housing deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E60HousingUpdate(APIView):

    def get_object(self, pk):
        try:
            return E60Housing.objects.get(pk=pk)
        except E60Housing.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60Housing with the specified id
        '''
        e60housing = self.get_object(pk)
        serializer = E60HousingSerializers(e60housing)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E60Housing with the specified id
        '''
        e60housing = self.get_object(pk)
        serializer = E60HousingSerializers(
            e60housing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
######################################
#E60LtLighting Arrestors
######################################
class E60LtlightningarresterByE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all lighting arrestors  for a particular e60 form with the specified id
        '''
        e60Ltlightningarrester= E60Ltlightningarrester.objects.filter(e60_id=e60_id)
        serializer = E60LtlightningarresterSerializer( e60Ltlightningarrester, many=True).data
        return Response(serializer)

class E60LtLightingArrestorGet(APIView):
    def get(self, request, pk):
        e60ltlightingarrestor = E60Ltlightningarrester.objects.filter(pk=pk)
        serializer = E60LtlightningarresterSerializer(e60ltlightingarrestor, many=True).data
        return Response(serializer)
    
class E60LtLightingArrestors(APIView):
    def get(self, request, format=None):
        e60ltlightingarrestor = E60Ltlightningarrester.objects.all()
        serializer = E60LtlightningarresterSerializer(
            e60ltlightingarrestor, many=True).data
        return Response(serializer)


class E60LtlightningarresterPost(APIView):
    def post(self, request):
        serializer = E60LtlightningarresterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class E60LtlightningarresterDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E60 LTLighting with the specified id
        '''
        e60ltlightingarrestor = E60Ltlightningarrester.objects.filter(e60ltlightningarrester_id=pk)
        serializer = E60LtlightningarresterSerializer(e60ltlightingarrestor, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E60 LTLighting with the specified id
        '''
        e60ltlightingarrestor = E60Ltlightningarrester.objects.filter(e60ltlightningarrester_id=pk)
        e60ltlightingarrestor.delete()
        return Response("E60 LTLighting deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E60LtlightningarresterUpdate(APIView):

    def get_object(self, pk):
        try:
            return E60Ltlightningarrester.objects.get(pk=pk)
        except E60Ltlightningarrester.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60 LTLighting with the specified id
        '''
        e60ltlightingarrestor = self.get_object(pk)
        serializer = E60LtlightningarresterSerializer(e60ltlightingarrestor)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E60 LTLighting with the specified id
        '''
        e60ltlightingarrestor = self.get_object(pk)
        serializer = E60LtlightningarresterSerializer(
            e60ltlightingarrestor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


######################################
#E60HtLighting Arrestors
######################################
class E60HtlightningarresterByE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all Htlighting arrestors for a particular e60 form with the specified id
        '''
        e60Htlightningarrester= E60Htlightningarrester.objects.filter(e60_id=e60_id)
        serializer = E60HtlightningarresterSerializers( e60Htlightningarrester, many=True).data
        return Response(serializer)

class e60HtlightningarresterGet(APIView):
    def get(self, request, pk):
        e60Htlightningarrester = E60Htlightningarrester.objects.filter(pk=pk)
        serializer = E60HtlightningarresterSerializers(e60Htlightningarrester, many=True).data
        return Response(serializer)
    
class e60Htlightningarresters(APIView):
    def get(self, request, format=None):
        e60Htlightningarrester = E60Htlightningarrester.objects.all()
        serializer = E60HtlightningarresterSerializers(
            e60Htlightningarrester, many=True).data
        return Response(serializer)


class e60HtlightningarresterPost(APIView):
    def post(self, request):
        serializer = E60HtlightningarresterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class e60HtlightningarresterDelete(APIView):

    def get(self, request, pk):
        '''
        Returns details of a single E60HTlighting with the specified id
        '''
        e60Htlightningarrester = E60Htlightningarrester.objects.filter(e60htlightningarrester_id=pk)
        serializer = E60HtlightningarresterSerializers(e60Htlightningarrester, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E60HTlighting with the specified id
        '''
        e60Htlightningarrester = E60Htlightningarrester.objects.filter(e60htlightningarrester_id=pk)
        e60Htlightningarrester.delete()
        return Response(" E60HTlighting deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E60HtlightningarresterUpdate(APIView):

    def get_object(self, pk):
        try:
            return E60Htlightningarrester.objects.get(pk=pk)
        except E60Htlightningarrester.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60metering with the specified id
        '''
        e60Htlightningarrester = self.get_object(pk)
        serializer = E60HtlightningarresterSerializers(e60Htlightningarrester)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50 with the specified id
        '''
        e60Htlightningarrester = self.get_object(pk)
        serializer = E60HtlightningarresterSerializers(
            e60Htlightningarrester, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

######################################
#E60METERING
######################################
class E60MeteringE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all Htlighting arrestors for a particular e60 form with the specified id
        '''
        e60metering= E60Metering.objects.filter(e60_id=e60_id)
        serializer = E60MeteringSerializers( e60metering, many=True).data
        return Response(serializer)

class E60Meterings(APIView):
    def get(self, request, pk):
        e60meterswitch = E60Metering.objects.filter(pk=pk)
        serializer = E60MeteringSerializers(e60meterswitch, many=True).data
        return Response(serializer)
    
class E60MeteringGet(APIView):
    def get(self, request, format=None):
        e60meterswitch = E60Metering.objects.all()
        serializer = E60MeteringSerializers(
            e60meterswitch, many=True).data
        return Response(serializer)


class E60MeteringPost(APIView):
    def post(self, request):
        serializer = E60MeteringSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E60MeteringDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E60 Metering with the specified id
        '''
        e60meteringdel = E60Metering.objects.filter(e60metering_id=pk)
        serializer = E60MeteringSerializers(e60meteringdel, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50 with the specified id
        '''
        e60meteringdel = E60Metering.objects.filter(e60metering_id=pk)
        e60meteringdel.delete()
        return Response(" E60 Metering deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E60MeteringUpdate(APIView):

    def get_object(self, pk):
        try:
            return E60Metering.objects.get(pk=pk)
        except E60Metering.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E60metering with the specified id
        '''
        e60meteringup = self.get_object(pk)
        serializer = E60MeteringSerializers(e60meteringup)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50 with the specified id
        '''
        e60meteringup = self.get_object(pk)
        serializer = E60MeteringSerializers(
            e60meteringup, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class E60sByJobId(APIView):
    def get(self, request, job):
        '''
        Returns details of a single E50 with the specified id
        '''
        e60 = E60.objects.filter(job=job)        
        serializer = E60Serializer(e60, many=True).data
        return Response(serializer)

###############################################################################################################################################

# Job Status Views

class SingleJobStatus(APIView):

    '''
    Returns job status details for a single job
    ''' 
    def get(self, request, status):        
        jobstatus = JobStatus.objects.filter(job_status_id=status)           
        serializer = JobStatusSerializer(jobstatus, many=True).data
        return Response(serializer)
 
class JobStatusGet(APIView):
    def get(self,request):
        status = JobStatus.objects.all()
        data = JobStatusSerializer(status,many=True).data
        return Response(data)
class JobStatusPost(APIView):
    def post(self,request):
        serializer = JobStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobstatusDelete(APIView):
    def get(self,request,pk):
        jobStatus = JobStatus.objects.filter(job_status_id=pk)
        serializer = JobStatusSerializer(jobStatus,many=True).data
        return Response(serializer)
 
    def delete(self, request, pk):
        jobStatus = JobStatus.objects.filter(job_status_id=pk)
        jobStatus.delete()
        return Response("Content deleted successfully", status=status.HTTP_204_NO_CONTENT)


class JobstatusModify(APIView):
    def get_object(self, pk):
        try:
            return JobStatus.objects.get(pk=pk)
        except JobStatus.DoesNotExist:
            raise Http404
 
    def get(self, request, pk, format=None):
        jobStatus = self.get_object(pk)
        serializer = JobStatusSerializer(jobStatus)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        jobstatusModify = self.get_object(pk)
        serializer = JobStatusSerializer(
            jobstatusModify, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class JobStatusUpdate(APIView):
    def get_object(self, pk):
        try:
            return JobStatus.objects.get(pk=pk)
        except JobStatus.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        jobStatus = self.get_object(pk)
        serializer = JobStatusSerializer(jobStatus)
        return Response(serializer.data)
    def patch(self, request, pk):
        jobStatusUpdate = self.get_object(pk)
        serializer = JobStatusSerializer(
            jobStatusUpdate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
# Job Type View
class SingleJobType(APIView):

    '''
    Returns job type details for a single job
    ''' 
    def get(self, request, type):        
        jobtype = JobType.objects.filter(job_type_id=type)           
        serializer = JobTypeSerializer(jobtype, many=True).data
        return Response(serializer)


class JobTypeGet(APIView):
    def get(self,request):
        j_type = JobType.objects.all()
        data = JobTypeSerializer(j_type,many=True).data
        return Response(data)
 
class JobTypePost(APIView):
    def post(self,request):
        serializer = JobTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class JobTypeDelete(APIView):
    def get(self,request,pk):
        jobType = JobType.objects.filter(job_type_id=pk)
        serializer = JobTypeSerializer(jobType,many=True).data
        return Response(serializer)
 
    def delete(self, request, pk):
        jobtype = JobType.objects.filter(job_type_id=pk)
        jobtype.delete()
        return Response("Content deleted successfully", status=status.HTTP_204_NO_CONTENT)
 
class JobTypeModify(APIView):
    def get_object(self, pk):
        try:
            return JobType.objects.get(pk=pk)
        except JobType.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        jobType = self.get_object(pk)
        serializer = JobTypeSerializer(jobType)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        jobtypeModify = self.get_object(pk)
        serializer = JobTypeSerializer(
            jobtypeModify, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class JobTypeUpdate(APIView):
    def get_object(self, pk):
        try:
            return JobType.objects.get(pk=pk)
        except JobType.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        jobtype = self.get_object(pk)
        serializer = JobTypeSerializer(jobtype)
        return Response(serializer.data)
    def patch(self, request, pk):
        jobtypeUpdate = self.get_object(pk)
        serializer = JobTypeSerializer(
            jobtypeUpdate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Centres Views
class CentreGet(APIView):
    def get(self,request):
        j_centre=Centre.objects.all()
        data = CentreSerializer(j_centre,many=True).data
        return Response(data)

class CentreByCentreId(APIView):
    def get(self, request, pk):
        '''
        Returns centre details for a particular centre with the centre id
        '''
        centre = Centre.objects.filter(pk=pk)
        serializer = CentreSerializer( centre, many=True).data
        return Response(serializer)

class CentrePost(APIView):
    def post(self,request):
        serializer = CentreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CentreDelete(APIView):
    def get(self,request,pk):
        centre = Centre.objects.filter(centre_id=pk)
        serializer = CentreSerializer(centre,many=True).data
        return Response(serializer)
    def delete(self, request, pk):
        centre = Centre.objects.filter(centre_id=pk)
        centre.delete()
        return Response("Content deleted successfully", status=status.HTTP_204_NO_CONTENT)
 
class CentreModify(APIView):
    def get_object(self, pk):
        try:
            return Centre.objects.get(pk=pk)
        except Centre.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        centre = self.get_object(pk)
        serializer = CentreSerializer(centre)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        centremodify = self.get_object(pk)
        serializer = CentreSerializer(
            centremodify, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
 
class CentreUpdate(APIView):
    def get_object(self, pk):
        try:
            return Centre.objects.get(pk=pk)
        except Centre.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        centre = self.get_object(pk)
        serializer = CentreSerializer(centre)
        return Response(serializer.data)
    def patch(self, request, pk):
        centreUpdate = self.get_object(pk)
        serializer = CentreSerializer(
            centreUpdate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


 # PROFILE
class ProfileGet(APIView):
    
    def get_object(self,pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns a single profile. User should specify the id.
        '''
        profile = self.get_object(pk)
        serializer = ProfileSerializer([profile], many=True).data
        return Response(serializer)   

class Profiles(APIView):
    def get(self, request, format=None):
        profiles = Profile.objects.prefetch_related().all()
        serializer=ProfileSerializer(profiles,many=True).data
        return Response(serializer)

class ProfileCreate(APIView):
    '''
    Enables the creation of a profile
    '''
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDelete(APIView):    
    
    def get(self, request, pk):

        '''
        Returns details of the profile with the specified id
        '''
        profile = Profile.objects.filter(profile_code=pk)
        serializer = ProfileSerializer(profile, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes profile with the specified id
        '''
        profile = Profile.objects.filter(profile_code=pk)
        profile.delete()
        return Response("Profile deleted successfully", status=status.HTTP_204_NO_CONTENT)


class ProfileUpdate(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of the profile with the specified id
        '''
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


    def patch(self, request, pk):

        '''
        Updates a profile with the specified id
        '''
           
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(status=status)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
 # ROLE PROFILE


class RoleProfileGet(APIView):
    
    def get_object(self,pk):
        try:
            return Roleprofile.objects.get(pk=pk)
        except Roleprofile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns a single role profile. User should specify the id.
        '''
        roleprofile = self.get_object(pk)
        serializer = RoleProfileSerializer([roleprofile], many=True).data
        return Response(serializer)   



class RoleProfiles(APIView):

    '''
    Returns a list of all role profiles created in the system
    '''
    def get(self, request, format=None):
        roleprofiles = Roleprofile.objects.all()
        serializer = RoleProfileSerializer(roleprofiles, many=True).data
        return Response(serializer)

class RoleProfileCreate(APIView):
    '''
    Enables the creation of a role profile
    '''
    def post(self, request):
        serializer = RoleProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleProfileDelete(APIView):    
    
    def get(self, request, pk):

        '''
        Returns details of the role profile with the specified id
        '''
        roleprofile = Roleprofile.objects.filter(profile_code=pk)
        serializer = RoleProfileSerializer(roleprofile, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes role profile with the specified id
        '''
        roleprofile = Roleprofile.objects.filter(profile_code=pk)
        roleprofile.delete()
        return Response("Role Profile deleted successfully", status=status.HTTP_204_NO_CONTENT)


class RoleProfileUpdate(APIView):
    def get_object(self, pk):
        try:
            return Roleprofile.objects.get(pk=pk)
        except Roleprofile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of the role profile with the specified id
        '''
        roleprofile = self.get_object(pk)
        serializer = RoleProfileSerializer(roleprofile)
        return Response(serializer.data)


    def patch(self, request, pk):

        '''
        Updates a role profile with the specified id
        '''
           
        roleprofile = self.get_object(pk)
        serializer = RoleProfileSerializer(
            roleprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(status=status)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 # USER PROFILE


class UserProfileGet(APIView):
    
    def get_object(self,pk):
        try:
            return Userprofile.objects.get(pk=pk)
        except Userprofile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns a single user profile. User should specify the id.
        '''
        userprofile = self.get_object(pk)
        serializer = UserProfileSerializer([userprofile], many=True).data
        return Response(serializer)   



class UserProfiles(APIView):

    '''
    Returns a list of all user profiles created in the system
    '''
    def get(self, request, format=None):
        roleprofiles = Roleprofile.objects.all()
        serializer = RoleProfileSerializer(roleprofiles, many=True).data
        return Response(serializer)

class UserProfileCreate(APIView):
    '''
    Enables the creation of a user profile
    '''
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDelete(APIView):    
    
    def get(self, request, pk):

        '''
        Returns details of the user profile with the specified id
        '''
        userprofile = Userprofile.objects.filter(username=pk)
        serializer = UserProfileSerializer(userprofile, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes user profile with the specified id
        '''
        userprofile = Userprofile.objects.filter(username=pk)
        userprofile.delete()
        return Response("Role Profile deleted successfully", status=status.HTTP_204_NO_CONTENT)


class UserProfileUpdate(APIView):
    def get_object(self, pk):
        try:
            return Userprofile.objects.get(pk=pk)
        except Userprofile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of the user profile with the specified id
        '''
        userprofile = self.get_object(pk)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)


    def patch(self, request, pk):

        '''
        Updates a role profile with the specified id
        '''
           
        userprofile = self.get_object(pk)
        serializer = UserProfileSerializer(
            userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(status=status)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobsWorkflowStatus(APIView):

    """
    
    Arguments:
        [job_id]
    
    Returns:
        Job workflow status data
    """
    def get(self, request,pk):
        jobs = Job.objects.job_workflow_status(pk=pk)
        return Response(jobs)



class JobsAwaitingActionProcedure(APIView):

    '''
    Returns a list of  jobs awaiting action in the system
    '''
    def get(self, request, ec_num):
        jobs = Jobworkflow.objects.job_awaiting_action_procedure(ec_num=ec_num)
        return Response(jobs)

class JobWorkflowProcedure(APIView):

    '''
    Arguments:
        [job_id]
    Returns:
        Workflow for the specified job
    '''
    def get(self, request, job_id):
        jobs = Jobworkflow.objects.job_workflow_procedure(job_id=job_id)
        return Response(jobs)

class ParentCentres(APIView):
    '''
    Arguments:
        [centreparent]
    Returns:
        All centres based on the given values(Parent centre)
    '''

    def get(self, request,centreparent):
        centres = Job.objects.all_parentcentres(centreparent)
        return Response(centres)

class JobsViewProcedure(APIView):
    '''
    Arguments:
        [username,section]
    Returns:
        Job id and Workorder id for the specified user
    '''
    def get(self, request, username,section,status):
        jobs = Job.objects.jobs_view_procedure(username=username,section=section,status=status)
        return Response(jobs)




#E117
class E117Get(APIView):  

    def get_object(self, pk):
        try:
            return E117.objects.get(pk=pk)
        except E117.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single E117 with the specified id
        '''
        e117 = self.get_object(pk)
        serializer = E117Serializer([e117], many=True).data
        return Response(serializer)

class E117Inspection(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E117 records in the system
        '''
        e117 = E117.objects.select_related('e117client','job','client_contractor')  
        serializer = E117Serializer(e117, many=True).data
        return Response(serializer)

class E117Create(APIView):
    def post(self, request):
        '''
        Enables the creation of a e117
        '''
        serializer = E117Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E117Delete(APIView):
    def get_object(self, pk):
        try:
            return E117.objects.get(pk=pk)
        except E117.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single e117 with the specified id
        '''
        e117 = self.get_object(pk)
        serializer = E117Serializer([e117], many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes an e117 record with the specified id
        '''
        e117 = self.get_object(pk)
        e117.delete()
        return Response("E117 deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E117Update(APIView):
    def get_object(self, pk):
        try:
            return E117.objects.get(pk=pk)
        except E117.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single e117 with the specified id
        '''
        e117 = self.get_object(pk)
        serializer = E117Serializer(e117)
        return Response(serializer.data)

    def patch(self, request, pk):

        '''
        Updates details of an e117 with the specified id
        '''
        e117 = self.get_object(pk)
        serializer = E117Serializer(
            e117, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#E117 Equipment

class E117EquipmentGet(APIView):  

    def get_object(self, pk):
        try:
            return E117Equipment.objects.get(pk=pk)
        except E117Equipment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single E117Equipment with the specified id
        '''
        e117equipment = self.get_object(pk)
        serializer = E117EquipmentSerializer([e117equipment], many=True).data
        return Response(serializer)

class E117EquipmentInspection(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E117Equipment records in the system
        '''
        e117equipment = E117Equipment.objects.all()
        serializer = E117EquipmentSerializer(e117equipment, many=True).data
        return Response(serializer)

class E117EquipmentCreate(APIView):
    def post(self, request):
        '''
        Enables the creation of a e117equipment
        '''
        serializer = E117EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E117EquipmentDelete(APIView):
    def get_object(self, pk):
        try:
            return E117Equipment.objects.get(pk=pk)
        except E117Equipment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single e117equipment with the specified id
        '''
        e117equipment = self.get_object(pk)
        serializer = E117EquipmentSerializer([e117equipment], many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes an e117equipment record with the specified id
        '''
        e117equipment = self.get_object(pk)
        e117equipment.delete()
        return Response("E117Equipment deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E117EquipmentUpdate(APIView):
    def get_object(self, pk):
        try:
            return E117Equipment.objects.get(pk=pk)
        except E117Equipment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single e117equipment with the specified id
        '''
        e117equipment = self.get_object(pk)
        serializer = E117EquipmentSerializer(e117equipment)
        return Response(serializer.data)

    def patch(self, request, pk):

        '''
        Updates details of an e117equipment with the specified id
        '''
        e117equipment = self.get_object(pk)
        serializer = E117EquipmentSerializer(
            e117equipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstallationInspectionForJob(APIView):
    def get(self, request, job_id):
        '''
        Returns details of a single E117 with the specified id
        '''
        e117 = E117.objects.get(job=job_id)
        serializer = E117Serializer([e117], many=True).data
        return Response(serializer)


#E117 Contractor

class E117ContractorGet(APIView):  

    def get_object(self, pk):
        try:
            return E117Contractor.objects.get(pk=pk)
        except E117Contractor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single E117Contractor with the specified id
        '''
        e117contractor = self.get_object(pk)
        serializer = E117ContractorSerializer([e117contractor], many=True).data
        return Response(serializer)

class E117Contractors(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E117Contractor records in the system
        '''
        e117contractor = E117Contractor.objects.all()
        serializer = E117ContractorSerializer(e117contractor, many=True).data
        return Response(serializer)

class E117ContractorCreate(APIView):
    def post(self, request):
        '''
        Enables the creation of a e117contractor
        '''
        serializer = E117ContractorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E117ContractorDelete(APIView):
    def get_object(self, pk):
        try:
            return E117Contractor.objects.get(pk=pk)
        except E117Contractor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single e117contractor with the specified id
        '''
        e117contractor = self.get_object(pk)
        serializer = E117ContractorSerializer([e117contractor], many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes an e117contractor record with the specified id
        '''
        e117contractor = self.get_object(pk)
        e117contractor.delete()
        return Response("E117Contractor deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E117ContractorUpdate(APIView):
    def get_object(self, pk):
        try:
            return E117Contractor.objects.get(pk=pk)
        except E117Contractor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single e117contractor with the specified id
        '''
        e117contractor = self.get_object(pk)
        serializer = E117ContractorSerializer(e117contractor)
        return Response(serializer.data)

    def patch(self, request, pk):

        '''
        Updates details of an e117contractor with the specified id
        '''
        e117contractor = self.get_object(pk)
        serializer = E117ContractorSerializer(
            e117contractor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#E117 Reinspection

class E117ReinspectionGet(APIView):  

    def get_object(self, pk):
        try:
            return E117Reinspection.objects.get(pk=pk)
        except E117Reinspection.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single E117Reinspection with the specified id
        '''
        reinspection = self.get_object(pk)
        serializer = E117ReinspectionSerializer([reinspection], many=True).data
        return Response(serializer)

class E117Reinspections(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E117Reinspection records in the system
        '''
        reinspection = E117Reinspection.objects.all()
        serializer = E117ReinspectionSerializer(reinspection, many=True).data
        return Response(serializer)

class E117ReinspectionCreate(APIView):
    def post(self, request):
        '''
        Enables the creation of a reinspection
        '''
        serializer = E117ReinspectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E117ReinspectionDelete(APIView):
    def get_object(self, pk):
        try:
            return E117Reinspection.objects.get(pk=pk)
        except E117Reinspection.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''
        Returns details of a single reinspection with the specified id
        '''
        reinspection = self.get_object(pk)
        serializer = E117ReinspectionSerializer([reinspection], many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes an reinspection record with the specified id
        '''
        reinspection = self.get_object(pk)
        reinspection.delete()
        return Response("E117Reinspection deleted successfully", status=status.HTTP_204_NO_CONTENT)

class E117ReinspectionUpdate(APIView):
    def get_object(self, pk):
        try:
            return E117Reinspection.objects.get(pk=pk)
        except E117Reinspection.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single reinspection with the specified id
        '''
        reinspection = self.get_object(pk)
        serializer = E117ReinspectionSerializer(reinspection)
        return Response(serializer.data)

    def patch(self, request, pk):

        '''
        Updates details of an reinspection with the specified id
        '''
        reinspection = self.get_object(pk)
        serializer = E117ReinspectionSerializer(
            reinspection, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReinspectionE117(APIView):    

    def get(self, request, e117):
        '''
        Returns details of a single E117Reinspection with the specified id
        '''
        reinspection = E117Reinspection.objects.get(e117_id=e117)
        serializer = E117ReinspectionSerializer([reinspection], many=True).data
        return Response(serializer)



class E117JobsForReinspection(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E117Reinspection records in the system
        '''
        jobs = JobsForReinspectionModel.objects.all()
        serializer = JobsForReinpsectionSerializers(jobs, many=True).data
        return Response(serializer)


# 
# STATION
# 

class StationGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Station with the specified id
        '''
        station = Station.objects.filter(stationid=pk)
        serializer = StationSerializer(station, many=True).data
        return Response(serializer)

    
class Stations(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Stations in the system
        '''
        station = Station.objects.all()
        serializer = StationSerializer(station, many=True).data
        return Response(serializer)



class StationCreate(APIView):
    def post(self, request):
        '''
        Creates a single Station record
        '''
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StationDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Station with the specified id
        '''
        station = Station.objects.filter(stationid=pk)
        serializer = StationSerializer(station, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single station with the specified id
        '''
        station = Station.objects.filter(stationid=pk)
        station.delete()
        return Response("Station deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  StationUpdate(APIView):
    def get_object(self, pk):
        try:
            return Station.objects.get(pk=pk)
        except Station.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Station with the specified id
        '''
        station = self.get_object(pk)
        serializer = StationSerializer(station)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Station with the specified id
        '''
        station = self.get_object(pk)
        serializer = StationSerializer(
            station, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
##############################################################################
# 
# ASSET RELATIONSHIPS
# 

class AssetRelationshipsGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Assetrships with the specified id
        '''
        asset_relationships = Assetrships.objects.filter(assetrships_id=pk)
        serializer = AssetRelationshipsSerializer(asset_relationships, many=True).data
        return Response(serializer)

    
class AssetRelationships(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all AssetRelationships in the system
        '''
        asset_relationships = Assetrships.objects.all()
        serializer = AssetRelationshipsSerializer(asset_relationships, many=True).data
        return Response(serializer)



class AssetRelationshipsCreate(APIView):
    def post(self, request):
        '''
        Creates a single Assetrships record
        '''
        serializer = AssetRelationshipsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetRelationshipsDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Assetrships with the specified id
        '''
        asset_relationships = Assetrships.objects.filter(assetrships_id=pk)
        serializer = AssetRelationshipsSerializer(asset_relationships, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single asset_relationships with the specified id
        '''
        asset_relationships = Assetrships.objects.filter(assetrships_id=pk)
        asset_relationships.delete()
        return Response("Assetrships deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  AssetRelationshipsUpdate(APIView):
    def get_object(self, pk):
        try:
            return Assetrships.objects.get(pk=pk)
        except Assetrships.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Assetrships with the specified id
        '''
        asset_relationships = self.get_object(pk)
        serializer = AssetRelationshipsSerializer(asset_relationships)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Assetrships with the specified id
        '''
        asset_relationships = self.get_object(pk)
        serializer = AssetRelationshipsSerializer(
            asset_relationships, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



####################################################################################

# 
# E50Controlcubicle
# 

class E50ControlcubicleGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Controlcubicle with the specified id
        '''
        e50controlcubicle = E50Controlcubicle.objects.filter(control_cubicle_id=pk)
        serializer = E50ControlcubicleSerializer(e50controlcubicle, many=True).data
        return Response(serializer)

    
class E50Controlcubicles(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50Controlcubicles in the system
        '''
        e50controlcubicle = E50Controlcubicle.objects.all()
        serializer = E50ControlcubicleSerializer(e50controlcubicle, many=True).data
        return Response(serializer)



class E50ControlcubicleCreate(APIView):
    def post(self, request):
        '''
        Creates a single E50Controlcubicle record
        '''
        serializer = E50ControlcubicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50ControlcubicleDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Controlcubicle with the specified id
        '''
        e50controlcubicle = E50Controlcubicle.objects.filter(control_cubicle_id=pk)
        serializer = E50ControlcubicleSerializer(e50controlcubicle, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50Controlcubicle with the specified id
        '''
        e50controlcubicle = E50Controlcubicle.objects.filter(control_cubicle_id=pk)
        e50controlcubicle.delete()
        return Response("E50Controlcubicle deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50ControlcubicleUpdate(APIView):
    def get_object(self, pk):
        try:
            return E50Controlcubicle.objects.get(pk=pk)
        except E50Controlcubicle.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50Controlcubicle with the specified id
        '''
        e50controlcubicle = self.get_object(pk)
        serializer = E50ControlcubicleSerializer(e50controlcubicle)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50Controlcubicle with the specified id
        '''
        e50controlcubicle = self.get_object(pk)
        serializer = E50ControlcubicleSerializer(
            e50controlcubicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#######################################################################################
# 
# E50Protectioncubicle
# 

class E50ProtectioncubicleGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Protectioncubicle with the specified id
        '''
        e50protectioncubicle = E50Protectioncubicle.objects.filter(protection_cubicle_id=pk)
        serializer = E50ProtectioncubicleSerializer(e50protectioncubicle, many=True).data
        return Response(serializer)

    
class E50Protectioncubicles(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50Controlcubicles in the system
        '''
        e50protectioncubicle = E50Protectioncubicle.objects.all()
        serializer = E50ProtectioncubicleSerializer(e50protectioncubicle, many=True).data
        return Response(serializer)



class E50ProtectioncubicleCreate(APIView):
    def post(self, request):
        '''
        Creates a single E50Protectioncubicle record
        '''
        serializer = E50ProtectioncubicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50ProtectioncubicleDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Protectioncubicle with the specified id
        '''
        e50protectioncubicle = E50Protectioncubicle.objects.filter(protection_cubicle_id=pk)
        serializer = E50ProtectioncubicleSerializer(e50protectioncubicle, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50Protectioncubicle with the specified id
        '''
        e50protectioncubicle = E50Protectioncubicle.objects.filter(protection_cubicle_id=pk)
        e50protectioncubicle.delete()
        return Response("E50Protectioncubicle deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50ProtectioncubicleUpdate(APIView):
    def get_object(self, pk):
        try:
            return E50Protectioncubicle.objects.get(pk=pk)
        except E50Protectioncubicle.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50Protectioncubicle with the specified id
        '''
        e50protectioncubicle = self.get_object(pk)
        serializer = E50ProtectioncubicleSerializer(e50protectioncubicle)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50Protectioncubicle with the specified id
        '''
        e50protectioncubicle = self.get_object(pk)
        serializer = E50ProtectioncubicleSerializer(
            e50protectioncubicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 




########################################################################################
# 
# E50
# 

class E50sByJobId(APIView):
    def get(self, request, job):
        '''
        Returns details of a single E50 with the specified id
        '''
        e50 = E50.objects.filter(job=job)        
        serializer = E50Serializer(e50, many=True).data
        return Response(serializer)



class E50Get(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50 with the specified id
        '''
        e50 = E50.objects.filter(e50_id=pk)
        serializer = E50Serializer(e50, many=True).data
        return Response(serializer)

    
class E50s(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50s in the system
        '''
        e50= E50.objects.all()
        serializer = E50Serializer(e50, many=True).data
        return Response(serializer)



class E50Create(APIView):
    def post(self, request):
        '''
        Creates a single E50 record
        '''
        serializer = E50Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50Delete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50 with the specified id
        '''
        e50 = E50.objects.filter(e50_id=pk)
        serializer = E50Serializer(e50, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50 with the specified id
        '''
        e50 = E50.objects.filter(e50_id=pk)
        e50.delete()
        return Response("E50 deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50Update(APIView):
    def get_object(self, pk):
        try:
            return E50.objects.get(pk=pk)
        except E50.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50 with the specified id
        '''
        e50 = self.get_object(pk)
        serializer = E50Serializer(e50)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50 with the specified id
        '''
        e50 = self.get_object(pk)
        serializer = E50Serializer(
            e50, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# 
# E50Autodisconnector
# 

class E50AutodisconnectorGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Autodisconnector with the specified id
        '''
        e50autodisconnector = E50Autodisconnector.objects.filter(e50autodisconnect_id=pk)
        serializer = E50AutodisconnectorSerializer( e50autodisconnector, many=True).data
        return Response(serializer)

    
class E50Autodisconnectors(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50Autodisconnectors in the system
        '''
        e50autodisconnector= E50Autodisconnector.objects.all()
        serializer = E50AutodisconnectorSerializer(e50autodisconnector, many=True).data
        return Response(serializer)



class E50AutodisconnectorCreate(APIView):
    def post(self, request):
        '''
        Creates a single E50Autodisconnector record
        '''
        serializer = E50AutodisconnectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50AutodisconnectorDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Autodisconnector with the specified id
        '''
        e50autodisconnector = E50Autodisconnector.objects.filter(e50autodisconnect_id=pk)
        serializer = E50AutodisconnectorSerializer(e50autodisconnector, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50Autodisconnector with the specified id
        '''
        e50autodisconnector = E50Autodisconnector.objects.filter(e50autodisconnect_id=pk)
        e50autodisconnector.delete()
        return Response("E50Autodisconnector deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50AutodisconnectorUpdate(APIView):
    def get_object(self, pk):
        try:
            return E50Autodisconnector.objects.get(pk=pk)
        except E50Autodisconnector.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50Autodisconnector with the specified id
        '''
        e50autodisconnector = self.get_object(pk)
        serializer = E50AutodisconnectorSerializer(e50autodisconnector)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50Autodisconnector with the specified id
        '''
        e50autodisconnector = self.get_object(pk)
        serializer = E50AutodisconnectorSerializer(
            e50autodisconnector, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

###################################################
# 
# E50Circuitbreakers
# 

class E50CircuitbreakersGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = E50Circuitbreakers.objects.filter(e50circuitbreakers_id=pk)
        serializer = E50CircuitbreakersSerializer( e50circuitbreaker, many=True).data
        return Response(serializer)

    
class E50CircuitBreakers(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50Circuitbreakers in the system
        '''
        e50circuitbreaker= E50Circuitbreakers.objects.all()
        serializer = E50CircuitbreakersSerializer(e50circuitbreaker, many=True).data
        return Response(serializer)



class E50CircuitbreakersCreate(APIView):
    def post(self, request):
        '''
        Creates a single E50Circuitbreaker record
        '''
        serializer = E50CircuitbreakersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50CircuitbreakersDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = E50Circuitbreakers.objects.filter(e50circuitbreakers_id=pk)
        serializer = E50CircuitbreakersSerializer(e50circuitbreaker, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = E50Circuitbreakers.objects.filter(e50circuitbreakers_id=pk)
        e50circuitbreaker.delete()
        return Response("E50Circuitbreaker deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50CircuitbreakersUpdate(APIView):
    def get_object(self, pk):
        try:
            return E50Circuitbreakers.objects.get(pk=pk)
        except E50Circuitbreakers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = self.get_object(pk)
        serializer = E50CircuitbreakersSerializer(e50circuitbreaker)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = self.get_object(pk)
        serializer = E50CircuitbreakersSerializer(
            e50circuitbreaker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


# 
# E50Feeders
# 

class E50FeedersGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Feeder with the specified id
        '''
        e50feeders = E50Feeders.objects.filter(e50feeders_id=pk)
        serializer = E50FeedersSerializer( e50feeders, many=True).data
        return Response(serializer)

    
class E50feeders(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50Feeders in the system
        '''
        e50feeders= E50Feeders.objects.all()
        serializer = E50FeedersSerializer(e50feeders, many=True).data
        return Response(serializer)



class E50FeedersCreate(APIView):
    def post(self, request):
        '''
        Creates a single E50Feeder record
        '''
        serializer = E50FeedersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50FeedersDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Feeder with the specified id
        '''
        e50feeders = E50Feeders.objects.filter(e50feeders_id=pk)
        serializer = E50FeedersSerializer(e50feeders, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50Feeders with the specified id
        '''
        e50feeders = E50Feeders.objects.filter(e50feeders_id=pk)
        e50feeders.delete()
        return Response("E50Feeders deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50FeedersUpdate(APIView):
    def get_object(self, pk):
        try:
            return E50Feeders.objects.get(pk=pk)
        except E50Feeders.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50Feeder with the specified id
        '''
        e50feeders = self.get_object(pk)
        serializer = E50FeedersSerializer(e50feeders)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50Feeder with the specified id
        '''
        e50feeders = self.get_object(pk)
        serializer = E50FeedersSerializer(
            e50feeders, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# 
# E50Circuitbreakers
# 

class E50CircuitbreakersGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = E50Circuitbreakers.objects.filter(e50circuitbreakers_id=pk)
        serializer = E50CircuitbreakersSerializer( e50circuitbreaker, many=True).data
        return Response(serializer)

    
class E50CircuitBreakers(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50Circuitbreakers in the system
        '''
        e50circuitbreaker= E50Circuitbreakers.objects.all()
        serializer = E50CircuitbreakersSerializer(e50circuitbreaker, many=True).data
        return Response(serializer)



class E50CircuitbreakersCreate(APIView):
    def post(self, request):
        '''
        Creates a single E50Circuitbreaker record
        '''
        serializer = E50CircuitbreakersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50CircuitbreakersDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = E50Circuitbreakers.objects.filter(e50circuitbreakers_id=pk)
        serializer = E50CircuitbreakersSerializer(e50circuitbreaker, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = E50Circuitbreakers.objects.filter(e50circuitbreakers_id=pk)
        e50circuitbreaker.delete()
        return Response("E50Circuitbreaker deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50CircuitbreakersUpdate(APIView):
    def get_object(self, pk):
        try:
            return E50Circuitbreakers.objects.get(pk=pk)
        except E50Circuitbreakers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = self.get_object(pk)
        serializer = E50CircuitbreakersSerializer(e50circuitbreaker)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50Circuitbreaker with the specified id
        '''
        e50circuitbreaker = self.get_object(pk)
        serializer = E50CircuitbreakersSerializer(
            e50circuitbreaker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


# 
# E50Transformer
# 

class E50TransformerGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Transformer with the specified id
        '''
        e50transformer = E50Transformer.objects.filter(e50transformer_id=pk)
        serializer = E50TransformerSerializer( e50transformer, many=True).data
        return Response(serializer)

    
class E50Transformers(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all E50Transformer in the system
        '''
        e50transformer= E50Transformer.objects.all()
        serializer = E50TransformerSerializer(e50transformer, many=True).data
        return Response(serializer)



class EE50TransformerCreate(APIView):
    def post(self, request):
        '''
        Creates a single E50Transformer record
        '''
        serializer = E50TransformerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class E50TransformerDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single E50Transformer with the specified id
        '''
        e50transformer = E50Transformer.objects.filter(e50transformer_id=pk)
        serializer = E50TransformerSerializer(e50transformer, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single E50Transformer with the specified id
        '''
        e50transformer = E50Transformer.objects.filter(e50transformer_id=pk)
        e50transformer.delete()
        return Response("E50Transformer deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  E50TransformerUpdate(APIView):
    def get_object(self, pk):
        try:
            return E50Transformer.objects.get(pk=pk)
        except E50Transformer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single E50Transformer with the specified id
        '''
        e50transformer = self.get_object(pk)
        serializer = E50TransformerSerializer(e50transformer)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single E50Transformer with the specified id
        '''
        e50transformer = self.get_object(pk)
        serializer = E50TransformerSerializer(
            e50transformer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class TransformerAssets(APIView):
    
    '''
    Arguments:
        [substation id]
    Returns:
        Returns a list of all assets in a specified substation
    '''
    def get(self, request, parent_assetid):
        asset = Assetrships.objects.transformer_assets(parent_assetid=parent_assetid)        
        return Response(asset)


class TransformerAssets(APIView):
    
    '''
    Arguments:
        [substation id]
    Returns:
        Returns a list of all assets in a specified substation
    '''
    def get(self, request, parent_assetid):
        asset = Assetrships.objects.transformer_assets(parent_assetid=parent_assetid)        
        return Response(asset)

class StationAssets(APIView):

    '''
    Arguments:
        [substation id]
    Returns:
        Returns a list of all assets in a specified substation
    '''
    def get(self, request, parent_assetid):
        asset = Assetrships.objects.station_assets(parent_assetid=parent_assetid)        
        return Response(asset)


class StationsByCentre(APIView):

    '''
    Arguments:
        [depot code]
    Returns:
        Returns a list of all substations for a specified depot/centre
    '''
    def get(self, request, depot):
        asset = Station.objects.filter(depot=depot)        
        serializer = StationSerializer(asset, many=True)
        return Response(serializer.data)


class StationTransformers(APIView):

    '''
    Arguments:
        [substation id]
    Returns:
        Returns a list of all transformers in a specified substation
    '''
    def get(self, request, parent_assetid):
        asset = Assetrships.objects.station_transformers(parent_assetid=parent_assetid)        
        return Response(asset)

class StationFeeders(APIView):

    '''
    Arguments:
        [substation id]
    Returns:
        Returns a list of all feeders in a specified substation
    '''
    def get(self, request, parent_assetid):
        asset = Assetrships.objects.station_feeders(parent_assetid=parent_assetid)        
        return Response(asset)


class StationCircuitBreakers(APIView):

    '''
    Arguments:
        [substation id]
    Returns:
        Returns a list of all Circuit Breakers in a specified substation
    '''
    def get(self, request, parent_assetid):
        asset = Assetrships.objects.station_switchgear_breakers(parent_assetid=parent_assetid)        
        return Response(asset)

class StationSwitchgearIsolators(APIView):

    '''
    Arguments:
        [substation id]
    Returns:
        Returns a list of all Switchgear Isolators in a specified substation
    '''
    def get(self, request, parent_assetid):
        asset = Assetrships.objects.station_switchgear_isolators(parent_assetid=parent_assetid)        
        return Response(asset)

class TransformersMetering(APIView):
    '''
    Arguments:
        [transformer id]
    Returns:
        Returns a list of all meterings in a specified transformer
    '''
    def get(self, request, parent_assetid):
        metering = Assetrships.objects.transformer_metering(parent_assetid=parent_assetid)        
        return Response(metering)

class TransformerLightiningArresters(APIView):
    def get(self, request,parent_assetid):
        lightningarrester = Assetrships.objects.transformerlightningarrester(parent_assetid=parent_assetid)
        return Response(lightningarrester)

class TransformerSwitchgear(APIView):
    def get(self, request, parent_assetid):
        switchgear = Assetrships.objects.transformerswitchgear(parent_assetid=parent_assetid)
        return Response(switchgear)

class TransformerDfuses(APIView):
    def get(self, request, parent_assetid):
        dfuses = Assetrships.objects.transformerdfuses(parent_assetid=parent_assetid)
        return Response(dfuses)
       
class E50TransformersByE50Id(APIView):
    def get(self, request, e50_id):
        '''
        Returns details of all Transformers for a particular e50 form with the specified id
        '''
        e50transformer = E50Transformer.objects.filter(e50_id=e50_id)
        serializer = E50TransformerSerializer( e50transformer, many=True).data
        return Response(serializer)

class E50FeedersByE50Id(APIView):
    def get(self, request, e50_id):
        '''
        Returns details of all Feeders for a particular e50 form with the specified id
        '''
        feeder = E50Feeders.objects.filter(e50_id=e50_id)
        serializer = E50FeedersSerializer( feeder, many=True).data
        return Response(serializer)


class E50CircuitBreakersByE50Id(APIView):
    def get(self, request, e50_id):
        '''
        Returns details of all Circuit Breakers for a particular e50 form with the specified id
        '''
        circuitbreaker = E50Circuitbreakers.objects.filter(e50_id=e50_id)
        serializer = E50CircuitbreakersSerializer( circuitbreaker, many=True).data
        return Response(serializer)

class E50AutodisconnectorsByE50Id(APIView):
    def get(self, request, e50_id):
        '''
        Returns details of all Auto Disconnectors and Isolators for a particular e50 form with the specified id
        '''
        autodisconnector = E50Autodisconnector.objects.filter(e50_id=e50_id)
        serializer = E50AutodisconnectorSerializer( autodisconnector, many=True).data
        return Response(serializer)

class E50ProtectionCubiclesByE50Id(APIView):
    def get(self, request, e50_id):
        '''
        Returns details of all Protection Cubicles and Isolators for a particular e50 form with the specified id
        '''
        protection_cubicle= E50Protectioncubicle.objects.filter(e50_id=e50_id)
        serializer = E50ProtectioncubicleSerializer( protection_cubicle, many=True).data
        return Response(serializer)


class E50ControlCubiclesByE50Id(APIView):
    def get(self, request, e50_id):
        '''
        Returns details of all Control Cubicles and Isolators for a particular e50 form with the specified id
        '''
        control_cubicle = E50Controlcubicle.objects.filter(e50_id=e50_id)
        serializer = E50ControlcubicleSerializer( control_cubicle, many=True).data
        return Response(serializer)

class E50GeneralByE50Id(APIView):
    def get(self, request, e50_id):
        '''
        Returns general E50 details for a particular e50 form with the specified id
        '''
        general_data = E50.objects.filter(e50_id=e50_id)
        serializer = E50Serializer( general_data, many=True).data
        return Response(serializer)

############################
#DFUSE
############################
class DfusesGet(APIView):
    def get(self, request, pk):
        dfuse = Dfuse.objects.filter(pk=pk)
        serializer = DfuseSerializers(dfuse, many=True).data
        return Response(serializer)


class  Dfuses(APIView):
    def get(self, request, format=None):
        dfuser =  Dfuse.objects.all()
        serializer = DfuseSerializers( dfuser, many=True).data
        return Response(serializer)



class  DfusesPost(APIView):
    def post(self, request):
        serializer = DfuseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class  DfusesDelete(APIView):

    def get(self, request, pk):
        '''
        Returns details of a single Dfuses with the specified id
        '''
        dfuses = Dfuse.objects.filter(dfuse_id=pk)
        serializer = DfuseSerializers(dfuses, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single Dfuses with the specified id
        '''
        dfuses = Dfuse.objects.filter(dfuse_id=pk)
        dfuses.delete()
        return Response("Dfuses deleted successfully", status=status.HTTP_204_NO_CONTENT)

class  DfusesUpdate(APIView):
    def get_object(self, pk):
        try:
            return Dfuse.objects.get(pk=pk)
        except Dfuse.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Dfuse with the specified id
        '''
        dfuses = self.get_object(pk)
        serializer = DfuseSerializers(dfuses)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Dfuses with the specified id
        '''
        dfuses = self.get_object(pk)
        serializer = DfuseSerializers(
            dfuses, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


############################
#E60 DFUSE
############################

class E60DfuseE60Id(APIView):
    def get(self, request, e60_id):
        '''
        Returns details of all Dfuse for a particular e60 form with the specified id
        '''
        e60dfuse= E60Dfuse.objects.filter(e60_id=e60_id)
        serializer = E60DfusesSerializers( e60dfuse, many=True).data
        return Response(serializer)

class E60DfusesGet(APIView):
    def get(self, request, pk):
        e60dfuse = E60Dfuse.objects.filter(pk=pk)
        serializer = E60DfusesSerializers(e60dfuse, many=True).data
        return Response(serializer)


class  E60Dfuses(APIView):
    def get(self, request, format=None):
        e60dfuser =  E60Dfuse.objects.all()
        serializer = E60DfusesSerializers( e60dfuser, many=True).data
        return Response(serializer)



class  E60DfusesPost(APIView):
    def post(self, request):
        serializer = E60DfusesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class  E60DfusesDelete(APIView):

    def get(self, request, pk):
        '''
        Returns details of a single Dfuses with the specified id
        '''
        e60dfuses = E60Dfuse.objects.filter(dfuse_id=pk)
        serializer = E60DfusesSerializers(e60dfuses, many=True).data
        return Response(serializer)

    def delete(self, request, pk):
        '''
        Deletes a single Dfuses with the specified id
        '''
        e60dfuses = E60Dfuse.objects.filter(dfuse_id=pk)
        e60dfuses.delete()
        return Response("Dfuses deleted successfully", status=status.HTTP_204_NO_CONTENT)

class  E60DfusesUpdate(APIView):
    def get_object(self, pk):
        try:
            return E60Dfuse.objects.get(pk=pk)
        except Dfuse.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a single Dfuse with the specified id
        '''
        e60dfuses = self.get_object(pk)
        serializer = E60DfusesSerializers(e60dfuses)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a single Dfuses with the specified id
        '''
        e60dfuses = self.get_object(pk)
        serializer = E60DfusesSerializers(
            e60dfuses, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

###########################
#Metering

class MeteringsGet(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single  Metering with the specified id
        '''
        metering = Metering.objects.filter(metering_id=pk)
        serializer = MeteringSerializers(metering, many=True).data
        return Response(serializer)

    
class Meterings(APIView):
    def get(self, request, format=None):
        '''
        Returns a list of all Lightning Arresters
        '''
        metering = Metering.objects.all()
        serializer = MeteringSerializers(metering, many=True).data
        return Response(serializer)


class MeteringsPost(APIView):
    def post(self, request):
        '''
        Creates a single Lightning Arrester
        '''
        serializer = MeteringSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeteringsDelete(APIView):
    def get(self, request, pk):
        '''
        Returns details of a single Lightning Arrester with the specified id
        '''
        metering = Metering.objects.filter(metering_id=pk)
        serializer = MeteringSerializers(metering, many=True).data
        return Response(serializer)

    def delete(self, request, pk):

        '''
        Deletes a single Lightning Arrester with the specified id
        '''
        metering = Metering.objects.filter(metering_id=pk)
        Metering.delete()
        return Response("Lightning Arrester deleted successfully", status=status.HTTP_204_NO_CONTENT)


class  MeteringsUpdate(APIView):
    def get_object(self, pk):
        try:
            return Metering.objects.get(pk=pk)
        except Feeder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''
        Returns details of a a single Lightning Arrester with the specified id
        '''
        metering = self.get_object(pk)
        serializer = MeteringSerializers(metering)
        return Response(serializer.data)

    def patch(self, request, pk):
        '''
        Updates details of a Lightning Arrester with the specified id
        '''
        metering = self.get_object(pk)
        serializer = MeteringSerializers(
            metering, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransformersMetering(APIView):
    '''
    Arguments:
        [transformer id]
    Returns:
        Returns a list of all meterings in a specified transformer
    '''
    def get(self, request, parent_assetid):
        metering = Assetrships.objects.transformer_metering(parent_assetid=parent_assetid)        
        return Response(metering)

class TransformerLightiningArresters(APIView):
    def get(self, request,parent_assetid):
        lightningarrester = Assetrships.objects.transformerlightningarrester(parent_assetid=parent_assetid)
        return Response(lightningarrester)

class TransformerSwitchgear(APIView):
    def get(self, request, parent_assetid):
        switchgear = Assetrships.objects.transformerswitchgear(parent_assetid=parent_assetid)
        return Response(switchgear)

class TransformerDfuses(APIView):
    def get(self, request, parent_assetid):
        dfuses = Assetrships.objects.transformerdfuses(parent_assetid=parent_assetid)
        return Response(dfuses)
