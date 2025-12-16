from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from api.api import api

urlpatterns = [
    path('api/', api.urls),  # Django Ninja API

    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('martor/', include('martor.urls'))
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.utils.translation import gettext_lazy as _


admin.site.site_title = _("Boshqaruv paneli")
admin.site.site_header = _("Admin boshqaruvi")
admin.site.index_title = _("Boshqaruv")