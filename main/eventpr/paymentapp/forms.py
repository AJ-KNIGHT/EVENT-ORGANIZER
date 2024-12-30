from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['proof_of_payment', 'payment_method', 'amount']

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        # Make proof of payment optional
        self.fields['proof_of_payment'].required = False  
        self.fields['proof_of_payment'].widget.attrs.update({'class': 'form-control'})
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})

    def clean_payment_method(self):
        payment_method = self.cleaned_data.get('payment_method')
        # Allow Razorpay as a valid payment method
        if payment_method not in ['UPI', 'Bank Transfer', 'Cash', 'Online', 'Razorpay']:
            raise forms.ValidationError("Invalid payment method.")
        return payment_method
