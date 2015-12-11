# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0061_companygroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('company_group', models.ForeignKey(related_name='company_group_members', to='app.CompanyGroup')),
                ('user', models.ForeignKey(related_name='company_group_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
