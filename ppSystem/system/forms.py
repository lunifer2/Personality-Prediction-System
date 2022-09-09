
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import UserProfile

class RegisterForm(UserCreationForm):
    # class Meta:
    #     model= User
    #     fields=['username','first_name','last_name','email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields["password1"].widget.attrs.update({
            'class':'register_pw','placeholder':'Enter password'
        })
        self.fields["password2"].widget.attrs.update({
            'class':'rewrite_pw','placeholder':'Re-enter password'
        })
        self.fields["username"].widget.attrs.update({
            'class':'register_username','placeholder':'Enter username'
        })
    class Meta:
        model= User
        fields= ['first_name','last_name','email','username','password1','password2']
        widgets= {
            'first_name':forms.TextInput(attrs={'class':'first_name','placeholder':'Your first name','required':True}),
        'last_name':forms.TextInput(attrs={'class':'last_name','placeholder':'Your last name','required':True}),
        'email':forms.EmailInput(attrs={'class':'register_email','placeholder':'Enter emailaddress','required':True}),
        
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class':'email','placeholder':'Enter username'
        })
        self.fields["password"].widget.attrs.update({
            'class':'password','placeholder':'Enter password'
        })
        class Meta:
         model= User
         fields= ['username','password']


class ProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)

        for upload_cv in self.fields:
            self.fields[upload_cv].required=False

    GENDER_CHOICES=[('Male',''),('Female',''),('Others','')]
    gender=forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect())
    class Meta:
        model= UserProfile
        fields= ['age','phone','gender','upload_cv','oppeness','conscientiousness','extraversion','agreeableness','neuroticism']
        # widgets={
        # 'age':forms.NumberInput(attrs={'name':'candidate_age','placeholder':'Enter your'}),
        # 'phone':forms.NumberInput(attrs={'class':'cand_phone','placeholder':'Your Phone number'}),
        # 'gender':forms.RadioSelect(),
        # 'upload_cv':forms.FileInput(attrs={'class':'upload_cv'}),
        # 'oppeness':forms.NumberInput(attrs={'class':'cand_oppeness','placeholder':'1-10 '}),
        # 'conscientiousness':forms.NumberInput(attrs={'class':'cand_conscientiousness','placeholder':'1-10'}),
        # 'extraversion':forms.NumberInput(attrs={'class':'cand_extraversion','placeholder':'1-10'}),
        # 'agreeableness':forms.NumberInput(attrs={'class':'cand_agreeableness','placeholder':'1-10'}),
        # 'neuroticism':forms.NumberInput(attrs={'class':'cand_neuroticism','placeholder':'1-10'}),}
