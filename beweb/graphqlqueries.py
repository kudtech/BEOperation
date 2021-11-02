
from graphene import Schema, ObjectType, Field, String, List, Int,Mutation,Float
import datetime
from django.db.models.functions import Lower
from django.db.models import Q
from graphene_django.types import DjangoObjectType
from beapi.models import *

"""DATA TYPES """

class TeamObj(DjangoObjectType):
    class Meta:
        model=Team
class JobObj(DjangoObjectType):
    class Meta:
        model=Job
class JobTeamObj(DjangoObjectType):
    class Meta:
        model=Jobteam
class TeamObj(DjangoObjectType):
    class Meta:
        model=Team
class WorkorderObj(DjangoObjectType):
    class Meta:
        model=Workorder
class JobprogressObj(DjangoObjectType):
    class Meta:
        model=Jobprogress
class JobprogressObj(DjangoObjectType):
    class Meta:
        model=Jobprogress
class JobprogressObj(DjangoObjectType):
    class Meta:
        model=Jobprogress

class TeamLeaderObj(DjangoObjectType):
    class Meta:
        model=TeamLeader
"""QUERY STRINGS"""
class Query(ObjectType):
    teamleders = List(TeamLeaderObj)
    teamleder = Field(TeamLeaderObj, id=String())
    teams = List(TeamObj)
    team = List(TeamObj, id=String())
    jobs = List(JobObj)
    myJobs = List(JobObj, id=String())

    jobteam = List(JobTeamObj)
    myjobteam = List(JobTeamObj, id=String())

    jobprogres=List(JobprogressObj)
    myjobprogres=List(JobprogressObj,id=String())
    
    """QUERY STRINGS"""

    """RESOLVERS"""
    
    def resolve_teamleders(self,info):
        return TeamLeader.objects.all()
    def resolve_teamleader(root, info, id):
        return TeamLeader.objects.get(team_leader=id)

    def resolve_teams(self,info):
        return Team.objects.all()
    def resolve_team(self, info ,id ):
        return Team.objects.filter(team_leader=id)
  
    def resolve_jobs(self,info):
        return Job.objects.all()
    def resolve_myjobs(self, info ,id ):
        return Job.objects.filter(id=id)
    
    def resolve_jobprogress(self,info):
        return Jobprogress.objects.all()
    def resolve_myjobprogres(self, info ,id ):
        return Jobprogress.objects.filter(id=id)
  
    def resolve_jobteam(self,info):
        return Jobteam.objects.all()
  
    def resolve_myjobteam(self, info ,id ):
        return Jobteam.objects.filter(id=id)
  
"""RESOLVERS"""
"""SCHEMA STRING"""

schema = Schema(query=Query)