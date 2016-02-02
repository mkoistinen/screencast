# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Question, PollResultsPluginModel


class PollListPlugin(CMSPluginBase):
    cache = False
    model = CMSPlugin
    module = 'Polls'
    name = _('Poll List')
    render_template = 'polls/plugins/poll_list.html'

    def render(self, context, instance, placeholder):
        context = super(PollListPlugin, self).render(context, instance, placeholder)
        context['question_list'] = Question.objects.filter(pub_date__lte=timezone.now)
        return context

plugin_pool.register_plugin(PollListPlugin)


class PollResultsPlugin(CMSPluginBase):
    cache = False
    model = PollResultsPluginModel
    module = 'Polls'
    name = _('Poll Results')
    render_template = 'polls/plugins/poll_results.html'

    def render(self, context, instance, placeholder):
        context = super(PollResultsPlugin, self).render(context, instance, placeholder)
        context['question'] = instance.question
        context['choices'] = instance.question.choices.order_by('-votes').all()
        return context

plugin_pool.register_plugin(PollResultsPlugin)
