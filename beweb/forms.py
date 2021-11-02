"""
Definition of forms.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from multiselectfield import MultiSelectField

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254, widget=forms.TextInput(
        {'class': 'form-control', 'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(
        {'class': 'form-control', 'placeholder': 'Password'}))


class WorkOrderForm(forms.Form):
    # center = forms.CharField(label='Center', max_length=100)
    description = forms.CharField(
        label='Description', max_length=100, widget=forms.Textarea(attrs={'rows': 3, 'cols': 15}))
    status = forms.ChoiceField(
        choices=(('created', 'created'), ('complete', 'complete')))
    # center.widget.attrs['class'] = 'form-control'
    description.widget.attrs['class'] = 'form-control'
    status.widget.attrs['class'] = 'form-control'
    status.widget.attrs['editable'] = 'true'


class JobForm(forms.Form):
    Team_leader = (('ze900536', 'Magaya'),
                   ('ze87645', 'Chinaka'), ('ze073589', 'Mavugara'))
    Job_Choice = (('inspection', 'Inspection'),
                  ('Mantainance', 'Mantainance'), ('OverHaul', 'OverHaul'))
    assignee = forms.ChoiceField(choices=Team_leader)
    type = forms.ChoiceField(choices=Job_Choice)
    description = forms.CharField(label='description', widget=forms.Textarea(
        {'rows': 3, 'cols': 15, 'class': 'form-control', 'type': 'text'}))
    workflow_id = forms.ChoiceField(
        choices=(('Workflow1', 'Work Flow 1'), ('Work Flow 2', 'Work Flow 2')))

    type.widget.attrs['class'] = 'form-control'
    assignee.widget.attrs['class'] = 'form-control'
    workflow_id.widget.attrs['class'] = 'form-control'


class assetForm(forms.Form):
    user_center = (('Dangamvura', 'Dangamvura'),
                   ('Urburn', 'Urburn'), ('Manicaland', 'Manicaland'))

    Team_Choice = (('ze900536', 'Magaya'),
                   ('ze87645', 'Chinaka'), ('ze073589', 'Mavugara'))
    asset_id = forms.CharField(max_length=100, label='Asset Id', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))
    asset_name = forms.CharField(max_length=100, label='Asset Name', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))
    asset_type = forms.ChoiceField(
        choices=(('Transformer', 'Transformer'), ('Switch', 'Switch Gear')))
    asset_number = forms.CharField(max_length=100, label='Asset Number', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))
    expected_end_dt = forms.DateTimeField(label='Expected End Date', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'date'}))
    reference_no = forms.CharField(max_length=100, label='Ref Number', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))
    asset_serial = forms.CharField(max_length=100, label='Serial Number', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))
    # This field type is a guess.
    geom = forms.CharField(label='Geometry Number', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))

    team = forms.MultipleChoiceField(choices=Team_Choice)
    team.widget.attrs['class'] = 'form-control'
    asset_type.widget.attrs['class'] = 'form-control'


class GeneralForm(forms.Form):
    created_by = forms.CharField(max_length=100, label='Created By', widget=forms.TextInput({
        'class': 'form-control', 'value': '',
        'type': 'text'}))
    created_on = forms.DateTimeField(label='Created On', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'date'}))
    modified_by = forms.CharField(max_length=100, label='Modified By', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))
    modified_on = forms.DateTimeField(label='Modified On', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'date'}))
    comments = forms.CharField(label='Comments', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'text'}))
    closed_by = forms.CharField(max_length=100, label='Closed By', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'date'}))
    closed_dt = forms.DateTimeField(label='Closed Date', widget=forms.TextInput({
        'class': 'form-control',
        'type': 'date'}))


class TeamForm(forms.Form):
    Team = forms.CharField(label='Team Name', widget=forms.TextInput({
        'class': 'form-control'}), max_length=100)


class E84Form(forms.Form):
    your_name = forms.CharField(label='your name', max_length=100)


class NameForm(forms.Form):
    your_name = forms.CharField(label='your name', max_length=100)
