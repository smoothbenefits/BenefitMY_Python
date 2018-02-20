
from app.models.onboarding.user_onboarding_step_state import (
    UserOnboardingStepState,
    STEP_BASIC_INFO,
    STEP_EMPLOYMENT_AUTHORIZATION,
    STEP_W4_INFO,
    STEP_STATE_TAX_INFO,
    STEP_DIRECT_DEPOSIT,
    STEP_DOCUMENTS,
    STATE_SKIPPED,
    STATE_COMPLETED
)

class UserOnboardingStateService(object):

    def __init__(self):
        self._onboarding_step_sequence = {
            STEP_BASIC_INFO: 1,
            STEP_EMPLOYMENT_AUTHORIZATION: 2,
            STEP_W4_INFO: 3,
            STEP_STATE_TAX_INFO: 4,
            STEP_DIRECT_DEPOSIT: 5,
            STEP_DOCUMENTS: 6
        }

        self._last_step_index = len(self._onboarding_step_sequence)

    def has_onboarding_process_completed_by_user(self, user_id):
        # Note: This would assume the below
        #   * If there is a new step added before the original last step, the user would still be
        #     considered "completed" onboarding
        #   * If there is a new step added to the last to serve as the new last step, then the user
        #     would now be considered "not completed"
        #   * If the order of the steps changed in any fashion that the original last steps is no 
        #     longer the last step, the result would depend on the completion state of the updated
        #     new last step.

        # If the user completed the last step, then it is considered he/she completed 
        # onboarding process
        # Note: 
        #   For the purpose of the function, it is considered that the user completed
        #   the step either it is completed or simply skipped.      
        user_completed_steps = self._get_steps_with_states_by_user(user_id, [STATE_COMPLETED, STATE_SKIPPED])
        return any(self._is_last_step(step) for step in user_completed_steps)

    def _is_last_step(self, step):
        step_index = self._onboarding_step_sequence.get(step)
        return step_index is not None and step_index >= self._last_step_index

    def _get_steps_with_states_by_user(self, user_id, state_list):
        return UserOnboardingStepState.objects.filter(user=user_id, state__in=state_list).values_list('step', flat=True)
    