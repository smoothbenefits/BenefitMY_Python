var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UserOnboardingStepStateService',
    ['$q',
    'UserOnboardingStepStateRepository',
    'UserService',
    function (
        $q, 
        UserOnboardingStepStateRepository, 
        UserService){

        var Steps = {
            directDeposit: 'direct_deposit'
        };

        var States = {
            skipped: 'skipped',
            completed: 'completed'
        }

        var getStepStatesByUser = function(userId) {
            return UserOnboardingStepStateRepository.ByUser.query({userId:userId}).$promise;
        };

        var getStateModelByUserAndStep = function(userId, step) {
            return getStepStatesByUser(userId).then(
                function(states) {
                    var stepState = _.find(states, function(state) {
                        return state.step == step;
                    });

                    return stepState
                }
            );
        };

        var getStateByUserAndStep = function(userId, step) {
            return getStateModelByUserAndStep(userId, step).then(
                function(stepState) {
                    return stepState ? stepState.state : null;
                }
            );
        };

        var updateStateByUserAndStep = function(userId, step, toState) {
            return getStateModelByUserAndStep(userId, step).then(
                function(stepState) {
                    if (stepState) {
                        // Exists, update
                        stepState.state = toState;
                        
                        return UserOnboardingStepStateRepository.ById.update({entryId:stepState.id}, stepState).$promise;
                    } else {
                        // Create
                        var stepState = {
                            user: userId,
                            step: step,
                            state: toState
                        };

                        return UserOnboardingStepStateRepository.ById.save({}, stepState).$promise;
                    }
                }
            );
        };

        return {

            Steps: Steps,
            States: States,
            getStateByUserAndStep: getStateByUserAndStep,
            updateStateByUserAndStep: updateStateByUserAndStep,

        };
    }
]);
