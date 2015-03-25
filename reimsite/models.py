from django.db import models

# Create your models here.
class Detail(models.Model):
	source = models.CharField(max_length=10)
	def __str__(self):
		return self.source

class Funds(models.Model):
	credit = models.CharField(max_length=20)
	def __str__(self):
		return self.credit

class Application(models.Model):
	date = models.DateField("apply date")
	days = models.IntegerField(default=0)
	category = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
	total = models.IntegerField(default=0)
	others = models.CharField(max_length=50)
	remain = models.CharField(max_length=50)
	status = models.IntegerField(default=0)
	def __str__(self):
		return self.name

class Item(models.Model):
	detail = models.ForeignKey(Detail)
	money = models.IntegerField(default=0)
	record = models.ForeignKey(Application)
	def __str__(self):
		return str(self.money)

class Reim(models.Model):
	funds = models.ForeignKey(Funds)
	number = models.CharField(max_length=10)
	record = models.OneToOneField(Application)
	def __str__(self):
		return self.number

class Config(models.Model):
	name = models.CharField(max_length=50)
	value = models.CharField(max_length=50)
	def __str__(self):
		return "%s : %s" % (self.name, self.value)