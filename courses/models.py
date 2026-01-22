from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    instructor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='courses')
    thumbnail = models.ImageField(default='course_thumbnails/default-course-thumbnail.png',upload_to='course_thumbnails/',blank=True,null=True)
    level = models.CharField(
        max_length=25,
        choices=[('beginner','Beginner'),('intermidiate','Intermediate'),('advanced','Advanced')]
        )
    language = models.CharField(default='English',max_length=50)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Section(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='sections')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    section = models.ForeignKey(Section,on_delete=models.CASCADE,related_name='lessons')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='lesson_videos/')
    notes = models.FileField(upload_to='lesson_notes/',blank=True,null=True)
    is_preview = models.BooleanField(default=False)
    order = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
