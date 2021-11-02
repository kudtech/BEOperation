# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.



from django.db import models
from django.utils import timezone
from .managers import JobManager,JobWorkflowManager, AssetRelationshipManager
from datetime import datetime
from django.utils.timezone import now

class Appflow(models.Model):
    workflow_code = models.CharField(primary_key=True, max_length=100)
    section = models.CharField(max_length=100, blank=True, null=True)
    app = models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appflow'


class JobStatus(models.Model):
    job_status_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobstatus'

    
    def __str__(self):
        return '%s' % self.status


class Workorder(models.Model):
    created_by = models.CharField(max_length=100, blank=False, null=False)
    created_on = models.DateTimeField(default=now, editable=False)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    work_order_id = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=100, blank=False, null=False)
    centre = models.CharField(max_length=100, blank=False, null=False)
    comments = models.CharField(max_length=100, blank=True, null=True)
    status = models.ForeignKey(JobStatus, on_delete=models.CASCADE, db_column='status',default=1, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'workorder'

        
    def __str__(self):
        return self.description

class Job(models.Model):
    created_by = models.CharField(max_length=100, blank=False, null=False)
    created_on = models.DateTimeField(default=now, editable=False)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    job_id = models.CharField(primary_key=True, max_length=100)
    work_order = models.ForeignKey('Workorder', on_delete=models.CASCADE, db_column='work_order_id',related_name='jobs')
    type = models.ForeignKey('Jobtype', on_delete=models.CASCADE, db_column='type', blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    asset_id = models.CharField(max_length=100, blank=True, null=True)
    assignee = models.CharField(max_length=100, blank=False, null=False)
    comments = models.TextField(blank=True, null=True)
    closed_by = models.CharField(max_length=100, blank=True, null=True)
    closed_dt = models.DateTimeField(blank=True, null=True)
    asset_name = models.CharField(max_length=100, blank=True, null=True)
    asset_type = models.CharField(max_length=100, blank=True, null=True)
    asset_number = models.CharField(max_length=100, blank=True, null=True)
    expected_end_dt = models.DateField(blank=True, null=True)
    reference_no = models.CharField(max_length=100, blank=True, null=True)
    asset_serial = models.CharField(max_length=100, blank=True, null=True)
    geom = models.TextField(blank=True,null=True) 
    workflow = models.ForeignKey('Appflow', on_delete=models.CASCADE,db_column='workflow_id',related_name='related_jobs')
    rowid = models.IntegerField(blank=True, null=True)
    rowversion = models.IntegerField(blank=True, null=True)
    sync_status = models.IntegerField(blank=True, null=True,default=0)
    status = models.ForeignKey('Jobstatus', on_delete=models.CASCADE, db_column='status', blank=False, null=False)
    trigger = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    # Override default Job Manager
    objects=JobManager()
   


    class Meta:
        managed = False
        db_table = 'job'
    def __str__(self):
        return self.job_id

class Feeder(models.Model):
    depot = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    assetno = models.CharField(max_length=100, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=100, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    feederno = models.CharField(max_length=100, blank=True, null=True)
    modifiedby = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    districtid = models.CharField(max_length=100, blank=True, null=True)
    wardid = models.CharField(max_length=100, blank=True, null=True)
    provinceid = models.CharField(max_length=100, blank=True, null=True)
    id = models.CharField(max_length=100, blank=True, null=True)
    feedercode = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom2d = models.TextField(blank=True, null=True)  # This field type is a guess.
    sourcesscode = models.CharField(max_length=20, blank=True, null=True)
    voltagelevel = models.FloatField(blank=True, null=True)
    asset_change = models.CharField(max_length=100, blank=True, null=True)
    trregion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feeder'


    def __str__(self):
        return self.name

class Lightningarrester(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    lightningarrester_id = models.CharField(primary_key=True, max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    make = models.CharField(max_length=100, blank=True, null=True)
    ht_lt = models.CharField(max_length=100, blank=True, null=True)
    voltage_rating = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    kvar_rating = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    phase = models.CharField(max_length=100, blank=True, null=True)
    centre = models.CharField(max_length=100, blank=True, null=True)
    geom2d = models.TextField(blank=True, null=True)  # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'lightningarrester'
    def __str__(self):
        return self.lightning_arrester_id


class Station(models.Model):
    depot = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    assetno = models.CharField(max_length=100, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=100, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    districtid = models.CharField(max_length=100, blank=True, null=True)
    wardid = models.CharField(max_length=100, blank=True, null=True)
    provinceid = models.CharField(max_length=100, blank=True, null=True)
    id = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    classification = models.CharField(max_length=20, blank=True, null=True)
    enclosure = models.CharField(max_length=20, blank=True, null=True)
    landownership = models.CharField(max_length=20, blank=True, null=True)
    controlbuilding = models.BooleanField(blank=True, null=True)
    guardroom = models.BooleanField(blank=True, null=True)
    fireprotection = models.CharField(max_length=20, blank=True, null=True)
    expcubicle = models.BooleanField(blank=True, null=True)
    transformerbaysno = models.IntegerField(blank=True, null=True)
    feederbaysno = models.IntegerField(blank=True, null=True)
    exmcubicle = models.BooleanField(blank=True, null=True)
    incomerbaysno = models.IntegerField(blank=True, null=True)
    hvbussectionsno = models.IntegerField(blank=True, null=True)
    lvbussectionsno = models.IntegerField(blank=True, null=True)
    hvreservebusbar = models.BooleanField(blank=True, null=True)
    lvreservebusbar = models.BooleanField(blank=True, null=True)
    lvtiebar = models.BooleanField(blank=True, null=True)
    dmbusbar = models.BooleanField(blank=True, null=True)
    hvbstype = models.CharField(max_length=20, blank=True, null=True)
    lvbstype = models.CharField(max_length=20, blank=True, null=True)
    perimeterlights = models.BooleanField(blank=True, null=True)
    baylights = models.BooleanField(blank=True, null=True)
    buscoupler = models.BooleanField(blank=True, null=True)
    rtuinstalled = models.BooleanField(blank=True, null=True)
    batterybankoutput = models.IntegerField(blank=True, null=True)
    rcequipment = models.CharField(max_length=20, blank=True, null=True)
    geom2d = models.TextField()  # This field type is a guess.
    stationid = models.CharField(primary_key=True, max_length=100)
    geom3d = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_change = models.CharField(max_length=100, blank=True, null=True)
    trregion = models.CharField(max_length=50, blank=True, null=True)

   

    class Meta:
        managed = False
        db_table = 'station'

    def __str__(self):
        return self.stationid


class Substationmeter(models.Model):
    meter_id = models.CharField(primary_key=True, max_length=100)
    meter_no = models.CharField(max_length=100, blank=True, null=True)
    equipment_id = models.CharField(max_length=100, blank=True, null=True)
    make = models.CharField(max_length=100, blank=True, null=True)
    amps = models.CharField(max_length=100, blank=True, null=True)
    volts = models.CharField(max_length=100, blank=True, null=True)
    voltage = models.CharField(max_length=100, blank=True, null=True)
    maker_type = models.CharField(max_length=100, blank=True, null=True)
    maker_serial_number = models.CharField(max_length=100, blank=True, null=True)
    zetdc_number = models.CharField(max_length=100, blank=True, null=True)
    vad_transformer_zetdc_number = models.CharField(max_length=100, blank=True, null=True)
    ct_ratio = models.CharField(max_length=100, blank=True, null=True)
    meter_protection_type = models.CharField(max_length=100, blank=True, null=True)
    constant_rx = models.CharField(max_length=100, blank=True, null=True)
    feeder_id_field = models.CharField(db_column='feeder_id ', max_length=100, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    status = models.CharField(max_length=100, blank=True, null=True)
    centre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'substationmeter'
    def __str__(self):
        return self.meter_id
        return self.equipment_id


class Switchgear(models.Model):
    depot = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    assetno = models.CharField(max_length=100, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=100, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    districtid = models.CharField(max_length=100, blank=True, null=True)
    wardid = models.CharField(max_length=100, blank=True, null=True)
    provinceid = models.CharField(max_length=100, blank=True, null=True)
    id = models.CharField(max_length=100, blank=True, null=True)
    switchgearid = models.CharField(primary_key=True, max_length=100)
    serialno = models.CharField(max_length=20, blank=True, null=True)
    make = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    constructiontype = models.CharField(max_length=20, blank=True, null=True)
    mco = models.CharField(max_length=20, blank=True, null=True)
    opmech = models.CharField(max_length=20, blank=True, null=True)
    busbarsno = models.IntegerField(blank=True, null=True)
    optype = models.CharField(max_length=20, blank=True, null=True)
    standard = models.CharField(max_length=10, blank=True, null=True)
    voltagerating = models.FloatField(blank=True, null=True)
    insulationmedium = models.CharField(max_length=50, blank=True, null=True)
    interruptingmedium = models.CharField(max_length=50, blank=True, null=True)
    ratedcc = models.FloatField(blank=True, null=True)
    ratedscbc = models.FloatField(blank=True, null=True)
    ratedmc = models.FloatField(blank=True, null=True)
    ratedscwt = models.FloatField(blank=True, null=True)
    ratedstwc = models.FloatField(blank=True, null=True)
    controlvoltage = models.FloatField(blank=True, null=True)
    motorost = models.CharField(max_length=20, blank=True, null=True)
    motorvoltage = models.FloatField(blank=True, null=True)
    auxvoltage = models.FloatField(blank=True, null=True)
    possiblecountsetting = models.IntegerField(blank=True, null=True)
    autoreclosingtype = models.CharField(max_length=20, blank=True, null=True)
    dutycycle = models.CharField(max_length=20, blank=True, null=True)
    netmass = models.FloatField(blank=True, null=True)
    ocinstalled = models.BooleanField(blank=True, null=True)
    bil = models.FloatField(blank=True, null=True)
    commissionyear = models.IntegerField(blank=True, null=True)
    installationyear = models.IntegerField(blank=True, null=True)
    baytype = models.CharField(max_length=20, blank=True, null=True)
    use = models.TextField(blank=True, null=True)
    tripcoilsno = models.IntegerField(blank=True, null=True)
    normalopstatus = models.CharField(max_length=20, blank=True, null=True)
    cdpoint = models.BooleanField(blank=True, null=True)
    feedercode = models.CharField(max_length=50, blank=True, null=True)
    geom2d = models.TextField()  # This field type is a guess.
    mvboard = models.CharField(max_length=30, blank=True, null=True)
    switchgearno = models.CharField(max_length=30, blank=True, null=True)
    geom3d = models.TextField(blank=True, null=True)  # This field type is a guess.
    nostatus = models.CharField(max_length=20, blank=True, null=True)
    manufactureyear = models.IntegerField(blank=True, null=True)
    installed_on = models.CharField(max_length=100, blank=True, null=True)
    asset_change = models.CharField(max_length=100, blank=True, null=True)
    trregion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'switchgear'

    def __str__(self):
        return self.switchgearid


class Transformer(models.Model):
    depot = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    assetno = models.CharField(max_length=100, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=100, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
    modifiedby = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    districtid = models.CharField(max_length=100, blank=True, null=True)
    wardid = models.CharField(max_length=100, blank=True, null=True)
    provinceid = models.CharField(max_length=100, blank=True, null=True)
    id = models.CharField(max_length=100, blank=True, null=True)
    transformerid = models.CharField(primary_key=True, max_length=100)
    serialno = models.CharField(max_length=50, blank=True, null=True)
    sscode = models.CharField(max_length=50, blank=True, null=True)
    systemno = models.CharField(max_length=50, blank=True, null=True)
    highvoltage = models.FloatField()
    lowvoltage = models.FloatField()
    application = models.CharField(max_length=20, blank=True, null=True)
    mounting = models.CharField(max_length=20, blank=True, null=True)
    voltageratio = models.CharField(max_length=20, blank=True, null=True)
    standard = models.CharField(max_length=50, blank=True, null=True)
    make = models.CharField(max_length=50, blank=True, null=True)
    transformerinsulation = models.CharField(max_length=20, blank=True, null=True)
    manufactureryear = models.IntegerField(blank=True, null=True)
    installationyear = models.IntegerField(blank=True, null=True)
    commissionyear = models.IntegerField(blank=True, null=True)
    windingsno = models.CharField(max_length=20, blank=True, null=True)
    bil = models.FloatField(blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    vectorgroup = models.CharField(max_length=20, blank=True, null=True)
    impedance = models.FloatField(blank=True, null=True)
    ironlosses = models.FloatField(blank=True, null=True)
    copperlosses = models.FloatField(blank=True, null=True)
    taperange = models.IntegerField(blank=True, null=True)
    cooling = models.CharField(max_length=30, blank=True, null=True)
    capacity = models.DecimalField(max_digits=10, decimal_places=1)
    geom2d = models.TextField()  # This field type is a guess.
    name = models.CharField(max_length=50, blank=True, null=True)
    maxcapacity = models.CharField(max_length=15, blank=True, null=True)
    windings = models.CharField(max_length=25, blank=True, null=True)
    geom3d = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_change = models.CharField(max_length=100, blank=True, null=True)
    trregion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transformer'

    def __str__(self):
        return self.transformerid

class Boqlabour(models.Model):
    boq_labour_id = models.CharField(primary_key=True, max_length=100)
    e117 = models.ForeignKey('E117', on_delete=models.CASCADE, blank=True, null=True,related_name='labour')
    labour_class = models.CharField(max_length=100, blank=True, null=True)
    number_of_people = models.CharField(max_length=100, blank=True, null=True)
    man_hours = models.CharField(max_length=100, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boqlabour'


class Boqmaterial(models.Model):
    boq_id = models.CharField(primary_key=True, max_length=100)
    e117 = models.ForeignKey('E117', on_delete=models.CASCADE, blank=True, null=True,related_name='materials')
    material = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=100, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boqmaterial'


class Boqvehicle(models.Model):
    boq_vehicle_id = models.CharField(primary_key=True, max_length=100)
    e117 = models.ForeignKey('E117', on_delete=models.CASCADE, blank=True, null=True,related_name='vehicles')
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    no_of_vehicles = models.CharField(max_length=100, blank=True, null=True)
    distance = models.CharField(max_length=100, blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boqvehicle'


class E117(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e117_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=True, null=True,related_name='e117',db_column="job_id")
    client_inspection_type = models.CharField(max_length=250, blank=True, null=True)
    e117client = models.ForeignKey('E117Client', on_delete=models.CASCADE, blank=True, null=True,related_name='e117')
    client_contractor = models.ForeignKey('E117Contractor', on_delete=models.CASCADE, blank=True, null=True,related_name='e117')
    soi_size = models.IntegerField(blank=True, null=True)
    soi_voltage = models.IntegerField(blank=True, null=True)
    soi_conduit = models.IntegerField(blank=True, null=True)
    soi_switch_type = models.CharField(max_length=250, blank=True, null=True)
    soi_switch_capacity = models.FloatField(blank=True, null=True)
    soi_switch_setting = models.FloatField(blank=True, null=True)
    insd_neutrals_fused = models.CharField(max_length=20, blank=True, null=True)
    insd_neutrals_fused_cmt = models.TextField(blank=True, null=True)
    insd_block_fitted = models.CharField(max_length=20, blank=True, null=True)
    insd_block_fitted_cmt = models.TextField(blank=True, null=True)
    insd_electrode_installed = models.CharField(max_length=20, blank=True, null=True)
    insd_electrode_installed_cmt = models.TextField(blank=True, null=True)
    insd_electrode_type = models.CharField(max_length=250, blank=True, null=True)
    insd_bonded_earth = models.CharField(max_length=20, blank=True, null=True)
    insd_bonded_earth_cmt = models.TextField(blank=True, null=True)
    insd_polarity_switches = models.CharField(max_length=250, blank=True, null=True)
    insd_outlets_earthed = models.CharField(max_length=20, blank=True, null=True)
    insd_outlets_earthed_cmt = models.TextField(blank=True, null=True)
    insd_socket_outlets = models.CharField(max_length=250, blank=True, null=True)
    insd_type_wiring = models.CharField(max_length=250, blank=True, null=True)
    insd_conductors_size = models.CharField(max_length=20, blank=True, null=True)
    insd_conductors_size_cmt = models.TextField(blank=True, null=True)
    insd_condition_wiring = models.CharField(max_length=20, blank=True, null=True)
    insd_condition_wiring_cmt = models.TextField(blank=True, null=True)
    insd_cord_positions = models.CharField(max_length=250, blank=True, null=True)
    insd_bathroom_switch = models.CharField(max_length=20, blank=True, null=True)
    insd_bathroom_switch_cmt = models.TextField(blank=True, null=True)
    insd_unearthed_metalclad = models.CharField(max_length=250, blank=True, null=True)
    inst_megger_ln = models.FloatField(blank=True, null=True)
    inst_megger_le = models.FloatField(blank=True, null=True)
    inst_megger_ne = models.FloatField(blank=True, null=True)
    inst_continuity_resistance = models.IntegerField(blank=True, null=True)
    conduits_conduits_bushed = models.CharField(max_length=20, blank=True, null=True)
    conduits_conduits_bushed_cmt = models.TextField(blank=True, null=True)
    conduits_bonded = models.CharField(max_length=20, blank=True, null=True)
    conduits_bonded_cmt = models.TextField(blank=True, null=True)
    conduits_correct_size = models.CharField(max_length=20, blank=True, null=True)
    conduits_correct_size_cmt = models.TextField(blank=True, null=True)
    conduits_adequately_supported = models.CharField(max_length=20, blank=True, null=True)
    conduits_adequately_supported_cmt = models.TextField(blank=True, null=True)
    conduits_suitable_type = models.CharField(max_length=20, blank=True, null=True)
    conduits_suitable_type_cmt = models.TextField(blank=True, null=True)
    lighting_lighting_points = models.IntegerField(blank=True, null=True)
    lighting_maximum_lighting_points = models.IntegerField(blank=True, null=True)
    plugs_plug_points = models.IntegerField(blank=True, null=True)
    plugs_maximum_plug_points = models.IntegerField(blank=True, null=True)
    appliances_number_motors = models.IntegerField(blank=True, null=True)
    appliances_size_motors = models.IntegerField(blank=True, null=True)
    appliances_motor_installation = models.CharField(max_length=20, blank=True, null=True)
    appliances_motor_installation_cmt = models.TextField(blank=True, null=True)
    appliances_outbuildings_switches = models.CharField(max_length=20, blank=True, null=True)
    appliances_outbuildings_switches_cmt = models.TextField(blank=True, null=True)
    oh_height_satisfactory = models.CharField(max_length=20, blank=True, null=True)
    oh_height_satisfactory_cmt = models.TextField(blank=True, null=True)
    oh_support_satisfactory = models.CharField(max_length=20, blank=True, null=True)
    oh_support_satisfactory_cmt = models.TextField(blank=True, null=True)
    oh_conductor_size = models.IntegerField(blank=True, null=True)
    oh_condition_line = models.CharField(max_length=20, blank=True, null=True)
    oh_condition_line_cmt = models.TextField(blank=True, null=True)
    oh_earthwires_fitted = models.CharField(max_length=20, blank=True, null=True)
    oh_earthwires_fitted_cmt = models.TextField(blank=True, null=True)
    defects_installation = models.CharField(max_length=250, blank=True, null=True)
    defects_contractor = models.CharField(max_length=20, blank=True, null=True)
    defects_contractor_cmt = models.TextField(blank=True, null=True)
    general_switch_details = models.CharField(max_length=250, blank=True, null=True)
    general_supply_status = models.CharField(max_length=20, blank=True, null=True)
    general_installation_status = models.CharField(max_length=100, blank=True, null=True)
    general_installation_status_cmt = models.TextField(blank=True, null=True)
    boq_connection_duration_hr = models.FloatField(blank=True, null=True)
    datetime_completed = models.DateTimeField(blank=True, null=True)
    completed_by = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    number_of_clients = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e117'
        verbose_name_plural='E117(Inspection Reports)'

    def __str__(self):
        return self.e117_id


class E117Equipment(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    equipment_id = models.CharField(primary_key=True, max_length=250)
    e117 = models.ForeignKey(E117, on_delete=models.CASCADE, blank=True, null=True,related_name='equipment')
    description = models.CharField(max_length=250, blank=True, null=True)
    wattage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e117equipment'
        verbose_name_plural='E117 Equipment'

    def __str__(self):
        return self.equipment_id



class E117Reinspection(models.Model):
    reinspection_id = models.CharField(primary_key=True, max_length=100)
    e117 = models.ForeignKey(E117, on_delete=models.CASCADE, blank=True, null=True)
    receipt_no = models.CharField(max_length=100, blank=True, null=True)
    date_paid = models.DateField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    service_number = models.CharField(max_length=100, blank=True, null=True)
    
    

    class Meta:
        managed = False
        db_table = 'e117reinspection'
        verbose_name_plural='E117 Reinspection Receipts'

    def __str__(self):
        return self.reinspection_id


class E117Client(models.Model):
    client_id = models.CharField(primary_key=True, max_length=100)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    property_address = models.CharField(max_length=100, blank=True, null=True)
    client_phone = models.CharField(max_length=100, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    owner_address = models.TextField(blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    meter_number = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    connection_type = models.CharField(max_length=100, blank=True, null=True)
    tariff = models.CharField(max_length=100, blank=True, null=True)
    number_of_clients = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e117client'
        verbose_name_plural='E117 Clients'

    def __str__(self):
        return self.client_name


class E117Contractor(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e117contractor_id = models.CharField(primary_key=True, max_length=100)
    contractor_name = models.CharField(max_length=100, blank=True, null=True)
    contractor_address = models.CharField(max_length=100, blank=True, null=True)
    contractor_phone = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e117contractor'
        verbose_name_plural='E117 Contractors'

    def __str__(self):
        return self.e117contractor_id


class E50Controlcubicle(models.Model):
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    control_cubicle_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    clean_relays_operate = models.CharField(max_length=100, blank=True, null=True)
    fuses_links_position = models.CharField(max_length=100, blank=True, null=True)
    lamps_indicating = models.CharField(max_length=100, blank=True, null=True)
    clean_panel_wiring_inorder = models.CharField(max_length=100, blank=True, null=True)
    cubicle_lights_heaters = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    section_completed = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e50controlcubicle'









class E50Protectioncubicle(models.Model):
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    protection_cubicle_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=True, null=True)
    relay_satisf_flag_reset = models.CharField(max_length=100, blank=True, null=True)
    sef_uniselector_reset = models.CharField(max_length=100, blank=True, null=True)
    fuses_links_position = models.CharField(max_length=100, blank=True, null=True)
    clean_panel_wiring_inorder = models.CharField(max_length=100, blank=True, null=True)
    float_voltage = models.CharField(max_length=100, blank=True, null=True)
    charger_current = models.CharField(max_length=100, blank=True, null=True)
    switch_off_charger = models.CharField(max_length=100, blank=True, null=True)
    battery_voltage = models.CharField(max_length=100, blank=True, null=True)
    min_cell_voltage = models.CharField(max_length=100, blank=True, null=True)
    load_test = models.CharField(max_length=100, blank=True, null=True)
    top_up_cells = models.CharField(max_length=100, blank=True, null=True)
    clean_terminal = models.CharField(max_length=100, blank=True, null=True)
    terminal_connections = models.CharField(max_length=100, blank=True, null=True)
    switch_on_charger = models.CharField(max_length=100, blank=True, null=True)
    cubicle_lights_heaters = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    section_completed = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e50protectioncubicle'


class Metering(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    metering_id = models.CharField(primary_key=True, max_length=100)
    make = models.CharField(max_length=100, blank=True, null=True)
    amps = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    volts = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    maker_type = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    zesa_number = models.CharField(max_length=100, blank=True, null=True)
    vad_transformer_no = models.CharField(max_length=100, blank=True, null=True)
    ct_ratio = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    protection_type = models.CharField(max_length=100, blank=True, null=True)
    geom2d = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'metering'



class E60(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    # transformer = models.ForeignKey('Transformer', on_delete=models.CASCADE, blank=True, null=True)
    e60_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    transformer = models.ForeignKey('Transformer', models.DO_NOTHING, blank=True, null=True)
    e60_dt = models.DateTimeField(blank=True, null=True)
    line_section = models.CharField(max_length=100, blank=True, null=True)
    construction_type = models.CharField(max_length=100, blank=True, null=True)
    type_of_work = models.CharField(max_length=100, blank=True, null=True)
    sub_condition = models.CharField(max_length=100, blank=True, null=True)
    condition_cmt = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    completed_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60'
    
    def __str__(self):
        return self.e60_id



class Dfuse(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    dfuse_id = models.CharField(primary_key=True, max_length=100)
    rating = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    dfuse_type = models.CharField(max_length=100, blank=True, null=True)
    phase = models.CharField(max_length=100, blank=True, null=True)
    geom2d = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'dfuse'

class E60Dfuse(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60dfuse_id = models.CharField(null = False,primary_key=True,max_length=100)
    e60_id = models.CharField(max_length=100, blank=True, null=True)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    washers_fitted = models.CharField(max_length=100, blank=True, null=True)
    washers_fitted_cmt = models.TextField(blank=True, null=True)
    holders_drop_freely = models.CharField(max_length=100, blank=True, null=True)
    holders_drop_freely_cmt = models.TextField(blank=True, null=True)
    holders_make_contact = models.CharField(max_length=100, blank=True, null=True)
    holders_make_contact_cmt = models.TextField(blank=True, null=True)
    contacts_treated = models.CharField(max_length=100, blank=True, null=True)
    contacts_treated_cmt = models.TextField(blank=True, null=True)
    dfuse = models.ForeignKey('Dfuse', models.DO_NOTHING, blank=True, null=True)
    asset_change = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60dfuse'


class E60Housing(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60housing_id = models.CharField(primary_key=True, max_length=100)
    e60_id = models.CharField(max_length=100, blank=True, null=True)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    housing_type = models.CharField(max_length=100, blank=True, null=True)
    housing_weatherproof = models.CharField(max_length=100, blank=True, null=True)
    housing_weatherproof_cmt = models.TextField(blank=True, null=True)
    door_weatherproof = models.CharField(max_length=100, blank=True, null=True)
    door_weatherproof_cmt = models.TextField(blank=True, null=True)
    door_padlocks = models.CharField(max_length=100, blank=True, null=True)
    door_padlocks_cmt = models.TextField(blank=True, null=True)
    padlock_lubricated = models.CharField(max_length=100, blank=True, null=True)
    padlock_lubricated_cmt = models.TextField(blank=True, null=True)
    paintwork = models.CharField(max_length=100, blank=True, null=True)
    paintwork_cmt = models.TextField(blank=True, null=True)
    outlet_conduit = models.CharField(max_length=100, blank=True, null=True)
    outlet_conduit_cmt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60housing'

class E60Htlightningarrester(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60htlightningarrester_id = models.CharField(max_length=100,primary_key=True, blank=True)
    e60 = models.ForeignKey(E60, models.DO_NOTHING, blank=True, null=True)
    lightningarrester_id = models.CharField(null = False,max_length=100)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    dfuse_connection = models.CharField(max_length=100, blank=True, null=True)
    dfuse_connection_cmt = models.TextField(blank=True, null=True)
    rails_connection = models.CharField(max_length=100, blank=True, null=True)
    rails_connection_cmt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60htlightningarrester'



class E60Ltlightningarrester(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60ltlightningarrester_id = models.CharField(max_length=100,primary_key=True, blank=True)
    e60 = models.ForeignKey(E60, models.DO_NOTHING, blank=True, null=True)
    lightningarrester_id = models.CharField(null = False,max_length=100)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    capacitor_satisfactory = models.CharField(max_length=100, blank=True, null=True)
    capacitor_satisfactory_cmt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60ltlightningarrester'


class E60Metering(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60metering_id = models.CharField(primary_key=True, max_length=100)
    e60 = models.ForeignKey(E60, models.DO_NOTHING, blank=True, null=True)
    metering = models.ForeignKey('Metering', models.DO_NOTHING, blank=True, null=True)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    meter_case_earthed = models.CharField(max_length=100, blank=True, null=True)
    meter_case_earthed_cmt = models.TextField(blank=True, null=True)
    fuses_condition = models.CharField(max_length=100, blank=True, null=True)
    fuses_condition_cmt = models.TextField(blank=True, null=True)
    phase_rotation = models.CharField(max_length=100, blank=True, null=True)
    connections_tight = models.CharField(max_length=100, blank=True, null=True)
    connections_tight_cmt = models.TextField(blank=True, null=True)
    metering_sealed = models.CharField(max_length=100, blank=True, null=True)
    metering_sealed_cmt = models.TextField(blank=True, null=True)
    cards_available = models.CharField(max_length=100, blank=True, null=True)
    cards_available_cmt = models.TextField(blank=True, null=True)
    asset_change = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60metering'

class E60Safety(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60safety_id = models.CharField(primary_key=True, max_length=100)
    e60 = models.ForeignKey(E60, models.DO_NOTHING, blank=True, null=True)
    danger_notices = models.CharField(max_length=100, blank=True, null=True)
    danger_notices_cmt = models.TextField(blank=True, null=True)
    anti_climbing = models.CharField(max_length=100, blank=True, null=True)
    anti_climbing_cmt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60safety'


class E60Subgeneral(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60subgeneral_id = models.CharField(primary_key=True, max_length=100)
    e60 = models.ForeignKey(E60, models.DO_NOTHING, blank=True, null=True)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    earth_resistance = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    earth_electrodes = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    structures_bonded = models.CharField(max_length=100, blank=True, null=True)
    structures_bonded_cmt = models.TextField(blank=True, null=True)
    sheath_bonded = models.CharField(max_length=100, blank=True, null=True)
    sheath_bonded_cmt = models.TextField(blank=True, null=True)
    mains_condition = models.CharField(max_length=100, blank=True, null=True)
    mains_condition_cmt = models.TextField(blank=True, null=True)
    poles_condition = models.CharField(max_length=100, blank=True, null=True)
    poles_condition_cmt = models.TextField(blank=True, null=True)
    paint_work = models.CharField(max_length=100, blank=True, null=True)
    paint_work_cmt = models.TextField(blank=True, null=True)
    vegetation_undergrowth = models.CharField(max_length=100, blank=True, null=True)
    vegetation_undergrowth_cmt = models.TextField(blank=True, null=True)
    site_access = models.CharField(max_length=100, blank=True, null=True)
    site_access_cmt = models.TextField(blank=True, null=True)
    lt_mains = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60subgeneral'


class E60Switchgear(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60switchgear_id = models.CharField(primary_key=True, max_length=100)
    e60 = models.ForeignKey(E60, models.DO_NOTHING, blank=True, null=True)
    switchgear = models.ForeignKey('Switchgear', models.DO_NOTHING, blank=True, null=True)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    trip_setting = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    oil_condition = models.CharField(max_length=100, blank=True, null=True)
    oil_condition_cmt = models.TextField(blank=True, null=True)
    contacts_condition = models.CharField(max_length=100, blank=True, null=True)
    contacts_condition_cmt = models.TextField(blank=True, null=True)
    conn_conditions = models.CharField(max_length=100, blank=True, null=True)
    conn_conditions_cmt = models.TextField(blank=True, null=True)
    consumer_trip_setting = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    asset_change = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60switchgear'


class E60Transformer(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e60transformer_id = models.CharField(primary_key=True, max_length=100)
    e60 = models.ForeignKey('E60', models.DO_NOTHING, blank=True, null=True)
    transformer = models.ForeignKey('Transformer', models.DO_NOTHING, blank=True, null=True)
    as_state = models.CharField(max_length=100, blank=True, null=True)
    mounting_security = models.CharField(max_length=100, blank=True, null=True)
    mounting_security_cmt = models.TextField(blank=True, null=True)
    tank_bonded_earth = models.CharField(max_length=100, blank=True, null=True)
    tank_bonded_earth_cmt = models.TextField(blank=True, null=True)
    neutral_bonded_earth = models.CharField(max_length=100, blank=True, null=True)
    neutral_bonded_earth_cmt = models.TextField(blank=True, null=True)
    bushings_condition = models.CharField(max_length=100, blank=True, null=True)
    bushings_condition_cmt = models.TextField(blank=True, null=True)
    paintwork_condition = models.CharField(max_length=100, blank=True, null=True)
    paintwork_condition_cmt = models.TextField(blank=True, null=True)
    arcing_settings = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    silica_condition = models.CharField(max_length=100, blank=True, null=True)
    silica_condition_cmt = models.TextField(blank=True, null=True)
    oil_leaks = models.CharField(max_length=100, blank=True, null=True)
    megger_ht_e = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    megger_lt_e = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    megger_ht_lt = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    megger_ht_lt_e = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    oil_temp = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    oil_dielectric_test = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    tap_position = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    asset_change = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e60transformer'


class E84General(models.Model):
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    e84_general_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    section_number = models.CharField(max_length=100, blank=True, null=True)
    construction_type = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    overall_result = models.CharField(max_length=100, blank=True, null=True)
    rowid = models.IntegerField(blank=True, null=True)
    sync_status = models.IntegerField(blank=True, null=True)
    section_length = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'e84general'
        verbose_name_plural='E84 General'

    def __str__(self):
        return self.e84_general_id

class E84Lineinspection(models.Model):
    line_inspection_id = models.CharField(primary_key=True, max_length=100)
    pole_number = models.CharField(max_length=100, blank=True, null=True)
    pole_type = models.CharField(max_length=100, blank=True, null=True)
    wayleave = models.CharField(max_length=100, blank=True, null=True)
    pole = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    cross_arm = models.CharField(max_length=100, blank=True, null=True)
    insulator = models.CharField(max_length=100, blank=True, null=True)
    conductors = models.CharField(max_length=100, blank=True, null=True)
    stays = models.CharField(max_length=100, blank=True, null=True)
    earthing = models.CharField(max_length=100, blank=True, null=True)
    cradles = models.CharField(max_length=100, blank=True, null=True)
    anti_climbing_device = models.CharField(max_length=100, blank=True, null=True)
    rowid = models.IntegerField(blank=True, null=True)
    sync_status = models.IntegerField(blank=True, null=True)
    e84_general = models.ForeignKey(E84General, on_delete=models.CASCADE, blank=True, null=True,db_column='e84_general_id',related_name='inspections')
    pole_material = models.CharField(max_length=100, blank=True, null=True)
    voltage_level = models.CharField(max_length=100, blank=True, null=True)
    point = models.CharField(max_length=100, blank=True, null=True)
        


    class Meta:
        managed = False
        db_table = 'e84lineinspection'
        verbose_name_plural='E84 Line Inspection'

    def __str__(self):
        return self.line_inspection_id

class Jobattachment(models.Model):
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    job_attach_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    attachment = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobattachment'

class Jobprogress(models.Model):
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    job_progress_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=True, db_column='job_id',related_name='job_progress')    
    start_dt = models.DateTimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)
    fleet_no = models.CharField(max_length=100, blank=True, null=True)
    open_mileage = models.IntegerField(blank=True, null=True)
    close_mileage = models.IntegerField(blank=True, null=True)
    geom_start = models.TextField(blank=True, null=True) 
    geom_end = models.TextField(blank=True, null=True)  
    comments = models.TextField(blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    status = models.ForeignKey('Jobstatus', on_delete=models.CASCADE, db_column='status', blank=False, null=False,default=1)
    rowid = models.IntegerField(blank=True, null=True)
    sync_status = models.IntegerField(blank=True, null=True,default=0)

    class Meta:
        managed = False
        db_table = 'jobprogress'
    def __str__(self):
        return self.job_progress_id


class Jobsync(models.Model):
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    jobsync_id = models.CharField(primary_key=True, max_length=100)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    table_name = models.CharField(max_length=100, blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    sqlstatement = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobsync'


class Jobteam(models.Model):
    job_team_id = models.CharField(max_length=100, primary_key=True)
    job_progress = models.ForeignKey(
        'Jobprogress', on_delete=models.CASCADE, related_name='jobteam_members')
    ec_num = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    start_dt = models.CharField(max_length=100, blank=True, null=True)
    end_dt = models.CharField(max_length=100, blank=True, null=True)
    teamleader = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    rowid = models.IntegerField(blank=True, null=True)
    sync_status = models.IntegerField(blank=True, null=True,default=0)

    class Meta:
        managed = False
        db_table = 'jobteam'

    def __str__(self):
        return self.ec_num




class Jobworkflow(models.Model):
    job_workflow_id = models.CharField(primary_key=True, max_length=100)
    ec_num = models.CharField(max_length=100, blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    action_dt = models.DateTimeField(blank=True, null=True)
    workflow = models.ForeignKey('Workflow', on_delete=models.CASCADE, blank=True, null=True,related_name='job_workflows')
    #Override default manager
    objects=JobWorkflowManager()


    class Meta:
        managed = False
        db_table = 'jobworkflow'
       
    def __str__(self):
        return '%s' % self.job

class Office(models.Model):
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    office_id = models.CharField(primary_key=True, max_length=100)
    supervisor_id = models.CharField(max_length=100, blank=True, null=True)
    office_description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'office'
       
    def __str__(self):
        return '%s' % self.office_id

class Permission(models.Model):
    perm_id = models.CharField(primary_key=True, max_length=100)
    perm_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission'

       
    def __str__(self):
        return '%s' % self.perm_name

class Pole(models.Model):
    pole_id = models.CharField(primary_key=True, max_length=100)
    equipment_id = models.CharField(max_length=100, blank=True, null=True)
    pole_no = models.CharField(max_length=100, blank=True, null=True)
    pole_type = models.CharField(max_length=100, blank=True, null=True)
    centre = models.CharField(max_length=100, blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'pole'

       
    def __str__(self):
        return '%s' % self.pole_type

class Role(models.Model):
    role_code = models.CharField(primary_key=True, max_length=100)
    role_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    app = models.CharField(max_length=100, blank=True, null=True)
    dt_created = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'
       
    def __str__(self):
        return '%s' % self.role_name


class Rolepermission(models.Model):
    role_permission_id = models.CharField(primary_key=True, max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    perm = models.ForeignKey(Permission, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rolepermission'

       
    def __str__(self):
        return '%s %s' % self.perm, self.role


class TeamLeader(models.Model):
    team_leader = models.CharField(max_length=100, primary_key=True)
    specialisation = models.CharField(max_length=100, blank=True, null=True)
    centre = models.CharField(max_length=100, blank=True, null=True)
    # added onduty which will be true or false 
    # onduty = models.CharField(max_length=5, default=False)


    class Meta:
        managed = False
        db_table = 'teamleader'

    def __str__(self):
        return self.team_leader 

    
class Team(models.Model):
    team_id = models.CharField(primary_key=True, max_length=100)
    team_leader = models.ForeignKey('TeamLeader', on_delete=models.CASCADE, db_column='team_leader', related_name='members')
    team_member = models.CharField(max_length=100, blank=True, null=True)
    specialisation = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    centre = models.CharField(max_length=100, blank=True, null=True)
    # added onduty which will be true or false 
    # onduty = models.CharField(max_length=5, default=False)


    class Meta:
        managed = False
        db_table = 'team'

    def __str__(self):
        return self.team_member



class Userrole(models.Model):
    user_role_id = models.CharField(primary_key=True, max_length=100)
    ec_num = models.CharField(max_length=100, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True,null=True,related_name='user_roles')
    status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userrole'

       
    def __str__(self):
        return '%s' % self.ec_num

class Userroletrail(models.Model):
    user_role_trail_id = models.CharField(primary_key=True, max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    ec_num = models.CharField(max_length=100, blank=True, null=True)
    period = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    user_role_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userroletrail'
    
       
    def __str__(self):
        return '%s' % self.role


class JobType(models.Model):
    job_type_id = models.CharField(primary_key=True, max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'jobtype'

    
    def __str__(self):
        return '%s' % self.type
        

class Workflow(models.Model):
    workflow_id = models.BigIntegerField(primary_key=True)
    workflow_code = models.ForeignKey(Appflow, on_delete=models.CASCADE, db_column='workflow_code', blank=True, null=True,related_name='app_workflows')
    step = models.IntegerField(blank=True, null=True)
    role_code = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_code', blank=True, null=True,related_name='workflows')
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    approve = models.ForeignKey(JobStatus, on_delete=models.CASCADE, db_column='approve', blank=True, null=True, related_name='approve')
    reject = models.ForeignKey(JobStatus, on_delete=models.CASCADE, db_column='reject', blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'workflow'
        unique_together = (('workflow_code', 'step'),)

    def __str__(self):
        return '%s' % self.workflow_id


class Centre(models.Model):
    centre_id = models.CharField(primary_key=True, max_length=100)
    centre_code = models.CharField(max_length=100, blank=True, null=True)
    centre_name = models.CharField(max_length=100, blank=True, null=True)
    cost_centre = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'centre'

    
    def __str__(self):
        return '%s' % self.centre_name

class Profile(models.Model):
    profile_code = models.CharField(primary_key=True, max_length=100)
    profile_name = models.CharField(max_length=100, blank=True, null=True)
    dt_created = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'

    
    def __str__(self):
        return '%s' % self.profile_name

class Roleprofile(models.Model):
    role_profile_id = models.IntegerField(primary_key=True)
    profile_code = models.ForeignKey(Profile,on_delete=models.CASCADE, db_column='profile_code',related_name='role_profiles')
    role_code = models.ForeignKey(Role,on_delete=models.CASCADE, db_column='role_code',related_name='roles')
    created_by = models.CharField(max_length=100, blank=True, null=True)
    dt_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roleprofile'
        unique_together = (('profile_code', 'role_code'),)

    
    def __str__(self):
        return '%s' % self.profile_code+" - "+self.role_code

class Sectiongroup(models.Model):
    section = models.CharField(primary_key=True, max_length=255)
    grp = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sectiongroup'
        unique_together = (('section', 'grp'),)


class Userprofile(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    profile_code = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_code',related_name='user_profiles') #  ManyToMany Relationship
    state = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'userprofile'
        unique_together = (('username', 'profile_code', 'section'),)

    
    def __str__(self):
        return '%s' % self.username +" - "+self.profile_code+" - "+self.section

class JobWorkflowStatus(models.Model):
    profile_code = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    responsible = models.CharField(max_length=100, blank=True, null=True)
    ec_num = models.CharField(max_length=100, blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table='job_workflow_status'

class JobFormsModel(models.Model):
    job_id=models.ForeignKey('Job', on_delete=models.CASCADE,db_column='job_id',related_name='job_form')
    form_id=models.ForeignKey('E84General', on_delete=models.CASCADE,db_column='form_id')
    type=models.CharField(max_length=100, blank=True, null=True)
    assignee=models.CharField(max_length=100, blank=True, null=True)
    decision=models.CharField(max_length=100, blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'zdforms'


class JobsForReinspectionModel(models.Model):
    work_order_id=models.ForeignKey('Job', on_delete=models.CASCADE,db_column='work_order_id',related_name='reinspection_workorder')
    job_id=models.ForeignKey('Job', on_delete=models.CASCADE,db_column='job_id',related_name='reinspection_job')
    description=models.CharField(max_length=100, blank=True, null=True)
    created_on=models.CharField(max_length=100, blank=True, null=True)
    status = models.ForeignKey('Jobstatus', on_delete=models.CASCADE,db_column='status')
    decision=models.CharField(max_length=100, blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'jobsforreinspection'



class E50(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e50_id = models.CharField(primary_key=True, max_length=100)
    station = models.ForeignKey('Station', on_delete=models.CASCADE, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    e50_dt = models.DateTimeField(blank=True, null=True)
    relays_flags_reset = models.CharField(max_length=100, blank=True, null=True)
    relays_flags_reset_comment = models.TextField(blank=True, null=True)
    sef_uniselector_reset = models.CharField(max_length=100, blank=True, null=True)
    sef_uniselector_reset_comment = models.TextField(blank=True, null=True)
    fuses_links_position = models.CharField(max_length=100, blank=True, null=True)
    fuses_links_position_comment = models.TextField(blank=True, null=True)
    panels_wiring_order = models.CharField(max_length=100, blank=True, null=True)
    panels_wiring_order_comment = models.TextField(blank=True, null=True)
    record_charger_voltage = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    record_charger_current = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    battery_voltage = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    cell_voltage = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    apply_load_test = models.CharField(max_length=100, blank=True, null=True)
    apply_load_test_comment = models.TextField(blank=True, null=True)
    topup_cells_water = models.CharField(max_length=100, blank=True, null=True)
    topup_cells_water_comment = models.TextField(blank=True, null=True)
    clean_terminal_cases = models.CharField(max_length=100, blank=True, null=True)
    clean_terminal_cases_comment = models.TextField(blank=True, null=True)
    terminal_connections = models.CharField(max_length=100, blank=True, null=True)
    terminal_connections_comment = models.TextField(blank=True, null=True)
    float_voltage = models.CharField(max_length=100, blank=True, null=True)
    float_voltage_comment = models.TextField(blank=True, null=True)
    cubicle_lights = models.CharField(max_length=100, blank=True, null=True)
    cubicle_lights_comment = models.TextField(blank=True, null=True)
    relays_clean_operate = models.CharField(max_length=100, blank=True, null=True)
    relays_clean_operate_comment = models.TextField(blank=True, null=True)
    cubicle_fuses_links = models.CharField(max_length=100, blank=True, null=True)
    cubicle_fuses_links_comment = models.TextField(blank=True, null=True)
    indicating_lamps = models.CharField(max_length=100, blank=True, null=True)
    indicating_lamps_comment = models.TextField(blank=True, null=True)
    panel_clean_wiring = models.CharField(max_length=100, blank=True, null=True)
    panel_clean_wiring_comment = models.TextField(blank=True, null=True)
    cubicle_lights_heaters = models.CharField(max_length=100, blank=True, null=True)
    cubicle_lights_heaters_comment = models.TextField(blank=True, null=True)
    insulators_arrestors_inorder = models.CharField(max_length=100, blank=True, null=True)
    insulators_arrestors_inorder_comment = models.TextField(blank=True, null=True)
    dfuse_isolators_inorder = models.CharField(max_length=100, blank=True, null=True)
    dfuse_isolators_inorder_comment = models.TextField(blank=True, null=True)
    busbars_jumpers_inorder = models.CharField(max_length=100, blank=True, null=True)
    busbars_jumpers_inorder_comment = models.TextField(blank=True, null=True)
    ss_earthresistance_date = models.DateField(blank=True, null=True)
    earthing_structure_fence = models.CharField(max_length=100, blank=True, null=True)
    earthing_structure_fence_comment = models.TextField(blank=True, null=True)
    fire_equipment_expiry = models.DateField(blank=True, null=True)
    cables_boxes_glands = models.CharField(max_length=100, blank=True, null=True)
    cables_boxes_glands_comment = models.TextField(blank=True, null=True)
    substation_surrounds_clean = models.CharField(max_length=100, blank=True, null=True)
    substation_surrounds_clean_comment = models.TextField(blank=True, null=True)
    paintwork_general_condition = models.CharField(max_length=100, blank=True, null=True)
    paintwork_general_condition_comment = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    reading_by = models.CharField(max_length=100, blank=True, null=True)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e50'

    def __str__(self):
        return self.e50_id


class E50Autodisconnector(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e50autodisconnect_id = models.CharField(primary_key=True, max_length=100)
    e50 = models.ForeignKey(E50, on_delete=models.CASCADE)
    switchgearid = models.CharField(max_length=100, blank=True, null=True)
    mechanism_operation = models.CharField(max_length=100, blank=True, null=True)
    mechanism_operation_comment = models.TextField(blank=True, null=True)
    bushing_condition = models.CharField(max_length=100, blank=True, null=True)
    bushing_condition_comment = models.TextField(blank=True, null=True)
    earthing_intact = models.CharField(max_length=100, blank=True, null=True)
    earthing_intact_comment = models.TextField(blank=True, null=True)
    tripping_circuit_healthy = models.CharField(max_length=100, blank=True, null=True)
    tripping_circuit_healthy_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e50autodisconnect'

    def __str__(self):
        return self.e50autodisconnect_id


class E50Circuitbreakers(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e50circuitbreakers_id = models.CharField(primary_key=True, max_length=100)
    e50_id = models.CharField(max_length=100)
    switchgearid = models.ForeignKey('Switchgear', on_delete=models.CASCADE, db_column='switchgearid', blank=True, null=True)
    present_counter_readings = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    last_overhaul_reading = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    number_of_operations = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    date_oil_changed = models.DateField(blank=True, null=True)
    bushings_condition = models.CharField(max_length=100, blank=True, null=True)
    bushings_condition_comment = models.TextField(blank=True, null=True)
    oil_leaks = models.CharField(max_length=100, blank=True, null=True)
    oil_leaks_comment = models.TextField(blank=True, null=True)
    eathing_intact = models.CharField(max_length=100, blank=True, null=True)
    eathing_intact_comment = models.TextField(blank=True, null=True)
    tripping_circuit_healthy = models.CharField(max_length=100, blank=True, null=True)
    tripping_circuit_healthy_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e50circuitbreakers'

    def __str__(self):
        return self.e50circuitbreakers_id





class E50Feeders(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e50feeders_id = models.CharField(primary_key=True, max_length=100)
    e50_id = models.CharField(max_length=100)
    feeder_code = models.ForeignKey('Feeder', on_delete=models.CASCADE, db_column='feeder_code', blank=True, null=True)
    nominal_voltage = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    feeder_number = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    indicated_red_phase = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    indicated_yellow_phase = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    indicated_blue_phase = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    md_amps = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e50feeders'

    def __str__(self):
        return self.e50feeders_id

        


class E50Transformer(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    e50transformer_id = models.CharField(primary_key=True, max_length=100)
    e50_id = models.CharField(max_length=100, blank=True, null=True)
    transformer = models.ForeignKey('Transformer', on_delete=models.CASCADE, blank=True, null=True)
    ind_amps = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    md_amps = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    ind_volts = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    kva_md = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    tap_position = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    max_tap = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    min_tap = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    tx_on_load = models.CharField(max_length=100, blank=True, null=True)
    tx_on_load_comment = models.CharField(max_length=100, blank=True, null=True)
    max_oil_temp = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    max_wnd_temp = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    present_tap_change = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    last_tap_change = models.DateField(blank=True, null=True)
    past_tap_change = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    tap_change_operations = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    ave_tap_change = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    tap_range = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    ops_satisfactory = models.CharField(max_length=100, blank=True, null=True)
    ops_satisfactory_comment = models.TextField(blank=True, null=True)
    oil_leaks = models.CharField(max_length=100, blank=True, null=True)
    oil_leaks_comment = models.TextField(blank=True, null=True)
    tank_oil_level = models.CharField(max_length=100, blank=True, null=True)
    tank_oil_level_comment = models.TextField(blank=True, null=True)
    diverter_tank_level = models.CharField(max_length=100, blank=True, null=True)
    diverter_tank_level_comment = models.TextField(blank=True, null=True)
    aux_tx_oil = models.CharField(max_length=100, blank=True, null=True)
    aux_tx_oil_comment = models.TextField(blank=True, null=True)
    main_tx_breather = models.CharField(max_length=100, blank=True, null=True)
    main_tx_breather_comment = models.TextField(blank=True, null=True)
    aux_tx_breather = models.CharField(max_length=100, blank=True, null=True)
    aux_tx_breather_comment = models.TextField(blank=True, null=True)
    last_overhaul_date = models.DateField(blank=True, null=True)
    last_oil_test = models.DateField(blank=True, null=True)
    counter_reading_overhauled = models.DecimalField(max_digits=65535, decimal_places=5, blank=True, null=True)
    diverter_switches = models.CharField(max_length=100, blank=True, null=True)
    diverter_switches_comment = models.TextField(blank=True, null=True)
    selector_switches = models.CharField(max_length=100, blank=True, null=True)
    selector_switches_comment = models.TextField(blank=True, null=True)
    mechanism_lubrication = models.CharField(max_length=100, blank=True, null=True)
    mechanism_lubrication_comment = models.TextField(blank=True, null=True)
    bushings_condition = models.CharField(max_length=100, blank=True, null=True)
    bushings_condition_comment = models.TextField(blank=True, null=True)
    sign_of_flashover = models.CharField(max_length=100, blank=True, null=True)
    sign_of_flashover_comment = models.TextField(blank=True, null=True)
    buccholz_gas = models.CharField(max_length=100, blank=True, null=True)
    buccholz_gas_comment = models.TextField(blank=True, null=True)
    tx_earthing_intact = models.CharField(max_length=100, blank=True, null=True)
    tx_earthing_intact_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e50transformer'

    def __str__(self):
        return self.e50transformer_id


class Assetrships(models.Model):
    modified_by = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    assetrships_id = models.CharField(primary_key=True, max_length=100)
    parent_assetid = models.CharField(max_length=100, blank=True, null=True)
    parent_asset_type = models.CharField(max_length=100, blank=True, null=True)
    child_assetid = models.CharField(max_length=100, blank=True, null=True)
    child_asset_type = models.CharField(max_length=100, blank=True, null=True)

    objects=AssetRelationshipManager()
   

    class Meta:
        managed = False
        db_table = 'assetrships'

    def __str__(self):
        return self.assetrships_id
