import django_tables2 as tables
from django.contrib.auth.models import User
from .models import *
from beapi.models import *
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView
import django_filters

# class FilteredPersonListView(SingleTableMixin, FilterView):
#     table_class = PersonTable
#     model = Person
#     template_name = 'template.html'
#     filterset_class = PersonFilter


class PersonTable(tables.Table):

    class Meta:
        model = Person
        template_name = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-hover'}


class EmployeeTable(tables.Table):
    # users = User.objects.all()
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)

    class Meta:
        # sequence = ('selection', 'username', 'is_active')
        model = User
        attrs = {'class': 'table table-hover'}
        fields = ('username', 'email', 'is_superuser',
                  'is_staff', 'is_active', 'first_name', 'last_name',)


class TransformerTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=False)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'transformer_id', 'equipment_id')
        model = Transformer
        attrs = {'class': 'table table-hover'}


class SubstationTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=False)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'meter_id', 'equipment_id')
        model = Substationmeter
        attrs = {'class': 'table table-hover'}
        fields = ('selection', 'meter_id', 'equipment_id',
                  'meter_no', 'make', 'vad_transformer_zetdc_number',)


class SwitchTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=False)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'switchgear_id', 'equipment_id')
        model = Switchgear
        attrs = {'class': 'table table-hover'}


class PoleTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pole_id', orderable=False)
    my_column = tables.TemplateColumn(accessor='pole_id', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'pole_id', 'equipment_id')
        model = Pole
        attrs = {'class': 'table table-hover'}


class FeederTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=False)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'feeder_id_pk', 'equipment_id')
        model = Feeder
        attrs = {'class': 'table table-hover'}


class JobTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)
    class Meta:
        sequence = ('selection', 'description',  'assignee')
        model = Job
        attrs = {'class': 'table table-striped'}
        fields = ('selection', 'job_id','description',  'assignee', )
        # exclude = ('selection',)        
class JobTable1(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)
    class Meta:
        sequence = ('selection', 'description', 'assignee')
        model = Job
        attrs = {'class': 'table table-striped'}
        fields = ('selection', 'description',  'assignee', )
        exclude = ('selection',)        


class WorkorderTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:

        sequence = ('selection', 'description')
        model = Workorder
        attrs = {'class': 'table table-hover'}
        fields = ('selection', 'description')

class WorkorderTable1(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:

        sequence = ('selection', 'description')
        model = Workorder
        attrs = {'class': 'table table-hover'}
        fields = ('selection', 'description')
        exclude = ('selection',)

class JobProgressTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'start_dt', 'status', )
        model = Jobprogress
        attrs = {'class': 'table table-hover'}
        fields = ( 'selection', 'start_dt', 'status', )
        exclude = ('selection',)        
class JobTeamTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:

        sequence = ('ec_num','description',  'start_dt', )
        model = Jobteam
        attrs = {'class': 'table table-hover'}
        fields = ('ec_num', 'description', 'start_dt', )
        exclude = ('selection',)

class E84Table(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'job')
        model = E84Lineinspection
        attrs = {'class': 'table table-hover'}
        fields = ('selection', 'job','pole_type','pole_number','wayleave','comment','cross_arm','insulator','conductors','stays','earthing','cradles','anti_climbing_device')
        exclude = ('selection', 'job')
class E84Table1(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                        template_name='beweb/assets/buttons.html',
                                        orderable=False)
    class Meta:
        sequence = ('selection', 'job')
        model = E84General
        attrs = {'class': 'table table-hover'}
        fields = ('selection', 'job','line_section','section_number','section_number','construction_type','overall_result','created_by','created_on','modified_by','modified_on',)
        exclude = ('selection', 'job')


class AppflowTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'appflow_id')
        model = Appflow
        attrs = {'class': 'table table-hover'}
        fields = ('selection', 'appflow_id','section', 'app', 'workflow_code',)

class OfficeTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
    my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''),
                                      template_name='beweb/assets/buttons.html',
                                      orderable=False)

    class Meta:
        sequence = ('selection', 'office_id')
        model = Office
        attrs = {'class': 'table table-hover'}
        fields = ('selection', 'office_id','section', 'supervisor_id', 'office_description',)

class WorkflowTable(tables.Table):
        selection = tables.CheckBoxColumn(accessor='pk', orderable=True)
        my_column = tables.TemplateColumn(accessor='pk', verbose_name=(''), template_name='beweb/assets/buttons.html',orderable=False)
                    
        class Meta:
            sequence = ('selection', 'workflow_id')
            model = Workflow
            attrs = {'class': 'table table-hover'}
            fields = ('selection','workflow_id', 'workflow_code','step', 'office_id', 'created_by',)
                
                        
class WorkorderFilter(django_filters.FilterSet):
    class Meta:
        model = Workorder
        fields = ['description']


class FilteredWorkorderListView(SingleTableMixin, FilterView):
    table_class = WorkorderTable
    model = Workorder
    template_name = 'template.html'

    filterset_class = Workorder
