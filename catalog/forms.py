from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import BookInstance
import datetime


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Introduce una fecha entre hoy y dentro de 4 semanas (por defecto 3)')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Verificar que la fecha no haya pasado
        if data < datetime.date.today():
            raise ValidationError(_('Fecha no valida - Pasada fecha de renovación'))
        
        #Verificar que la fecha no supera las 4 semanas
        if data > datetime.date.today() + datetime.timedelta(weeks = 4):
            raise ValidationError(_('Fecha no valida - La renovación no puede ser superior a 4 semanas'))
        
        return data
    
# Lo mismo pero con ModelForm
# class RenewBookModelForm(ModelForm):
#     def clean_due_back(self):
#        data = self.cleaned_data['due_back']

#        #Check date is not in past.
#        if data < datetime.date.today():
#            raise ValidationError(_('Invalid date - renewal in past'))

#        #Check date is in range librarian allowed to change (+4 weeks)
#        if data > datetime.date.today() + datetime.timedelta(weeks=4):
#            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

#        # Remember to always return the cleaned data.
#        return data

#     class Meta:
#         model = BookInstance
#         fields = ['due_back',]
#         labels = { 'due_back': _('Renewal date'), }
#         help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), }