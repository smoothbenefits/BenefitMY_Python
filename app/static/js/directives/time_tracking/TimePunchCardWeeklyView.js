BenefitMyApp.controller('TimePunchCardEditModalController', [
  '$scope',
  '$modalInstance',
  'TimePunchCardService',
  'UsStateService',
  'punchCard',
  'adminView',
  function(
    $scope,
    $modalInstance,
    TimePunchCardService,
    UsStateService,
    punchCard,
    adminView){
    $scope.headerText = punchCard ? 'Edit Punch Card' : 'Create Punch Card';

    $scope.punchCard = punchCard;
    $scope.adminView = adminView;

    $scope.cardTypes = TimePunchCardService.GetAvailablePunchCardTypes();
    $scope.allStates = UsStateService.GetAllStates();

    $scope.allProjects = [
        '205 Aloha Avenue',
        'The Universal Tower',
        'Harland Street Rework'
    ];

    $scope.selectedState = null;
    $scope.selectedProject = null;
    $scope.hourlyRate = 65.4;

    $scope.save = function(){
        TimePunchCardService.SavePunchCard($scope.punchCard).then(
            function(successResponse) {
                $modalInstance.close(true);
            },
            function(errors) {
                $modalInstance.close(false);
            }
        );
    }
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
          $scope.$watchGroup(['week', 'user', 'company'], function(watchGroup){
            var weekSelected = watchGroup[0];
            var user = watchGroup[1];
            var company = watchGroup[2];
            if(weekSelected && user && company) {
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

        $scope.getDisplayTime = function(dateTime) {
            var time = moment(dateTime);
            return time.format('hh:mm');
        };

        var showEditModal = function(punchCard) {
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/time_punch_card/modal_edit_time_punch_card.html',
                controller: 'TimePunchCardEditModalController',
                size: 'md',
                backdrop: 'static',
                resolve: {
                  'punchCard': function() {
                    return punchCard;
                  },
                  'adminView' : function() {
                    return $scope.adminView;
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
                    $scope.company,
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
            if ($scope.week && $scope.user && $scope.company) {
                TimePunchCardService.GetWeeklyPunchCardsByEmployeeUser(
                    $scope.user, $scope.week.weekStartDate, $scope.week.weekEndDate).then(
                    function(punchCards) {
                        $scope.weeklyPunchCards = punchCards;
                    }
                );
            }
        };
    }
  ]
).directive('bmTimePunchCardWeeklyView', function() {
  return {
    restrict: 'E',
    scope: {
        week: '=',
        user: '=',
        company: '=',
        adminMode: '=?'
    },
    templateUrl: '/static/partials/time_punch_card/directive_time_punch_card_weekly_view.html',
    controller: 'TimePunchCardWeeklyViewController'
  };
});
