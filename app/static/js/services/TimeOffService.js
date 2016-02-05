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
                    status: domainModel.status,
                    approver: domainModel.approver.email,
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
          var domainModel = {
            'status': 'PENDING',
            'startDateTime': viewModel.starting_date,
            'type': viewModel.type,
            'duration': viewModel.duration,
          };

          var requestor = {
            'personDescriptor': _GetEnvAwareId(viewModel.requestor.profileId),
            'firstName': viewModel.requestor.first_name,
            'lastName': viewModel.requestor.last_name,
            'email': viewModel.requestor.email
          }

          domainModel.requestor = requestor;

          if (viewModel.alt_approver && viewModel.alt_approver.first_name
          && viewModel.alt_approver.last_name && viewModel.alt_approver.email) {

            // No person id for alternative approver
            // Use request's id with current date time
            var altApprover = {
              'personDescriptor': _GetEnvAwareId(viewModel.requestor.profileId)
                + moment().format('yyyyMMDDTHH:mm:ss'),
              'firstName': viewModel.alt_approver.first_name,
              'lastName': viewModel.alt_approver.last_name,
              'email': viewModel.alt_approver.email
            }

            domainModel.approver = altApprover;
          } else{
            var approver = {
              'personDescriptor': _GetEnvAwareId(viewModel.approver.id),
              'firstName': viewModel.approver.first_name,
              'lastName': viewModel.approver.last_name,
              'email': viewModel.approver.email
            }

            domainModel.approver = approver;
          }

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
