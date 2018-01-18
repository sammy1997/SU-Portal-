from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^download_bus/$', views.export_bus_xls, name='download'),
    url(r'^$', views.index, name='index'),
    url(r'^bus/$', views.bus, name='bus'),
    url(r'^get_valid_seats/$', views.get_valid_seats, name='validateSeat'),
    url(r'^cost/$', views.cost, name='cost'),
    url(r'^sendmail/$', views.send_email, name='emailer'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^services/$', views.services, name='services'),
    url(r'^loginAuth/$', views.login, name='login'),
    url(r'^login/$', views.login_page, name='loginPage'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^registerExcel/$', views.register_excel, name='excelReg'),
    url(r'^registerBus/$', views.register_bus, name="registerBus"),
    url(r'^cancelBus/$', views.cancel_bus, name="cancel"),
    url(r'^updateExcel/$',views.update_excel, name='update'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]
