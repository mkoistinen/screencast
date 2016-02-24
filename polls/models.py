# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from cms.models import CMSPlugin


@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices',
                                 on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


@python_2_unicode_compatible
class PollListPluginModel(CMSPlugin):

    polls = models.ManyToManyField(Question, default=None, blank=True)

    def __str__(self):
        return 'Poll list'

    def copy_relations(self, old_instance):
        """
        Ensures that the public version of this plugin keeps the same state as
        the unpublished one. This is necessary for plugins that have M2M or that
        have FKs to another model.
        """
        self.polls = old_instance.polls.all()


@python_2_unicode_compatible
class PollResultsPluginModel(CMSPlugin):

    ORDERING_CHOICES = (
        ('pk', 'natural', ),
        ('-votes,choice_text', 'vote (descending)', ),
        ('votes,choice_text', 'vote (ascending)', ),
        ('choice_text', 'choice (a-z)', ),
    )

    question = models.ForeignKey(Question, default=None, blank=True, null=True,
                                 on_delete=models.SET_NULL)
    ordering = models.CharField(max_length=32, choices=ORDERING_CHOICES,
                                default='pk')

    @property
    def total_votes(self):
        """
        Returns the total number of votes across all of this question's choices.

        This performs one query (with a join).
        """
        if self.question:
            return Choice.objects.filter(question=self.question).aggregate(
                models.Sum('votes'))['votes__sum']
        else:
            return 0

    def __str__(self):
        if self.question:
            return self.question.question_text
        else:
            return "<unset>"
