var benefitmyService = angular.module('benefitmyService');
benefitmyService.factory('UploadService',
  ['$http',
   '$upload',
   '$q',
   'UserService',
   'UploadRepository',
   'ApplicationFeatureService',
   function($http,
            $upload,
            $q,
            UserService,
            UploadRepository,
            ApplicationFeatureService){

    var _getCurrentUserInfo = function(){
        var deferred = $q.defer();
        UserService.getCurUserInfo().then(
            function(userInfo){
                deferred.resolve(userInfo);
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
        return deferred.promise;
    };

    var get_file_type = function(file){
        return file.type != '' ? file.type : 'application/octet-stream'
    }

    var _getS3Key = function(companyName, fileKey, fileName){
        var s3Key = companyName + ':' + fileKey + ':' + fileName;
        s3Key = s3Key.split(' ').join('_');
        return s3Key;
    };

    var _uploadToS3 = function(file, uploadInfo){
        var deferred = $q.defer();
        $upload.upload({
              url: uploadInfo.s3Host,
              method: 'POST',
              fields : {
                key: uploadInfo.fileKey, // the key to store the file on S3, could be file name or customized
                AWSAccessKeyId: uploadInfo.accessKey,
                acl: 'private', // sets the access to the uploaded file in the bucket: private or public
                policy: uploadInfo.policy, // base64-encoded json policy (see article below)
                signature: uploadInfo.signature, // base64-encoded signature based on policy string (see article below)
                "Content-Type": get_file_type(file),// content type of the file (NotEmpty)
                filename: file.name, // this is needed for Flash polyfill IE8-9
                "x-amz-server-side-encryption": "AES256"
              },
              file: file
          }).progress(function (evt) {
              deferred.notify(evt);
              var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
              console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
          }).success(function (data, status, headers, config) {
              deferred.resolve(data, config);
          }).error(function(data, status, headers, config){
              deferred.reject(data, status, headers, config);
          });
        return deferred.promise;
    };

    var _deleteFromS3 = function(s3, auth, curTime){
        var deferred = $q.defer();
        var req = {
            method: 'DELETE',
            url: s3,
            headers: {
              'Authorization': auth,
              'x-amz-date': curTime
             }
        };

        $http(req).success(function(response){
            deferred.resolve(response);
        }).error(function(errorResponse){
            deferred.reject(errorResponse);
        });
        return deferred.promise;
    };

    var SetUploadApplicationFeature = function(uploadFileId, uploadType, featureId){
      var deferred = $q.defer();

      ApplicationFeatureService.getApplicationFeatures().then(function(appFeatures){
        if(!appFeatures[uploadType]){
          deferred.reject('The ApplicationFeature provided did not match what server returned!');
        }
        UploadRepository.uploadApplicationFeature.save(
          {app_feature:appFeatures[uploadType], feature_id:featureId},
          {upload: uploadFileId},
          function(resp){
            deferred.resolve(resp);
          }, function(error){
            deferred.reject(error);
          });
      });

      return deferred.promise;
    };

    var uploadFile = function(file, uploadType){
        var deferred = $q.defer();

        _getCurrentUserInfo().then(function(userInfo){
            var fileToUpload = {
              'company': userInfo.currentRole.company.id,
              'user': userInfo.user.id,
              'company_name': userInfo.currentRole.company.name,
              'file_name': file.name,
              'file_type': get_file_type(file)
            }
            UploadRepository.uploadsByUser.save(
                {pk:userInfo.user.id},
                fileToUpload,
                function(response){
                  //now we are able to actually upload to S3
                  _uploadToS3(file, response).then(
                    function(data, config){
                        deferred.resolve(response);
                    }, function(data, status, headers, config){
                        //need to call our server to remove the record
                        deferred.reject(response, data, status, headers, config);
                    }, function(evt){
                        deferred.notify(evt);
                    })
                }, function(error){
                    deferred.reject(error);
                });
        });
        return deferred.promise;
    };

    var getAllUploadsByCurrentUser = function(){
        var deferred = $q.defer();
        _getCurrentUserInfo().then(function(userInfo){
            UploadRepository.uploadsByUser.query({pk:userInfo.user.id})
            .$promise.then(function(uploadedFiles){
                deferred.resolve(uploadedFiles);
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
        });
        return deferred.promise;
    };

    var getUploadsByFeature = function(featureId, uploadType){
      var deferred = $q.defer();

      ApplicationFeatureService.getApplicationFeatures().then(function(appFeatures){
        if(!appFeatures[uploadType]){
          deferred.reject('The ApplicationFeature provided did not match what server returned!');
        }
        UploadRepository.uploadApplicationFeature
        .query({app_feature: appFeatures[uploadType], feature_id: featureId},
          function(resp){
            var files = [];
            if(resp.length > 0){
              _.each(resp, function(item){
                files.push(item.upload);
              });
            }
            deferred.resolve(files);
          }, function(error){
            deferred.reject(error);
          });
      });

      return deferred.promise;
    };

    var deleteFile = function(id){
        var deferred = $q.defer();
        UploadRepository.upload.delete({pk:id})
        .$promise.then(function(deletedFile){
            //here is where we should delete it from S3
            _deleteFromS3(deletedFile.S3, deletedFile.auth, deletedFile.time)
            .then(function(deleteResponse){
                deferred.resolve(deleteResponse);
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
            deferred.resolve(deletedFile);
        }, function(errorResponse){
            deferred.reject(errorResponse);
        });
        return deferred.promise;
    };

    var getEmployeeUploads = function(companyId, employeeId){
      var deferred = $q.defer();
      UploadRepository.uploadsByCompany.query({compId:companyId, pk:employeeId})
      .$promise.then(function(resp){
        deferred.resolve(resp);
      }, function(errResp){
        deferred.reject(errResp);
      });

      return deferred.promise;
    };

    return{
        uploadFile: uploadFile,
        getFileType: get_file_type,
        getAllUploadsByCurrentUser: getAllUploadsByCurrentUser,
        deleteFile: deleteFile,
        getEmployeeUploads: getEmployeeUploads,
        SetUploadApplicationFeature: SetUploadApplicationFeature,
        getUploadsByFeature: getUploadsByFeature
    };
   }
]);
