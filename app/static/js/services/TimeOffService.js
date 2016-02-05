var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimeOffService',
  ['$q',
   'envService',
   'TimeOffRepository',
   function TimeOffService(
    $q,
    envService,
    TimeOffRepository){
        var _GetEnvAwareId = function(id){
            var env = envService.get();
            return env + '_' + id;
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
            var id = _GetEnvAwareId(requestor);
            return TimeOffRepository.ByRequestor.query({userId:id})
                .$promise.then(function(timeoffs){
                    return mapDomainModelsToViewModels(timeoffs);
                });
        };

        var mapViewModelToDomainModel = function(viewModel) {
          var domainModel = angular.copy(viewModel);

          domainModel.requestor.personDescriptor = _GetEnvAwareId(viewModel.requestor.person);
          domainModel.requestor.firstName = viewModel.requestor.first_name;
          domainModel.requestor.lastName = viewModel.requestor.last_name;
          
          domainModel.approver.personDescriptor = _GetEnvAwareId(viewModel.approver.person);
          domainModel.approver.firstName = viewModel.approver.first_name;
          domainModel.approver.lastName = viewModel.approver.last_name;
          domainModel.status = 'PENDING';

          return domainModel;
        };

        var requestTimeOff = function(request) {

          var requestDto = mapViewModelToDomainModel(request);
          return TimeOffRepository.Collection.save({}, requestDto).$promise
          .then(function(savedRequest) {
            return savedRequest;
          });
        };

        return {
            GetTimeOffsByRequestor: GetTimeOffsByRequestor,
            RequestTimeOff: requestTimeOff
        };
    }
]);
