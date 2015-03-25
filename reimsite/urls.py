from django.conf.urls import patterns, include, url
import reimsite.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Reimbursement.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', reimsite.views.index, name='index'),
    url(r'^add/', reimsite.views.add_record, name="add"),
    url(r'^show/', reimsite.views.show_applications, name="show"),
    url(r'^add_item/', reimsite.views.add_item, name="add_item"),
    url(r'^rm_item/', reimsite.views.rm_item, name="rm_item"),
    url(r'^rm_record/', reimsite.views.rm_record, name="rm_record"),
    url(r'^adminrm_record/', reimsite.views.adminrm_record, name="adminrm_record"),
    url(r'^login/', reimsite.views.login, name="login"),
    url(r'^init/', reimsite.views.init, name='init'),
    url(r'^add_reim/', reimsite.views.add_reim, name="add_reim"),
    url(r'^deal/', reimsite.views.deal_application, name="deal_app"),
    url(r'^backend/', reimsite.views.backend, name="backend"),
    url(r'^search/', reimsite.views.search, name="search"),
    url(r'^export/', reimsite.views.export, name="export"),
    url(r'^detail/', reimsite.views.detail, name="detail"),
    url(r'^chpass/', reimsite.views.chpass, name="chpass"),
    url(r'^logout/', reimsite.views.logout, name="logout"),
    url(r'^apply/', reimsite.views.apply, name="apply"),
    url(r'^source/', reimsite.views.source, name="source"),
    url(r'^credit/', reimsite.views.credit, name="credit")
)