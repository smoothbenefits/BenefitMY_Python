BenefitMyApp.directive('bmCompanyGroupSelection', function() {

  var controller = [
    '$scope',
    '$attrs',
    'CompanyBenefitGroupService',
    function CompanyGroupSelectionDirectiveController(
      $scope, 
      $attrs,
      CompanyBenefitGroupService) {

        // Allow customized panel header, with fallback to 
        // a default
        $scope.topLabelText = ('labelText' in $attrs) 
                                ? $scope.labelText
                                : 'Company Group Selection';

        $scope.showTopBar = ('showTopSeparationLine' in $attrs);

        $scope.companyGroups = [];
        CompanyBenefitGroupService.GetCompanyBenefitGroupByCompany($scope.companyId).then(
            function(companyGroups) {
                $scope.companyGroups = companyGroups;
            }
        );
    }
  ];

  return {
    restrict: 'E',
    scope: {
        companyId: '=',
        showTopSeparationLine: '=',
        labelText: '=',
        selectedGroupsModel: '='
    },
    templateUrl: '/static/partials/common/directive_company_group_selection.html',
    controller: controller
  };
});
