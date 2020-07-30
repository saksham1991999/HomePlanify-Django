from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models

class propertyForm(forms.ModelForm):
    class Meta:
        model = models.property
        exclude = ['verified', 'views', 'owner', 'visible', 'dateadded', 'featured']
        labels = {
            'type': _('Select Type'),
            'property_name': _('Property Name'),
            'city': _('City'),
            'bedrooms': _('No of Bedrooms'),
            'bathrooms': _('No of Bathrooms'),
            'rooms': _('No of Rooms'),
            'construction_status': _('Construction Status (Optional)'),
            'available_from': _('Available from Date (YYYY-MM-DD) (Optional)'),
            'price_sq': _('Price per sq m (Optional)'),
            'total_price': _('Total Price'),
            'additional_features': _('Additional Features'),
            'image': _('Main Image'),
            'label': _('Label (Optional)'),
            'features': _('Features (Multi-Select)'),
            'video': _('Add a Video (Optional)'),
        }
        widgets = {
            'features': forms.SelectMultiple(attrs={'style':'height: auto;'})
        }

class contactForm(forms.ModelForm):
    class Meta:
        model = models.contact
        fields = [
            'name',
            'email',
            'subject',
            'message',
        ]

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = models.enquiry
        fields = [
            'name',
            'mobile_no',
            'email',
            'subject',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'mobile_no': forms.TextInput(attrs={'placeholder': 'Mobile Number', 'pattern':'[0-9]{10}'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email ID'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
        }

class MainEnquiryForm(forms.ModelForm):
    class Meta:
        model = models.enquiry
        fields = [
            'name',
            'mobile_no',
            'email',
            'subject',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'mobile_no': forms.TextInput(attrs={'placeholder': 'Mobile Number', 'pattern':'[0-9]{10}'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email ID'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
        }

        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a'}),
        #     'sender_email': forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a'}),
        #     'mobile_number': forms.NumberInput(attrs={'class': 'form-control form-control-lg form-control-a'}),
        #     'whatsapp_number': forms.NumberInput(attrs={'class': 'form-control form-control-lg form-control-a'}),
        #     'street_address': forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a'}),
        #     'city': forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a'}),
        #     'pincode': forms.NumberInput(attrs={'class': 'form-control form-control-lg form-control-a'}),
        #     'message': forms.Textarea(attrs={'class': 'form-control form-control-lg form-control-a', 'rows': 4}),
        #     'country': CountrySelectWidget(
        #         attrs={'class': 'form-control form-control-lg form-control-a', 'style': "margin-bottom: 25px"}),
        #     'product_quantity': forms.NumberInput(
        #         attrs={'min': '100', 'class': 'form-control form-control-lg form-control-a',
        #                'style': "margin-bottom: 25px"}),
        #     'product': forms.Select(
        #         attrs={'class': 'form-control form-control-lg form-control-a', 'style': "margin-bottom: 25px"}),
        #
        # }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name']


class ImagesForm(forms.ModelForm):
    class Meta:
        model = models.images
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'multiple': True})
        }


class SingupForm(forms.ModelForm):
    email = forms.CharField(label='E-mail', min_length=3)
    password1 = forms.CharField(label='Password', min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password', min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.User
        fields = ['email', 'password1', 'password2']


class LoginForm(forms.ModelForm):
    email = forms.CharField(label='E-mail', min_length=3)
    password = forms.CharField(label='Password', min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.User
        fields = ['email', 'password']