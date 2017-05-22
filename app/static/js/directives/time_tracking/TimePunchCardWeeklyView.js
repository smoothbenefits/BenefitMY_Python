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
    $scope.headerText = punchCard ? 'Edit Punch Card' : 'Create Punch Card';

    $scope.punchCard = punchCard;
    $scope.adminView = adminView;

    $scope.cardTypes = TimePunchCardService.GetAvailablePunchCardTypes();
    $scope.allStates = UsStateService.GetAllStates();

    UserService.getCurrentRoleCompleteFeatureStatus()
    .then(function(allFeatureStatus) {
      $scope.allFeatureStatus = allFeatureStatus;
    });

    $scope.$watch('punchCard.hours', function(hours){
      if(hours){
        $scope.punchCard.start = TimePunchCardService.getDefaultStartTime();
        $scope.punchCard.end = moment(TimePunchCardService.getDefaultStartTime()).add(hours, 'h');
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

    $scope.isTimeVisisble = function() {
        return $scope.punchCard.recordType
            && $scope.punchCard.recordType.behavior.timeRangeOn;
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

    $scope.isValidToSave = function() {
      if ($scope.form.$invalid) {
        return false;
      }

      if ($scope.isTimeVisisble()
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
    function TimePunchCardWeekDirectiveController(
      $scope,
      $attrs,
      $modal,
      $controller,
      TimePunchCardService,
      TimePunchCardDetectionConfigurations) {

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
                TimePunchCardService.GetWeeklyPunchCardsByEmployeeUser(
                    $scope.user, $scope.week.weekStartDate, $scope.week.weekEndDate).then(
                    function(punchCards) {
                        $scope.weeklyPunchCards = punchCards;
                    }
                );
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
