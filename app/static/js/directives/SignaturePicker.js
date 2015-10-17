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

        $scope.signatureAlreadySaved = function() {
            return $scope.signature && $scope.signature.id;
        };

        $scope.clearSignature = function() {
            $sigdiv.jSignature("reset");
            signatureUpdated = false;
        };

        $scope.confirmSign = function() {
            if ($scope.signatureAlreadySaved()) {
                if ($scope.onConfirmSign) {
                    $scope.onConfirmSign({resultSignature: $scope.signature});
                }
            }
            else 
            {
                var signatureData = $sigdiv.jSignature('getData', 'svg');
                $scope.signature.signature = "data:" + signatureData[0] + ',' + signatureData[1];

                SignatureService.saveSignature($scope.signature)
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
            }
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        onConfirmSign: '&',
        userId: '=',
        signatureId: '=',
        viewMode: '=' 
    },
    templateUrl: '/static/partials/employee_profile/directive_signature_picker.html',
    controller: controller
  };
});
