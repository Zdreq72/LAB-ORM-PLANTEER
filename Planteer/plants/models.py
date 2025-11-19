from django.db import models

class Plant(models.Model):

    class CategoryChoices(models.TextChoices):
        TREE = "Tree", "Tree"
        FLOWER = "Flower", "Flower"
        HERB = "Herb", "Herb"
        VEGETABLE = "Vegetable", "Vegetable"
        FRUIT = "Fruit", "Fruit"

    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
