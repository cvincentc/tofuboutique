from django.db import models

class SizeChoices(models.TextChoices):
    XS = 'XS', 'XS'
    S = 'S', 'S'
    M = 'M', 'M'
    L = 'L', 'L'
    XL = 'XL', 'XL'

class GenderChoices(models.TextChoices):
    MALE = 'MALE', '男性'
    FEMALE = 'FEMALE', "女性"
    UNISEX = 'UNISEX', "男/女"

class ProductStatusChoices(models.TextChoices):
    AVAILABLE = 'AVAILABLE'
    UNAVAILABLE = 'UNAVAILABLE'

class TokenPrefix(models.TextChoices):
    IMAGE_PREFIX = 'img-',
    
class AlertTypeChoices(models.TextChoices):
    ERROR = 'error'
    SUCCESS = 'success'
    WARNING = 'warning'
    INFO = 'info'