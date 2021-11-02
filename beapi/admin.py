from django.contrib import admin
from .models import *

admin.site.register(Appflow)
admin.site.register(Workorder)
# admin.site.register(E60Meter)
admin.site.register(Metering)
admin.site.register(E60)
admin.site.register(Dfuse)
admin.site.register(E60Dfuse)
admin.site.register(E60Housing)
admin.site.register(E60Htlightningarrester)
admin.site.register(E60Ltlightningarrester)
admin.site.register(E60Metering)
admin.site.register(E60Safety)
admin.site.register(E60Subgeneral)
admin.site.register(E60Switchgear)
admin.site.register(E60Transformer)


admin.site.register(E50Protectioncubicle)
admin.site.register(E50Controlcubicle)
admin.site.register(E50Autodisconnector)
admin.site.register(E50)
admin.site.register(E50Circuitbreakers)
admin.site.register(E50Feeders)
admin.site.register(E50Transformer)
admin.site.register(Assetrships)
admin.site.register(Station)
admin.site.register(Switchgear)
admin.site.register(Transformer)
admin.site.register(Feeder)


# the following were done by @tsitsiflora
admin.site.register(Jobteam)
admin.site.register(Jobsync)
admin.site.register(Jobprogress)
admin.site.register(Jobattachment)
admin.site.register(E84Lineinspection)
admin.site.register(E84General)

# model registration by tsitsi ends here


admin.site.register(Lightningarrester)
admin.site.register(Substationmeter)

admin.site.register(Boqlabour)
admin.site.register(Boqmaterial)
admin.site.register(Boqvehicle)
admin.site.register(E117Client)

# model registration by Sarah
admin.site.register(Team)
admin.site.register(TeamLeader)
admin.site.register(Userroletrail)
admin.site.register(Userrole)
admin.site.register(Rolepermission)
admin.site.register(Role)
admin.site.register(Pole)
admin.site.register(Permission)
admin.site.register(Office)
admin.site.register(Jobworkflow)
admin.site.register(Job)
# model registration by sarah ends here

# model registration done by kuda
admin.site.register(JobStatus)
admin.site.register(JobType)
admin.site.register(Centre)
# model reg by Kuda ends here
admin.site.register(Profile)
admin.site.register(Roleprofile)
admin.site.register(Userprofile)
admin.site.register(Workflow)
admin.site.register(E117)
admin.site.register(E117Equipment)


