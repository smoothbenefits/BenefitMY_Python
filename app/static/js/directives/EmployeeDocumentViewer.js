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
                $scope.documents = _.filter(documents, function(doc) {
                    return !doc.signature;
                });
            }
        );

        $scope.signDocuments = function(signature) {
            // Sign all the documents with the signature
            DocumentService.batchSignUserDocuments($scope.documents, signature.id).then(
                function(response) {
                    if ('onDocumentsSigned' in $attrs) {
                        $scope.onDocumentsSigned();
                    }
                }
            );
        };

        $scope.allDocumentsAccepted = function() {
            return !_.some($scope.documents, function(doc) {
                return !doc.accepted;
            });
        };

        $scope.showDocument = function(document) {
            $modal.open({
              templateUrl: '/static/partials/documents/modal_view_document.html',
              controller: viewDocumentModalController,
              size: 'lg',
              resolve: {
                  document: function () {
                    return document;
                  }
              }
            });
        };
    }
  ];

  var viewDocumentModalController = [
    '$scope',
    '$modal',
    '$modalInstance',
    'document',
    function viewDocumentModalController(
      $scope,
      $modal,
      $modalInstance,
      document) {
        $scope.document = document;

        $scope.ok = function () {
          $modalInstance.close();
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        userId: '=',
        onDocumentsSigned: '&'
    },
    templateUrl: '/static/partials/documents/directive_employee_document_viewer.html',
    controller: controller
  };
});
