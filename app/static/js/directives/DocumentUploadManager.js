BenefitMyApp.directive('bmdocumentuploadmanager', 
  function() {
    return {
      restrict: 'E',
      scope: {
        // Call back when an upload is successfully uploaded
        onUploadAdded: '&',
        // Call back when and upload is deleted
        onUploadDeleted: '&',
        // view-only mode
        viewOnlyMode: '='
      },
      templateUrl: '/static/partials/documents/document_upload.html',
      controller: ['$scope',
                   '$timeout',
                   '$attrs',
                   'UploadService',
                   'TemplateService',
                   'DocumentService',
          function($scope,
                   $timeout,
                   $attrs,
                   UploadService,
                   TemplateService,
                   DocumentService) {

            // For the use case where either an existing template ID
            // or a document ID is given, don't actually delete the 
            // relevant uploads, as those could be shared with others
            $scope.hideAndNotDelete = $attrs.templateId || $attrs.documentId;

            $scope.uploadManager = {
              maxUploads: 1,
              uploadedFiles: [],
              files:[],
              deleteS3File: function(file){
                // If indicated so, do not really delete the files, but rather hide from
                // from the view. 
                if ($scope.hideAndNotDelete) {
                    $scope.uploadManager.onDeleteSuccess(file);
                }
                else {
                    UploadService.deleteFile(file.id, file.S3).then(function(deletedFile){
                      $scope.uploadManager.onDeleteSuccess(file);
                    });
                }
              },
              onDeleteSuccess: function(file) {
                $scope.uploadManager.uploadedFiles = _.without($scope.uploadManager.uploadedFiles, file);
                $scope.uploadManager.deleteSuccess = true;
                if ('onUploadDeleted' in $attrs) {
                    $scope.onUploadDeleted({upload: file});
                }
                $timeout(function(){
                    $scope.uploadManager.deleteSuccess = false;
                }, 5000);
              }
            }; 

            var handleUploadArea = function(files){
              if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                  var file = files[i];
                  $scope.uploadManager.inProgress = {file:file};
                  UploadService.uploadFile(file).then(
                    function(fileUploaded){
                      $scope.uploadManager.inProgress = undefined;
                      $scope.uploadManager.uploadedFiles.unshift(fileUploaded);
                      if ('onUploadAdded' in $attrs) {
                        $scope.onUploadAdded({upload: fileUploaded});
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

            $scope.hideUploadArea = function() {
                return $scope.viewOnlyMode
                    || ($scope.uploadManager.uploadedFiles
                        && $scope.uploadManager.uploadedFiles.length >= $scope.uploadManager.maxUploads);
            };

            $scope.$watch('uploadManager.files', function(){
              handleUploadArea($scope.uploadManager.files);
            });

            $scope.getDownloadUrl = function(uploadFile) {
                return uploadFile.documentDownloadUrl
                    ? uploadFile.documentDownloadUrl
                    : uploadFile.S3;
            };

            if ('templateId' in $attrs) {
                $attrs.$observe('templateId', function(templateId) {
                    $scope.uploadManager.uploadedFiles = [];
                    if ($attrs.templateId) {
                        TemplateService.getTemplateById($attrs.templateId)
                          .then(function(template){
                            if (template && template.upload) {
                                $scope.uploadManager.uploadedFiles.push(template.upload);
                            }
                        });
                    }
                });
            } 
            else if ('documentId' in $attrs) {
                $attrs.$observe('documentId', function(documentId) {
                    $scope.uploadManager.uploadedFiles = [];
                    if ($attrs.documentId) {
                        DocumentService.getDocumentById($attrs.documentId)
                          .then(function(document){
                            if (document && document.upload) {
                                var uploadToAdd = angular.copy(document.upload);
                                uploadToAdd.documentDownloadUrl = document.downloadUrl;
                                $scope.uploadManager.uploadedFiles.push(uploadToAdd);
                            }
                        });
                    }
                });
            }
          }]
    };
  });
