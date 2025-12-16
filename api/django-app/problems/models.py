# ==================== problems/models.py ====================
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from martor.models import MartorField

from lessons.models import Lesson
from contest.models import Contest
from app.models import TimeMixsin
from utils.get_slug import generate_slug_with_case

User = settings.AUTH_USER_MODEL



# -------------------- Category --------------------
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=500, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


# -------------------- Tags --------------------
class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"

    def __str__(self):
        return self.name


# -------------------- Language --------------------
class Language(TimeMixsin):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Dasturlash tili"
        verbose_name_plural = "Dasturlash tillari"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(30)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -------------------- Problem --------------------
class Problem(TimeMixsin):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name="problems", null=True, blank=True)
    contest = models.ForeignKey(Contest ,related_name="problems", on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name="problems", blank=True)
    language = models.ManyToManyField(Language, related_name="problems", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="problems", null=True, blank=True
    )
    problem_type = models.CharField(
        max_length=50, 
        choices=[('darslik', 'darslik'), ('test', 'test'), ('probelm', 'probelm')],
        default=False,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    description = MartorField()


    is_active = models.BooleanField(default=True, db_index=True)
    constraints = models.TextField(
        help_text="HTML formatida cheklovlar",
        default="""
        <ul>
            <li><code>2 ≤ nums.length ≤ 10<sup>4</sup></code></li>
        </ul>
        """,
    )

    DIFFICULTY_CHOICES = [
        (1, "Oson"),
        (2, "O‘rtacha"),
        (3, "Qiyin"),
    ]
    difficulty = models.PositiveIntegerField(choices=DIFFICULTY_CHOICES, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ["id"]
        verbose_name = "Masala"
        verbose_name_plural = "Masalalar"
        indexes = [
            models.Index(fields=["is_active", "difficulty"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Slug avtomatik
        if not self.slug:
            self.slug = slugify(self.title)

        # Point avtomatik
        if not self.points:
            self.points = {1: 100, 2: 250, 3: 450}.get(self.difficulty, 100)

        super().save(*args, **kwargs)


# -------------------- Hint --------------------
class Hint(models.Model):
    problem = models.ForeignKey(Problem, related_name="hints", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Hint: {self.problem.title}"


# -------------------- Challenge --------------------
class Challenge(models.Model):
    problem = models.ForeignKey(Problem, related_name="challenges", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Challenge: {self.problem.title}"


# -------------------- Examples --------------------
class Examples(TimeMixsin):
    problem = models.ForeignKey(Problem, related_name="examples", on_delete=models.CASCADE)
    input_txt = models.TextField(help_text="Kirish ma'lumotlari, masalan: '[2,7,11,15]\\n9'")
    output_txt = models.TextField(help_text="Chiqish ma'lumotlari, masalan: '[0,1]'")
    explanation = models.TextField(help_text="Tushuntirish matni")

    class Meta:
        verbose_name = "Misol"
        verbose_name_plural = "Misollar"

    def __str__(self):
        return f"Example: {self.problem.title}"


# -------------------- Function --------------------
class Function(TimeMixsin):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="functions", on_delete=models.CASCADE)
    function = models.TextField()

    class Meta:
        unique_together = ("problem", "language")
        verbose_name = "Funksiya shabloni"
        verbose_name_plural = "Funksiya shablonlari"

    def __str__(self):
        return f"{self.language.name} - {self.problem.title}"


# -------------------- ExecutionTestCase --------------------
class ExecutionTestCase(TimeMixsin):
    problem = models.ForeignKey(Problem, related_name="execution_problem", on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name="execution_language", on_delete=models.CASCADE)
    top_code = models.TextField(null=True, blank=True)
    bootom_code = models.TextField()

    class Meta:
        unique_together = ("problem", "language")
        verbose_name = "Ishga tushirish testi"
        verbose_name_plural = "Ishga tushirish testlari"


# -------------------- TestCase --------------------
class TestCase(TimeMixsin):
    problem = models.ForeignKey(Problem, related_name="test_problem", on_delete=models.CASCADE)
    input_txt = models.CharField(max_length=250, help_text="Test Input")
    output_txt = models.CharField(max_length=250, help_text="Chiqish Output")
    is_correct = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["problem"])]
        verbose_name = "Test case"
        verbose_name_plural = "Test caselar"

    def __str__(self):
        return f"Test: {self.problem.title}"




class Video(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('uploading', 'Yuklanmoqda'),
        ('processing', 'Qayta ishlanmoqda'),
        ('completed', 'Tayyor'),
        ('failed', 'Xatolik'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ← QO'SHILDI
    problem = models.ForeignKey(
        Problem, 
        on_delete=models.SET_NULL, 
        related_name='videos', 
        blank=True, 
        null=True
    )
    
    # ← QO'SHILDI
    title = models.CharField(max_length=255, default='Untitled Video')
    slug = models.SlugField(max_length=300, blank=True, unique=True)
    description = models.TextField(blank=True)
    
    # MinIO saqlash
    original_file = models.FileField(
        upload_to='videos/originals/',
        help_text="Asl video fayl"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Video metadata
    duration = models.PositiveIntegerField(default=0, help_text='Soniyalarda')  # ← QO'SHILDI
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    fps = models.FloatField(null=True, blank=True)
    bitrate = models.IntegerField(null=True, blank=True)
    codec = models.CharField(max_length=50, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True, help_text="Baytlarda")
    
    # Statistics  ← QO'SHILDI
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)
    
    # Thumbnail
    thumbnail = models.ImageField(
        upload_to='videos/thumbnails/',
        blank=True,
        null=True
    )
    
    # HLS playlist
    hls_playlist = models.CharField(
        max_length=500,
        blank=True,
        help_text="master.m3u8 fayl manzili"
    )
    
    # Processing
    processing_progress = models.IntegerField(default=0)
    processing_error = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videolar'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Slug avtomatik
        if not self.slug:
            base_slug = slugify(self.title) or f'video-{str(self.id)[:8]}'
            slug = base_slug
            counter = 1
            while Video.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_hls_url(self):
        """HLS master playlist URL"""
        if self.hls_playlist:
            return f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.hls_playlist}"
        return None

    def get_thumbnail_url(self):
        """Thumbnail URL"""
        if self.thumbnail:
            return self.thumbnail.url
        return None

    def increment_views(self):
        """Ko'rishlar sonini oshirish"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class VideoQuality(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='qualities')
    quality = models.CharField(max_length=20, help_text='Masalan: 360p, 720p, 1080p')
    width = models.IntegerField()
    height = models.IntegerField()
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField(default=0, help_text='Baytlarda')
    is_ready = models.BooleanField(default=False)
    bitrate = models.CharField(max_length=20, default='0k', help_text='Masalan: 800k, 2800k')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Video Sifati'
        verbose_name_plural = 'Video Sifatlari'
        unique_together = ['video', 'quality']
        ordering = ['height']

    def __str__(self):
        return f"{self.video.title} - {self.quality}"

    def get_url(self):
        """Quality-specific HLS URL"""
        if self.file_path:
            return f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.file_path}"
        return None