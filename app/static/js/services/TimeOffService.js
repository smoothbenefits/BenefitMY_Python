var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimeOffService',
  ['$q',
   'utilityService',
   'TimeOffRepository',
   function TimeOffService(
    $q,
    utilityService,
    TimeOffRepository){
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
            var id = utilityService.getEnvAwareId(requestor);
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
            'personDescriptor': utilityService.getEnvAwareId(viewModel.requestor.id),
            'firstName': viewModel.requestor.first_name,
            'lastName': viewModel.requestor.last_name,
            'email': viewModel.requestor.email
          }

          domainModel.requestor = requestor;

          var approver = {
            'personDescriptor': utilityService.getEnvAwareId(viewModel.approver.userId),
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
        };
        
        var GetTimeOffsByApprover = function(approver){
            var id = utilityService.getEnvAwareId(approver);
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

        var GetTimeOffQuota = function(userId){
            var id = utilityService.getEnvAwareId(userId);
            return TimeOffRepository.QuotaByUser.get({userId:id})
                .$promise.then(function(timeoffQuota){
                    return timeoffQuota.quota;
                });
        };

        return {
            GetTimeOffsByRequestor: GetTimeOffsByRequestor,
            RequestTimeOff: requestTimeOff,
            GetTimeOffsByApprover: GetTimeOffsByApprover,
            UpdateTimeOffStatus: UpdateTimeOffStatus,
            GetTimeOffQuota: GetTimeOffQuota
        };
    }
]);
