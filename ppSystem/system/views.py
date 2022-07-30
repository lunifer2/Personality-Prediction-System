from pickle import NONE
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
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
def register(request):
    if request.method== "POST":
     rg= RegisterForm(request.POST)
     if rg.is_valid():
        
        messages.success(request,'Account registered succesfully')
        rg.save()
        return HttpResponseRedirect('/login/')
    else:
     rg = RegisterForm()
    return render(request, 'register.html',{'form':rg})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
         lg=LoginForm(request=request,data=request.POST)
         if lg.is_valid():
            uname=lg.cleaned_data['username']
            upassword=lg.cleaned_data['password']
            user= authenticate(username=uname,password=upassword)
            # if user is not None:
            #     uid=str(request.user.id)
            #     res= UserProfile.objects.get(user_id=uid)  
            #     if res is not NONE:
                     
            #         #  user=request.user
            if request.user.is_anonymous:
                users= request.user.id
                if users is not None:
                     return redirect('result_id',id=users)
                
                login(request, user)

                return render(request,'profile.html')
        else:
            lg= LoginForm()
        return render(request, 'login.html',{'form':lg})
    else:
        
         return redirect('/profile/')   

def profile(request):
 if request.user.is_authenticated:
        if request.method== 'POST':
            pr=ProfileForm(request.POST,request.FILES,instance=request.user)
            if pr.is_valid():
                uage=pr.cleaned_data.get("age")
                uphone=pr.cleaned_data.get("phone")
                ugender=pr.cleaned_data.get("gender")
                ucv=pr.cleaned_data.get("upload_cv")
                uoppeness=pr.cleaned_data.get("oppeness")
                uneuroticism=pr.cleaned_data.get("neuroticism")
                uconscientiousness=pr.cleaned_data.get("conscientiousness")
                uagreeableness=pr.cleaned_data.get("agreeableness")
                uextraversion=pr.cleaned_data.get("extraversion")
                uid=str(request.user.id)
                pro=UserProfile(age=uage,phone=uphone,gender=ugender,upload_cv=ucv,oppeness=uoppeness,neuroticism=uneuroticism,conscientiousness=uconscientiousness,agreeableness=uagreeableness,extraversion=uextraversion,user_id=uid)

                pro.save()
                # return render(request,'results.html',{'pk':uid,'name':request.user})
                return redirect('result_id',id=uid)
            else:
                pr=UserProfile()
                return render(request,'profile.html',{'form':pr,'name':request.user})
        else:
         pr=ProfileForm()
         return render(request,'profile.html',{'form':pr,'name':request.user})
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

# def prediction_result(top, aplcnt_name, cv_path, personality_values):
#     "after applying a job"
#     top.withdraw()
#     applicant_data={"Candidate Name":aplcnt_name.get(),  "CV Location":cv_path}
    
#     age = personality_values[1]
    
#     print("\n############# Candidate Entered Data #############\n")
#     print(applicant_data, personality_values)
    
#     personality = model.test(personality_values)
#     print("\n############# Predicted Personality #############\n")
#     print(personality)
#     data = ResumeParser(cv_path).get_extracted_data()
    
#     try:
#         del data['name']
#         if len(data['mobile_number'])<10:
#             del data['mobile_number']
#     except:
#         pass
    
#     print("\n############# Resume Parsed Data #############\n")

#     for key in data.keys():
#         if data[key] is not None:
#             print('{} : {}'.format(key,data[key]))
    
#     result=Tk()
#   #  result.geometry('700x550')
#     result.overrideredirect(False)
#     result.geometry("{0}x{1}+0+0".format(result.winfo_screenwidth(), result.winfo_screenheight()))
#     result.configure(background='White')
#     result.title("Predicted Personality")
    
#     #Title
#     (result, text = str('{} : {}'.format("Name:", aplcnt_name.get())).title(), foreground='black', bg='white', anchor='w').pack(fill=BOTH)
#     (result, text = str('{} : {}'.format("Age:", age)), foreground='black', bg='white', anchor='w').pack(fill=BOTH)
#     for key in data.keys():
#         if data[key] is not None:
#             (result, text = str('{} : {}'.format(check_type(key.title()),check_type(data[key]))), foreground='black', bg='white', anchor='w', width=60).pack(fill=BOTH)
#     (result, text = str("perdicted personality: "+personality).title(), foreground='black', bg='white', anchor='w').pack(fill=BOTH)

    
#     terms_mean = """
# # Openness:
#     People who like to learn new things and enjoy new experiences usually score high in openness. Openness includes traits like being insightful and imaginative and having a wide variety of interests.

# # Conscientiousness:
#     People that have a high degree of conscientiousness are reliable and prompt. Traits include being organised, methodic, and thorough.

# # Extraversion:
#     Extraversion traits include being; energetic, talkative, and assertive (sometime seen as outspoken by Introverts). Extraverts get their energy and drive from others, while introverts are self-driven get their drive from within themselves.

# # Agreeableness:
#     As it perhaps sounds, these individuals are warm, friendly, compassionate and cooperative and traits include being kind, affectionate, and sympathetic. In contrast, people with lower levels of agreeableness may be more distant.

# # Neuroticism:
#     Neuroticism or Emotional Stability relates to degree of negative emotions. People that score high on neuroticism often experience emotional instability and negative emotions. Characteristics typically include being moody and tense.    
# """
    
#     Label(result, text = terms_mean, foreground='green', bg='white', anchor='w', justify=LEFT).pack(fill=BOTH)

#     result.mainloop()
    

# def perdict_person():
#     """Predict Personality"""
    
#     # Closing The Previous Window
#     root.withdraw()
    
#     # Creating new window
#     top = Toplevel()
#     top.geometry('700x500')
#     top.configure(background='black')
#     top.title("Apply For A Job")
    
#     #Title
#     titleFont = font.Font(family='Helvetica', size=20, weight='bold')
#     lab=Label(top, text="Personality Prediction", foreground='red', bg='black', font=titleFont, pady=10).pack()

#     #Job_Form
#     # job_list=('Select Job', '101-Developer at TTC', '102-Chef at Taj', '103-Professor at MIT')
#     # job = StringVar(top)
#     # job.set(job_list[0])
#     submitBtn.config(command=lambda: prediction_result(top,sName,loc,(gender.get(),age.get(),openness.get(),neuroticism.get(),conscientiousness.get(),agreeableness.get(),extraversion.get())))
#     submitBtn.place(x=350, y=400, width=200)
    

#     top.mainloop()

# def OpenFile(b4):
#     global loc;
#     name = filedialog.askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
#                             filetypes =(("Document","*.docx*"),("PDF","*.pdf*"),('All files', '*')),
#                            title = "Choose a file."
#                            )
#     try:
#         filename=os.path.basename(name)
#         loc=name
#     except:
#         filename=name
#         loc=name
#     b4.config(text=filename)
#     return



# if __name__ == "__main__":
#     model = train_model()
#     model.train()

#     root = Tk()
#     root.geometry('1440x1024')
#     root.configure(background='orange')
#     root.title("Personality Prediction System")
#     titleFont = font.Font(family='Helvetica', size=25, weight='bold')
#     homeBtnFont = font.Font(size=12, weight='bold')
#     lab=Label(root, text="Personality Prediction System", bg='white', font=titleFont, pady=30).pack()
#     b2=Button(root, padx=4, pady=4, width=30, text="Predict Personality", bg='black', foreground='white', bd=1, font=homeBtnFont, command=perdict_person).place(relx=0.5, rely=0.5, anchor=CENTER)
#     root.mainloop()
