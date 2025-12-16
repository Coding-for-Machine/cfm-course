from django.db import models
from django.utils.text import slugify
from martor.models import MartorField
from app.models import TimeMixsin
from users.models import BaseUser as User


class Course(TimeMixsin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    description = MartorField()
    instructor = models.CharField(max_length=250)
    is_free = models.BooleanField(default=True)
    image = models.ImageField(upload_to="courses/images/")
    thumbnail = models.CharField(max_length=500, blank=True, null=True, help_text="Bu rasim urli")

    lesson_count = models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Enrollment(TimeMixsin):
    user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"


class Modules(TimeMixsin):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)  # "related_name" qo‘shildi
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = MartorField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"Module: {self.title} (Course: {self.course.title})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)