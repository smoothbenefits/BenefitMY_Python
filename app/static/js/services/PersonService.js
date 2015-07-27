var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('PersonService',
  ['peopleRepository',
   '$q',
    function(peopleRepository,
      $q){

      var getSelfPersonInfo = function(uId){
        var deferred = $q.defer();
        peopleRepository.ByUser.get({userId:uId})
          .$promise.then(function(userPerson){
            var selfPerson = _.findWhere(userPerson.family, {relationship:'self'});
            if(selfPerson){
              var viewSelfPerson = mapDtoPersonToViewPerson(selfPerson)
              deferred.resolve(viewSelfPerson);
            }
            else{
              deferred.reject(null);
            }
          });
        return deferred.promise;
      };

      var getFamilyInfo = function(uid){
        var deferred = $q.defer();
        peopleRepository.ByUser.get({userId:uid}).$promise
        .then(function(response){
          var viewFamily = [];
          _.each(response.family, function(familyMember){
            viewFamily.push(mapDtoPersonToViewPerson(familyMember));
          });
          deferred.resolve(viewFamily);
        });
        return deferred.promise;
      };

      var mapViewPersonToDto = function(viewPerson){
        viewPerson.birth_date = moment(viewPerson.birth_date).format('YYYY-MM-DD');
        var apiUserPerson = angular.copy(viewPerson);
        apiUserPerson.addresses = [];
        viewPerson.address.address_type = 'home';
        viewPerson.address.state = viewPerson.address.state.toUpperCase();
        apiUserPerson.addresses.push(viewPerson.address);
        if(apiUserPerson.phones && apiUserPerson.phones.length > 0){
          apiUserPerson.phones[0].number = viewPerson.phone.number;
        }
        else{
          apiUserPerson.phones = [];
          apiUserPerson.phones.push({phone_type:'home', number:viewPerson.phone.number});
        }
        if(!apiUserPerson.person_type){
          apiUserPerson.person_type = 'primary_contact';
        }
        if(!apiUserPerson.relationship){
          apiUserPerson.relationship = 'self';
        }
        apiUserPerson.emergency_contact=[];
        if(viewPerson.emergency){
          viewPerson.emergency.reason_for_change = apiUserPerson.reason_for_change;
          apiUserPerson.emergency_contact.push(viewPerson.emergency);
        }
        return apiUserPerson;
      };

      var mapDtoPersonToViewPerson = function(DtoPerson){
        var viewPerson = angular.copy(DtoPerson);
        viewPerson.reason_for_change = undefined;
        if(viewPerson.phones && viewPerson.phones.length > 0){
          viewPerson.phone = viewPerson.phones[0];
        }
        if(viewPerson.addresses && viewPerson.addresses.length > 0){
          viewPerson.address = viewPerson.addresses[0];
        }
        if(viewPerson.emergency_contact && viewPerson.emergency_contact.length > 0){
          viewPerson.emergency = viewPerson.emergency_contact[0];
        }

        viewPerson.reason_for_change = undefined;
        return viewPerson;
      };

      var savePersonInfo = function(uId, viewInfo){
        var deferred = $q.defer();

        var newUserInfo = mapViewPersonToDto(viewInfo);
        if(viewInfo.id){
          if(!newUserInfo.ssn){
            newUserInfo.ssn = undefined;
          }
          peopleRepository.ById.update({personId:viewInfo.id}, newUserInfo)
          .$promise.then(function(response){
            deferred.resolve(response);
          }, function(errorResponse){
            deferred.reject(errorResponse);
          });
        }
        else{
          peopleRepository.ByUser.save({userId:uId}, newUserInfo,
          function(response){
            deferred.resolve(response);
          }, function(errorResponse){
            deferred.reject(errorResponse);
          });
        }
        return deferred.promise;
      };

      var deletePerson = function(personId){
        peopleRepository.ById.delete({personId:personId});
      };

      return{
        getSelfPersonInfo: getSelfPersonInfo,
        savePersonInfo: savePersonInfo,
        getFamilyInfo: getFamilyInfo,
        deletePerson: deletePerson
      };

}]);
