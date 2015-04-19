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
                  UploadService.uploadFile(file, uploadType).then(
                    function(fileUploaded){
                      $scope.uploadManager.uploadedFiles.unshift(fileUploaded);
                    },
                    function(error){
                      alert('upload error happened!');
                    },
                    function(evt){
                      //Here is the function for showing upload progress
                    });
                }
              }
            };
            $scope.$watch('uploadManager.files', function(){
              handleUploadArea($scope.uploadManager.files, $attrs.uploadType);
            });
            UploadService.getAllUploadsByCurrentUser().then(function(resp){
              $scope.uploadManager.uploadedFiles = resp;
            });
          }]
    };
  });
