from django.db import models
import uuid
class Workout(models.Model):
    # owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    featured_img=models.ImageField(null=True,blank=True,default='default.jpg')
    # exercise = models.ManyToManyField(Exercise,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    volume = models.IntegerField(null=True,blank=True,default=0)
    sets = models.IntegerField(null=True,blank=True,default=0)
    duration = models.DurationField()
    
    def __str__(self):
        return self.name

