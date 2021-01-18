from django.db import models


from django.db import models 
from django.contrib.auth import get_user_model 
from django.core.validators import MaxValueValidator, MinValueValidator
 
 
User = get_user_model() 
 
 
class Title(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 
 
 
class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
                                default=5,
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ])
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    title = models.ForeignKey(Title,
                             on_delete=models.CASCADE,
                             related_name="reviews",
                             blank=True,
                             null=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="reviews")
 
 
class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    review = models.ForeignKey(Review,
                             on_delete=models.CASCADE,
                             related_name="comments",
                             blank=True,
                             null=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments")
