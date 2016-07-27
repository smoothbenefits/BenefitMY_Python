BenefitMyApp.controller('TimePunchCardEditModalController', [
  '$scope',
  '$modalInstance',
  'TimePunchCardService',
  'ProjectService',
  'UsStateService',
  'PersonService',
  'CompensationService',
  'utilityService',
  'punchCard',
  'adminView',
  'companyId',
  function(
    $scope,
    $modalInstance,
    TimePunchCardService,
    ProjectService,
    UsStateService,
    PersonService,
    CompensationService,
    utilityService,
    punchCard,
    adminView,
    companyId){
    $scope.headerText = punchCard ? 'Edit Punch Card' : 'Create Punch Card';

    $scope.punchCard = punchCard;
    $scope.adminView = adminView;

    $scope.cardTypes = TimePunchCardService.GetAvailablePunchCardTypes();
    $scope.allStates = UsStateService.GetAllStates();

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
            if(compensation.hourly_rate){
              $scope.punchCard.attributes.hourlyRate.value = parseFloat(compensation.hourlyRate);
            }
            else{
              $scope.punchCard.attributes.hourlyRate.value = parseFloat(compensation.salary) / 40 / 52;
            }
          }
        });
      });
    }

    var isAttributeVisible = function(attribute) {
        return !attribute.type.adminOnly || $scope.adminMode;
    };

    $scope.isTimeRangeVisisble = function() {
        return $scope.punchCard.recordType
            && $scope.punchCard.recordType.behavior.timeRangeOn;
    };

    $scope.isHourlyRateAttributeVisisble = function() {
        return $scope.punchCard.recordType
            && isAttributeVisible(punchCard.attributes.hourlyRate);
    };

    $scope.isValidToSave = function() {
      if ($scope.form.$invalid) {
        return false;
      }

      if ($scope.isTimeRangeVisisble()
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
    function TimePunchCardWeekDirectiveController(
      $scope,
      $attrs,
      $modal,
      $controller,
      TimePunchCardService) {

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
