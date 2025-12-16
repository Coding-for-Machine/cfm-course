from django.db import models
from courses.models import Modules
from app.models import TimeMixsin
from utils.get_slug import generate_slug_with_case
from users.models import BaseUser as User




class Lesson(TimeMixsin):
    module = models.ForeignKey(Modules, related_name="lesson", on_delete=models.CASCADE)  # Modulga bog'lanadi
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    preview = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Lesson: (Module: {self.module.title})"  
    
    def save(self, *args, **kwargs):
        if not self.slug or Lesson.objects.filter(slug=self.slug).exists():
            self.slug = generate_slug_with_case(30)
        super().save(*args, **kwargs)