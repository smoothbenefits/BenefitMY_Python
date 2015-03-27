var employersController = angular.module('benefitmyApp.employers.controllers',[]);


var employerHome = employersController.controller('employerHome',
                                                  ['$scope',
                                                  '$location',
                                                  'employerRepository',
                                                  'currentUser',
                                                  'clientListRepository',
                                                  'documentRepository',
                                                  'templateRepository',
                                                  'benefitListRepository',
                                                  'countRepository',
                                                  'documentTypeService',
                                                  'BenefitElectionService',
  function employerHome($scope,
                        $location,
                        employerRepository,
                        currentUser,
                        clientListRepository,
                        documentRepository,
                        templateRepository,
                        benefitListRepository,
                        countRepository,
                        documentTypeService,
                        BenefitElectionService){

    $scope.employeeCount = 0;
    $scope.brokerCount = 0;
    $scope.benefitCount = 0;
    $scope.templateCountArray = [];

    var getTemplates = function(company){
      templateRepository.byCompany.get({companyId:company.id}).$promise.then(function(response){
        $scope.templateArray = response.templates;
      });
    }
    var getWorkerCount = function(company){
      countRepository.employeeCount.get({companyId:company.id})
        .$promise.then(function(employeeCountResponse){
          $scope.employeeCount = employeeCountResponse.employees_count;
        });
      countRepository.brokerCount.get({companyId:company.id})
        .$promise.then(function(brokerCountResponse){
          $scope.brokerCount = brokerCountResponse.brokers_count;
        });
    };

    var getBenefitCount = function(company){
      benefitListRepository.get({clientId:company.id})
        .$promise.then(function(response){
            var benefitNameArray = [];
            _.each(response.benefits, function(benefit){
              var name = _.find(benefitNameArray, function(bnf){
                return bnf.benefit_plan.name == benefit.benefit_plan.name;
              });
              if(!name){
                benefitNameArray.push(benefit);
              }
            });
            $scope.benefitCount = _.size(benefitNameArray);
        });
    };

    var getTemplateCount = function(company){
      templateRepository.byCompany.get({companyId:company.id})
        .$promise.then(function(response){
          _.each($scope.documentTypes, function(type){
            $scope.templateCountArray[type.name] = 0;
          });

          _.each(response.templates, function(template){
            $scope.templateCountArray[template.document_type.name] ++;
          });
        });
    };

    var getBenefitElectionCount = function(company){
      var selectedEmployeeArray = [];
      BenefitElectionService.getBenefitElectionsByCompany(company.id, 
        function(benefitSelectionArray){
          _.each(benefitSelectionArray, function(benefitItem){
            var existingEmployee = _.find(selectedEmployeeArray, function(employee){
              return employee.userId === selectedEmployeeArray.userId;
            });
            if(!existingEmployee){
              selectedEmployeeArray.push(benefitItem);
            }
          });
          $scope.benefitEnrollCount = _.size(selectedEmployeeArray);
        }, function(error){

        });
    };

    var userPromise = currentUser.get()
      .$promise.then(function(response)
         {
            $scope.curUser = response.user;
            return response.user;
         }
    );
    var clientPromise = userPromise.then(function(user){
      return clientListRepository.get({userId:user.id}).$promise;
    });

    clientPromise.then(function(clientListResponse){
      _.every(clientListResponse.company_roles, function(company_role)
        {
          if(company_role.company_user_type === 'admin')
          {
            $scope.company = company_role.company;
            documentTypeService.getDocumentTypes($scope.company, function(doc_types){
              $scope.documentTypes = doc_types;

              getTemplates($scope.company);
              getWorkerCount($scope.company);
              getBenefitCount($scope.company);
              getTemplateCount($scope.company);
              getBenefitElectionCount($scope.company);
            });
          }
        });
    });

    $scope.addBrokerClick = function(companyId)
    {
       $location.path('/admin/broker/add/'+ companyId);
    }

    $scope.viewBrokerClick = function(companyId)
    {
        $location.path('/admin/broker/' + companyId);
    }

    $scope.viewBenefitsClick = function(companyId)
    {
       $location.path('/admin/benefits/'+ companyId);
    }

    $scope.addEmployeeClick = function(companyId)
    {
       $location.path('/admin/employee/add/'+ companyId);
    }

    $scope.viewEmployeeClick = function(companyId)
    {
       $location.path('/admin/employee/'+ companyId);
    }

    $scope.templateClick = function(companyId, docType)
    {
       $location.search({type:docType.name}).path('/admin/generate_template/'+ companyId);
    };

    $scope.viewBenefitElection = function(companyId)
    {
      $location.path('/admin/benefit/election/'+companyId);
    }
  }
]);

var employerUser = employersController.controller('employerUser',
  ['$scope',
   '$location',
   '$stateParams',
   'employerWorkerRepository',
   'usersRepository',
   'userDocument',
   'emailRepository',
   'documentTypeService',
   'templateRepository',
  function employerUser($scope,
                        $location,
                        $stateParams,
                        employerWorkerRepository,
                        usersRepository,
                        userDocument,
                        emailRepository,
                        documentTypeService,
                        templateRepository){
      var compId = $stateParams.company_id;
      $scope.employees=[];
      $scope.addUser = {send_email:true, new_employee:true, create_docs:true};
      $scope.brokers = [];
      $scope.templateFields = [];
      $scope.docTypeArray = [];
      employerWorkerRepository.get({companyId:compId})
        .$promise.then(function(response){
            _.each(response.user_roles, function(role){
              if(role.company_user_type=='employee')
              {
                $scope.employees.push(role);
              }
              else if(role.company_user_type=='broker')
              {
                $scope.brokers.push(role);
              }
            })
        });

      templateRepository.getAllFields.query({id:compId})
        .$promise.then(function(fields){
          $scope.templateFields = fields;
        });
      documentTypeService.getDocumentTypes(compId, function(response){
        $scope.docTypeArray = response;
      });

      var gotoUserView = function(userType){
        $location.path('/admin/' + userType + '/' + compId);
      }

      var mapToAPIUser = function(viewUser, userType){
        var apiUser = {};
        apiUser.company = compId;
        apiUser.company_user_type = userType;
        apiUser.new_employee = viewUser.new_employee;
        apiUser.user = {};
        apiUser.user.email = viewUser.email;
        apiUser.user.first_name = viewUser.first_name;
        apiUser.user.last_name = viewUser.last_name;
        apiUser.create_docs = viewUser.create_docs;
        apiUser.fields = $scope.templateFields
        apiUser.send_email = viewUser.send_email;
        return apiUser;
      }

      var validateAddUser = function(addUser){
        if(addUser.first_name && addUser.last_name && addUser.email)
        {
          return true;
        }
        return false;
      }

      $scope.addLink = function(userType)
      {
        $location.path('/admin/'+ userType + '/add/'+compId);
      }

      $scope.createUser = function(userType){
        if(validateAddUser($scope.addUser))
        {
          usersRepository.save(mapToAPIUser($scope.addUser, userType),
            function(){
              if($scope.addUser.send_email){
                alert('Email sent successful.');
              }
              gotoUserView(userType);
            }, function(err){
                if(err.status === 409){
                  $scope.alreadyExists = true;
                }
        				else if (err.status === 503){
        				  alert('Failed to send email.');
        				}
                else{
                  $scope.addError = true;
                }
        				alert('Failed to add employee.');
            });
        }
        else
        {
          $scope.validation_failed = true;
        }
      }
      $scope.gotoEmployerDashboardLink = function(){
        $location.path('/admin');
      }
      $scope.gotoUserViewLink = gotoUserView;

      $scope.documentLink = function(employeeId, docType)
      {
        userDocument.query({userId:employeeId})
        .$promise.then(function(response){
          var doc = _.filter(response, function(doc){return doc.document_type.id === docType.id});
          var pathKey = 'create_letter';
          if(doc && doc.length > 0)
          {
            pathKey='view_letter';
          }
          
          $location.search({type:docType.name}).path('/admin/' + pathKey + '/' +compId +'/'+employeeId);
        });
      };

      $scope.viewEmployeeDetail = function(employee){
        $location.path('/admin/employee_detail/' + compId).search('eid', employee.user.id);
      };
  }
]);

var employerBenefits = employersController.controller('employerBenefits', ['$scope', '$location', '$stateParams', 'benefitDisplayService', 'LifeInsuranceService',
  function employerBenefits($scope, $location, $stateParams, benefitDisplayService, LifeInsuranceService){
    var compId = $stateParams.company_id;
    $scope.role = 'Admin';
    $scope.showAddBenefitButton = false;
    benefitDisplayService($stateParams.company_id, false, function(groupObj, nonMedicalArray, benefitCount){
      $scope.medicalBenefitGroup = groupObj;
      $scope.nonMedicalBenefitArray = nonMedicalArray;
      $scope.benefitCount = benefitCount;
    });

    $scope.sortBy = function(predicate){
      if ($scope.medicalPolicyPredicate === predicate){
        $scope.medicalPolicyReverse = !$scope.medicalPolicyReverse;
      }
      else{
        $scope.medicalPolicyPredicate = predicate;
      }
    };

    $scope.backtoDashboard = function(){
      $location.path('/admin');
    };

    /////////////////////////////////////////////////////////////////////
    // Life Insurance
    // TODO: split this off once we have tabs
    /////////////////////////////////////////////////////////////////////

    LifeInsuranceService.getLifeInsurancePlansForCompany($stateParams.company_id, function(response) {
          $scope.lifeInsurancePlans = response;
          _.each($scope.lifeInsurancePlans, function(companyPlan) {
            companyPlan.created_date_for_display = new Date(companyPlan.created_at).toDateString();
          });
    });
  }
]);

var employerLetterTemplate = employersController.controller('employerLetterTemplate',
  ['$scope', '$location', '$state', '$stateParams', 'templateRepository', 'documentTypeService',
  function employerLetterTemplate($scope, $location, $state, $stateParams, templateRepository, documentTypeService){
    $scope.documentType = $stateParams.type;
    $scope.addMode = $stateParams.add;
    $scope.companyId = $stateParams.company_id;
    $scope.viewTitle = 'Create ' + $scope.documentType + ' Template';
    $scope.showEditButton = false;
    $scope.existingTemplateList = [];

    $scope.isInAddMode = function(){
      return _.isEmpty($scope.existingTemplateList) || $scope.addMode === 'true';
    };

    var updateExistingTemplateList = function(){
      templateRepository.byCompany.get({companyId:$stateParams.company_id})
        .$promise.then(function(response){
          $scope.existingTemplateList = _.sortBy(
            _.filter(response.templates,
              function(template){
                return template.document_type.name === $scope.documentType;
            }),
            function(elm){return elm.id;}
          ).reverse();

          if(!_.isEmpty($scope.existingTemplateList))
          {
            $scope.viewTitle = 'Manage ' + $scope.documentType + ' Template';
          }
          else
          {
            $location.search({type:$scope.documentType, add:'true'});
          }
        });
      };

    var updateWithExistingTemplate = function(template)
    {
      if(template)
      {
        $scope.templateId = template.id;
        $scope.templateContent = template.content;
        $scope.templateName = template.name;
        $scope.showCreateButton = false;
        $scope.showEditButton = true;
      }
    };

    if(!$scope.addMode || $scope.addMode === 'false'){
      updateExistingTemplateList();
    }
    else{
      documentTypeService.getDocumentTypes($scope.companyId, function(types){
        var docType = _.findWhere(types, {name:$scope.documentType});
        if(docType){
          $scope.templateContent = docType.default_content;
        }
      });
    }

    $scope.modifyExistingTemplate = function(template){
      updateWithExistingTemplate(template);
    };
    $scope.saveTemplateChanges = function(){
      var template = {};
      template.name = $scope.templateName;
      template.content = $scope.templateContent;
      template.document_type = $scope.documentType;
      var updateObject = {company: $scope.companyId, template: template};
      templateRepository.update.update({id: $scope.templateId}, updateObject, function(response){
        updateWithExistingTemplate(response.template);
        $location.search({add:'false', type: $scope.documentType});
        updateExistingTemplateList();
      }, function(response){
        $scope.templateCreateFailed = true;
      })
    }
    $scope.addOfferTemplate = function(){
      $location.search({type:$scope.documentType, add:'true'});
    };
    $scope.viewDashboard = function(){
      $location.path('/admin');
    };
    $scope.createTemplate = function(){
      if($scope.templateName && $scope.templateContent)
      {
        var newTemplate = {};
        newTemplate.document_type = $scope.documentType;
        newTemplate.name = $scope.templateName;
        newTemplate.content = $scope.templateContent;
        var postObj = {company:$scope.companyId, template:newTemplate};
        templateRepository.create.save(postObj, function(response){
          updateWithExistingTemplate(response.template);
          $scope.justCreated = true;
          $location.search({add:'false', type:$scope.documentType})
        }, function(response){
          $scope.templateCreateFailed = true;
        });
      }
    }
  }
]);

var employerCreateLetter = employersController.controller('employerCreateLetter',
                                                          ['$scope',
                                                          '$location',
                                                          '$stateParams',
                                                          'documentRepository',
                                                          'templateRepository',
  function employerCreateLetter($scope,
                                $location,
                                $stateParams,
                                documentRepository,
                                templateRepository){
    $scope.companyId = $stateParams.company_id;
    var employeeId = $stateParams.employee_id;
    $scope.newDoc = {};


    $scope.documentType = $stateParams.type;

    templateRepository.byCompany.get({companyId:$scope.companyId})
      .$promise.then(function(response){
        $scope.templateArray = [];

        _.each(response.templates, function(template){
          if (template.document_type.name === $scope.documentType){
            $scope.templateArray.push(template);
          }
        });

        _.sortBy($scope.templateArray, function(template){
          return template.name;
        });
      });

    $scope.getTemplateFields = function(sTemplate){
      if(sTemplate)
      {
        var fieldList = _.uniq(sTemplate.fields, false, function(field){
          return field.name;
        });
        return fieldList;
      }
      else
      {
        return [];
      }
    };

    $scope.doCreateLetter = function()
    {
      var curTemplate = $scope.selectedTemplate;
      $scope.newDoc.fields = curTemplate.fields;
      _.each($scope.newDoc.fields, function(field){
        if(!field.value){
          var foundValue = _.findWhere($scope.newDoc.fields, {name:field.name});
          if(foundValue){
            field.value = foundValue.value;
          }
        }
      });
      $scope.newDoc.document_type = $scope.documentType;
      var postObj={company:$scope.companyId, user:employeeId, template:curTemplate.id, signature:'', document:$scope.newDoc};
      documentRepository.create.save(postObj, function(response){
        $location.search({type:$scope.documentType}).path('/admin/view_letter/' + $scope.companyId + '/' + employeeId);
      }, function(errResponse){
        $scope.createFailed = true;
      });
    }
  }]);

var employerViewLetter = employersController.controller('employerViewLetter',
                                                          ['$scope',
                                                          '$location',
                                                          '$state',
                                                          '$stateParams',
                                                          'documentRepository',
  function employerViewLetter($scope,
                              $location,
                              $state,
                              $stateParams,
                              documentRepository){
    $scope.companyId = $stateParams.company_id;
    var employeeId = $stateParams.employee_id;
    $scope.documentType = $stateParams.type;
    $scope.documentList = [];
    $scope.activeDocument = {};
    $scope.signaturePresent = false;
    $scope.signatureCreatedDate = moment().format('MMM Do YYYY');

    documentRepository.byUser.query({userId:employeeId}).$promise.then(function(response){
      var unsortedDocumentList = _.filter(response, function(doc){
          return doc.document_type.name === $scope.documentType
        });
        $scope.documentList = _.sortBy(unsortedDocumentList, function(elm){return elm.id;}).reverse();
      });

    $scope.deleteExistingLetter = function(doc){
      documentRepository.getById.delete({id: doc.id}).$promise
        .then(function(response){
          alert("Deleted document " + doc.name);
          $state.reload();
        });
    };

    $scope.updateExistingLetter = function(){
      var doc = $scope.activeDocument;
      var request = {
        "company": doc.company.id,
        "user": doc.user.id,
        "signature": doc.signature,
        "document": {
          "document_type": doc.document_type.name,
          "name": doc.name,
          "content": doc.content
        }
      };

      documentRepository.updateById.update({id:doc.id}, request).$promise
        .then(function(response){
          alert("Successful update " + response.name);
        });
    }

    $scope.anyActiveDocument = function(){
      return typeof $scope.activeDocument.name !== 'undefined';
    }

    $scope.viewExistingLetter = function(doc){
      $scope.activeDocument = doc;
      if (doc.signature && doc.signature.signature){
        $scope.signatureImage = doc.signature.signature;
        $scope.signaturePresent = true;
        $scope.signatureCreatedDate = moment(doc.signature.created_at).format('MMM Do YYYY');
      }
    };

    $scope.createNewLetter = function(){
      $location.search({type:$scope.documentType}).path('/admin/create_letter/'+ $scope.companyId +'/' + employeeId);
    };

    $scope.viewEmployeesLink = function(){
      $location.path('/admin/employee/' + $scope.companyId);
    };
  }]);

var employerViewEmployeeDetail = employersController.controller('employerViewEmployeeDetail', [
  '$scope', 
  '$location', 
  '$stateParams', 
  'profileSettings', 
  'employeeFamily',
  'employmentAuthRepository',
  'employeeTaxRepository',
  function($scope, 
           $location, 
           $stateParams, 
           profileSettings,
           employeeFamily,
           employmentAuthRepository,
           employeeTaxRepository){

    var compId = $stateParams.company_id;
    var employeeId = $stateParams.eid;
    $scope.employee = {};
    $scope.showEditButton = false;

    employeeFamily.get({userId:employeeId})
      .$promise.then(function(employeeDetail){
        $scope.employee.first_name = employeeDetail.first_name;
        $scope.employee.last_name = employeeDetail.last_name;
        $scope.employee.email = employeeDetail.email;
        var selfInfo = _.findWhere(employeeDetail.family, {relationship:'self'});
        if(selfInfo){
          $scope.employee.birth_date = selfInfo.birth_date;
          $scope.employee.phones = selfInfo.phones;
          $scope.employee.addresses = selfInfo.addresses;
          $scope.employee.emergency_contact = selfInfo.emergency_contact;
          $scope.employee.gender = (selfInfo.gender === 'F' ? 'Female' : 'Male');
        }
      });

    employmentAuthRepository.get({userId: employeeId}).$promise.then(function(response){
      $scope.employee.i9 = convertResponse(response, 'i9');
    });

    employeeTaxRepository.get({userId: employeeId}).$promise.then(function(response){
      $scope.employee.w4 = convertResponse(response, 'w4');
    });

    var convertResponse = function(res, type){
      var pairs = _.pairs(res);
      var validFields = _.findWhere(profileSettings, {name: type}).valid_fields;
      var output = [];
      _.each(pairs, function(pair){
        var key = pair[0];
        var inSetting = _.findWhere(validFields, {name: key});
        if (inSetting){
          if (inSetting.datamap){
            var value = pair[1];
            var mappedValue = _.find(inSetting.datamap, function(map){
              return map[0] === value.toString();
            });
            if (!mappedValue){
              inSetting.value = 'UNKNOWN';
            } else{
              inSetting.value = mappedValue[1];
            }
          } else{
            inSetting.value = pair[1];
          }
          output.push(inSetting);
        }
      });
      return _.filter(output, function(item){return item.value != null;});
    }

    $scope.editEmployeeDetail = function(){

    };

    $scope.backToDashboard = function(){
      $location.path('/admin');
    };

    $scope.backToList = function(){
      $location.path('/admin/employee/' + compId);
    }
}]);

var employerBenefitsSelected = employersController.controller('employerBenefitsSelected', [
  '$scope', 
  '$location', 
  '$stateParams', 
  'companyRepository',
  'employeeBenefitElectionFactory',
  'FsaService',
  'LifeInsuranceService',
  'CompanyEmployeeSummaryService',
  function($scope, 
           $location, 
           $stateParams, 
           companyRepository,
           employeeBenefitElectionFactory,
           FsaService,
           LifeInsuranceService,
           CompanyEmployeeSummaryService){
    var company_id = $stateParams.company_id;
    $scope.employeeList = [];

    companyRepository.get({clientId: company_id}).$promise.then(function(response){
        $scope.companyName = response.name;
      });

      var promise = employeeBenefitElectionFactory(company_id);
      promise.then(function(employeeList){

        // TODO: Could/should FSA information be considered one kind of benefit election
        //       and this logic of getting FSA data for an employee be moved into the
        //       employeeBenefitElectionFactory? 
        _.each(employeeList, function(employee) {
          FsaService.getFsaElectionForUser(employee.user.id, function(response) {
            employee.fsaElection = response;
          });
        });

        // TODO: like the above comment for FSA, Life Insurance, or more generally speaking,
        //       all new benefits going forward, we should consider creating as separate 
        //       entity and maybe avoid trying to artificially bundle them together. 
        //       Also, once we have tabs working, we should split them into proper flows.
        _.each(employeeList, function(employee) {
          LifeInsuranceService.getInsurancePlanEnrollmentsForAllFamilyMembersByUser(employee.user.id, function(response) {
            employee.familyInsurancePlan = response;
          });
          
          LifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(employee.user.id, function(response){
            employee.basicLifeInsurancePlan = response;
          });
        });

        $scope.clientCount = _.size(employeeList);
        $scope.employeeList = employeeList;
      }, function(errorResponse){
        alert(errorResponse.content);
      });
    
    $scope.isLifeInsuranceWaived = function(employeeFamilyLifeInsurancePlan) {
        return (!employeeFamilyLifeInsurancePlan) 
          || (!employeeFamilyLifeInsurancePlan.mainPlan)
          || (!employeeFamilyLifeInsurancePlan.mainPlan.id);
      };

    $scope.viewDetails = function(employeeId){
        $location.path('/admin/employee_detail/' + company_id).search('eid', employeeId);
    };

    $scope.back = function(){
      $location.path('/admin');
    };

    $scope.exportCompanyEmployeeSummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryExcelUrl(company_id);
    $scope.exportCompanyEmployeeLifeBeneficiarySummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl(company_id);
}]);

