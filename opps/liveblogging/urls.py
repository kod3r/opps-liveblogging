#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

from .views import EventAPIList, MessageAPIList, EventServerDetail
from .views import EventAdminList, EventAdminDetail, EventDetail
from .conf import settings


urlpatterns = patterns(
    '',
    url(r'^admin/liveblogging/message/(?P<slug>[\w-]+)$',
        login_required(EventAdminDetail.as_view()), name='event-admin-detail',
        kwargs={'channel__long_slug': settings.OPPS_LIVEBLOGGING_CHANNEL}),
    url(r'^admin/liveblogging/message/$',
        login_required(EventAdminList.as_view()), name='event-admin-list',
        kwargs={'channel__long_slug': settings.OPPS_LIVEBLOGGING_CHANNEL}),
)

urlpatterns += patterns(
    '',
    url(r'^{}/(?P<slug>[\w-]+)$'.format(
        settings.OPPS_LIVEBLOGGING_CHANNEL),
        EventDetail.as_view(), name='event',
        kwargs={'channel__long_slug': settings.OPPS_LIVEBLOGGING_CHANNEL}),

    url(r'^{}/server/(?P<slug>[\w-]+)$'.format(
        settings.OPPS_LIVEBLOGGING_CHANNEL),
        EventServerDetail.as_view(), name='event-server',
        kwargs={'channel__long_slug': settings.OPPS_LIVEBLOGGING_CHANNEL}),

    url(r'^{}/event/(?P<event__id>\d+).api$'.format(
        settings.OPPS_LIVEBLOGGING_CHANNEL),
        cache_page(settings.OPPS_CACHE_EXPIRE_DETAIL)(
            MessageAPIList.as_view()), name='event-api',
        kwargs={'channel__long_slug': settings.OPPS_LIVEBLOGGING_CHANNEL}),

    url(r'^{}/events.api$'.format(settings.OPPS_LIVEBLOGGING_CHANNEL),
        cache_page(settings.OPPS_CACHE_EXPIRE_DETAIL)(
            EventAPIList.as_view()), name='events-api',
        kwargs={'channel__long_slug': settings.OPPS_LIVEBLOGGING_CHANNEL}),
)
