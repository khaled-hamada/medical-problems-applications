from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Shab,Note_Type,Medical
from datetime import datetime,date
from django.contrib.sessions.models import Session
# Create your views here.


def home(request):
   
    if request.method == 'POST':
        # print(request.POST)
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            failed =0
            login(request, user)
            # request.session.set_expiry(1)

            print('username: ' + request.user.username + ' has log in to system at ' + str(datetime.now()))

            if user.groups.filter(name='فرع الشكاوى').exists():
                #return redirect('taktet/')
                return shakawi_user(request)

            ## all general users have only one view page -> search for single persons data
            elif  user.groups.filter(name='مستخدم عام').exists():
                return general_user(request)

        else:
            failed =1
            context = {'failed' : failed,
                        'show':0,

                        }
            return render(request, 'shakawi/login.html', context = context)


    return render(request, 'shakawi/login.html',  context={'show':0} )

@login_required
def logout_view(request):
    logout(request)
    # print('username: ' + userna + ' has log out of system at ' + str(datetime.now()))

    return render(request, 'shakawi/login.html' , context={'show':0})





@login_required
@user_passes_test(lambda u: u.groups.filter(name='فرع الشكاوى').count() != 0, login_url='/denied')
def shakawi_user(request):

    return redirect('shakawi:new_shab_fit',0)



@login_required
@user_passes_test(lambda u: u.groups.all().count() != 0, login_url='/denied')
def general_user(request):
    # context = {'times':1}
    # return render(request, 'shakawi/search_single.html', context = context)
    return redirect('shakawi:search_single')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='فرع الشكاوى').count() != 0, login_url='/denied')
def new_shab(request,page_id):

    ###########
    ##  page id
    ## 0.  new shab fit
    ## 1. new shab unfit
    ## 2. new shab ability
    ## 3. new shab 10%
    ##########


    if request.method == 'POST':
        rays = ""
        reports=""
        shab_name=""
        shab_year = request.POST['year']
        shab_markaz = request.POST['markaz']
        shab_mosalsal = request.POST['mosalsal']
        if 'name' in request.POST:
            shab_name = request.POST['name']
        shab_city = request.POST['city']

        medical_dec = request.POST['medical_dec']
        medical_dec = Medical.objects.get(g_id = int(medical_dec)).note

        note_type = request.POST['note_type']
        note_type = Note_Type.objects.get(g_id = int(note_type)).note

        shab_image = request.FILES['image']
        if 'rays' in request.POST:
            rays = request.POST['rays']
        if 'reports' in request.POST:
            reports = request.POST['reports']
        shab_data = Shab.objects.filter(shab_year  = shab_year, shab_markaz = shab_markaz, shab_mosalsal = shab_mosalsal , date_recored = date.today() )
        if (len(shab_data)) > 0:

            context ={
                'data' : shab_data.first(),

                'show':1,
                'error':1,
            }
            return render(request, 'shakawi/show_single.html',context)
        else:
            if page_id == 0: ## new shab fit
                shab_num = get_shab_num(date.today().year, note_type, shab_city,1)
                new_sh=Shab(shab_num = shab_num, shab_year=shab_year, shab_markaz= shab_markaz, shab_mosalsal = shab_mosalsal, shab_name = shab_name,
                                    shab_city = shab_city, medical_dec = medical_dec, note_type = note_type, shab_image = shab_image ,rays = rays, reports = reports)

                new_sh.save()


            elif page_id == 1: ## new shab unfit
                shab_num = get_shab_num(date.today(), note_type, shab_city,0)
                new_sh=Shab(shab_num = shab_num, shab_year=shab_year, shab_markaz= shab_markaz, shab_mosalsal = shab_mosalsal, shab_name = shab_name,
                                    shab_city = shab_city, medical_dec = medical_dec, note_type = note_type, shab_image = shab_image ,rays = rays, reports = reports)

                new_sh.save()


            elif page_id == 2: ## new shab ability
                    shab_num =0
                    new_sh=Shab(shab_num = shab_num, shab_year=shab_year, shab_markaz= shab_markaz, shab_mosalsal = shab_mosalsal, shab_name = shab_name,
                                        shab_city = shab_city, medical_dec = medical_dec, note_type = note_type, shab_image = shab_image ,rays = rays, reports = reports)

                    new_sh.save()


            elif page_id == 3:## new shab 10%
                shab_num =0
                new_sh=Shab(shab_num = shab_num, shab_year=shab_year, shab_markaz= shab_markaz, shab_mosalsal = shab_mosalsal, shab_name = shab_name,
                                    shab_city = shab_city, medical_dec = medical_dec, note_type = note_type, shab_image = shab_image ,rays = rays, reports = reports)

                new_sh.save()

    total,medicals,notes = get_total_notes_medicals(int(page_id))

    context = {

                 'show':1,
                'sh_72':get_arabic_date(total),
                'notes' : notes,
                'medicals' : medicals,

                }
    if page_id==0 :## new shab fit
        return render(request, 'shakawi/new_shab_fit.html', context = context)
    elif page_id==1 :## new shab unfit
        return render(request, 'shakawi/new_shab_unfit.html', context = context)

    elif page_id==2 :## new shab ability
        return render(request, 'shakawi/new_shab_ability.html', context = context)

    elif page_id==3 :## new shab 10%
        return render(request, 'shakawi/new_shab_ten.html', context = context)




def get_total_notes_medicals(page_id):
    total = medical = notes = 0
    n_names = []
    if page_id ==0:## new shab fit
        notes = Note_Type.objects.filter(g_id__in=[1,2,6])
        medical = Medical.objects.filter(g_id__in=[1,2])
        n_names.extend([notes[0].note,notes[1].note,notes[2].note])
        total = len(Shab.objects.filter(date_recored = date.today(), note_type__in=n_names))
        if Shab.objects.filter(date_recored = date.today(), note_type__in=n_names) :
            print(date.today())
    elif page_id ==1:## new shab unfit
        notes = Note_Type.objects.filter(g_id__in=[3])
        medical = Medical.objects.filter(g_id__in=[3])
        n_names.extend([notes[0].note])
        total = len(Shab.objects.filter(date_recored = date.today(), note_type__in=n_names))
    elif page_id ==2:## new shab ability
        notes = Note_Type.objects.filter(g_id__in=[4])
        medical = Medical.objects.filter(g_id__in=[4,5])
        n_names.extend([notes[0].note])
        total = len(Shab.objects.filter(date_recored = date.today(), note_type__in=n_names))
    elif page_id ==3:## new shab 10%
        notes = Note_Type.objects.filter(g_id__in=[5])
        medical = Medical.objects.filter(g_id__in=[6,7])
        n_names.extend([notes[0].note])
        total = len(Shab.objects.filter(date_recored = date.today(), note_type__in=n_names))


    return (total,medical,notes)


###########################################
# get each new shab id based on there filters
#1. city
#2. note_type
#3. year of date_recored
#4. status 1. continous counting from start to the end of the year
#   status 0 . count day by day
#################################################
def get_shab_num(year_rec, note_type, city, status):
    shab_num = 1

    if status == 1 :
        shab_num = len(Shab.objects.filter(date_recored__year = year_rec, note_type = note_type, shab_city = city)) +1
    elif status ==0:
        shab_num = len(Shab.objects.filter(date_recored = year_rec, note_type = note_type, shab_city = city)) +1



    return shab_num



###############################################################################
#
#\ all users  views
################################################################################

@login_required
@user_passes_test(lambda u: u.groups.all().count() != 0, login_url='/denied')
def search_single(request):
    if request.method == "POST":
        year = request.POST['year']
        markaz = request.POST['markaz']
        mosalsal = request.POST['mosalsal']
        shab_data = Shab.objects.filter(shab_year = year, shab_markaz = markaz, shab_mosalsal = mosalsal).last()
        # date = get_arabic_date(shab_data.date_recored)
        # shab_data.date_recored = date
        context ={
            'data' : shab_data,

            'show':1,
        }
        return render(request, 'shakawi/show_single.html',context)
    else:
        context = {

                    'show':1,
                    }
        return render(request, 'shakawi/search_single.html',  context = context)


from django.utils.translation import gettext as _

@login_required
@user_passes_test( lambda u :u.groups.filter(name='فرع الشكاوى').count() != 0 , login_url='/denied')
def print_reports(request):

    if request.method == "POST":
        search_date = request.POST['date_recored']
        if not search_date:
            search_date = date.today()
        city = request.POST['city']
        note_type = int(request.POST['note_type'])
        note_type = Note_Type.objects.get(g_id = note_type).note

        data = Shab.objects.filter(shab_city = city, note_type = note_type , date_recored = search_date).order_by('shab_num')
        print("data found # %d"%(len(data)))
        search_date = get_arabic_date(search_date)
        context = {
            'data':data,
            'search_date':search_date,
            'city':city,
            'note_type':note_type,

            'show':1,
        }

        return render(request,'shakawi/show_reports.html',context = context)

    notes = Note_Type.objects.filter(g_id__in=[1,2,3,6])
    context = {
                'show':1,
                'notes' : notes,
                }



    return render(request, 'shakawi/search_reports.html',context = context)



def get_arabic_num(number):
    arabicNumbers = {
                        0:'۰',
                        1:'١'
                        ,2: '٢'
                        ,3: '٣'
                        ,4: '٤'
                        , 5:'٥'
                        , 6:'٦'
                        , 7:'٧'
                        , 8:'٨'
                        , 9:'٩'


                    }
    return arabicNumbers.get(number)

def get_arabic_date(search_date):
    str_date = str(search_date)
    output =""
    for num in str_date:
        if num !='-':
            output += str(get_arabic_num(int(num)))
        else:
            output +=' / '
    output = output.split('/')
    result=""
    for part in range(len(output)-1,-1,-1):
        result +=output[part]+' / '
    result = result.rstrip(' / ')
    return result

@login_required
def denied(request):
    return render(request, 'shakawi/denied.html')





#############################
##
## display all departs with their ids
###############################
@login_required
@user_passes_test(lambda u: u.groups.all().count() != 0, login_url='/denied')
def data(request):
    notes = Note_Type.objects.all()
    medicals= Medical.objects.all()
    context ={
        'notes' : notes,
        'medicals' : medicals,
    }
    return render(request, 'shakawi/depts_users.html',context = context)
