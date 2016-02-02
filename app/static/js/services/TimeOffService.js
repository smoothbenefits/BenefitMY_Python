var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimeOffService',
  ['$q',
   'EnvironmentService',
   'TimeOffRepository',
   function TimeOffService(
    $q,
    EnvironmentService,
    TimeOffRepository){
        var _GetEnvAwareId = function(id){
            return EnvironmentService.getEnvironment().then(function(env){
                    return env + '_' + id;
                });
        };

        var mapDomainModelsToViewModels = function(domainModels){
            var viewModels = [];
            _.each(domainModels, function(domainModel){
                var viewModel = {
                    type: domainModel.type,
                    duration: domainModel.duration,
                    start: moment(domainModel.startDateTime).format(DATE_TIME_FORMAT_STRING),
                    created: moment(domainModel.timeStamp).format(DATE_TIME_FORMAT_STRING)
                };
                viewModels.push(viewModel);
            });
            return viewModels;
        };

        var GetTimeOffsByRequestor = function(requestor){
            return _GetEnvAwareId(requestor).then(function(id){
                return TimeOffRepository.then(function(resource){
                    return resource.ByRequestor.query({userId:id})
                        .$promise.then(function(timeoffs){
                            return mapDomainModelsToViewModels(timeoffs);
                        });
                    });
                });
        };

        return {
            GetTimeOffsByRequestor: GetTimeOffsByRequestor
        };
    }
]);