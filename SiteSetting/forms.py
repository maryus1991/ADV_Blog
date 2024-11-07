from django import forms
from .models import Contact
from ckeditor.widgets import CKEditorWidget


class ContactModelForm(forms.ModelForm):
    """
    creating form for contact model
    """

    # add  ckeditor.widgets to message for contact
    message = forms.CharField(
        widget=CKEditorWidget(
            config_name="comment",
            attrs={
                "placeholder": "Enter message",
                "id": "validationDefault05",
                "cols": "350",
                "rows": "10",
            },
        )
    )

    class Meta:
        # add and set the configurations
        model = Contact
        fields = ("full_name", "email", "phone_number", "subject", "message")

        widgets = {
            "full_name": forms.TextInput(
                attrs={"placeholder": "Full Name", "id": "validationDefault01"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "id": "validationDefault02"}
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Phone Number", "id": "validationDefault03"}
            ),
            "subject": forms.TextInput(
                attrs={"placeholder": "Phone Number", "id": "validationDefault04"}
            ),
        }
