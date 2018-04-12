# -*- coding: utf-8 -*-
__author__ = 'yzh'
__date__ = '2018/3/28/028 15:30'

import  xadmin
from  xadmin import views

from .models import EmailVerifyRecord
from  .models import Banner


class GlobalSetting(object):
    site_title=u'后台管理系统'
    site_footer=u'YZH LAB'
    menu_style='accordion'

class BaseSetting(object):
    enable_themes = True
    use_booswatch = True

class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_type']
    search_fields = ['code','email','send_type']#搜索框
    list_filter =['code','email','send_type','send_type']#过滤器


class BannerAdmin(object):
    pass


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)