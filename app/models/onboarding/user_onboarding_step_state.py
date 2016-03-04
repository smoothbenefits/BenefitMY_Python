import reversion

from django.db import models

from app.custom_authentication import AuthUser

STATE_SKIPPED = 'skipped'
STATE_COMPLETED = 'completed'
STATES = (
        (STATE_SKIPPED, 'skipped'),
        (STATE_COMPLETED, 'completed'),
    )

STEP_DIRECT_DEPOSIT = 'direct_deposit'
STEPS = (
        (STEP_DIRECT_DEPOSIT, 'direct_deposit'),
    )


@reversion.register
class UserOnboardingStepState(models.Model):
    step = models.CharField(max_length=255, choices=STEPS)
    state = models.CharField(max_length=2048, choices=STATES, null=True, blank=True)
    user = models.ForeignKey(AuthUser,
                             related_name="onboarding_step_state")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('step', 'user',)
