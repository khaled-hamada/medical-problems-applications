#configure setting for import files
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shakawi_manzoma.settings')
import django
django.setup()

from shakawi.models import Shab,Note_Type,Medical
from datetime import date



def get_shab_num(year_rec, note_type, city, status):
            shab_num = 1

            if status == 1 :
                shab_num = len(Shab.objects.filter(date_recored__year = year_rec, note_type = note_type, shab_city = city)) +1
            elif status ==0:
                shab_num = len(Shab.objects.filter(date_recored = year_rec, note_type = note_type, shab_city = city)) +1



            return shab_num



shab_year = 2000
shab_num = 1
shab_markaz = 201

shab_name_o = "خالد حمادة منصور"

shab_city = "القنال"

notes = Note_Type.objects.all()
medicals = Medical.objects.all()


shab_image ="C:/Users/emad/Desktop/shakawi_manzoma/shakawi_manzoma/shakawi/static/shakawi/background.JPG"
# shab_image = None
rays="اشعة"
reports = "ابحاث"
mosalsal=Shab.objects.all().last().shab_mosalsal + 1
for note in notes :
    print("note g_id %d"%(note.g_id))
    for medical in medicals:
        for m in range(5):
                medical_dec = medical.note
                note_type = note.note
                ## 1 continous count
                if note_type == '72 جند غير لائق':
                    shab_num = get_shab_num(date.today(), note_type, shab_city,0)
                elif note_type !='بدون' and note_type !='كشف قدرة' and  note_type !='كشف 10%':
                    shab_num = get_shab_num(date.today().year, note_type, shab_city,1)
                else:
                    shab_num = 0

                shab_name = shab_name_o+"-"+str(m)

                new_sh=Shab(shab_num = shab_num, shab_year=shab_year, shab_markaz= shab_markaz, shab_mosalsal = mosalsal, shab_name = shab_name,
                            shab_city = shab_city, medical_dec = medical_dec, note_type = note_type, shab_image = shab_image ,rays = rays, reports = reports)

                mosalsal +=1
                new_sh.save()
