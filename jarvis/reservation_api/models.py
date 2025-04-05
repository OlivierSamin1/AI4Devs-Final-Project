from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='real_estate_asset', blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=False, null=True, help_text="nickname you want to give to this asset")
    address = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    bank_accounts = models.ManyToManyField('finances.BankAccount', related_name='asset', related_query_name='asset', blank=True)
    buying_date = models.DateField(blank=True, null=True)
    buying_price = models.PositiveIntegerField(blank=True, null=True)
    has_on_going_mortgage = models.BooleanField(blank=True, null=True)
    is_rented = models.BooleanField(blank=True, null=True)
    renting_contract = models.OneToOneField('real_estate.RentingManagementContract', related_name='asset_renting_contract', blank=True, null=True, on_delete=models.CASCADE)
    copro_contract = models.OneToOneField('real_estate.CoproManagementContract', related_name='asset_copro_contract', blank=True, null=True, on_delete=models.CASCADE)
    is_our_living_house = models.BooleanField(blank=True, null=True)
    tax_management = models.ForeignKey('tax.TaxManagementContract', on_delete=models.CASCADE, related_name='asset', blank=True, null=True, help_text='this asset taxes are managed by a company?')
    details = models.JSONField(blank=True, null=True, help_text="ex: {'notary_number': 112345, ...")
    results_by_year = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['owner', 'nickname', 'buying_date']
        verbose_name_plural = "Assets"

    def __str__(self):
        return self.nickname


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
