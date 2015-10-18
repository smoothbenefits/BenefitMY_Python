BenefitMyApp.directive('bmSignaturePicker', function() {

  var controller = [
    '$scope',
    '$location',
    '$window',
    '$attrs',
    '$modal',
    'SignatureService',
    function SignaturePickerDirectiveController(
      $scope,
      $location,
      $window,
      $attrs,
      $modal,
      SignatureService) {

        // Allow customized panel header, with fallback to 
        // a default
        $scope.panelHeader = ('panelHeaderText' in $attrs) 
                                ? $scope.panelHeaderText
                                : 'Signature';

        // Whether user check the box to express the intect to sign
        $scope.electSign = false;

        // Are we in view only mode?
        $scope.inViewMode = function() {
            // If an existing signature ID is given, or
            // if it is explicitly specified for viewMode
            // we are in view only mode.
            return 'viewMode' in $attrs || $scope.signatureId;
        };

        // The general rule is that:
        //  - If it is given an existing signature Id, try using that
        //  - If a user ID is also given, try resolving to a signature 
        //    based on that, if none found by signature ID
        //  i.e. Give signatureId priority over userId 
        var userIdWatcher = null;
        if (!$scope.inViewMode()) {
            if ($attrs.userId) {
                userIdWatcher = $scope.$watch('userId', function(newVal) {
                    if(newVal) { 
                        SignatureService.getSignatureByUser(newVal)
                        .then(function(signature) {
                            // Don't overwrite, if a signatureId is already 
                            // found.
                            if (!$scope.signatureId) {
                                $scope.signature = signature;
                                // Set the date stamp to current date
                                // as this path is to use only to re-use
                                // existing signature on user account to
                                // create new signatures
                                $scope.signature.createdDateForDisplay = moment().format(DATE_FORMAT_STRING);
                            }
                        });
                    }
                }, true);
            }
        }

        if ('signatureId' in $attrs) {
            $scope.$watch('signatureId', function(newVal) {
                if(newVal) {
                    // unwatch user id if found a signature by 
                    // the given ID
                    if (userIdWatcher) {
                        userIdWatcher();
                    }
                    SignatureService.getSignatureById(newVal)
                    .then(function(signature) {
                        $scope.signature = signature;
                    });
                } else {
                    $scope.signature = null;
                }
            }, true);
        } 

        var $sigdiv = $("#doc_signature");
        $sigdiv.jSignature();

        // 
        $scope.signatureExists = function() {
            return $scope.signature && $scope.signature.id;
        };

        $scope.clearSignature = function() {
            $sigdiv.jSignature("reset");
            signatureUpdated = false;
        };

        $scope.confirmSign = function() {
            var signatureData = $scope.signatureExists()
                                ? $scope.signature.signature
                                : $sigdiv.jSignature('getData', 'svg');

            var modelToSave = {
                'signature': signatureData,
                'userId': $scope.signature.userId
            };

            SignatureService.saveSignature(modelToSave)
            .then(
                function(resultSignature) {
                    $scope.signature = resultSignature;
                    if ($scope.onConfirmSign) {
                        $scope.onConfirmSign({resultSignature: $scope.signature});
                    }
                }
              , function(error) {
                    alert('Failed to submit the signature. Please try again later.');
                }
            );
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        onConfirmSign: '&',
        userId: '=',
        signatureId: '=',
        viewMode: '=',
        panelHeaderText: '=' 
    },
    templateUrl: '/static/partials/employee_profile/directive_signature_picker.html',
    controller: controller
  };
});
