BenefitMyApp.directive('bmuploadmanager', 
  function() {
    return {
      restrict: 'E',
      scope: {},
      templateUrl: '/static/partials/common/upload.html',
      controller: ['$scope', 
                   '$timeout', 
                   '$attrs', 
                   'UploadService', 
          function($scope, 
                   $timeout, 
                   $attrs,
                   UploadService) {
            $scope.uploadManager = {
              hideUploadArea: false,
              canManageUpload: true,
              hideTypeColumn: $attrs.hideType,
              uploadMode: $attrs.uploadMode || 'area',
              viewMode: $attrs.viewMode || 'table',
              uploadedFiles: [],
              files:[],
              deleteS3File: function(file){
                UploadService.deleteFile(file.id, file.S3).then(function(deletedFile){
                  $scope.uploadManager.uploadedFiles = _.without($scope.uploadManager.uploadedFiles, file);
                  $scope.uploadManager.deleteSuccess = true;
                  $timeout(function(){
                    $scope.uploadManager.deleteSuccess = false;
                  }, 5000);
                });
              }};

            var handleUploadArea = function(files, uploadType){
              if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                  var file = files[i];
                  $scope.uploadManager.inProgress = {file:file};
                  UploadService.uploadFile(file, uploadType).then(
                    function(fileUploaded){
                      $scope.uploadManager.inProgress = undefined;
                      $scope.uploadManager.uploadedFiles.unshift(fileUploaded);
                      if($attrs.featureId){
                        UploadService.SetUploadApplicationFeature(fileUploaded.id, uploadType, $attrs.featureId)
                        .then(function(){
                        }, function(error){
                          alert(error);
                        });
                      }
                    },
                    function(error){
                      alert('upload error happened!');
                      $scope.uploadManager.inProgress = undefined;
                    },
                    function(evt){
                      $scope.uploadManager.inProgress.progress = (evt.loaded/evt.total)*100;
                    });
                }
              }
            };
            $scope.$watch('uploadManager.files', function(){
              handleUploadArea($scope.uploadManager.files, $attrs.uploadType);
            });

            if($attrs.featureId && $attrs.uploadType){
              $attrs.$observe('featureId', function(){
                UploadService.getUploadsByFeature($attrs.featureId, $attrs.uploadType)
                .then(function(resp){
                  $scope.uploadManager.uploadedFiles = resp;
                });  
              });  
            }
            else{
              UploadService.getAllUploadsByCurrentUser().then(function(resp){
                $scope.uploadManager.uploadedFiles = resp;
              });
            }
          }]
    };
  });
