from django.db import models, connection
 
 
class JobManager(models.Manager):
    def jobs_view_procedure(self, username, section,status):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.jobs_view_fx', [username,section,status])
            result = cursor.fetchall()
            result_list = []
            for row in result:
                results = {
                    "job_id": row[0],
                    "work_order_id": row[1],
                    "created_by":row[2],
                    "created_on":row[3].strftime("%Y-%m-%d %H:%M:%S"),
                    "modified_by":row[4],
                    "modified_on":row[5],
                    "type":row[6],
                    "description":row[7],
                    "asset_id":row[8],
                    "assignee":row[9],
                    "comments":row[10],
                    "closed_by":row[11],
                    "closed_dt":row[12],
                    "asset_name":row[13],
                    "asset_type":row[14],
                    "asset_number":row[15],
                    "expected_end_dt":row[16],
                    "reference_no":row[17],
                    "asset_serial":row[18],
                    "status":row[19],
                    "trigger":row[20],
                    "start_date":row[21],
                    "status_value":row[22],
                }
                result_list.append(results)
            return result_list


    def workorder_reports_view(self, workorder_centre, workorder_status,workorder_start_date,workorder_end_date):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.workorder_reports_fx', [workorder_centre, workorder_status,workorder_start_date,workorder_end_date])
            result = cursor.fetchall()
            result_list = []

            for row in result:
                results = {
                    "work_order_id": row[0],
                    "status": row[1],
                    "created_by":row[2],
                    "created_on":row[3].strftime("%Y-%m-%d %H:%M:%S"),
                    "modified_by":row[4],
                    "modified_on":row[5],
                    "description":row[6],
                    "centre":row[7],
                    "comments":row[8],
                    "workorderstatus":row[9],
                    "no_of_jobs":row[10]
                }
                result_list.append(results)
            return result_list

    def all_parentcentres(self, centreparent):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.parent_centres_fx', [ centreparent ])
            result = cursor.fetchall()
            result_list = []
            for row in result:
                results = {
                    "centrecode": row[0],
                    "centrename": row[1],
                    "centretype": row[2],
                    
                }
                result_list.append(results)
            return result_list

    def jobs_reports_view(self, jobtype, centre,status,start_date,end_date):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.job_reports_fx', [jobtype,centre,status,start_date,end_date])
            result = cursor.fetchall()
            result_list = []
            job_form={}
            form_count={}
            for row in result:
                form_count[row[0]]=form_count.get(row[0],0)+1

            for row in result:
                if row[0] in job_form:
                    pass
                else:
                    results = {
                        
                        "work_order_id": row[0],
                        "job_id": row[1],
                        "description":row[2],
                        "created_on":row[3].strftime("%Y-%m-%d %H:%M:%S"),
                        "end_dt":row[4],
                        "assignee":row[5],
                        "status":row[6],
                        "centre":row[7],
                        "status":row[8],
                        "form_id":row[9],
                        # //////
                        "number_of_forms":form_count[row[0]],
                        "job_form":row
                    }
                    result_list.append(results)
                job_form[row[0]]=job_form.get(row[0],0)+1 
            return result_list
 
    def job_workflow_status(self, pk):
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT roleprofile.profile_code ,workflow.section,userprofile.username as responsible ,jobworkflow.ec_num,jobworkflow.action
                        FROM core.job
                        INNER JOIN core.workflow on workflow.workflow_code = job.workflow_id
                        INNER JOIN core.roleprofile on roleprofile.role_code =  workflow.role_code
                        INNER JOIN core.userprofile on userprofile.profile_code = roleprofile.profile_code and userprofile.status='Active'
                        LEFT JOIN core.jobworkflow on workflow.workflow_id = jobworkflow.workflow_id
                        WHERE job.job_id = %s  ORDER BY workflow.step""", params=[pk]
                           )
            result_list = []
            for row in cursor.fetchall():
                results = {
                    "profile_code": row[0],
                    "section": row[1],
                    "responsible": row[2],
                    "ec_num": row[3],
                    "action": row[4]
                }
                result_list.append(results)
        return result_list
 
 
class JobWorkflowManager(models.Manager):
    def job_awaiting_action_procedure(self, ec_num):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.jobs_awaiting_action_fx', [ec_num, ])
            result = cursor.fetchall()
            result_list = []
            job_form={}
            form_count={}
            '''
                Generate a form_count dictionary with a count of the number of times a single job id (row[0]) appears in the result(above)
                variable and hence the number of forms associated with a job
            '''
            for row in result:
                form_count[row[0]]=form_count.get(row[0],0)+1 
           #THE BELOW LOOP POPULATES THE RESULTS DICTIONARY ONLY FOR A UNIQUE JOB ID
            for row in result: 
                if row[0] in job_form:
                    pass
                else:              
                    results = {
                        "job_id": row[0],
                        "created_by":row[1],
                        "created_on":row[2].strftime("%Y-%m-%d %H:%M:%S"),
                        "work_order_id": row[3],
                        "type":row[4],
                        "description":row[5],
                        "assignee":row[6],
                        "comments":row[7],
                        "closed_by":row[8],
                        "closed_dt":row[9],
                        "status":row[10],
                        "approve":row[11],
                        "reject":row[12],
                        "role_name":row[13],
                        "status_value":row[14],
                        #THE NUMBER OF FORMS ASSOCIATED WITH A JOB IS DERIVED FROM THE form_count dictionary as commented above
                        "number_of_forms":form_count[row[0]],
                        "job_form":row
                    }
                    result_list.append(results)
                # COUNT THE NUMBER OF TIMES A JOB ID APPEARS IN THE RESULT LIST 
                job_form[row[0]]=job_form.get(row[0],0)+1             
        return result_list 
  
 
    def job_workflow_procedure(self, job_id):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.job_workflow_fx', [job_id, ])
            result = cursor.fetchall()
            result_list = []
            for row in result:
                results = {
                    "profile_code": row[0],
                    "section": row[1],
                    "responsible": row[2],
                    "ec_num": row[3],
                    "action": row[4],
                    "created_on": row[5].strftime("%Y-%m-%d %H:%M:%S"),
                    "action_dt": row[6],
                    "step": row[7],
                    "comments": row[8]
                }
                result_list.append(results)
            return result_list
 
        def approve_job(self,job_workflow_id,job_id,actioner,decision):
            with connection.cursor() as cursor:
                return cursor.callproc(
                    'core.approve_job',[job_workflow_id,job_id,actioner,decision])

        def redo_job(self,job_workflow_id,job_id,assignee,comment):
            with connection.cursor() as cursor:
                return cursor.callproc(
                    'core.redo_job',[job_workflow_id,job_id,assignee,comment])        
            
 
 
class AssetRelationshipManager(models.Manager):
    def station_assets(self, parent_assetid):
        with connection.cursor() as cursor:
 
            cursor.callproc(
            'core.stationtransformers_fx', [parent_assetid])
            transformers = cursor.fetchall()
 
            cursor.callproc(
            'core.stationfeeders_fx', [parent_assetid])
            feeders = cursor.fetchall()
 
            cursor.callproc(
            'core.stationswitchgears_breakers_fx', [parent_assetid])
            breakers = cursor.fetchall()
 
            cursor.callproc(
            'core.stationswitchgear_isolators_fx', [parent_assetid])
            isolators = cursor.fetchall()
 
 
            result_list = []
            assets={}
            transformer_list=[]
            for row in transformers:
                result = {
                    "transformerid": row[0],
                    "name": row[1],
                    "voltageratio": row[2],
                    "sscode": row[3],
                    "depot" :row[4] ,
                    "district":row[5], 
                    "region": row[6],
                    "assetno":row[7],
                    "createdon": row[8].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[9],
                    "modifiedon": row[10],
                    "modifiedby": row[11],
                    "comments": row[12],
                    "status": row[13],
                    "districtid": row[14],
                    "wardid": row[15],
                    "provinceid": row[16],
                    "id": row[17],
                    "serialno": row[18],
                    "systemno": row[19],
                    "highvoltage":row[20],
                    "lowvoltage":row[21],
                    "application": row[22],
                    "mounting": row[23],
                    "standard": row[24],
                    "make": row[25],
                    "transformerinsulation": row[26],
                    "manufactureryear":row[27],
                    "installationyear": row[28],
                    "commissionyear": row[29],
                    "windingsno": row[30],
                    "bil": row[31],
                    "mass": row[32],
                    "vectorgroup": row[33],
                    "impedance":row[34],
                    "ironlosses": row[35],
                    "copperlosses": row[36],
                    "taperange": row[37],
                    "cooling": row[38],
                    "capacity": row[39],
                    "geom2d": row[40],
                    "maxcapacity": row[41],
                    "windings": row[42],
                    "geom3d": row[43],
                    "asset_change": row[44],
                    "trregion": row[45],
                }
                transformer_list.append(result) 
            assets['transformers']=transformer_list
 
            feeder_list=[]
            for row in feeders:
                result = {
                    "feedercode": row[0],
                    "name": row[1],
                    "voltagelevel": row[2] ,
                    "depot":row[3],
                    "district": row[4],
                    "region":row[5],
                    "assetno":row[6],
                    "createdon": row[7].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[8],
                    "modifiedon":row[9],
                    "feederno":row[10],
                    "modifiedby":row[11],
                    "comments":row[12],
                    "status":row[13],
                    "districtid":row[14],
                    "wardid":row[15],
                    "provinceid":row[16],
                    "id":row[17],
                    "geom2d": row[18],
                    "sourcesscode":row[19],
                    "asset_change":row[20],
                    "trregion":row[21]                                    
                }
                feeder_list.append(result)
            assets['feeders'] = feeder_list
    
            breaker_list=[]
            for row in breakers:
                result = {
                    "switchgearno": row[0],
                    "switchgearid": row[1],
                    "type": row[2] ,
                    "voltagerating":row[3],
                    "make":row[4],
                    "depot": row[5],
                    "district":row[6],
                    "region":row[7],
                    "assetno":row[8],
                    "createdon": row[9].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[10],
                    "modifiedon": row[11],
                    "modifiedby":row[12],
                    "comments":row[13],
                    "status":row[14],
                    "districtid":row[15],
                    "wardid":row[16],
                    "provinceid":row[17],
                    "id":row[18],
                    "serialno":row[19],
                    "model":row[20],
                    "constructiontype": row[21],
                    "mco":row[22],
                    "opmech": row[23],
                    "busbarsno":row[24],
                    "optype": row[25],
                    "standard":row[26],
                    "insulationmedium": row[27],
                    "interruptingmedium":row[28],
                    "ratedcc":row[29],
                    "ratedscbc":row[30],
                    "ratedmc":row[31],
                    "ratedscwt":row[32],
                    "ratedstwc":row[33],
                    "controlvoltage":row[34],
                    "motorost":row[35],
                    "motorvoltage":row[36],
                    "auxvoltage":row[37],
                    "possiblecountsetting":row[38],
                    "autoreclosingtype":row[39],
                    "dutycycle":row[40],
                    "netmass":row[41],
                    "ocinstalled":row[42],
                    "bil":row[43],
                    "commissionyear":row[44],
                    "installationyear":row[45],
                    "baytype": row[46],
                    "use":row[47],
                    "tripcoilsno":row[48],
                    "normalopstatus": row[49],
                    "cdpoint":row[50],
                    "feedercode":row[51],
                    "geom2d": row[52],
                    "mvboard":row[53],
                    "geom3d":row[54],
                    "nostatus":row[55],
                    "manufactureyear":row[56],
                    "installed_on":row[57],
                    "asset_change":row[58],
                    "trregion":row[59]                                         
                }
                breaker_list.append(result)
            assets['breakers']=breaker_list
 
            isolator_list=[]
            for row in isolators:
                result = {
                    "switchgearno": row[0],
                    "switchgearid": row[1],
                    "type": row[2] ,
                    "voltagerating":row[3],
                    "make":row[4],
                    "depot": row[5],
                    "district":row[6],
                    "region":row[7],
                    "assetno":row[8],
                    "createdon": row[9].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[10],
                    "modifiedon": row[11],
                    "modifiedby":row[12],
                    "comments":row[13],
                    "status":row[14],
                    "districtid":row[15],
                    "wardid":row[16],
                    "provinceid":row[17],
                    "id":row[18],
                    "serialno":row[19],
                    "model":row[20],
                    "constructiontype": row[21],
                    "mco":row[22],
                    "opmech": row[23],
                    "busbarsno":row[24],
                    "optype": row[25],
                    "standard":row[26],
                    "insulationmedium": row[27],
                    "interruptingmedium":row[28],
                    "ratedcc":row[29],
                    "ratedscbc":row[30],
                    "ratedmc":row[31],
                    "ratedscwt":row[32],
                    "ratedstwc":row[33],
                    "controlvoltage":row[34],
                    "motorost":row[35],
                    "motorvoltage":row[36],
                    "auxvoltage":row[37],
                    "possiblecountsetting":row[38],
                    "autoreclosingtype":row[39],
                    "dutycycle":row[40],
                    "netmass":row[41],
                    "ocinstalled":row[42],
                    "bil":row[43],
                    "commissionyear":row[44],
                    "installationyear":row[45],
                    "baytype": row[46],
                    "use":row[47],
                    "tripcoilsno":row[48],
                    "normalopstatus": row[49],
                    "cdpoint":row[50],
                    "feedercode":row[51],
                    "geom2d": row[52],
                    "mvboard":row[53],
                    "geom3d":row[54],
                    "nostatus":row[55],
                    "manufactureyear":row[56],
                    "installed_on":row[57],
                    "asset_change":row[58],
                    "trregion":row[59]                                     
                }
                isolator_list.append(result)
            assets['isolators']=isolator_list
        return assets
 
 
    def station_transformers(self, parent_assetid):
        with connection.cursor() as cursor:
 
            cursor.callproc(
            'core.stationtransformers_fx', [parent_assetid])
            transformers = cursor.fetchall()
            transformer_list=[]
            for row in transformers:
                result = {
                   "transformerid": row[0],
                    "name": row[1],
                    "voltageratio": row[2],
                    "sscode": row[3],
                    "depot" :row[4] ,
                    "district":row[5], 
                    "region": row[6],
                    "assetno":row[7],
                    "createdon": row[8].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[9],
                    "modifiedon": row[10],
                    "modifiedby": row[11],
                    "comments": row[12],
                    "status": row[13],
                    "districtid": row[14],
                    "wardid": row[15],
                    "provinceid": row[16],
                    "id": row[17],
                    "serialno": row[18],
                    "systemno": row[19],
                    "highvoltage":row[20],
                    "lowvoltage":row[21],
                    "application": row[22],
                    "mounting": row[23],
                    "standard": row[24],
                    "make": row[25],
                    "transformerinsulation": row[26],
                    "manufactureryear":row[27],
                    "installationyear": row[28],
                    "commissionyear": row[29],
                    "windingsno": row[30],
                    "bil": row[31],
                    "mass": row[32],
                    "vectorgroup": row[33],
                    "impedance":row[34],
                    "ironlosses": row[35],
                    "copperlosses": row[36],
                    "taperange": row[37],
                    "cooling": row[38],
                    "capacity": row[39],
                    "geom2d": row[40],
                    "maxcapacity": row[41],
                    "windings": row[42],
                    "geom3d": row[43],
                    "asset_change": row[44],
                    "trregion": row[45],                  
                }
 
                transformer_list.append(result) 
        return transformer_list
 
 
    def station_feeders(self, parent_assetid):
        with connection.cursor() as cursor:            
 
            cursor.callproc(
            'core.stationfeeders_fx', [parent_assetid])
            feeders = cursor.fetchall()
            feeder_list=[]
            for row in feeders:
                result = {
                    "feedercode": row[0],
                    "name": row[1],
                    "voltagelevel": row[2] ,
                    "depot":row[3],
                    "district": row[4],
                    "region":row[5],
                    "assetno":row[6],
                    "createdon": row[7].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[8],
                    "modifiedon":row[9],
                    "feederno":row[10],
                    "modifiedby":row[11],
                    "comments":row[12],
                    "status":row[13],
                    "districtid":row[14],
                    "wardid":row[15],
                    "provinceid":row[16],
                    "id":row[17],
                    "geom2d": row[18],
                    "sourcesscode":row[19],
                    "asset_change":row[20],
                    "trregion":row[21]                                     
                }
                feeder_list.append(result)
            return feeder_list
 
    def station_switchgear_breakers(self, parent_assetid):
        with connection.cursor() as cursor:          
            cursor.callproc(
            'core.stationswitchgears_breakers_fx', [parent_assetid])
            breakers = cursor.fetchall()
            breaker_list=[]
            for row in breakers:
                result = {
                    "switchgearno": row[0],
                    "switchgearid": row[1],
                    "type": row[2] ,
                    "voltagerating":row[3],
                    "make":row[4],
                    "depot": row[5],
                    "district":row[6],
                    "region":row[7],
                    "assetno":row[8],
                    "createdon": row[9].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[10],
                    "modifiedon": row[11],
                    "modifiedby":row[12],
                    "comments":row[13],
                    "status":row[14],
                    "districtid":row[15],
                    "wardid":row[16],
                    "provinceid":row[17],
                    "id":row[18],
                    "serialno":row[19],
                    "model":row[20],
                    "constructiontype": row[21],
                    "mco":row[22],
                    "opmech": row[23],
                    "busbarsno":row[24],
                    "optype": row[25],
                    "standard":row[26],
                    "insulationmedium": row[27],
                    "interruptingmedium":row[28],
                    "ratedcc":row[29],
                    "ratedscbc":row[30],
                    "ratedmc":row[31],
                    "ratedscwt":row[32],
                    "ratedstwc":row[33],
                    "controlvoltage":row[34],
                    "motorost":row[35],
                    "motorvoltage":row[36],
                    "auxvoltage":row[37],
                    "possiblecountsetting":row[38],
                    "autoreclosingtype":row[39],
                    "dutycycle":row[40],
                    "netmass":row[41],
                    "ocinstalled":row[42],
                    "bil":row[43],
                    "commissionyear":row[44],
                    "installationyear":row[45],
                    "baytype": row[46],
                    "use":row[47],
                    "tripcoilsno":row[48],
                    "normalopstatus": row[49],
                    "cdpoint":row[50],
                    "feedercode":row[51],
                    "geom2d": row[52],
                    "mvboard":row[53],
                    "geom3d":row[54],
                    "nostatus":row[55],
                    "manufactureyear":row[56],
                    "installed_on":row[57],
                    "asset_change":row[58],
                    "trregion":row[59]                                   
                }
                breaker_list.append(result)
            return breaker_list
 
    def station_switchgear_isolators(self, parent_assetid):
        with connection.cursor() as cursor:   
            cursor.callproc(
            'core.stationswitchgear_isolators_fx', [parent_assetid])
            isolators = cursor.fetchall()
            isolator_list=[]
            for row in isolators:
                result = {
                     "switchgearno": row[0],
                    "switchgearid": row[1],
                    "type": row[2] ,
                    "voltagerating":row[3],
                    "make":row[4],
                    "depot": row[5],
                    "district":row[6],
                    "region":row[7],
                    "assetno":row[8],
                    "createdon": row[9].strftime("%Y-%m-%d %H:%M:%S"),
                    "createdby": row[10],
                    "modifiedon": row[11],
                    "modifiedby":row[12],
                    "comments":row[13],
                    "status":row[14],
                    "districtid":row[15],
                    "wardid":row[16],
                    "provinceid":row[17],
                    "id":row[18],
                    "serialno":row[19],
                    "model":row[20],
                    "constructiontype": row[21],
                    "mco":row[22],
                    "opmech": row[23],
                    "busbarsno":row[24],
                    "optype": row[25],
                    "standard":row[26],
                    "insulationmedium": row[27],
                    "interruptingmedium":row[28],
                    "ratedcc":row[29],
                    "ratedscbc":row[30],
                    "ratedmc":row[31],
                    "ratedscwt":row[32],
                    "ratedstwc":row[33],
                    "controlvoltage":row[34],
                    "motorost":row[35],
                    "motorvoltage":row[36],
                    "auxvoltage":row[37],
                    "possiblecountsetting":row[38],
                    "autoreclosingtype":row[39],
                    "dutycycle":row[40],
                    "netmass":row[41],
                    "ocinstalled":row[42],
                    "bil":row[43],
                    "commissionyear":row[44],
                    "installationyear":row[45],
                    "baytype": row[46],
                    "use":row[47],
                    "tripcoilsno":row[48],
                    "normalopstatus": row[49],
                    "cdpoint":row[50],
                    "feedercode":row[51],
                    "geom2d": row[52],
                    "mvboard":row[53],
                    "geom3d":row[54],
                    "nostatus":row[55],
                    "manufactureyear":row[56],
                    "installed_on":row[57],
                    "asset_change":row[58],
                    "trregion":row[59]                                     
                }
                isolator_list.append(result)
            return isolator_list
    
    def transformer_metering(self, parent_assetid):
            with connection.cursor() as cursor:
                cursor.callproc(
                'core.transformermetering_fx', [parent_assetid])
                metering = cursor.fetchall()
                metering_list=[]
                for row in metering:
                    result = {
                        "metering_id": row[0],
                        "make": row[1],
                        "amps":row[2],
                        "volts": row[3],
                        "maker_type" :row[4] ,
                        "serial_number":row[5], 
                        "zesa_number": row[6],
                        "created_on":row[7],
                        "created_by": row[8],
                        "modified_on": row[9],
                        "modified_by": row[10],
                        "vad_transformer_no": row[11],
                        "ct_ratio": row[12],
                        "protection_type": row[13],
                        "geom2d":row[14],
                    
                    }
                    metering_list.append(result) 
            return metering_list


    def transformerlightningarrester(self,parent_assetid):
        with connection.cursor() as cursor:
            cursor.callproc(
            'core.transformerlightningarrester_fx',[parent_assetid])
            lightningarrester = cursor.fetchall()
            lightiningarrester_list=[]
            for row in lightningarrester:
                result = {
                    "lightningarrester_id":[0],
                    "ht_lt":[1],
                    "voltage_rating":[2],
                    "kvar_rating":[3],
                    "phase":[4],
                    "make":[5],
                    "type":[6],
                    "created_on":[7],
                    "created_by":[8],
                    "modified_on":[9],
                    "modified_by":[10],
                    "centre":[11],
                    "geom2d":[12]

                }
                lightiningarrester_list.append(result)
            return lightiningarrester_list

    def transformerswitchgear(self, parent_assetid):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.transformerswitchgear_fx',[parent_assetid])
            switchgear = cursor.fetchall()
            switchgear_list=[]
            for row in switchgear:
                result = {

                    "switchgearid":[0],
                    "depot":[1],
                    "district":[2], 
                    "region":[3], 
                    "assetno":[4], 
                    "createdon":[5], 
                    "createdby":[6],
                    "modifiedon":[7], 
                    "modifiedby":[8], 
                    "comments":[9], 
                    "status":[10], 
                    "districtid":[11], 
                    "wardid":[12], 
                    "provinceid":[13], 
                    "id":[14],
                    "serialno":[15], 
                    "make":[16], 
                    "model":[17], 
                    "type":[18], 
                    "constructiontype":[19], 
                    "mco":[20], 
                    "opmech":[21], 
                    "busbarsno":[22], 
                    "optype":[23], 
                    "standard":[24], 
                    "voltagerating":[25], 
                    "insulationmedium":[26], 
                    "interruptingmedium":[27], 
                    "ratedcc":[28],
                    "ratedscbc":[29], 
                    "ratedmc":[30], 
                    "ratedscwt":[31], 
                    "ratedstwc":[32], 
                    "controlvoltage":[33], 
                    "motorost":[34],
                    "motorvoltage":[35], 
                    "auxvoltage":[36], 
                    "possiblecountsetting":[37], 
                    "autoreclosingtype":[38], 
                    "dutycycle":[39], 
                    "netmass":[40], 
                    "ocinstalled":[41], 
                    "bil":[42], 
                    "commissionyear":[43], 
                    "installationyear":[44],
                    "baytype":[45], 
                    "use":[46], 
                    "tripcoilsno":[47], 
                    "normalopstatus":[48], 
                    "cdpoint":[49], 
                    "feedercode":[50], 
                    "geom2d":[51],
                    "mvboard":[52], 
                    "switchgearno":[53], 
                    "geom3d":[54], 
                    "nostatus":[55], 
                    "manufactureyear":[56], 
                    "installed_on":[57], 
                    "asset_change":[58], 
                    "trregion":[59]
                }
                switchgear_list.append(result)
            return switchgear_list

    def transformerdfuses(self, parent_assetid):
        with connection.cursor() as cursor:
            cursor.callproc(
                'core.transformerdfuses_fx',[parent_assetid])
            dfuses = cursor.fetchall()
            dfuses_list=[]
            for row in dfuses:
                result = {
                    "dfuse_id":[0],
                    "modified_on":[1],
                    "modified_by":[2], 
                    "created_by":[3], 
                    "created_on":[4], 
                    "rating":[5], 
                    "dfuse_type":[6], 
                    "phase":[7], 
                    "geom2d":[8]
                }
                dfuses_list.append(result)
            return dfuses_list

    def transformer_assets(self, parent_assetid):
        with connection.cursor() as cursor:
 
            cursor.callproc(
            'core.transformerdfuses_fx', [parent_assetid])
            dfuses = cursor.fetchall()
 
            cursor.callproc(
            'core.transformerswitchgear_fx', [parent_assetid])
            switchgears = cursor.fetchall()
 
            cursor.callproc(
            'core.transformerlightningarrester_fx', [parent_assetid])
            lightningarrester = cursor.fetchall()
 
            cursor.callproc(
            'core.transformermetering_fx', [parent_assetid])
            metering = cursor.fetchall()
 
            result_list = []
            assets={}
            dfuses_list=[]
            for row in dfuses:
                result = {
                    "dfuse_id":[0],
                    "modified_on":[1],
                    "modified_by":[2], 
                    "created_by":[3], 
                    "created_on":[4], 
                    "rating":[5], 
                    "dfuse_type":[6], 
                    "phase":[7], 
                    "geom2d":[8]
                }
                dfuses_list.append(result) 
            assets['dfuses']=dfuses_list
 
            switchgears_list=[]
            for row in switchgears:
                result = {
                    "switchgearid":[0],
                    "depot":[1],
                    "district":[2], 
                    "region":[3], 
                    "assetno":[4], 
                    "createdon":[5], 
                    "createdby":[6],
                    "modifiedon":[7], 
                    "modifiedby":[8], 
                    "comments":[9], 
                    "status":[10], 
                    "districtid":[11], 
                    "wardid":[12], 
                    "provinceid":[13], 
                    "id":[14],
                    "serialno":[15], 
                    "make":[16], 
                    "model":[17], 
                    "type":[18], 
                    "constructiontype":[19], 
                    "mco":[20], 
                    "opmech":[21], 
                    "busbarsno":[22], 
                    "optype":[23], 
                    "standard":[24], 
                    "voltagerating":[25], 
                    "insulationmedium":[26], 
                    "interruptingmedium":[27], 
                    "ratedcc":[28],
                    "ratedscbc":[29], 
                    "ratedmc":[30], 
                    "ratedscwt":[31], 
                    "ratedstwc":[32], 
                    "controlvoltage":[33], 
                    "motorost":[34],
                    "motorvoltage":[35], 
                    "auxvoltage":[36], 
                    "possiblecountsetting":[37], 
                    "autoreclosingtype":[38], 
                    "dutycycle":[39], 
                    "netmass":[40], 
                    "ocinstalled":[41], 
                    "bil":[42], 
                    "commissionyear":[43], 
                    "installationyear":[44],
                    "baytype":[45], 
                    "use":[46], 
                    "tripcoilsno":[47], 
                    "normalopstatus":[48], 
                    "cdpoint":[49], 
                    "feedercode":[50], 
                    "geom2d":[51],
                    "mvboard":[52], 
                    "switchgearno":[53], 
                    "geom3d":[54], 
                    "nostatus":[55], 
                    "manufactureyear":[56], 
                    "installed_on":[57], 
                    "asset_change":[58], 
                    "trregion":[59]                                 
                }
                switchgears_list.append(result)
            assets['switchgears'] = switchgears_list
    
            lightningarrester_list=[]
            for row in lightningarrester:
                result = {
                    "lightningarrester_id":[0],
                    "ht_lt":[1],
                    "voltage_rating":[2],
                    "kvar_rating":[3],
                    "phase":[4],
                    "make":[5],
                    "type":[6],
                    "created_on":[7],
                    "created_by":[8],
                    "modified_on":[9],
                    "modified_by":[10],
                    "centre":[11],
                    "geom2d":[12]                                         
                }
                lightningarrester_list.append(result)
            assets['lightningarrester']=lightningarrester_list
 
            metering_list=[]
            for row in metering:
                result = {
                    "metering_id": row[0],
                        "make": row[1],
                        "amps":row[2],
                        "volts": row[3],
                        "maker_type" :row[4] ,
                        "serial_number":row[5], 
                        "zesa_number": row[6],
                        "created_on":row[7],
                        "created_by": row[8],
                        "modified_on": row[9],
                        "modified_by": row[10],
                        "vad_transformer_no": row[11],
                        "ct_ratio": row[12],
                        "protection_type": row[13],
                        "geom2d":row[14],
                                                         
                }
                metering_list.append(result)
            assets['metering']=metering_list
        return assets
 