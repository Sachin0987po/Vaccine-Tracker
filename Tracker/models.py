from django.db import models


class userEntry(models.Model):
    name = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 50)
    pincode = models.CharField(max_length = 6)
    dose_type = models.IntegerField(default = 1)
    min_age_limit = models.IntegerField(default = 18)


