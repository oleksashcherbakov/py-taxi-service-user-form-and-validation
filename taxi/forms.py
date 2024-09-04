from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    @staticmethod
    def validate_license_number(license_number):
        if (
            license_number
            and len(license_number) == 8
            and license_number[:3].isalpha()
            and (license_number[:3].isupper() and license_number[3:].isdigit())
        ):
            return True
        return False

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if self.validate_license_number(license_number):
            return license_number
        raise ValidationError("Provided license is not correct")


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
            "email",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if DriverLicenseUpdateForm.validate_license_number(license_number):
            return license_number
        else:
            raise ValidationError("This license is wrong")


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
