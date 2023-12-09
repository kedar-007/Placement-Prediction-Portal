from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from .models import EligibleCompany
from decimal import Decimal
from student import models as student
from exam.models import Result
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

 
 
 
 
 
#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')
def Aboutus(request):
    return render(request,'exam/about1.html')
def Contact1 (request):
    return render(request,'exam/contact1.html')
 
def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)
 
 
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):  # sourcery skip: remove-unreachable-code
    student = models.Student.objects.get(user=request.user)
 
    tenth_marks = Decimal(student.tenth_marks) if student.tenth_marks else Decimal(0)
    twelfth_marks = Decimal(student.twelfth_marks) if student.twelfth_marks else Decimal(0)
    graduation_marks = Decimal(student.graduation_marks) if student.graduation_marks else Decimal(0)
    graduation_branch = student.graduation_branch if student.graduation_branch else ""
 
    if graduation_branch=='CS':
        # Check if the student's 10th marks and 12th marks are greater than 60
        if tenth_marks >= 60 and twelfth_marks >= 60 and graduation_marks >= 60:
         return render(request,'student/cse.html')
        elif tenth_marks >=35 and twelfth_marks >= 35 and graduation_marks >= 50:
            return render(request,'student/cse60.html')
        else: 
            HttpResponseRedirect("SORRY YOU ARE ")
    
    if graduation_branch=='CE':
        # Check if the student's 10th marks and 12th marks are greater than 60
        if tenth_marks >= 60 and twelfth_marks >= 60 and graduation_marks >= 60:
         return render(request,'student/ece.html')
        elif tenth_marks >=35 and twelfth_marks >= 35 and graduation_marks >= 50:
            return render(request,'student/ece60.html')
        else: 
            HttpResponseRedirect("SORRY YOU ARE ")
        
    
    if graduation_branch=='CH':
        # Check if the student's 10th marks and 12th marks are greater than 60
        if tenth_marks >= 60 and twelfth_marks >= 60 and graduation_marks >= 60:
         return render(request,'student/chem.html')
        elif tenth_marks >=35 and twelfth_marks >= 35 and graduation_marks >= 50:
            return render(request,'student/chem.html')
        else:
            HttpResponseRedirect("Soory Your academic score is to low")
    if graduation_branch=='ME':
        # Check if the student's 10th marks and 12th marks are greater than 60
        if tenth_marks >= 60 and twelfth_marks >= 60 and graduation_marks >= 60:
         return render(request,'student/mech.html')
        elif tenth_marks >=35 and twelfth_marks >= 35 and graduation_marks >= 50:
            return render(request,'student/mech.html')
        else:
            HttpResponseRedirect("SORRY YOUR ACADEMICS SCORE IS TOO LOW")
    context = {
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'student': student,
        'tenth_marks': tenth_marks,
        'twelfth_marks': twelfth_marks,
 
    }
 
    return render(request, 'student/student_dashboard.html', context=context)
 
 
 
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
 
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response
 
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
 
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
 
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()
 
        return HttpResponseRedirect('view-result')
 
 
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
 
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})
 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})

def Prediction(request):
    student = models.Student.objects.get(user=request.user)
    
    tenth_marks = float(student.tenth_marks) if student.tenth_marks else float(0)
    twelfth_marks = float(student.twelfth_marks) if student.twelfth_marks else float(0)
    graduation_marks = float(student.graduation_marks) if student.graduation_marks else float(0)
    result = Result.objects.last()
    if result:
        marks_data =float(result.marks)
    print(marks_data)
        
    df=pd.read_csv("D:\portal\data2.csv")

    df =df.drop(["Internships"],axis=1)
    df =df.drop(["Gender"],axis=1)
    df =df.drop(["Stream"],axis=1)
     # Replace with the actual path to your dataset file

    # Separate the features (X) and the target variable (y)
    X = df.drop("PlacedOrNot", axis=1)  # Replace "PlacedOrNot" with the actual target column name
    y = df["PlacedOrNot"]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create an instance of Logistic Regression model
    model = LogisticRegression()

    # Train the model using the training data
    model.fit(X_train, y_train)

    # Make predictions on the test data
    X_new = [[marks_data, graduation_marks, twelfth_marks, tenth_marks]]
    pred = model.predict(X_new)
    print(pred)
    print(X_new)
    if pred==[1] and marks_data>=60:
        return render(request,'student/PredYes.html')
    else:
        return render(request,'student/PredNo.html')


    # Convert the prediction to the desired output format