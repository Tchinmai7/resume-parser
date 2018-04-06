# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Company(models.Model):
	company_name = models.CharField(max_length=200)
	class Meta:
		verbose_name_plural = "Companies"
	def __unicode__(self):
		return self.company_name

class PagesToWatch(models.Model):
	company = models.ForeignKey(Company, related_name='career_pages')
	page_url = models.URLField()

class Email(models.Model):
	company = models.ForeignKey(Company, related_name='company')
	senders_email = models.EmailField(max_length=200)
	subject_line = models.CharField(max_length=200)
	email_body = models.TextField()
	def __unicode__(self):
		return self.senders_email+" | "+self.subject_line

class Attachment(models.Model):
	email = models.ForeignKey(Email, related_name='attachments')
	attachment = models.URLField()

