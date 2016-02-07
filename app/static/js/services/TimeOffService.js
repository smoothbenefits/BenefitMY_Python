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

        var mapDomainModelToViewModel = function(domainModel){
            var viewModel = {
                id: domainModel._id,
                type: domainModel.type,
                status: domainModel.status,
                duration: domainModel.duration,
                start: moment(domainModel.startDateTime).format(DATE_TIME_FORMAT_STRING),
                created: moment(domainModel.requestTimestamp).format(DATE_TIME_FORMAT_STRING),
                requestor: domainModel.requestor,
                approver: domainModel.approver.email,
                actionNeeded: domainModel.status.toLowerCase() == 'pending',
                decisionTime: moment(domainModel.decisionTimestamp).format(DATE_TIME_FORMAT_STRING)
            };
            return viewModel;
        };

        var mapDomainModelsToViewModels = function(domainModels){
            var viewModels = [];
            _.each(domainModels, function(domainModel){
                viewModels.push(mapDomainModelToViewModel(domainModel));
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
          var domainModel = {
            'status': 'PENDING',
            'startDateTime': viewModel.starting_date,
            'type': viewModel.type,
            'duration': viewModel.duration,
          };

          var requestor = {
            'personDescriptor': _GetEnvAwareId(viewModel.requestor.id),
            'firstName': viewModel.requestor.first_name,
            'lastName': viewModel.requestor.last_name,
            'email': viewModel.requestor.email
          }

          domainModel.requestor = requestor;

          var approver = {
            'personDescriptor': _GetEnvAwareId(viewModel.approver.userId),
            'firstName': viewModel.approver.first_name,
            'lastName': viewModel.approver.last_name,
            'email': viewModel.approver.email
          }

          domainModel.approver = approver;

          return domainModel;
        };

        var requestTimeOff = function(request) {

          var requestDto = mapViewModelToDomainModel(request);
          return TimeOffRepository.Collection.save({}, requestDto).$promise
          .then(function(savedRequest) {
            return savedRequest;
          });
        var GetTimeOffsByApprover = function(approver){
            var id = _GetEnvAwareId(approver);
            return TimeOffRepository.ByApprover.query({userId:id})
                .$promise.then(function(timeoffs){
                    return mapDomainModelsToViewModels(timeoffs);
                });
        };

        var UpdateTimeOffStatus = function(timeOff){
            return TimeOffRepository.StatusByTimeoffId.update({timeoffId:timeOff.id}, {status: timeOff.status})
                .$promise.then(function(timeoff){
                    return mapDomainModelToViewModel(timeoff);
                });
        };

        return {
            GetTimeOffsByRequestor: GetTimeOffsByRequestor,
            RequestTimeOff: requestTimeOff,
            GetTimeOffsByApprover: GetTimeOffsByApprover,
            UpdateTimeOffStatus: UpdateTimeOffStatus
        };
    }
]);
