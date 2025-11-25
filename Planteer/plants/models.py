from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator #


class Benefit(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField()         
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
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
    benefits = models.ManyToManyField(Benefit, related_name="plants", blank=True)
    native_to = models.ManyToManyField("Countries", related_name="plants", blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.name}"
    

class Countries(models.Model):
    name = models.CharField(max_length=100, unique=True)
    flag = models.ImageField(upload_to="countries/")


    def __str__(self):
        return self.name
