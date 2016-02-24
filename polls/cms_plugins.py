# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import F
from django.utils.translation import ugettext as _
from django.utils import timezone

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import PollListPluginModel, PollResultsPluginModel


class PollListPlugin(CMSPluginBase):
    cache = False
    model = PollListPluginModel
    module = 'Polls'
    name = _('Poll List')
    render_template = 'polls/plugins/poll_list.html'

    filter_horizontal = ['polls', ]

    def render(self, context, instance, placeholder):
        context = super(PollListPlugin, self).render(
            context, instance, placeholder)
        context['polls'] = instance.polls.filter(pub_date__lte=timezone.now())
        return context

plugin_pool.register_plugin(PollListPlugin)


class PollResultsPlugin(CMSPluginBase):
    cache = False
    model = PollResultsPluginModel
    module = 'Polls'
    name = _('Poll Results')
    render_template = 'polls/plugins/poll_results.html'

    def render(self, context, instance, placeholder):
        context = super(PollResultsPlugin, self).render(
            context, instance, placeholder)
        context['question'] = instance.question
        context['total_votes'] = instance.total_votes
        context['choices'] = instance.question.choices.order_by(
            *instance.ordering.split(',')).annotate(
            pct=100.0 * F('votes') / instance.total_votes)
        return context

plugin_pool.register_plugin(PollResultsPlugin)
