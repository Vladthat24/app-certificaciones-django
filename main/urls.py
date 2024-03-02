"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from setup.urls_api import router as router_api_setup

urlpatterns = [
                  path('', include('apps.index.url')),
                  # path('accounts/login/', include('apps.index.url')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('manager/', admin.site.urls),

                  path('localizations/country/', include('apps.localizations.urls.country')),
                  path('localizations/department/', include('apps.localizations.urls.department')),
                  path('localizations/province/', include('apps.localizations.urls.province')),
                  path('localizations/district/', include('apps.localizations.urls.district')),

                  path('solicitud/', include('apps.solicitud.urls.solicitud')),

                  path('hospital/', include('apps.solicitud.urls.hospital')),
                  path('crematorio/', include('setup.urls.crematorio')),
                  path('usuario/', include('setup.urls.usuario')),
                  path('certificacion/', include('apps.certificacion.urls.certificacion')),
                  path('reporte/', include('apps.reporte_excel.urls')),

                  path('generic/resolucion/', include('apps.generic.urls.resolucion')),
                  path('grafico/', include('apps.reporte_grafico.urls')),

                  # API
                  path('api/', include(router_api_setup.urls)),
                  path('generic/calendario/', include('apps.generic.urls.calendario')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
