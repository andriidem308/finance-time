from django.db import models
from django.utils.timezone import now


# Create your models here.


class Currency(models.Model):
    CURRENCIES = (
        (1, "USD"),
        (2, "EUR"),
    )

    SOURCES = (
        (1, "MONOBANK"),
        (2, "YAHOO_FINANCE"),
        (3, "VKURSE")
    )

    currency = models.PositiveSmallIntegerField(choices=CURRENCIES)
    source = models.PositiveSmallIntegerField(choices=CURRENCIES)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=now)

