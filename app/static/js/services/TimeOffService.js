var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimeOffService',
  ['$q',
   'utilityService',
   'TimeOffRepository',
   'EmployeeProfileService',
   function TimeOffService(
    $q,
    utilityService,
    TimeOffRepository,
    EmployeeProfileService){

        // The enum listing out all supported timeoff types
        // This should be the only connonical source of truth
        // for this info.
        var TimeoffTypes = {
            Pto: 'Paid Time Off (PTO)',
            SickTime: 'Sick Time'
        };

        // The enum listing out all supported timeoff accural
        // frequency.
        var AccrualFrequency = {
            Annual: 'Annual',
            Monthly: 'Monthly',
            Weekly: 'Weekly',
            Daily: 'Daily',
            Hourly: 'Hourly'
        };

        // Available statuses
        var TimeoffStatus = {
            Pending: 'PENDING',
            Approved: 'APPROVED',
            Canceled: 'CANCELED',
            Denied: 'DENIED',
            Revoked: 'REVOKED'
        };

        /**
            Get the list of available time off types.
            TODO:
                For now this returns a static list, but in the
                future this will be turned into something that
                can return lists based on configuration for the
                company/user.
        */
        var getAvailableTimeoffTypes = function() {
            return [
              TimeoffTypes.Pto,
              TimeoffTypes.SickTime
            ];
        };

        /**
            Get the list of available accrual frequency.
            TODO:
                For now this returns a static list, but in the
                future this will be turned into something that
                can return lists based on configuration for the
                company/user.
        */
        var getAvailableAccrualFrequecy = function() {
            return [
              AccrualFrequency.Annual,
              AccrualFrequency.Monthly,
              AccrualFrequency.Weekly,
              AccrualFrequency.Daily,
              AccrualFrequency.Hourly
            ];
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
                actionNeeded: domainModel.status.toLowerCase() == TimeoffStatus.Pending.toLowerCase(),
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
            'status': TimeoffStatus.Pending,
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
                    var timeOffRequests = mapDomainModelsToViewModels(timeoffs);
                    return {
                        requestsPending: _.where(timeOffRequests, {actionNeeded: true}),
                        requestsActioned: _.where(timeOffRequests, {actionNeeded: false})
                    };
                });
        };

        var UpdateTimeOffStatus = function(timeOff, newStatus){
            return TimeOffRepository.StatusByTimeoffId.update({timeoffId:timeOff.id}, {status: newStatus})
                .$promise.then(function(timeoff){
                    return mapDomainModelToViewModel(timeoff);
                });
        };

        var GetTimeOffQuota = function(userId){
            var id = utilityService.getEnvAwareId(userId);
            return TimeOffRepository.QuotaByUser.get({userId:id})
                .$promise.then(function(timeoffQuota){
                    return timeoffQuota;
                });
        };

        var UpdateTimeOffQuotaByUser = function(userId, quotaModel){
            var id = utilityService.getEnvAwareId(userId);
            return TimeOffRepository.QuotaByUser.update({userId:id}, quotaModel)
                .$promise.then(function(timeoffQuota){
                    return timeoffQuota;
                });
        };

        var GetTimeOffQuotaByCompany = function(companyId) {
            var compId = utilityService.getEnvAwareId(companyId);
            return TimeOffRepository.QuotaByCompany.query({companyId:compId})
                .$promise.then(function(timeoffQuotaList){
                    return timeoffQuotaList;
                });
        };

        var GetBlankTimeOffQuota = function(companyId, userId) {
            return getBlankQuotaModel(companyId, userId);
        };

        var getBlankQuotaModel = function(companyId, userId) {
            var compId = utilityService.getEnvAwareId(companyId);
            var uId = utilityService.getEnvAwareId(userId);

            return { 
                personDescriptor: uId,
                companyDescriptor: compId,
                quotaInfoCollection:_.map(
                    getAvailableTimeoffTypes(),
                    getBlankAccrualModel)
            };
        };

        var getBlankAccrualModel = function(timeoffType) {
            return {
                timeoffType: timeoffType,
                bankedHours: 0.0,
                accrualSpecs: {
                    accrualRate: 0.0,
                    accrualFrequency: AccrualFrequency.Monthly,
                    accruedHours: 0.0
                }
            };
        };

        return {
            TimeoffTypes: TimeoffTypes,
            AccrualFrequency: AccrualFrequency,
            TimeoffStatus: TimeoffStatus,
            GetAvailableTimeoffTypes: getAvailableTimeoffTypes,
            GetAvailableAccrualFrequecy: getAvailableAccrualFrequecy,
            GetTimeOffsByRequestor: GetTimeOffsByRequestor,
            RequestTimeOff: requestTimeOff,
            GetTimeOffsByApprover: GetTimeOffsByApprover,
            UpdateTimeOffStatus: UpdateTimeOffStatus,
            GetTimeOffQuota: GetTimeOffQuota,
            UpdateTimeOffQuotaByUser: UpdateTimeOffQuotaByUser,
            GetTimeOffQuotaByCompany: GetTimeOffQuotaByCompany,
            GetBlankTimeOffQuota: GetBlankTimeOffQuota
        };
    }
]);
