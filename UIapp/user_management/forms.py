__author__ = 'mpetyx'


from django import forms
from django.contrib.auth.models import User, Group, Permission


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['id']

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass