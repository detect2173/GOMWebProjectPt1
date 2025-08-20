from django import forms


class LeadMagnetForm(forms.Form):
    name = forms.CharField(max_length=120, required=False, label="Name (optional)")
    email = forms.EmailField(label="Email")
    consent = forms.BooleanField(
        label="I agree to receive the free guide and occasional emails", required=True
    )
