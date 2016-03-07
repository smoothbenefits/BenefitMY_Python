# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_employeeprofile_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOnboardingStepState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('step', models.CharField(max_length=255, choices=[(b'direct_deposit', b'direct_deposit')])),
                ('state', models.CharField(blank=True, max_length=2048, null=True, choices=[(b'skipped', b'skipped'), (b'completed', b'completed')])),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='onboarding_step_state', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='useronboardingstepstate',
            unique_together=set([('step', 'user')]),
        ),
    ]
