import reversion

from django.db import models

from app.custom_authentication import AuthUser

STATE_SKIPPED = 'skipped'
STATE_COMPLETED = 'completed'
STATES = (
        (STATE_SKIPPED, 'skipped'),
        (STATE_COMPLETED, 'completed'),
    )

STEP_BASIC_INFO = 'basic_info'
STEP_EMPLOYMENT_AUTHORIZATION = 'employment_authorization'
STEP_W4_INFO = 'W4_info'
STEP_STATE_TAX_INFO = 'state_tax_info'
STEP_DIRECT_DEPOSIT = 'direct_deposit'
STEP_DOCUMENTS = 'documents'
STEPS = (
        (STEP_BASIC_INFO, 'basic_info'),
        (STEP_EMPLOYMENT_AUTHORIZATION, 'employment_authorization'),
        (STEP_W4_INFO, 'W4_info'),
        (STEP_STATE_TAX_INFO, 'state_tax_info'),
        (STEP_DIRECT_DEPOSIT, 'direct_deposit'),
        (STEP_DOCUMENTS, 'documents')
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
