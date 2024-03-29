BenefitMyApp.controller('TimePunchCardEditModalController', [
  '$scope',
  '$modalInstance',
  'TimePunchCardService',
  'ProjectService',
  'UsStateService',
  'PersonService',
  'UserService',
  'CompensationService',
  'utilityService',
  'CompanyFeatureService',
  'punchCard',
  'adminView',
  'companyId',
  'TimePunchCardDetectionConfigurations',
  function(
    $scope,
    $modalInstance,
    TimePunchCardService,
    ProjectService,
    UsStateService,
    PersonService,
    UserService,
    CompensationService,
    utilityService,
    CompanyFeatureService,
    punchCard,
    adminView,
    companyId,
    TimePunchCardDetectionConfigurations){
    $scope.headerText = 'Punch Card For ' + punchCard.employee.firstName + ' ' + punchCard.employee.lastName;

    $scope.punchCard = punchCard;
    $scope.adminView = adminView;

    $scope.cardTypes = TimePunchCardService.GetAvailablePunchCardTypes();
    if (!$scope.punchCard.recordType){ 
      $scope.punchCard.recordType = $scope.cardTypes[0];
    }
    $scope.allStates = UsStateService.GetAllStates();
    $scope.cardCheckedIn = true;
    $scope.cardCheckedOut = false;

    UserService.getCurrentRoleCompleteFeatureStatus()
    .then(function(allFeatureStatus) {
      $scope.allFeatureStatus = allFeatureStatus;
    });

    $scope.$watch('punchCard.hours', function(hours){
      if(hours){
        $scope.punchCard.start = TimePunchCardService.getDefaultStartTime($scope.punchCard.date);
        $scope.punchCard.end = moment($scope.punchCard.start).add(hours, 'h');
        $scope.inProgress = false;
      }
    });

    $scope.$watch('punchCard.inProgress', function(inProgress){
      if(inProgress){
        $scope.punchCard.end = null;
      }
      else if(!$scope.punchCard.end){
        $scope.punchCard.end = moment($scope.punchCard.start);
      }
    });

    ProjectService.GetProjectsByCompany(companyId).then(function(projects) {
        $scope.allProjects = projects;
    });

    //Fill in the hourly rate of the punchCard by compensation if missing
    if(!$scope.punchCard.attributes.hourlyRate.value){
      var userId = utilityService.retrieveIdFromEnvAwareId(
        $scope.punchCard.employee.personDescriptor);
      PersonService.getSelfPersonInfo(userId)
      .then(function(person){
        CompensationService.getCurrentCompensationByPerson(person.id)
        .then(function(compensation){
          if(compensation){
            if(compensation.hourlyRate){
              $scope.punchCard.attributes.hourlyRate.value = parseFloat(compensation.hourlyRate).toFixed(2);
            }
            else{
              $scope.punchCard.attributes.hourlyRate.value = (parseFloat(compensation.salary) / DEFAULT_HOURS_IN_YEAR ).toFixed(2);
            }
          }
        });
      });
    }

    $scope.isLowConfidenceDetected = function() {
      var confidence = 0;

      if ($scope.hasAssets($scope.punchCard.checkInAssets)) {
        confidence = $scope.punchCard.checkInAssets.imageDetectionAsset.confidence;
      }

      if ($scope.hasAssets($scope.punchCard.checkOutAssets)) {
        var checkOutConfidence = $scope.punchCard.checkOutAssets.imageDetectionAsset.confidence;
        if (checkOutConfidence < confidence) {
          confidence = checkOutConfidence;
        }
      }

      return TimePunchCardDetectionConfigurations.imageDetectionConfidenceThreshold >= confidence;
    };

    $scope.hasAssets = function (assets) {
      return assets && assets.imageDetectionAsset;
    };

    $scope.hasPunchCardAssets = function() {
      return $scope.hasAssets($scope.punchCard.checkInAssets) ||
             $scope.hasAssets($scope.punchCard.checkOutAssets);
    };

    $scope.getRealTimeImageAssetUrl = function(assets) {
      if (!$scope.hasAssets(assets)){
        return '';
      }

      return assets.imageDetectionAsset.realTimeImageAsset.url;
    }

    var isAttributeVisible = function(attribute) {
        return !attribute.type.adminOnly || $scope.adminView;
    };

    $scope.projectManagementEnabled = function() {
        return $scope.allFeatureStatus
            && $scope.allFeatureStatus.isFeatureEnabled(
                    CompanyFeatureService.AppFeatureNames.ProjectManagement);
    };

    $scope.isHourlyRateAttributeVisible = function() {
        // First, check whether the current user needs to
        // have salary data hidden
        if ($scope.allFeatureStatus
            && $scope.allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.HideSalaryData)) {
            return false;
        }

        return $scope.punchCard.recordType
            && isAttributeVisible(punchCard.attributes.hourlyRate);
    };

    $scope.isInProgressConfigurable = function(){
      return $scope.punchCard.recordType
        && $scope.punchCard.recordType.behavior.inProgressConfigurable
        && !$scope.punchCard.inHours;
    };

    $scope.allowMultipleTimeFormat = function(){
      return $scope.punchCard.recordType
        && $scope.punchCard.recordType.behavior.multipleTimeFormat;
    };
    
    $scope.recordTypeUpdated = function(){
      if(!$scope.allowMultipleTimeFormat()){
        $scope.punchCard.inHours = true;
      }
    };

    $scope.endTimeUpdated = function(){
      $scope.punchCard.inProgress = false;
    };

    $scope.isValidToSave = function() {
      if ($scope.form.$invalid) {
        return false;
      }

      if ($scope.punchCard.end != null
                && !moment($scope.punchCard.start).isBefore(moment($scope.punchCard.end))) {
        return false;
      }

      if ($scope.punchCard.attributes.hourlyRate.value
            && $scope.punchCard.attributes.hourlyRate.value < 0) {
        return false;
      }

      return true;
    };

    $scope.save = function() {
        // Perform card type based sanitization first
        $scope.punchCard.recordType.behavior.sanitizeViewModel($scope.punchCard);
        $scope.punchCard.systemStopped = false;
        // Now save
        TimePunchCardService.SavePunchCard($scope.punchCard).then(
            function(successResponse) {
                $modalInstance.close(true);
            },
            function(errors) {
                $modalInstance.close(false);
            }
        );
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };
  }
]).controller('TimePunchCardWeeklyViewController', [
    '$scope',
    '$attrs',
    '$modal',
    '$controller',
    'TimePunchCardService',
    'TimePunchCardDetectionConfigurations',
    'CompanyFeatureService',
    function TimePunchCardWeekDirectiveController(
      $scope,
      $attrs,
      $modal,
      $controller,
      TimePunchCardService,
      TimePunchCardDetectionConfigurations,
      CompanyFeatureService) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        $scope.adminView = 'adminMode' in $attrs;

        $scope.weekdayNums = [0, 1, 2, 3, 4, 5, 6];

        $scope.init = function(){
          $scope.$watchGroup(['week', 'user', 'companyId'], function(watchGroup){
            var weekSelected = watchGroup[0];
            var user = watchGroup[1];
            var companyId = watchGroup[2];
            if(weekSelected && user && companyId) {
              var startDate = weekSelected.weekStartDate;
              $scope.datesOfWeek = [];
              for (var i=0; i<7; i++){
                var weekDate = moment(startDate).add(i, 'days');
                $scope.datesOfWeek[i] = {
                    'weekdayName': weekDate.format('ddd'),
                    'displayDate': weekDate.format(SHORT_DATE_FORMAT_STRING_NO_YEAR),
                    'date': weekDate
                };
              }

              $scope.reloadCards();
            }
          });
        };

        $scope.init();

        var showEditModal = function(punchCard) {
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/time_punch_card/modal_edit_time_punch_card.html',
                controller: 'TimePunchCardEditModalController',
                size: 'md',
                backdrop: 'static',
                resolve: {
                  'punchCard': function() {
                    return angular.copy(punchCard);
                  },
                  'adminView' : function() {
                    return $scope.adminView;
                  },
                  'companyId': function() {
                    return $scope.companyId;
                  }
                }
            });

            modalInstance.result.then(function(success){
                if (!success){
                  var message = 'Failed to save time punch card. Please try again later.';
                  $scope.showMessageWithOkayOnly('Error', message);
                }

                $scope.reloadCards();
              });
        };

        $scope.createPunchCard = function(date) {
            var punchCard = TimePunchCardService.GetBlankPunchCardForEmployeeUser(
                    $scope.user,
                    $scope.companyId,
                    date);
            showEditModal(punchCard);
        };

        $scope.editPunchCard = function(punchCard) {
            showEditModal(punchCard);
        };

        $scope.deletePunchCard = function(punchCard) {
            TimePunchCardService.DeletePunchCard(punchCard).then(function(response) {
                $scope.reloadCards();
            });
        };

        $scope.reloadCards = function() {
            $scope.weeklyPunchCards = [];
            if ($scope.week && $scope.user && $scope.companyId) {
              setTimeout(function(){
                // Add a time delay to ensure all the cards are in stable state in timetracking service
                TimePunchCardService.GetWeeklyPunchCardsByEmployeeUser(
                    $scope.user, $scope.week.weekStartDate, $scope.week.weekEndDate).then(
                    function(punchCards) {
                        $scope.weeklyPunchCards = punchCards;
                    }
                );
                CompanyFeatureService.getAllApplicationFeatureStatusByCompanyUser($scope.companyId, $scope.user.id)
                .then(function(userFeaturesStatus){
                  $scope.userFeaturesStatus = userFeaturesStatus;
                });
              }, 300);
            }
        };

        $scope.isAttributeVisible = function(attribute) {
            return (!attribute.type.adminOnly || $scope.adminMode)
                && attribute.value;
        };

        $scope.attentionNeeded = function(punchCard) {

            var threshold = TimePunchCardDetectionConfigurations.imageDetectionConfidenceThreshold;

            // Examine check in assets
            if (punchCard.checkInAssets && punchCard.checkInAssets.imageDetectionAsset) {
                var confidence = punchCard.checkInAssets.imageDetectionAsset.confidence;
                if (!confidence || confidence <= threshold) {
                    return true;
                }
            }

            // Examine check out assets
            if (punchCard.checkOutAssets && punchCard.checkOutAssets.imageDetectionAsset) {
                var confidence = punchCard.checkOutAssets.imageDetectionAsset.confidence;
                if (!confidence || confidence <= threshold) {
                    return true;
                }
            }

            return false;
        };

        $scope.cardActionAllowed = function(){
          return $scope.adminMode ||
            !($scope.userFeaturesStatus &&
              $scope.userFeaturesStatus.isFeatureEnabled(
                    CompanyFeatureService.AppFeatureNames.EmployeeTimePunchCardViewOnly));
        }
    }
  ]
).directive('bmTimePunchCardWeeklyView', function() {
  return {
    restrict: 'E',
    scope: {
        week: '=',
        user: '=',
        companyId: '=',
        adminMode: '=?'
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_weekly_view.html',
    controller: 'TimePunchCardWeeklyViewController'
  };
});
