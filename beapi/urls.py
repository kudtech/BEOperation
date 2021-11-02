from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view


app_name = 'beapi'

schema_view = get_swagger_view(
    title="BE Operations API Endpoints Documentation")


urlpatterns = [
    # Appflow
    path('appflow', Appflows.as_view(), name="appflow"),
    path('appflowpost', AppflowsPost.as_view(), name="appflowpost"),
    path('appflowdelete/<pk>', AppflowDelete.as_view(), name='appflowdelete'),
    path('appflowmodify/<pk>', AppflowModify.as_view(), name='appflowmodify'),
    path('appflowupdate/<pk>', AppflowUpdate.as_view(), name='appflowmodify'),

    # Workorders
    path('workorder', Workorders.as_view(), name="workorder"),
    path('workorders/<pk>/',WorkorderJobs.as_view(), name="workorders"),
    path('workorderpost', WorkordersPost.as_view(), name="workorderpost"),
    path('workorderdelete/<pk>', WorkorderDelete.as_view(), name="workorderdelete"),
    path('workorderput/<pk>', WorkorderModify.as_view(), name="workorderput"),
    path('workorderpatch/<pk>', WorkOrderUpdate.as_view(), name="workorderpatch"),
    path('docs/', schema_view, name="schema_view"),

    # Jobs
    path('jobs', Jobs.as_view(), name="jobs"),
    path('jobs/artisan/<assignee>/', AssignedJobs.as_view(), name="artisan-jobs"),
    path('job/<pk>/', JobGet.as_view(), name="job"),
    path('jobpost', JobCreate.as_view(), name="jobpost"),
    path('jobdelete/<pk>', JobDelete.as_view(), name="jobdelete"),
    path('jobupdate/<pk>', JobUpdate.as_view(), name="jobupdate"),


    # Clients
    path('clients', Clients.as_view(), name="clients"),
    path('client/<pk>/', ClientGet.as_view(), name="client"),
    path('clientpost/', ClientCreate.as_view(), name="clientpost"),
    path('clientdelete/<pk>/', ClientDelete.as_view(), name="clientdelete"),
    path('clientupdate/<pk>/', ClientUpdate.as_view(), name="clientupdate"),

    # Feeders
    path('feeders', Feeders.as_view(), name="feeders"),
    path('feeder/<pk>', FeederGet.as_view(), name="feeder"),
    path('feederpost', FeederCreate.as_view(), name="feederpost"),
    path('feederdelete/<pk>', FeederDelete.as_view(), name="feederdelete"),
    path('feederupdate/<pk>', FeederUpdate.as_view(), name="feederupdate"),
    # LightningArresters
    path('lightningarresters', LightningArresters.as_view(),name="lightningarresters"),
    path('lightningarrester/<pk>', LightningArresterGet.as_view(),name="lightningarrester"),
    path('lightningarresterpost', LightningArresterCreate.as_view(),name="lightningarresterpost"),
    path('lightningarresterdelete/<pk>',LightningArresterDelete.as_view(), name="lightningarresterdelete"),
    path('lightningarresterupdate/<pk>',LightningArresterUpdate.as_view(), name="lightningarresterupdate"),


    # SubstationMeter
    path('substationmeters', SubstationMeters.as_view(), name="substationmeters"),
    path('substationmeter/<pk>', SubstationMeterGet.as_view(),name="substationmeter"),
    path('substationmeterpost', SubstationMeterCreate.as_view(),name="substationmeterpost"),
    path('substationmeterdelete/<pk>', SubstationMeterDelete.as_view(),name="substationmeterdelete"),
    path('substationmeterupdate/<pk>', SubstationMeterUpdate.as_view(),name="substationmeterupdate"),
    # Switchgear
    path('switchgears', Switchgears.as_view(), name="switchgears"),
    path('switchgear/<pk>', SwitchgearGet.as_view(), name="switchgear"),
    path('switchgearpost', SwitchgearCreate.as_view(), name="switchgearpost"),
    path('switchgeardelete/<pk>', SwitchgearDelete.as_view(),name="switchgeardelete"),
    path('switchgearupdate/<pk>', SwitchgearUpdate.as_view(),name="switchgearupdate"),
    # Transformer
    path('transformers', Transformers.as_view(), name="transformers"),
    path('transformer/<pk>', TransformerGet.as_view(), name="transformer"),
    path('transformerpost', TransformerCreate.as_view(), name="transformerpost"),
    path('transformerdelete/<pk>', TransformerDelete.as_view(),name="transformerdelete"),
    path('transformerupdate/<pk>', TransformerUpdate.as_view(),name="transformerupdate"),
    # BOQ Labour
    path('boqslabour', BoqsLabour.as_view(), name="boqslabour"),
    path('boqlabour/<pk>', BoqLabourGet.as_view(), name="boqlabour"),
    path('boqlabourpost', BoqLabourCreate.as_view(), name="boqlabourpost"),
    path('boqlabourdelete/<pk>', BoqLabourDelete.as_view(), name="boqlabourdelete"),
    path('boqlabourupdate/<pk>', BoqLabourUpdate.as_view(), name="boqlabourupdate"),
    # BOQ Material
    path('boqmaterials', BoqMaterial.as_view(), name="boqmaterials"),
    path('boqmaterial/<pk>', BoqMaterialGet.as_view(), name="boqmaterial"),
    path('boqmaterialpost', BoqMaterialCreate.as_view(), name="boqmaterialpost"),
    path('boqmaterialdelete/<pk>', BoqMaterialDelete.as_view(),name="boqmaterialdelete"),
    path('boqmaterialupdate/<pk>', BoqMaterialUpdate.as_view(),name="boqmaterialupdate"),
    # BOQ Vehicles
    path('boqvehicles', BoqVehicle.as_view(), name="boqvehicles"),
    path('boqvehicle/<pk>', BoqVehicleGet.as_view(), name="boqvehicle"),
    path('boqvehiclepost', BoqVehicleCreate.as_view(), name="boqvehiclepost"),
    path('boqvehicledelete/<pk>', BoqVehicleDelete.as_view(),name="boqvehicledelete"),
    path('boqvehicleupdate/<pk>', BoqVehicleUpdate.as_view(),name="boqvehicleupdate"),
    path('workorderpatch/<pk>', WorkOrderUpdate.as_view(), name="workorderpatch"),

    # Workflow urls
    path('workflow', Workflows.as_view(), name="workflow"),
    path('workflowpost', WorkflowsPost.as_view(), name="workflowpost"),
    path('workflowdelete/<pk>', WorkflowDelete.as_view(), name="workflowdelete"),
    path('workflowpatch/<pk>', WorkflowUpdate.as_view(), name="workflowpatch"),

    # User role trail urls
    path('userroletrail', UserRoleTrails.as_view(), name="userroletrail"),
    path('userroletrailpost', UserRoleTrailsPost.as_view(),name="userroletrailpost"),
    path('userroletraildelete/<pk>', UserRoleTrailDelete.as_view(),name="userroletraildelete"),
    path('userroletrailpatch/<pk>', UserRoleTrailUpdate.as_view(),name="userroletrailpatch"),

    # workorder urls
    path('workorder', Workorders.as_view(), name="workorder"),
    path('workorderpost', WorkordersPost.as_view(), name="workorderpost"),
    path('workorderdelete/<pk>', WorkorderDelete.as_view(), name="workorderdelete"),

    # Jobteam urls
    path('jobteams', JobteamGet.as_view(), name="jobteams"),
    path('jobteam/<pk>', JobTeam.as_view(), name="jobteam"),
    path('jobteams/<job_progress>', SpecificJobTeam.as_view(), name="jobteams"),
    path('jobteampost', JobteamPost.as_view(), name="jobteampost"),
    path('jobteamdelete/<pk>', JobteamDelete.as_view(), name="jobteamdelete"),
    path('jobteamupdate/<pk>', JobteamUpdate.as_view(), name="jobteamupdate"),

    # Jobsync urls
    path('jobsync', JobsyncGet.as_view(), name="jobsync"),
    path('jobsync/<pk>', Jobsync.as_view(), name="jobsyncid"),
    path('jobsyncpost', JobsyncPost.as_view(), name="jobsyncpost"),
    path('jobsyncdelete/<pk>', JobsyncDelete.as_view(), name="jobsyncdelete"),
    path('jobsyncupdate/<pk>', JobsyncUpdate.as_view(), name="jobsyncupdate"),

    # jobprogress urls
    path('artisan/jobprogress/<job_id>/',SingleJobProgress.as_view(), name="artisan-jobprogress"),
    path('jobprogress', JobprogressGet.as_view(), name="jobprogress"),
    path('jobprogress/<pk>', JobProgress.as_view(), name="jobprogressid"),
    path('jobprogresspost', JobprogressPost.as_view(), name="jobprogresspost"),
    path('jobprogressdelete/<pk>', JobprogressDelete.as_view(),name="jobprogressdelete"),
    path('jobprogressupdate/<pk>', JobprogressUpdate.as_view(),name="jobprogressupdate"),


    # E84Line Inspection urls
    path('e84line', E84LineinspectionGet.as_view(), name="e84line"),
    path('e84line/<pk>', E84LineInspection.as_view(), name="e84lineid"),
    path('e84linepost', E84LineinspectionPost.as_view(), name="e84linepost"),
    path('e84linedelete', E84LineinspectionDelete.as_view(), name="e84linedelete"),
    path('e84lineupdate/<pk>/', E84LineinspectionUpdate.as_view(),name="e84lineupdate"),

    # E84General urls
    path('e84general', E84GeneralGet.as_view(), name="e84general"),
    path('e84general/<pk>', E84general.as_view(), name="e84generalid"),
    path('e84generalpost', E84GeneralPost.as_view(), name="e84generalpost"),
    path('e84generaldelete/<pk>', E84GeneralDelete.as_view(),name="e84generaldelete"),
    path('e84generalupdate/<pk>/', E84GeneralUpdate.as_view(),name="e84generalupdate"),

    # E60 urls
    path('e60s', E60sGet.as_view(), name="e60s"),
    path('e60job/<job>/',E60sByJobId.as_view(),name="e60job"),
    path('e60/<pk>', E60s.as_view(), name="e60/"),
    path('e60post', E60Post.as_view(),name="e60post/"),
    path('e60delete/<pk>', E60Delete.as_view(),name="e60delete/"),
    path('e60update/<pk>', E60Update.as_view(),name="e60update/"),


    # E60Transformer urls
    path('e60/transformer/<e60_id>/',E60TransformersByE60Id.as_view(),name="e60-transformer"),
    path('e60transformers', E60TransformerGet.as_view(), name="e60transformers"),
    path('e60transformer/<pk>', E60Transformers.as_view(), name="e60transformerid"),
    path('e60transformerpost', E60TransformerPost.as_view(),name="e60transformerpost"),
    path('e60transformerdelete/<pk>', E60TransformerDelete.as_view(),name="e60transformerdelete"),
    path('e60transformerupdate/<pk>', E60TransformerUpdate.as_view(),name="e60transformerupdate"),

    # E60Switchgear urls
    path('e60/switchgear/<e60_id>/',E60SwitchgearByE60Id.as_view(),name="e60-switchgear"),
    path('e60switchgears', E60SwitchgearGet.as_view(), name="e60switchgears"),
    path('e60switchgear/<pk>', E60Switchgears.as_view(), name="e60switchgearid"),
    path('e60switchgearpost', E60SwitchgearPost.as_view(),name="e60switchgearpost"),
    path('e60switchgeardelete/<pk>', E60SwitchgearDelete.as_view(),name="e60switchgeardelete"),
    path('e60switchgearupdate/<pk>', E60SwitchgearUpdate.as_view(),name="e60switchgearupdate"),

    #E60Substation General
    path('e60/subgeneral/<e60_id>/',E60SubstationgeneralE60Id.as_view(),name="e50-subgeneral"),
    path('e60subgeneral', E60SubstationgeneralGet.as_view(), name="e60subgeneral"),
    path('e60subgeneral/<pk>', E60Substationgenerals.as_view(),name="e60subgeneralid"),
    path('e60subgeneralpost', E60SubstationgeneralPost.as_view(),name="e60subgeneralpost"),
    path('e60subgeneraldelete/<pk>', E60SubstationgeneralDelete.as_view(),name="e60subgeneraldelete"),
    path('e60subgeneralupdate/<pk>', E60SubstationgeneralUpdate.as_view(),name="e60subgeneralupdate"),

    # E60Metering urls
    path('e60/metering/<e60_id>/',E60MeteringE60Id.as_view(),name="e60-metering"),
    path('e60metering/<pk>',E60Meterings.as_view(),name='e60meteringid'),
    path('e60meterings',E60MeteringGet.as_view(),name='e60meterings'),
    path('e60meteringpost',E60MeteringPost.as_view(),name='e60meteringpost'),
    path('e60meteringdelete/<pk>',E60MeteringDelete.as_view(),name='e60meteringdelete'),
    path('e60meteringupdate/<pk>',E60MeteringUpdate.as_view(),name='e60meteringupdate'),
    
    ##E60LightingArresters
    path('e60/ltlightingarrester/<e60_id>',E60LtlightningarresterByE60Id.as_view(),name='e60/lightingarrester'),
    path('e60ltlightingarrester/<pk>',E60LtLightingArrestorGet.as_view(),name='e60ltlightingarresterid'),
    path('e60ltlightingarresters',E60LtLightingArrestors.as_view(),name='e60ltlightingarresters'),
    path('e60ltlightingarresterpost',E60LtlightningarresterPost.as_view(),name='e60ltlightingarresterpost'),
    path('e60ltlightingarresterdelete/<pk>',E60LtlightningarresterDelete.as_view(),name='e60ltlightingarresterdelete'),
    path('e60ltlightingarresterupdate/<pk>',E60LtlightningarresterUpdate.as_view(),name='e60ltlightingarresterupdate'),

    #E60HtLightingArrestor
    path('e60/htlightingarrester/<e60_id>',E60HtlightningarresterByE60Id.as_view(),name='e60/lightingarrester'),
    path('e60htlightingarresters',e60Htlightningarresters.as_view(),name='e60htlightingarresters'),
    path('e60htlightingarrester/<pk>',e60HtlightningarresterGet.as_view(),name='e60htlightingarresterid'),
    path('e60htlightingarresterpost',e60HtlightningarresterPost.as_view(),name='e60htlightingarresterpost'),
    path('e60htlightingarresterdelete/<pk>',e60HtlightningarresterDelete.as_view(),name='e60htlightingarresterdelete'),
    path('e60htlightingarresterupdate/<pk>',E60HtlightningarresterUpdate.as_view(),name='e60htlightingarresterupdate'),

    #E60Safety
    path('e60/safety/<e60_id>/',E60SafetysE60Id.as_view(),name="e60-safety"),
    path('e60safetys',E60SafetyGet.as_view(),name='e60safetys'),
    path('e60safety/<pk>',E60Safetys.as_view(),name='e60safetyid'),
    path('e60safetypost',E60SafetyPost.as_view(),name='e60safetypost'),
    path('e60safetydelete/<pk>',E60SafetyDelete.as_view(),name='e60safetydelete'),
    path('e60safetyupdate/<pk>',E60SafetyUpdate.as_view(),name='e60safetyupdate'),

    path('transformer/assets/<parent_assetid>/', TransformerAssets.as_view(), name="transformer-assets"),
    #E60Housing
    path('e60/housing/<e60_id>/',E60HousingE60Id.as_view(),name="e60-housing"),
    path('e60housings',E60HousingGet.as_view(),name='e60housings'),
    path('e60housing/<pk>',E60Housings.as_view(),name='e60housing'),
    path('e60housingpost',E60HousingsPost.as_view(),name='e60housingpost'),
    path('e60housingdelete/<pk>',E60HousingDelete.as_view(),name='e60housingdelete'),
    path('e60housingupdate/<pk>',E60HousingUpdate.as_view(),name='e60housingupdate'),


    path('workorderpatch/<pk>', WorkOrderUpdate.as_view(), name="workorderpatch"),

    # userrole urls
    path('userrole', UserRoles.as_view(), name="userrole"),
    path('userrolepost', UserRolePost.as_view(), name="userrolepost"),
    path('userroledelete/<pk>', UserRoleDelete.as_view(), name="userroledelete"),
    path('userrolepatch/<pk>', UserRoleUpdate.as_view(), name="userrolepatch"),

    # team urls
    path('teampost', TeamPost.as_view(), name="teampost"),
    path('teamdelete/<pk>', TeamDelete.as_view(), name="teamdelete"),
    path('teampatch/<pk>', TeamUpdate.as_view(), name="teampatch"),
    path('teams', Teams.as_view(), name="teams"),
    path('teams/<team_leader>', TeamGet.as_view(), name="teams-get"),
    path('teammembers', TeamView.as_view(), name="teammembers"),
    path('teamleaders', TeamLeaders.as_view(), name="teamleaders"),

    # rolepermission urls
    path('rolepermission', RolePermissions.as_view(), name="rolepermission"),
    path('rolepermissionpost', RolePermissionPost.as_view(),name="rolepermissionpost"),
    path('rolepermissiondelete/<pk>', RolePermissionDelete.as_view(),name="rolepermissiondelete"),
    path('rolepermissionpatch/<pk>', RolePermissionUpdate.as_view(),name="rolepermissionpatch"),

    # role urls
    path('role', Roles.as_view(), name="role"),
    path('rolepost', RolePost.as_view(), name="rolepost"),
    path('roledelete/<pk>', RoleDelete.as_view(), name="roledelete"),
    path('rolepatch/<pk>', RoleUpdate.as_view(), name="rolepatch"),

    # pole urls
    path('pole', Poles.as_view(), name="pole"),
    path('polepost', PolePost.as_view(), name="polepost"),
    path('poledelete/<pk>', PoleDelete.as_view(), name="poledelete"),
    path('polepatch/<pk>', PoleUpdate.as_view(), name="polepatch"),

    # Dfuses urls
    path('dfuse/<pk>',DfusesGet.as_view(),name='dfuseid'),
    path('dfuses',Dfuses.as_view(),name='dfuses'),
    path('dfusespost',DfusesPost.as_view(),name='dfusespost'),
    path('dfusesdelete/<pk>',DfusesDelete.as_view(),name='dfusesdelete'),
    path('dfusesupdate/<pk>',DfusesUpdate.as_view(),name='dfusesupdate'),

    # Metering urls
    path('meterings/<pk>',MeteringsGet.as_view(),name='meteringsid'),
    path('meterings',Meterings.as_view(),name='meterings'),
    path('meteringspost',MeteringsPost.as_view(),name='meteringspost'),
    path('meteringsdelete/<pk>',MeteringsDelete.as_view(),name='meteringsdelete'),
    path('meteringsupdate/<pk>',MeteringsUpdate.as_view(),name='meteringsupdate'),

    path('transformers/metering/<parent_assetid>/', TransformersMetering.as_view(), name="transformers-metering"),
    path('transformer/lightingarrester/<parent_assetid>/',TransformerLightiningArresters.as_view(),name="transformers-lighting"),
    path('transformer/switchgear/<parent_assetid>/',TransformerSwitchgear.as_view(),name="transformer-switchgear"),
    path('transformer/dfuse/<parent_assetid>/',TransformerDfuses.as_view(),name="transformer-dfuse"),
    
    # E60Dfuses urls
    path('e60/dfuse/<e60_id>/',E60DfuseE60Id.as_view(),name="e60-e60dfuse"),
    path('e60dfuse/<pk>',E60DfusesGet.as_view(),name='e60dfuse'),
    path('e60dfuses',E60Dfuses.as_view(),name='e60dfuse'),
    path('e60dfusepost',E60DfusesPost.as_view(),name='e60dfusepost'),
    path('e60dfusedelete/<pk>',E60DfusesDelete.as_view(),name='e60dfusedelete'),
    path('e60dfuseupdate/<pk>',E60DfusesUpdate.as_view(),name='e60dfuseupdate'),
    path('transformer/assets/<parent_assetid>/', TransformerAssets.as_view(), name="transformer-assets"),
    # permission urls
    path('permission', Permissions.as_view(), name="permission"),
    path('permissionpost', PermissionPost.as_view(), name="permissionpost"),
    path('permissiondelete/<pk>', PermissionDelete.as_view(),name="permissiondelete"),
    path('permissionpatch/<pk>', PermissionUpdate.as_view(), name="permissionpatch"),


    # office urls
    path('office', Offices.as_view(), name="office"),
    path('officepost', OfficePost.as_view(), name="officepost"),
    path('officedelete/<pk>', OfficeDelete.as_view(), name="officedelete"),
    path('officepatch/<pk>', OfficeUpdate.as_view(), name="officepatch"),

    # jobworkflow urls
    path('jobworkflow', Jobworkflows.as_view(), name="jobworkflow"),
    path('jobworkflowpost', JobworkflowPost.as_view(), name="jobworkflowpost"),
    path('jobworkflowdelete/<pk>', JobworkflowDelete.as_view(),name="jobworkflowdelete"),
    path('jobworkflowpatch/<pk>', JobworkflowUpdate.as_view(),name="jobworkflowpatch"),

    # urls by Kuda(KK)
    # Jobstatus urls
    path('single/jobstatus/<status>',SingleJobStatus.as_view(), name='single-jobstatus'),
    path('jobstatus', JobStatusGet.as_view(), name='jobstatus'),
    path('jobstatuspost', JobStatusPost.as_view(), name='jobstatuspost'),
    path('jobstatusdelete/<pk>', JobstatusDelete.as_view(), name='jobstatusdelete'),
    path('jobstatusmodify/<pk>', JobstatusModify.as_view(), name='jobstatusmodify'),
    path('jobstatusupdate/<pk>', JobStatusUpdate.as_view(), name='jobstatusupdate'),

    # JobType urls
    path('single/jobtype/<type>', SingleJobType.as_view(), name='single-jobtype'),
    path('jobtype', JobTypeGet.as_view(), name='jobtype'),
    path('jobtypepost', JobTypePost.as_view(), name='jobtypepost'),
    path('jobtypemodify/<pk>', JobTypeModify.as_view(), name='jobtypemodify'),
    path('jobtypedelete/<pk>', JobTypeDelete.as_view(), name='jobtypedelete'),
    path('jobtypeupdate/<pk>', JobTypeUpdate.as_view(), name='jobtypeupdate'),
    # Centre urls
    path('centres', CentreGet.as_view(), name='centres'),
    path('centrepost', CentrePost.as_view(), name='centrepost'),
    path('centredelete/<pk>', CentreDelete.as_view(), name='centredelete'),
    path('centremodify/<pk>', CentreModify.as_view(), name='centremodify'),
    path('centreupdate/<pk>', CentreUpdate.as_view(), name='centreupdate'),
    path('centre/<pk>/', CentreByCentreId.as_view(), name='centre'),

    # Profiles
    path('profiles', Profiles.as_view(), name="profiles"),
    path('profile/<pk>/', ProfileGet.as_view(), name="profile"),
    path('profilepost', ProfileCreate.as_view(), name="profilepost"),
    path('profiledelete/<pk>', ProfileDelete.as_view(), name="profiledelete"),
    path('profileupdate/<pk>', ProfileUpdate.as_view(), name="profileupdate"),

    # Role Profiles
    path('roleprofiles', RoleProfiles.as_view(), name="roleprofiles"),
    path('roleprofile/<pk>/', RoleProfileGet.as_view(), name="roleprofile"),
    path('roleprofilepost', RoleProfileCreate.as_view(), name="roleprofilepost"),
    path('roleprofiledelete/<pk>', RoleProfileDelete.as_view(),name="roleprofiledelete"),
    path('roleprofileupdate/<pk>', RoleProfileUpdate.as_view(),name="roleprofileupdate"),

    # User Profiles
    path('userprofiles', UserProfiles.as_view(), name="userprofiles"),
    path('userprofile/<pk>/', UserProfileGet.as_view(), name="userprofile"),
    path('userprofilepost', UserProfileCreate.as_view(), name="userprofilepost"),
    path('userprofiledelete/<pk>', UserProfileDelete.as_view(),name="userprofiledelete"),
    path('userprofileupdate/<pk>', UserProfileUpdate.as_view(),name="userprofileupdate"),
    path('jobs/workflow/status/<pk>/', JobsWorkflowStatus.as_view(),name="jobs-workflow-status"),
    path('job/awaiting/action/<ec_num>/', JobsAwaitingActionProcedure.as_view(),name="job-awaiting-action"),
    path('job/workflow/<job_id>/', JobWorkflowProcedure.as_view(),name="job-workflow"),
    path('jobs/view/<username>/<section>/<status>/', JobsViewProcedure.as_view(),name="jobs-view"),
    path('single/workorder/<pk>/', SingleWorkorder.as_view(),name="single-workorder"),
    path('workorder/jobs/<pk>',JobsWorkorder.as_view(),name="workorder-jobs"),
     # E117
    path('e117/all/', E117Inspection.as_view(), name="e117-all"),
    path('e117/<pk>/', E117Get.as_view(), name="e117"),
    path('e117post/', E117Create.as_view(), name="e117post"),
    path('e117delete/<pk>/', E117Delete.as_view(), name="e117delete"),
    path('e117update/<pk>/', E117Update.as_view(), name="e117update"),
    path('e117/job/<job_id>/',InstallationInspectionForJob.as_view(),name="job-e117"),

     # E117 Equipment
    path('e117equipment/all/', E117EquipmentInspection.as_view(), name="e117equipment-all"),
    path('e117equipment/<pk>/', E117EquipmentGet.as_view(), name="e117equipment"),
    path('e117equipmentpost/', E117EquipmentCreate.as_view(), name="e117equipmentpost"),
    path('e117equipmentdelete/<pk>/', E117EquipmentDelete.as_view(), name="e117equipmentdelete"),
    path('e117equipmentupdate/<pk>/', E117EquipmentUpdate.as_view(), name="e117equipmentupdate"),

     # E117 Contractor
    path('e117contractor/all/', E117Contractors.as_view(), name="e117contractor-all"),
    path('e117contractor/<pk>/', E117ContractorGet.as_view(), name="e117contractor"),
    path('e117contractorpost/', E117ContractorCreate.as_view(), name="e117contractorpost"),
    path('e117contractordelete/<pk>/', E117ContractorDelete.as_view(), name="e117contractordelete"),
    path('e117contractorupdate/<pk>/', E117ContractorUpdate.as_view(), name="e117contractorupdate"),

     # E117 Reinspection
    path('e117reinspection/all/', E117Reinspections.as_view(), name="e117reinspection-all"),
    path('e117reinspection/<pk>/', E117ReinspectionGet.as_view(), name="e117reinspection"),
    path('e117reinspectionpost/', E117ReinspectionCreate.as_view(), name="e117reinspectionpost"),
    path('e117reinspectiondelete/<pk>/', E117ReinspectionDelete.as_view(), name="e117reinspectiondelete"),
    path('e117reinspectionupdate/<pk>/', E117ReinspectionUpdate.as_view(), name="e117reinspectionupdate"),
    path('reinspection/<e117>/',ReinspectionE117.as_view(),name="reinspection-e117"),
    path('jobs/reinspection/',E117JobsForReinspection.as_view(),name="jobs-reinspection"),
    # STATIONS
    path('stations', Stations.as_view(), name="stations"),
    path('station/<pk>', StationGet.as_view(), name="station"),
    path('stationpost', StationCreate.as_view(), name="stationpost"),
    path('stationdelete/<pk>', StationDelete.as_view(),name="stationdelete"),
    path('stationupdate/<pk>', StationUpdate.as_view(),name="stationupdate"),
    # ASSET RELATIONSHIPS
    path('assetrelationships', AssetRelationships.as_view(), name="assetrelationships"),
    path('assetrelationship/<pk>', AssetRelationshipsGet.as_view(), name="assetrelationship"),
    path('assetrelationshippost', AssetRelationshipsCreate.as_view(), name="assetrelationshippost"),
    path('assetrelationshipdelete/<pk>', AssetRelationshipsDelete.as_view(),name="assetrelationshipdelete"),
    path('assetrelationshipupdate/<pk>', AssetRelationshipsUpdate.as_view(),name="assetrelationshipupdate"),
    # E50Controlcubicle
    path('e50controlcubicles', E50Controlcubicles.as_view(), name="e50controlcubicles"),
    path('e50controlcubicle/<pk>', E50ControlcubicleGet.as_view(), name="e50controlcubicle"),
    path('e50controlcubiclepost', E50ControlcubicleCreate.as_view(), name="e50controlcubiclepost"),
    path('e50controlcubicledelete/<pk>', E50ControlcubicleDelete.as_view(),name="e50controlcubicledelete"),
    path('e50controlcubicleupdate/<pk>', E50ControlcubicleUpdate.as_view(),name="e50controlcubicleupdate"),

    # E50Protectioncubicle
    path('e50protectioncubicles', E50Protectioncubicles.as_view(), name="e50protectioncubicles"),
    path('e50protectioncubicle/<pk>', E50ProtectioncubicleGet.as_view(), name="e50protectioncubicle"),
    path('e50protectioncubiclepost', E50ProtectioncubicleCreate.as_view(), name="e50protectioncubiclepost"),
    path('e50protectioncubicledelete/<pk>', E50ProtectioncubicleDelete.as_view(),name="e50protectioncubicledelete"),
    path('e50protectioncubicleupdate/<pk>', E50ProtectioncubicleUpdate.as_view(),name="e50protectioncubicleupdate"),

    # E50
    path('e50s', E50s.as_view(), name="e50s"),
    path('e50/job/<job>/',E50sByJobId.as_view(),name="e50-job"),
    path('e50/<pk>', E50Get.as_view(), name="e50"),
    path('e50post', E50Create.as_view(), name="e50post"),
    path('e50delete/<pk>', E50Delete.as_view(),name="e50delete"),
    path('e50update/<pk>', E50Update.as_view(),name="e50update"),
    # E50Autodisconnector
    path('e50autodisconnectors', E50Autodisconnectors.as_view(), name="e50autodisconnectors"),
    path('e50autodisconnector/<pk>', E50AutodisconnectorGet.as_view(), name="e50autodisconnector"),
    path('e50autodisconnectorpost', E50AutodisconnectorCreate.as_view(), name="e50autodisconnectorpost"),
    path('e50autodisconnectordelete/<pk>', E50AutodisconnectorDelete.as_view(),name="e50autodisconnectordelete"),
    path('e50autodisconnectorupdate/<pk>', E50AutodisconnectorUpdate.as_view(),name="e50autodisconnectorupdate"),
    # E50Circuitbreakers
    path('e50circuitbreakers', E50CircuitBreakers.as_view(), name="e50circuitbreakers"),
    path('e50circuitbreaker/<pk>', E50CircuitbreakersGet.as_view(), name="e50circuitbreaker"),
    path('e50circuitbreakerpost', E50CircuitbreakersCreate.as_view(), name="e50circuitbreakerpost"),
    path('e50circuitbreakerdelete/<pk>', E50CircuitbreakersDelete.as_view(),name="e50circuitbreakerdelete"),
    path('e50circuitbreakerupdate/<pk>', E50CircuitbreakersUpdate.as_view(),name="e50circuitbreakerupdate"),

    # E50Feeders
    path('e50feeders', E50feeders.as_view(), name="e50feeders"),
    path('e50feeder/<pk>', E50FeedersGet.as_view(), name="e50feeder"),
    path('e50feederpost', E50FeedersCreate.as_view(), name="e50feederpost"),
    path('e50feederdelete/<pk>', E50FeedersDelete.as_view(),name="e50feederdelete"),
    path('e50feederupdate/<pk>', E50FeedersUpdate.as_view(),name="e50feederupdate"),
    # E50Transformer
    path('e50transformers', E50Transformers.as_view(), name="e50transformers"),
    path('e50transformer/<pk>', E50TransformerGet.as_view(), name="e50transformer"),
    path('e50transformerpost', EE50TransformerCreate.as_view(), name="e50transformerpost"),
    path('e50transformerdelete/<pk>', E50TransformerDelete.as_view(),name="e50transformerdelete"),
    path('e50transformerupdate/<pk>', E50TransformerUpdate.as_view(),name="e50transformerupdate"),
   

    path('station/assets/<parent_assetid>/', StationAssets.as_view(), name="station-assets"),
    path('centre/stations/<depot>/', StationsByCentre.as_view(), name="centre-stations"),
    path('station/transformers/<parent_assetid>/', StationTransformers.as_view(), name="station-transformers"),
    path('station/feeders/<parent_assetid>/', StationFeeders.as_view(), name="station-feeders"),
    path('station/circuitbreakers/<parent_assetid>/', StationCircuitBreakers.as_view(), name="station-circuitbreakers"),
    path('station/isolators/<parent_assetid>/', StationSwitchgearIsolators.as_view(), name="station-isolators"),
    path('transformers/metering/<parent_assetid>/', TransformersMetering.as_view(), name="transformers-metering"),
    path('transformer/lightingarrester/<parent_assetid>/',TransformerLightiningArresters.as_view(),name="transformers-lighting"),
    path('transformer/switchgear/<parent_assetid>/',TransformerSwitchgear.as_view(),name="transformer-switchgear"),
    path('transformer/dfuse/<parent_assetid>/',TransformerDfuses.as_view(),name="transformer-dfuse"),
    path('transformer/e50/<e50_id>/',E50TransformersByE50Id.as_view(),name="e50-transformers"),
    path('e50/feeder/<e50_id>/',E50FeedersByE50Id.as_view(),name="e50-feeders"),
    path('e50/circuitbreaker/<e50_id>/',E50CircuitBreakersByE50Id.as_view(),name="e50-circuitbreakers"),

    path('e50/autodisconnectors/<e50_id>/',E50AutodisconnectorsByE50Id.as_view(),name="e50-autodisconnectors"),
    # path('e50/protectioncubicles/<e50_id>/',E50ProtectionCubiclesByE50Id.as_view(),name="e50-protectioncubicles"),
    # path('e50/controlcubicles/<e50_id>/',E50ControlCubiclesByE50Id.as_view(),name="e50-controlcubicles"),
    path('e50/general/<e50_id>/',E50GeneralByE50Id.as_view(),name="e50-general"),
    path('all_centres/<centreparent>',ParentCentres.as_view(),name='all_centres/')
]
