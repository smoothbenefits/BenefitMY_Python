/* global moment */
var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
  'FsaService',
  ['FsaRepository',
   'FsaPlanRepository',
   'CompanyFsaPlanRepository',
   'CompanyGroupFsaPlanRepository',
   'UserService',
   '$q',
   function (FsaRepository,
             FsaPlanRepository,
             CompanyFsaPlanRepository,
             CompanyGroupFsaPlanRepository,
             UserService,
             $q){

    var mapFsaPlanViewModelToDomainModel = function(broker, fsaPlanView) {
      return {
        broker_user: broker,
        name: fsaPlanView.name
      };
    };

    var mapFsaDomainModelToViewModel = function(fsaPlan) {
      return {
        companyPlanId: fsaPlan.id,
        company: fsaPlan.company,
        companyGroups: fsaPlan.company_groups,
        fsaPlanName: fsaPlan.fsa_plan.name,
        created: moment(fsaPlan.created_at).format(DATE_FORMAT_STRING),
        updated: moment(fsaPlan.updated_at).format(DATE_FORMAT_STRING)
      };
    };

    var mapCreatePlanViewToCompanyGroupPlanDomainModel = function(createPlanViewModel) {
      var domainModel = [];

      _.each(createPlanViewModel.selectedCompanyGroups, function(companyGroupModel) {
        domainModel.push({
          'company_fsa_plan': createPlanViewModel.companyPlanId,
          'company_group': companyGroupModel.id
        });
      });

      return domainModel;
    };

    var createFsaPlan = function(broker, fsaPlan) {
      var deferred = $q.defer();

      // To save a new FSA plan, use broker user id in the URL since
      // there is no plan id assigned to the new plan yet.
      var fsaDomainModel = mapFsaPlanViewModelToDomainModel(broker, fsaPlan);
      FsaPlanRepository.save({id: broker}, fsaDomainModel).$promise.then(function(response){
        var planId = response.id;
        deferred.resolve(planId);
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var assignFsaPlanToCompany = function(company, fsaPlan){
      var deferred = $q.defer();

      // To assign a company to a new FSA plan, use company id in the URL
      // since there is no company plan id assigned to the new plan yet.
      var postData = {"company": company, "fsa_plan": fsaPlan};
      CompanyFsaPlanRepository.ById.save({id: company}, postData).$promise.then(function(response){
        deferred.resolve(response);
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var signUpCompanyForFsaPlan = function(broker, company, fsaPlan){
      var deferred = $q.defer();

      createFsaPlan(broker, fsaPlan).then(function(fsaPlanId){
        assignFsaPlanToCompany(company, fsaPlanId).then(function(response){
          // Now link the company plan to company group(s)
          fsaPlan.companyPlanId = response.id;
          companyGroupPlans = mapCreatePlanViewToCompanyGroupPlanDomainModel(fsaPlan);
          linkCompanyFsaPlanToCompanyGroups(fsaPlan.companyPlanId, companyGroupPlans)
          .then(function(createdCompanyGroupPlans) {
            deferred.resolve(createdCompanyGroupPlans);
          }, function(errors) {
            deferred.reject(errors);
          });
        });
      }).catch(function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var getFsaPlanForCompanyGroup = function(companyGroupId) {
      var deferred = $q.defer();
      if (!companyGroupId) {
        deferred.resolve([]);
      } else {
        CompanyGroupFsaPlanRepository.ByCompanyGroup.query({companyGroupId:companyGroupId})
        .$promise.then(function(companyGroupPlans) {
            var resultPlans = [];

            _.each(companyGroupPlans, function(companyGroupPlan) {
              var companyPlan = companyGroupPlan.company_fsa_plan;
              resultPlans.push(mapFsaDomainModelToViewModel(companyPlan));
            });

            deferred.resolve(resultPlans);
        },
        function(failedResponse) {
            deferred.reject(failedResponse);
        });
      }
      return deferred.promise;
    };

    var linkCompanyFsaPlanToCompanyGroups = function(companyPlanId, companyGroupPlanModels){
      var deferred = $q.defer();

      CompanyGroupFsaPlanRepository.ByCompanyPlan.update(
        { pk: companyPlanId },
        companyGroupPlanModels,
        function (successResponse) {
          deferred.resolve(successResponse);
        }
      );

      return deferred.promise;
    };

    var getFsaPlanForCompany = function(company){
      var deferred = $q.defer();

      CompanyFsaPlanRepository.ByCompany.query({companyId: company}).$promise.then(function(fsaPlanDomainModels){
        var fsaPlans = [];
        _.each(fsaPlanDomainModels, function(fsaPlanDomainModel) {
          var fsaPlanViewModel = mapFsaDomainModelToViewModel(fsaPlanDomainModel);
          fsaPlans.push(fsaPlanViewModel);
        });

        deferred.resolve(fsaPlans);
      }, function(error) {
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var deleteCompanyFsaPlan = function(companyPlan) {
      var deferred = $q.defer();

      CompanyFsaPlanRepository.ById.get({id: companyPlan}).$promise.then(function(response){
        var fsaPlanId =  response.fsa_plan.id;
        CompanyFsaPlanRepository.ById.delete({id: companyPlan}).$promise.then(function(response) {
          FsaPlanRepository.delete({id: fsaPlanId}).$promise.then(function(response) {
            deferred.resolve(companyPlan);
          });
        });
      })
      .catch(function(error) {
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var getFsaElectionForUser = function(user_id, company) {
      var deferred = $q.defer();

      UserService.getUserDataByUserId(user_id).then(function(userData){
        getFsaPlanForCompanyGroup(userData.companyGroupId).then(function(plans){
          if (!plans || plans.length <= 0) {
            deferred.resolve(undefined);
          }
          else {
            FsaRepository.ByUser.get({userId:user_id})
            .$promise.then(function(existingFsa){

              var userFsa = existingFsa;
              userFsa.selected = true;
              userFsa.last_update_date_time = moment(userFsa.updated_at).format(DATE_FORMAT_STRING);

              if (userFsa.company_fsa_plan) {
                userFsa.primary_amount_per_year = parseFloat(userFsa.primary_amount_per_year);
                userFsa.dependent_amount_per_year = parseFloat(userFsa.dependent_amount_per_year);
                userFsa.waived = false;
              } else {
                userFsa.waived = true;
              }

              deferred.resolve(userFsa);
            },
            function(failedResponse){
              if (failedResponse.status === 404) {
                // Didn't locate FSA record for the user, return a shell one
                var shellFsa = {
                  user:user_id,
                  primary_amount_per_year:0,
                  dependent_amount_per_year:0,
                  selected: false,
                  waived: false
                };
                deferred.resolve(shellFsa);
              }
              else{
                deferred.reject(failedResponse);
              }
            });
          }
        })
      });
      return deferred.promise;
    };

    return {
      signUpCompanyForFsaPlan: signUpCompanyForFsaPlan,

      getFsaPlanForCompany: getFsaPlanForCompany,

      getFsaPlanForCompanyGroup: getFsaPlanForCompanyGroup,

      deleteCompanyFsaPlan: deleteCompanyFsaPlan,

      getFsaElectionForUser: getFsaElectionForUser,

      saveFsaElection: function(fsaElectionToSave, updateReason, successCallBack, errorCallBack) {
        fsaElectionToSave.record_reason_note = updateReason.notes;
        fsaElectionToSave.record_reason = updateReason.selectedReason.id;

        if(!fsaElectionToSave.id) {
          // New one, POST it
          // TODO: have to give a dummy ID for now to match the URL rules,
          // can this be eliminated?
          FsaRepository.ById.save({id:fsaElectionToSave.user}, fsaElectionToSave
            , function (successResponse) {
                if (successCallBack) {
                  successCallBack(successResponse);
                }
              }
            , function(errorResponse) {
                if (errorCallBack) {
                  errorCallBack(errorResponse);
              }
          });
        }
        else {
          // Existing, PUT it
          FsaRepository.ById.update({id:fsaElectionToSave.id}, fsaElectionToSave
            , function (successResponse) {
                if (successCallBack) {
                  successCallBack(successResponse);
                }
              }
            , function(errorResponse) {
                if (errorCallBack) {
                  errorCallBack(errorResponse);
              }
          });
        }
      }
    };
  }
]);
