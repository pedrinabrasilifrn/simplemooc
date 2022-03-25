from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, PasswordReset
from core.utils import generate_hash_key
from core.mail import send_mail_template

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput) 
    confirm = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm  = self.cleaned_data.get('confirm')
        if password and confirm and password != confirm:
            raise forms.ValidationError('A confirmação não está correta.')
        return confirm

    def save(self, commit = True):
        user = super(RegisterForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['email', 'name']

class EditAccountForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('E-mail já cadastrado.')
        return email

    class Meta:
        model = User
        fields = [ 'email', 'name']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário cadastrado com este e-mail')

    def save(self):
        user = User.objects.get(email = self.cleaned_data['email'])
        key = generate_hash_key(user.email)
        reset = PasswordReset(key= key, user = user)
        reset.save()
        template_name = 'password_reset_email.html'
        subject = 'Redefinir senha'
        context = {
            'reset' : reset,
        }
        send_mail_template(subject, template_name, context, [user.email])
