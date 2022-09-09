from pickle import NONE
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from requests import request
from .models import UserProfile
from .forms import ProfileForm, RegisterForm,LoginForm,ProfileForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import os
import pandas as pd
import numpy as np
from functools import partial
from pyresparser import ResumeParser
from sklearn import datasets, linear_model 
# Create your views here.
def info(request):
    if request.user.is_authenticated:
        return render(request,'info.html',{'name':request.user})
    else:
        return redirect('/login/')
   

    
def register(request):
    if request.method== "POST":
     rg= RegisterForm(request.POST)
     if rg.is_valid():
        
        messages.success(request,'Account registered succesfully')
        rg.save()
        return HttpResponseRedirect('/login/')
    else:
     rg = RegisterForm()
    return render(request, 'register1.html')

def user_login(request):
    print('asd')
    if not request.user.is_authenticated:
        
        if request.method == "POST":
            print('sdasd')
            lg=LoginForm(request=request,data=request.POST)
            if lg.is_valid():
                uname=lg.cleaned_data['username']
                upassword=lg.cleaned_data['password']
                user= authenticate(username=uname,password=upassword)
            
                login(request, user)
                return render(request,'questions.html')
        else:
            lg= LoginForm()
        return render(request, 'login1.html')
    else:
        
         return redirect('/profile/')   

def profile(request):
 if request.user.is_authenticated:
        if request.method== 'POST':
            pr=ProfileForm(request.POST,request.FILES,instance=request.user)
            if pr.is_valid():
                uage=pr.cleaned_data.get("candidate_age")
                uphone=pr.cleaned_data.get("candidate_phone")
                ugender=pr.cleaned_data.get("flexradioDefault")
                ucv=pr.cleaned_data.get("cv")
                uoppeness=pr.cleaned_data.get("oppeness")
                uneuroticism=pr.cleaned_data.get("neuroticism")
                uconscientiousness=pr.cleaned_data.get("conscientiousness")
                uagreeableness=pr.cleaned_data.get("agreeableness")
                uextraversion=pr.cleaned_data.get("extraversion")
                uid=str(request.user.id)
                pro=UserProfile(age=uage,phone=uphone,gender=ugender,upload_cv=ucv,oppeness=uoppeness,neuroticism=uneuroticism,conscientiousness=uconscientiousness,agreeableness=uagreeableness,extraversion=uextraversion,user_id=uid)

                pro.save()
                # return render(request,'results.html',{'pk':uid,'name':request.user})
                class train_model:
    
                    def train(self):
                        data =pd.read_csv('training_dataset.csv')
                        array = data.values

                        for i in range(len(array)):
                            if array[i][0]=="Male":
                                array[i][0]=1
                            else:
                                array[i][0]=0

                        df=pd.DataFrame(array)

                        maindf =df[[0,1,2,3,4,5,6]]
                        mainarray=maindf.values

                        temp=df[7]
                        train_y =temp.values
                        
                        self.mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter =1000)
                        self.mul_lr.fit(mainarray, train_y)
                        
                    def test(self, test_data):
                        try:
                            test_predict=list()
                            for i in test_data:
                                test_predict.append(int(i))
                            y_pred = self.mul_lr.predict([test_predict])
                            return y_pred
                        except:
                            print("All Factors For Finding Personality Not Entered!")

                    def check_type(data):
                        if type(data)==str or type(data)==str:
                         return str(data).title()
                        if type(data)==list or type(data)==tuple:
                         str_list=""
                         for i,item in enumerate(data):
                            str_list+=item+", "
                         return str_list
                        else:   return str(data)

                    def prediction_result (personality_values):
                     
                    
                     uage = personality_values[1] 
                     personality = train_model.test(personality_values)
                     data = ResumeParser(ucv).get_extracted_data()

                     for key in data.keys():
                        if data[key] is not None:
                            print('{} : {}'.format(key,data[key]))
                    
                    def perdict_person():
                     val=train_model.prediction_result(ugender,uage,uoppeness,uneuroticism,uconscientiousness,uagreeableness,uextraversion)

                   
                return redirect('result_id',id=uid)
            else:
                pr=UserProfile()
                return render(request,'questions.html',{'name':request.user})
        else:
         pr=ProfileForm()
         return render(request,'questions.html',{'name':request.user})
 else:
  return redirect('/login/')



def result_id(request,id):
    if request.user.is_authenticated:
        
        
        res= UserProfile.objects.get(user_id=id)   
        return render(request,'results.html',{'resu':res,'name':request.user,'fname':request.user.first_name,'lname':request.user.last_name}) 
    else:
     return redirect('/profile/')
   

def user_logout(request):
    logout(request)
    return redirect('/login/')

