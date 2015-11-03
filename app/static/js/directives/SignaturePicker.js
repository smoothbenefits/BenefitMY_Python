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

        // Allow customized description header, with fallback to 
        // a default
        $scope.description = ('descriptionText' in $attrs) 
                                ? $scope.descriptionText
                                : '';

        // Allow customized button display text, with fallback to 
        // a default
        $scope.confirmSignButtonText = ('signButtonText' in $attrs) 
                                ? $scope.signButtonText
                                : 'Confirm Sign';

        // Whether user check the box to express the intect to sign
        $scope.electSign = false;

        $scope.allowSign = function() {
            if ('allowSignPredicate' in $attrs) {
                return $scope.allowSignPredicate();
            }
            return true;
        }

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

        // Initialize the signature pad
        var signatureUpdated = false;
        var $sigdiv = $("#doc_signature");
        $sigdiv.jSignature();
        $sigdiv.bind('change', function(e){
         signatureUpdated = true;
        });

        // 
        $scope.signatureExists = function() {
            return $scope.signature && $scope.signature.id;
        };

        $scope.clearSignature = function() {
            $sigdiv.jSignature("reset");
            signatureUpdated = false;
        };

        $scope.confirmSign = function() {
            if (!$scope.signatureExists() && !signatureUpdated) {
                alert('Please sign your name on the signature pad');
                return;
            }

            var signatureData = null;
            if ($scope.signatureExists()) {
                signatureData = $scope.signature.signature;
            } else {
                var imageData = $sigdiv.jSignature('getData', 'svg');
                signatureData = "data:" + imageData[0] + ',' + imageData[1];
            }

            var modelToSave = {
                'signature': signatureData,
                'userId': $scope.signature.userId
            };

            SignatureService.saveSignature(modelToSave)
            .then(
                function(resultSignature) {
                    $scope.signature = resultSignature;
                    if ('onConfirmSign' in $attrs) {
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
        panelHeaderText: '=',
        descriptionText: '=',
        signButtonText: '=',
        allowSignPredicate: '&'
    },
    templateUrl: '/static/partials/employee_profile/directive_signature_picker.html',
    controller: controller
  };
});
