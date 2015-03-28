var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('personInfoService',
  ['employeeFamily',
    function(employeeFamily){
      return{
        getPersonInfo: function(uId, retrievedCallBack){
          employeeFamily.get({userId:uId})
            .$promise.then(function(userPerson){
              var selfPerson = _.findWhere(userPerson.family, {relationship:'self'});
              if(selfPerson){
                if(selfPerson.phones && selfPerson.phones.length > 0){
                  selfPerson.phone = selfPerson.phones[0];
                }
                if(selfPerson.addresses && selfPerson.addresses.length > 0){
                  selfPerson.address = selfPerson.addresses[0];
                }
                if(selfPerson.emergency_contact && selfPerson.emergency_contact.length > 0){
                  selfPerson.emergency = selfPerson.emergency_contact[0];
                }
                if(retrievedCallBack){
                  retrievedCallBack(selfPerson);
                }
              }
              else if(retrievedCallBack){
                retrievedCallBack(null);
              }
            });
        },

        savePersonInfo: function(uId, viewInfo, success, error){
          var mapUserPerson = function(viewPerson){
            viewPerson.birth_date = moment(viewPerson.birth_date).format('YYYY-MM-DD');
            var apiUserPerson = viewPerson;
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
              apiUserPerson.emergency_contact.push(viewPerson.emergency);
            }
            return apiUserPerson;
          };

          var newUserInfo = mapUserPerson(viewInfo);
          employeeFamily.save({userId:uId}, newUserInfo,
          function(response){
            if(success){
              success(response);
            }
          }, function(errorResponse){
            if(error){
              error(errorResponse);
            }
          });
        }
      };

}]);
