from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .tasks import process_video
from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from martor.widgets import AdminMartorWidget
from .models import Problem, Category, Tags, TestCase, ExecutionTestCase, Function, Language, Examples, Video, VideoQuality
from django.db import models



class ExecutionTestCaseInlineAdmin(StackedInline):  # unfold.admin.StackedInline
    model = ExecutionTestCase
    extra = 1


class FunctionInlineAdmin(StackedInline):  # unfold.admin.StackedInline
    model = Function
    extra = 1


@admin.register(Problem)
class ProblemAdmin(ModelAdmin):  # unfold.admin.ModelAdmin
    list_display = ["id", "title", "slug", "description", "difficulty", "created_at", "updated_at"]
    list_per_page = 20
    inlines = [ExecutionTestCaseInlineAdmin, FunctionInlineAdmin]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    list_display = ["id", "name", "slug", "created_at", "updated_at"]
    list_display_links = ["name"]
    list_per_page = 5


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["id", "name", "slug"]


@admin.register(TestCase)
class TestCaseAdmin(ModelAdmin):
    list_display = ["id", "input_txt", "output_txt"]
    list_per_page = 20


@admin.register(ExecutionTestCase)
class ExecutionTestCaseAdmin(ModelAdmin):
    list_display = ["id", "top_code", "created_at", "updated_at"]
    list_per_page = 20


@admin.register(Function)
class FunctionAdmin(ModelAdmin):
    list_display = ["id", "function", "created_at", "updated_at"]
    list_per_page = 20


@admin.register(Examples)
class ExamplesAdmin(ModelAdmin):
    list_display = ["id", "input_txt", "output_txt", "explanation"]
    list_per_page = 20


@admin.register(Tags)
class TagsAdmin(ModelAdmin):  # Iltimos: `ExamplesAdmin` deb xato yozilgan edi, to'g'irlandi.
    list_display = ["id", "name"]
    list_per_page = 20

@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = [
        'thumbnail_preview', 'title', 'status_badge', 'duration_display',
        'resolution_display', 'file_size_display', 'views_count', 'created_at', 'actions_column'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = [
        'id', 'slug', 'duration', 'width', 'height', 'fps', 'bitrate',
        'codec', 'file_size', 'processing_progress', 'processing_error',
        'hls_playlist', 'processed_at', 'thumbnail_preview_large',
        'video_preview', 'qualities_display'
    ]

    fieldsets = (
        ('Asosiy Maʼlumotlar', {
            'fields': ('id', 'title', 'description', 'slug')
        }),
        ('Fayl', {
            'fields': ('original_file', 'thumbnail')
        }),
        ('Status', {
            'fields': ('status', 'processing_progress', 'processing_error')
        }),
        ('Video Maʼlumotlari', {
            'fields': ('duration', 'width', 'height', 'fps', 'bitrate', 'codec', 'file_size'),
            'classes': ('collapse',)
        }),
        ('Streaming', {
            'fields': ('hls_playlist', 'qualities_display', 'video_preview')
        }),
        ('Statistika', {
            'fields': ('views_count', 'likes_count', 'dislikes_count', 'processed_at'),
            'classes': ('collapse',)
        }),
        ('Preview', {
            'fields': ('thumbnail_preview_large',)
        }),
    )

    actions = ['reprocess_videos', 'delete_processed_files']

    # === Custom display methods ===
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width:90px; border-radius:6px;" />', obj.thumbnail.url)
        return "—"
    thumbnail_preview.short_description = "Thumbnail"

    def thumbnail_preview_large(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-width:480px; border-radius:8px;" />', obj.thumbnail.url)
        return "Thumbnail mavjud emas"
    thumbnail_preview_large.short_description = "Katta Thumbnail"

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'uploading': '#17a2b8',
            'processing': '#007bff',
            'completed': '#28a745',
            'failed': '#dc3545'
        }
        icons = {
            'pending': '⏳',
            'uploading': '📤',
            'processing': '⚙️',
            'completed': '✅',
            'failed': '❌'
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '❔')
        return format_html(
            '<span style="background:{};color:white;padding:3px 8px;'
            'border-radius:12px;font-size:11px;font-weight:bold;">{} {}</span>',
            color, icon, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def duration_display(self, obj):
        if obj.duration:
            m, s = divmod(obj.duration, 60)
            return f"{m}:{s:02d}"
        return "—"
    duration_display.short_description = "Davomiyligi"

    def resolution_display(self, obj):
        if obj.width and obj.height:
            return f"{obj.width}×{obj.height}"
        return "—"
    resolution_display.short_description = "Resolution"

    def file_size_display(self, obj):
        if obj.file_size:
            if obj.file_size >= 1024 ** 3:
                return f"{obj.file_size / (1024 ** 3):.2f} GB"
            elif obj.file_size >= 1024 ** 2:
                return f"{obj.file_size / (1024 ** 2):.2f} MB"
            else:
                return f"{obj.file_size / 1024:.2f} KB"
        return "—"
    file_size_display.short_description = "Hajmi"

    def actions_column(self, obj):
        buttons = []
        if obj.status == 'completed':
            # Dynamic admin URL
            view_url = f"/admin/problems/video/{obj.id}/change/"
            buttons.append(
                f'<a href="{view_url}" target="_blank" '
                f'style="background:#007bff;color:white;padding:5px 8px;'
                f'border-radius:4px;font-size:11px;text-decoration:none;">▶️ Ko‘rish</a>'
            )
        if obj.status in ['pending', 'failed']:
            buttons.append(
                f'<a href="#" onclick="reprocessVideo(\'{obj.id}\');return false;" '
                f'style="background:#28a745;color:white;padding:5px 8px;'
                f'border-radius:4px;font-size:11px;text-decoration:none;">🔄 Qayta</a>'
            )
        return format_html(' '.join(buttons)) if buttons else "—"
    actions_column.short_description = "Amallar"

    def video_preview(self, obj):
        hls_url = obj.get_hls_url()
        if obj.status == 'completed' and hls_url:
            return format_html('''
                <div style="max-width:640px">
                    <video id="vid-{}" controls style="width:100%;border-radius:8px;"></video>
                    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
                    <script>
                        var v=document.getElementById("vid-{}");
                        if(Hls.isSupported()){var h=new Hls();h.loadSource("{}");h.attachMedia(v);}
                        else if(v.canPlayType('application/vnd.apple.mpegurl')){v.src="{}";}
                    </script>
                </div>
            ''', obj.id, obj.id, hls_url, hls_url)
        return "Video hali tayyor emas"
    video_preview.short_description = "Preview"

    def qualities_display(self, obj):
        qs = obj.qualities.all()
        if not qs:
            return "Sifatlar mavjud emas"
        html = ''.join([
            f"<li>{'✅' if q.is_ready else '⏳'} <strong>{q.quality}</strong> "
            f"({q.width}×{q.height}, {q.bitrate})</li>"
            for q in qs
        ])
        return mark_safe(f"<ul>{html}</ul>")
    qualities_display.short_description = "Mavjud Sifatlar"
