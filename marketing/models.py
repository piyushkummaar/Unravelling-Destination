from django.db import models


class Signup(models.Model):
    email = models.EmailField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
        db_table = 'tbl_newsletter'
        managed = True

    def __str__(self):
        return self.email