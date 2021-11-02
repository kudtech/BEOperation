from .models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
import requests



class AppflowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appflow
        fields = '__all__'



class WorkorderSerializers(serializers.ModelSerializer):
    jobs = serializers.StringRelatedField(many=True, read_only=True)
    status = serializers.SlugRelatedField(read_only=True, slug_field='status')


    class Meta:
        model = Workorder
        fields = '__all__'


class WorkorderJobsSerializers(serializers.ModelSerializer):
    jobs = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Workorder
        fields = ['work_order_id', 'jobs']


class JobteamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Jobteam
        fields = '__all__'


class JobprogressSerializers(serializers.ModelSerializer):
    jobteam_members = JobteamSerializers(many=True, read_only=True)
    status = serializers.SlugRelatedField(read_only=True, slug_field='status')

    class Meta:
        model = Jobprogress
        fields = '__all__'
    #This method returns the workorder attribute from the related job [i.e taking advantage of the ForeignKey relationship between Job and Jobprogress]. 
    #This attribute appears on the same level as any other attribute from the jobprogress model
    def get_workorder(self, obj):
        return obj.job.work_order_id
    #This method returns the asset_type attribute from the related job
    def get_asset_type(self, obj):
        return obj.job.asset_type

class JobprogressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobprogress
        fields = '__all__'


class JobsyncSerializers(serializers.ModelSerializer):

    class Meta:
        model = Jobsync
        fields = '__all__'


class JobattachmentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Jobattachment
        fields = '__all__'


class E84LineinspectionSerializers(serializers.ModelSerializer):

    class Meta:
        model = E84Lineinspection
        fields = '__all__'


class E84GeneralSerializers(serializers.ModelSerializer):
    inspections = E84LineinspectionSerializers(many=True, read_only=True)

    class Meta:
        model = E84General
        fields = '__all__'

class PermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class OfficeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'


class JobworkflowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Jobworkflow
        fields = '__all__'


class UserroletrailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Userroletrail
        fields = '__all__'


class TeamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields=['team_leader']


class TeamLeaderSerializer(serializers.ModelSerializer):
    members = TeamSerializers(many=True, read_only=True)

    class Meta:
        model = TeamLeader
        fields = ['team_leader', 'specialisation', 'members']


class TeamLeaderSerializers(serializers.ModelSerializer):
    team = TeamSerializers(write_only=True, many=True)

    class Meta:
        model = TeamLeader
        fields = ['team_leader', 'specialisation', 'team']

    def create(self, validated_data):
        team_data = validated_data.pop('team')         
        team_leader = TeamLeader.objects.create(**validated_data)        
        for data in team_data:        
            team=Team.objects.create(
            team_leader=team_leader,
            specialisation=data['specialisation'],
            team_id=data['team_id'],
            team_member=data['team_member'],
            # created_on=data['created_on'],
            # modified_by=data['modified_by'],
            # modified_on=data['modified_on'],
            # created_by=data['created_by']
            )
            created_team={
                "team_leader":team_leader,
                "team":team
            }
        return team


class RolePermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rolepermission
        fields = '__all__'

class PoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pole
        fields = '__all__'


class UserroleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Userrole
        fields = '__all__'


class JobFormSerializer(serializers.ModelSerializer):     
    assignee_username=serializers.SerializerMethodField('get_assignee_username')
    assignee = serializers.SerializerMethodField('get_assignee_fullname')

    def get_assignee_username(self,obj):       
        return obj.assignee

    def get_assignee_fullname(self, obj):      
        url = "http://172.20.0.10:8082/users/username/" + self.get_assignee_username(obj)
        r = requests.get(url=url)
        data = r.json()       
        return data['firstname'] + " " + data['surname']       

    class Meta:
        model=JobFormsModel
        fields='__all__'

class BoqLabourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boqlabour
        fields = '__all__'


class BoqMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boqmaterial
        fields = '__all__'


class BoqVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boqvehicle
        fields = '__all__'



class E117EquipmentSerializer(serializers.ModelSerializer):  
    class Meta:
        model = E117Equipment
        fields='__all__'


class E117ContractorSerializer(serializers.ModelSerializer):  
    class Meta:
        model = E117Contractor
        fields='__all__'


class E117ReinspectionSerializer(serializers.ModelSerializer):  
    class Meta:
        model = E117Reinspection
        fields='__all__'


class E117Serializer(serializers.ModelSerializer):  
        equipment=E117EquipmentSerializer(read_only=True,many=True) 
        labour=BoqLabourSerializer(read_only=True,many=True)
        materials=BoqMaterialSerializer(read_only=True,many=True)
        vehicles=BoqVehicleSerializer(read_only=True,many=True)
    
        class Meta:
            model = E117
            fields=['e117_id','job','client_inspection_type','e117client','client_contractor','soi_size','soi_voltage','soi_conduit','soi_switch_type','soi_switch_capacity','soi_switch_setting','insd_neutrals_fused',
    'insd_neutrals_fused_cmt','insd_block_fitted','insd_block_fitted_cmt','insd_electrode_installed','insd_electrode_installed_cmt','insd_electrode_type' ,
    'insd_bonded_earth','insd_bonded_earth_cmt','insd_polarity_switches','insd_outlets_earthed','insd_outlets_earthed_cmt','insd_socket_outlets', 
    'insd_type_wiring','insd_conductors_size','insd_conductors_size_cmt','insd_condition_wiring','insd_condition_wiring_cmt','insd_cord_positions', 
    'insd_bathroom_switch','insd_bathroom_switch_cmt','insd_unearthed_metalclad','inst_megger_ln','inst_megger_le','inst_megger_ne',
    'inst_continuity_resistance','conduits_conduits_bushed','conduits_conduits_bushed_cmt','conduits_bonded','conduits_bonded_cmt','conduits_correct_size',
    'conduits_correct_size_cmt','conduits_adequately_supported','conduits_adequately_supported_cmt','conduits_suitable_type','conduits_suitable_type_cmt' ,
    'lighting_lighting_points','lighting_maximum_lighting_points','plugs_plug_points','plugs_maximum_plug_points','appliances_number_motors', 
    'appliances_size_motors','appliances_motor_installation','appliances_motor_installation_cmt','appliances_outbuildings_switches',
    'appliances_outbuildings_switches_cmt','oh_height_satisfactory','oh_height_satisfactory_cmt','oh_support_satisfactory',
    'oh_support_satisfactory_cmt','oh_conductor_size','oh_condition_line','oh_condition_line_cmt','oh_earthwires_fitted','oh_earthwires_fitted_cmt', 
    'defects_installation','defects_contractor','defects_contractor_cmt','general_switch_details','general_supply_status','general_installation_status',
    'general_installation_status_cmt','boq_connection_duration_hr','datetime_completed','completed_by','designation','number_of_clients','customer_type','modified_by','modified_on',
    'created_by','created_on' ,'equipment','labour','materials','vehicles']


class ClientSerializer(serializers.ModelSerializer):
    e117=E117Serializer(read_only=True,many=True)
    class Meta:
        model = E117Client
        fields = ['client_id','client_name','property_address','client_phone','geom','owner_name','owner_address','email_address','meter_number','account_number','connection_type','tariff','number_of_clients','customer_type','e117']
        


class JobSerializer(serializers.ModelSerializer):
    job_progress = JobprogressSerializers(many=True, read_only=True)
    # e117=E117Serializer(many=True,read_only=True)

    class Meta:
        model = Job
        fields = '__all__'

class JobSerializerOnly(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(read_only=True, slug_field='status')


    class Meta:
        model = Job
        fields = '__all__'


class WorkorderSerializer(serializers.ModelSerializer):
    jobs=JobSerializerOnly(many=True,read_only=True)

    class Meta:
        model=Workorder
        fields=['jobs']


class FeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeder
        fields = '__all__'


class LightningArresterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lightningarrester
        fields = '__all__'


class SubstationMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substationmeter
        fields = '__all__'


class SwitchgearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switchgear
        fields = '__all__'


class TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = '__all__'





class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStatus
        fields = '__all__'


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = '__all__'


class CentreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centre
        fields = '__all__'

class RoleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roleprofile
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user_profiles=UserProfileSerializer(read_only=True,many=True)
    role_profiles=RoleProfileSerializer(read_only=True,many=True)
    class Meta:
        model = Profile
        fields = ['profile_code','profile_name','dt_created','created_by','user_profiles','role_profiles']


class WorkflowSerializer(serializers.ModelSerializer):
    job_workflows=JobworkflowSerializers(read_only=True,many=True)
    class Meta:
        model=Workflow
        fields=['workflow_id','workflow_code','step','role_code','created_on','modified_by','modified_on','created_by','approve','reject','section','job_workflows']   

class AppFlowSerializer(serializers.ModelSerializer):
    app_workflows = WorkflowSerializer(read_only=True,many=True)
    related_jobs=JobSerializer(read_only=True,many=True)
    class Meta:
        model = Appflow
        fields = ['appflow_id', 'section','app','workflow_code','modified_by','created_by','description','created_on','modified_on', 'app_workflows','related_jobs']


class RoleSerializers(serializers.ModelSerializer):
    workflows = WorkflowSerializer(read_only=True,many=True)
    roles=RoleProfileSerializer(read_only=True,many=True)
    class Meta:
        model = Role
        fields = ['role_code','role_name','description','app','dt_created','created_by','workflows','roles']

class JobWorkflowStatusSerializers(serializers.ModelSerializer):   
    class Meta:
        model = JobWorkflowStatus
        fields='__all__'


class JobsForReinpsectionSerializers(serializers.ModelSerializer):  
    status = serializers.SlugRelatedField(read_only=True, slug_field='status') 
    class Meta:
        model = JobsForReinspectionModel
        fields='__all__'



class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class TransformersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transformer
        fields = '__all__'
    
class AssetRelationshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assetrships
        fields = '__all__'

class E50ControlcubicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = E50Controlcubicle
        fields = '__all__'

class E50ProtectioncubicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = E50Protectioncubicle
        fields = '__all__'



class E50Serializer(serializers.ModelSerializer):
    class Meta:
        model = E50
        fields = '__all__'

class E50AutodisconnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = E50Autodisconnector
        fields = '__all__'

class E50CircuitbreakersSerializer(serializers.ModelSerializer):
    class Meta:
        model = E50Circuitbreakers
        fields = '__all__'

class E50FeedersSerializer(serializers.ModelSerializer):
    class Meta:
        model = E50Feeders
        fields = '__all__'


class E50TransformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = E50Transformer
        fields = '__all__'

class MeteringSerializers(serializers.ModelSerializer):
    class Meta:
        model = Metering
        fields = '__all__'

class DfuseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dfuse
        fields = '__all__'
        
class E60Serializer(serializers.ModelSerializer):
    class Meta:
        model = E60
        fields = '__all__'

class E60TransformerSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = E60Transformer
        fields = '__all__'

class E60LtlightningarresterSerializer(serializers.ModelSerializer):
    class Meta:
        model = E60Ltlightningarrester
        fields = '__all__'

class E60SubgeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = E60Subgeneral
        fields = '__all__'

class E60MeteringSerializers(serializers.ModelSerializer):
    class Meta:
        model = E60Metering
        fields = '__all__'

class E60SwitchgearSerializers(serializers.ModelSerializer):

    class Meta:
        model = E60Switchgear
        fields = '__all__'


class E60HtlightningarresterSerializers(serializers.ModelSerializer):
    class Meta:
        model = E60Htlightningarrester
        fields = '__all__'


class E60DfusesSerializers(serializers.ModelSerializer):
    class Meta:
        model = E60Dfuse
        fields = '__all__'

class E60SafetySerializers(serializers.ModelSerializer):
    class Meta:
        model= E60Safety
        fields = '__all__'

class E60HousingSerializers(serializers.ModelSerializer):
    class Meta:
        model = E60Housing
        fields = '__all__'

