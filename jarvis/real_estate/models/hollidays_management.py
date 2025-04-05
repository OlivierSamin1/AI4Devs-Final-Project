from django.db import models
from datetime import timedelta, date


class HollydaysPlatform(models.Model):
    """
    Hollydays platform model
    """
    name = models.CharField(max_length=50, blank=False, null=True)
    personal_email_used = models.EmailField(null=True, blank=True)
    site_app_company = models.CharField(max_length=70, blank=True, null=True, help_text="ex: myfoncia.com")
    comments = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Hollydays Platforms"
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        return self.name


class HollydaysReservation(models.Model):
    """
    Hollydays Reservation model
    """
    platform = models.ForeignKey('real_estate.HollydaysPlatform', related_name='platform', blank=False, null=True, on_delete=models.CASCADE)
    asset = models.ForeignKey('real_estate.Asset', related_name='reservation', on_delete=models.CASCADE, blank=True, null=True, default=2)
    reservation_number = models.CharField(max_length=50, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    number_of_nights = models.SmallIntegerField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    renting_person_full_name = models.CharField(max_length=100, blank=True, null=True)
    renting_person_dni = models.CharField(max_length=20, blank=True, null=True)
    renting_person_direction = models.CharField(max_length=50, blank=True, null=True)
    renting_person_postcode = models.CharField(max_length=50, blank=True, null=True)
    renting_person_city = models.CharField(max_length=50, blank=True, null=True)
    renting_person_region = models.CharField(max_length=50, blank=True, null=True)
    renting_person_country = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField(null=True, blank=True)
    received_bank = models.BooleanField(null=True, blank=True, default=False)
    cleaning = models.FloatField(null=True, blank=True, default=100, help_text="For R2R its 0. Else the price is inside the received money from the platform")
    commission_platform = models.FloatField(null=True, blank=True, default=0, help_text="For RBnB the commission is already taken so it is 0, not for Booking")
    commission_other = models.FloatField(null=True, blank=True, default=0, help_text="For Fuerte, This is the Katia commission")
    comments = models.TextField(null=True, blank=True)
    all_days = None

    class Meta:
        ordering = ['asset', 'platform', 'reservation_number']
        verbose_name_plural = "Hollydays Reservations"
        managed = False  # Important: don't try to manage this table

    def save(self, *args, **kwargs):
        self.generate_all_days()
        super().save(*args, **kwargs)

    def generate_all_days(self):
        if self.entry_date and self.end_date:
            self.all_days = {self.entry_date + timedelta(days=x) for x in range((self.end_date - self.entry_date).days + 1)}
        else:
            self.all_days = set()

    def __str__(self):
        return str(self.platform)
