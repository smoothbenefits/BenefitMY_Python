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
            Monthly: 'Monthly',
            Daily: 'Daily'
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

        /**
            TODO:
                Method as short term hack/mock for BM-1051.
                Needs to be removed once the real data for 
                timeoff quota is populated
        */
        var getFakeTimeoffQuotaModel = function(envAwareUserId, isFullTime) {
            var annualTargetPtoHours = isFullTime ? 80 : 20;
            var annualTargetSickTimeHours = isFullTime ? 40 : 20;
            var accruedPtoHours = ComputeAccruedHours(annualTargetPtoHours);
            var accruedSickTimeHours = ComputeAccruedHours(annualTargetSickTimeHours);

            return  {
                personDescriptor: envAwareUserId,
                quotaInfoCollection:[
                {
                    timeoffType: TimeoffTypes.Pto,
                    bankedHours: accruedPtoHours,
                    annualTargetHours: annualTargetPtoHours,
                    accrualSpecs: {
                        accrualFrequency: AccrualFrequency.Monthly,
                        accruedHours: accruedPtoHours
                    }
                },
                {
                    timeoffType: TimeoffTypes.SickTime,
                    bankedHours: accruedSickTimeHours,
                    annualTargetHours: annualTargetSickTimeHours,
                    accrualSpecs: {
                        accrualFrequency: AccrualFrequency.Monthly,
                        accruedHours: accruedSickTimeHours
                    }
                }]
            };
        };

        /**
            TODO:
                Method as short term hack/mock for BM-1051.
                Needs to be removed once the real data for 
                timeoff quota is populated
        */
        var ComputeAccruedHours = function(annualTargetHours) {
            //  - Accural Frequency: Monthly
            //  - moment().month() is zero based
            var fraction = moment().month() / 12.0;
            return (fraction * annualTargetHours).toFixed(1);
        };

        /**
            TODO:
                Method as short term hack/mock for BM-1051.
                Needs to be removed once the real data for 
                timeoff quota is populated
        */
        var GetFakeTimeOffQuota = function(userId, companyId) {
            return EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, userId).then(
                function(employeeProfile) {
                    var id = utilityService.getEnvAwareId(userId);
                    return getFakeTimeoffQuotaModel(
                        id,
                        EmployeeProfileService.isFullTimeEmploymentType(employeeProfile));
                }
            );
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
                    return timeoffQuota;
                });
        };

        var GetTimeOffQuotaByCompany = function(companyId){
            var compId = utilityService.getEnvAwareId(companyId);
            return TimeOffRepository.QuotaByCompany.query({companyId:compId})
                .$promise.then(function(timeoffQuotaList){
                    return timeoffQuotaList;
                });
        };

        return {
            TimeoffTypes: TimeoffTypes,

            GetAvailableTimeoffTypes: getAvailableTimeoffTypes,
            GetTimeOffsByRequestor: GetTimeOffsByRequestor,
            RequestTimeOff: requestTimeOff,
            GetTimeOffsByApprover: GetTimeOffsByApprover,
            UpdateTimeOffStatus: UpdateTimeOffStatus,
            
            // GetTimeOffQuota: GetTimeOffQuota

            /**
            TODO:
                This method export is for temp hack for BM-1051
                This should be removed and the above commented out
                line should be resumed once real timeoff quota data
                is in.
            */
            GetTimeOffQuota: GetFakeTimeOffQuota,
            GetTimeOffQuotaByCompany: GetTimeOffQuotaByCompany
        };
    }
]);
