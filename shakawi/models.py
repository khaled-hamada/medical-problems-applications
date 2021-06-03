from django.db import models
from datetime import date
# Create your models here.

class Shab(models.Model):
    shab_num = models.IntegerField()
    shab_year = models.IntegerField()
    shab_markaz = models.IntegerField()
    shab_mosalsal = models.IntegerField()
    shab_name = models.CharField(max_length = 255)
    shab_city = models.CharField(max_length = 64)
    medical_dec  =models.CharField(max_length = 64)
    note_type  =models.CharField(max_length = 64)
    shab_image = models.FileField(upload_to='shakawi_data/%Y/%m/%d')
    date_recored = models.DateField(default = date.today)
    rays = models.CharField(max_length = 64, default="")
    reports = models.CharField(max_length = 64, default="")


    def __str__(self):
        return self.shab_name + "  --->  الرقم الثلاثى : "+str(self.shab_year)+"-"+str(self.shab_markaz)+"-"+str(self.shab_mosalsal) + "    --  تاريخ التسجيل " + str(self.date_recored)







class Medical(models.Model):
    id = models.AutoField(primary_key = True)
    g_id = models.IntegerField(default=0)
    note = models.CharField(max_length=128)
    # name = models.CharField(max_length=50 , default="")

    def __str__(self):
        return self.note +" ------ ID -> " + str(self.g_id)
class Note_Type (models.Model):
    id = models.AutoField(primary_key = True)
    g_id = models.IntegerField(default=0)
    note  = models.CharField(max_length=128)

    def __str__(self):
        return self.note +" ------ ID ->" + str(self.g_id)
