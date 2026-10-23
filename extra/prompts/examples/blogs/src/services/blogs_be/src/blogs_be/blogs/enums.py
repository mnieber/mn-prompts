from django.db import models


class Audiences(models.TextChoices):
    EXPERT = "expert"
    NOVICE = "novice"
    ANY = "any"


class BlogPostLevels(models.TextChoices):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
