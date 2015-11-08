BenefitMyApp.directive('bmEmployeeDocumentViewer', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    '$attrs',
    '$modal',
    'DocumentService',
    function EmployeeDocumentViewerDirectiveController(
      $scope,
      $location,
      $window,
      $attrs,
      $modal,
      DocumentService) {

        // Get the list of documents for the given user
        DocumentService.getAllDocumentsForUser($scope.userId).then(
            function(documents) {
                $scope.documents = documents;
            }
        );
    }
  ];

  return {
    restrict: 'E',
    scope: {
        userId: '='
    },
    templateUrl: '/static/partials/documents/directive_employee_document_viewer.html',
    controller: controller
  };
});
