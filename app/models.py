from django.db import models
from django.utils import timezone
from datetime import datetime

class Company(models.Model):
    key = models.CharField(max_length = 128, verbose_name = "Kompaniya KEY", unique = True)
    bot_token = models.CharField(max_length = 255, verbose_name = "Kompaniya telegram bot tokeni", unique = True)
    channel_id = models.CharField(max_length = 64, verbose_name = "Kompaniya kanal yoki guruh nomi", unique = True)
    create_at = models.DateTimeField(default = datetime.now, verbose_name = "Qo'shilgan vaqti")

    def __str__(self):
        return self.key

class Users(models.Model):
    user_id = models.IntegerField(verbose_name = "Foydalanuvchi IDsi")
    full_name = models.CharField(max_length = 128, verbose_name = "To'liq ismi")
    company_key = models.ForeignKey(Company, on_delete = models.CASCADE, verbose_name="Kompaniya")

    join_date = models.DateTimeField(default = datetime.now, verbose_name = "Kelgan vaqti")
    left_date = models.DateTimeField(default = datetime.now, verbose_name = "Ketgan vaqti")

    def __str__(self):
        return self.full_name

class Attendance(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE, verbose_name="Foydalanuvchilar")
    company = models.ForeignKey(Company, on_delete = models.CASCADE, verbose_name="Kompaniya")

    join_date = models.TimeField(null = True, blank = True, verbose_name = "Kelgan vaqti")
    left_date = models.TimeField(null = True, blank = True, verbose_name = "Ketgan vaqti")
    date = models.DateField(default = datetime.now, verbose_name = "Sana")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Davomat"
        verbose_name_plural = "Davomatlar"
