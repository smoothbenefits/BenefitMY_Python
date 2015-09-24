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
  'CompanyBenefitEnrollmentSummaryService',
  function ($scope,
            $location,
            employerRepository,
            currentUser,
            clientListRepository,
            documentRepository,
            templateRepository,
            benefitListRepository,
            countRepository,
            documentTypeService,
            CompanyBenefitEnrollmentSummaryService){

    $scope.employeeCount = 0;
    $scope.brokerCount = 0;
    $scope.benefitCount = 0;
    $scope.benefitEnrollCount = 0;
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
      CompanyBenefitEnrollmentSummaryService.getEnrollmentSummary(company.id)
      .then(function(response){
        $scope.benefitEnrollCount = response.completed.length;
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
            documentTypeService.getDocumentTypes($scope.company).then(function(doc_types){
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
   '$state',
   '$stateParams',
   '$location',
   'employerWorkerRepository',
   'usersRepository',
   'emailRepository',
   'documentTypeService',
   'templateRepository',
   'DocumentService',
   'CompensationService',
   'EmployerEmployeeManagementService',
  function employerUser($scope,
                        $state,
                        $stateParams,
                        $location,
                        employerWorkerRepository,
                        usersRepository,
                        emailRepository,
                        documentTypeService,
                        templateRepository,
                        DocumentService,
                        CompensationService,
                        EmployerEmployeeManagementService){
      var compId = $stateParams.company_id;
      $scope.employees=[];
      $scope.brokers = [];
      $scope.templateFields = [];
      $scope.docTypeArray = [];
      $scope.employment_types = EmployerEmployeeManagementService.EmploymentTypes;
      $scope.addUser = {
        send_email:true,
        new_employee:true,
        create_docs:true,
        employment_type: _.findWhere($scope.employment_types, function(type) {
          return EmployerEmployeeManagementService.IsFullTimeEmploymentType(type);
        })
      };

      $scope.updateSalaryType = function(employee) {
        if (EmployerEmployeeManagementService.IsFullTimeEmploymentType(employee.employment_type)) {
          $scope.isHourlyRate = false;
        } else {
          $scope.isHourlyRate = true;
        }
      };

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
            });

            // Populate document data for employees
            _.each($scope.employees, function(employee) {
                DocumentService.getDocumentToTypeMappingForCompanyUser(employee.user.id, compId)
                .then(function(docTypeMapModel) {
                    employee.documentCollection = docTypeMapModel;
                });
            });
        });

      templateRepository.getAllFields.query({id:compId})
        .$promise.then(function(fields){
          $scope.templateFields = fields;
        });
      documentTypeService.getDocumentTypes(compId).then(function(response){
        $scope.docTypeArray = response;
      });

      var gotoUserView = function(userType){
        $location.path('/admin/' + userType + '/' + compId);
      }

      $scope.validatePassword = function(password, passwordConfirm) {
        if (!password) {
          $scope.passwordValidationError = "Password is required for the new employee account.";
          return false;
        } else if (passwordConfirm !== password) {
          $scope.passwordValidationError = "The two passwords do not match.";
          return false;
        } else if (password.length < 8) {
          $scope.passwordValidationError = "Password should be at least 8 character long.";
          return false;
        } else {
          return true;
        }
      };

      $scope.addLink = function(userType)
      {
        $location.path('/admin/'+ userType + '/add/'+compId)
      }

      $scope.createUser = function(userType) {
          EmployerEmployeeManagementService.AddNewEmployee(compId, $scope.addUser, $scope.templateFields)
          .then(function(response) {
            gotoUserView(userType);
          }, function(error) {
            alert('Failed to add a new employee.');
          });
      };

      $scope.gotoEmployerDashboardLink = function(){
        $state.go('/admin');
      }
      $scope.gotoUserViewLink = gotoUserView;

      $scope.documentLink = function(employeeId, docEntry)
      {
        var pathKey = 'create_letter';
        if(docEntry.hasDocument())
        {
            pathKey='view_letter';
        }

        $location.path('/admin/' + pathKey + '/' +compId +'/'+employeeId).search({'type': docEntry.docType.name});
      };

      $scope.viewEmployeeDetail = function(employee){
        $location.path('/admin/employee_detail/' + compId).search({'eid': employee.user.id});
      };

      $scope.uploadLink = function(employeeId){
        $state.go('admin_employee_uploads', {company_id:compId, employee_id:employeeId});
      }
  }
]);

var batchEmployeeAdditionController = employersController.controller('batchEmployeeAdditionController',
    ['$scope',
     '$state',
     '$stateParams',
     '$modal',
     'employerWorkerRepository',
     'usersRepository',
     'emailRepository',
     'CompensationService',
     'EmployerEmployeeManagementService',
     'BatchAccountCreationService',
    function($scope,
             $state,
             $stateParams,
             $modal,
             employerWorkerRepository,
             usersRepository,
             emailRepository,
             CompensationService,
             EmployerEmployeeManagementService,
             BatchAccountCreationService){

        var compId = $stateParams.company_id;

        // Share scope between child states
        $scope.batchAddUserModel = $scope.batchAddUserModel
            || { sendEmail:true, rawData:''};

        var wrapBatchAccountOperationResponse = function(response) {
            var result = response;
            result.hasIssues = function() {
                return this.issues && this.issues.length > 0;
            };
            result.hasRecords = function() {
                return this.output_data && this.output_data.length > 0;
            };
            result.getRecordsHaveIssues = function() {
                var result = [];

                if (!this.hasRecords()){
                    return result;
                }

                for (var i = 0; i < this.output_data.length; i++) {
                    var record = this.output_data[i];
                    if (record.issues && record.issues.length > 0) {
                        result.push(record);
                    }
                }

                return result;
            };
            result.hasFailRecords = function() {
                return this.getRecordsHaveIssues().length > 0;
            };
            result.allRecordsSuccessful = function() {
                return this.hasRecords() && !this.hasFailRecords();
            };

            return result;
        }

        $scope.openFormatRequirementsModal = function() {
            var modalInstance = $modal.open({
              templateUrl: '/static/partials/batch_employee_addition/modal_format_requirements.html',
              controller: function($scope) {
                $scope.close = function(){
                    modalInstance.dismiss();
                };
              },
              size: 'lg'
            });
        };

        $scope.openSpinnerModal = function() {
            if (!$scope.spinnerModalInstance) {
                $scope.spinnerModalInstance = $modal.open({
                  templateUrl: '/static/partials/common/modal_progress_bar_spinner.html',
                  controller: function($scope) {},
                  backdrop: 'static',
                  size: 'md'
                });
            }
        };

        $scope.closeSpinnerModal = function() {
            if ($scope.spinnerModalInstance) {
                $scope.spinnerModalInstance.dismiss();
                $scope.spinnerModalInstance = null;
            }
        };

        $scope.parseData = function() {
            $scope.openSpinnerModal();
            BatchAccountCreationService.parseRawData(compId, $scope.batchAddUserModel).then(function(response) {
                $scope.closeSpinnerModal();

                // Actually parse data here, and get result
                $scope.batchAddUserModel.parseDataResult = wrapBatchAccountOperationResponse(response);

                $state.go('batch_add_employees.parse_result');
            },
            function(error) {
                $scope.closeSpinnerModal();
                alert('Failed to parse the given data!');
            });
        };

        $scope.save = function() {
            $scope.openSpinnerModal();
            BatchAccountCreationService.saveAllAccounts(compId, $scope.batchAddUserModel).then(function(response) {
                $scope.closeSpinnerModal();
                // Actually parse data here, and get result
                $scope.batchAddUserModel.saveResult = wrapBatchAccountOperationResponse(response);

                $state.go('batch_add_employees.save_result');
            },
            function(error) {
                $scope.closeSpinnerModal();
                alert('Failed to save data!');
            });
        };

        $scope.backtoDashboard = function(){
          $state.go('/admin');
        };

        $scope.formatDateForDisplay = function(date) {
            return moment(date).format(DATE_FORMAT_STRING);
        };
    }
]);

var employerBenefits = employersController.controller('employerBenefits',
  ['$scope',
  '$location',
  '$stateParams',
  '$modal',
  'benefitDisplayService',
  'BasicLifeInsuranceService',
  'SupplementalLifeInsuranceService',
  'StdService',
  'LtdService',
  'FsaService',
  'HraService',
  'companyRepository',
  function ($scope,
            $location,
            $stateParams,
            $modal,
            benefitDisplayService,
            BasicLifeInsuranceService,
            SupplementalLifeInsuranceService,
            StdService,
            LtdService,
            FsaService,
            HraService,
            companyRepository){

    var compId = $stateParams.company_id;
    $scope.role = 'Admin';
    $scope.showAddBenefitButton = false;

    companyRepository.get({clientId:$stateParams.company_id})
    .$promise.then(function(company){
      $scope.company = company;
      benefitDisplayService.getHealthBenefitsForDisplay(company, false)
      .then(function(healthBenefitToDisplay){
        $scope.medicalBenefitGroup = healthBenefitToDisplay.medicalBenefitGroup;
        $scope.nonMedicalBenefitArray = healthBenefitToDisplay.nonMedicalBenefitArray;
        $scope.benefitCount = healthBenefitToDisplay.benefitCount;
      });
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

    BasicLifeInsuranceService.getLifeInsurancePlansForCompany($stateParams.company_id).then(function(response) {
      $scope.lifeInsurancePlans = response;
    });

    SupplementalLifeInsuranceService.getPlansForCompany($stateParams.company_id).then(function(response) {
      $scope.supplementalLifeInsurancePlans = response;
    });

    StdService.getStdPlansForCompany($stateParams.company_id).then(function(plans) {
        $scope.stdPlans = plans;
    });

    LtdService.getLtdPlansForCompany($stateParams.company_id).then(function(plans) {
        $scope.ltdPlans = plans;
    });

    FsaService.getFsaPlanForCompany($stateParams.company_id).then(function(plans) {
      $scope.fsaPlans = plans;
    });

    HraService.getPlansForCompany($stateParams.company_id).then(function(response) {
      $scope.hraPlans = response;
    });

    $scope.openSupplementalLifePlanDetailsModal = function(supplementalLifePlan) {
        $scope.detailsModalCompanyPlanToDisplay = supplementalLifePlan;
        $modal.open({
          templateUrl: '/static/partials/benefit_selection/modal_supplemental_life_plan_details.html',
          controller: 'planDetailsModalController',
          size: 'lg',
          scope: $scope
        });
    };

    $scope.openStdDetailsModal = function(stdPlan){
        $scope.stdPlanRatesToDisplay = stdPlan;
        $modal.open({
          templateUrl: '/static/partials/benefit_addition/modal_std_age_based_rates.html',
          controller: 'planDetailsModalController',
          size: 'lg',
          scope: $scope
        });
    };

    $scope.openLtdDetailsModal = function(ltdPlan){
        $scope.ltdPlanRatesToDisplay = ltdPlan;
        $modal.open({
          templateUrl: '/static/partials/benefit_addition/modal_ltd_age_based_rates.html',
          controller: 'planDetailsModalController',
          size: 'lg',
          scope: $scope
        });
    };
  }
]);

var planDetailsModalController = brokersControllers.controller('planDetailsModalController',
  ['$scope',
   '$modal',
   '$modalInstance',
   function selectedBenefitsController(
    $scope,
    $modal,
    $modalInstance){
        $scope.closePlanDetailsModal = function() {
          $modalInstance.dismiss();
        };
}]);

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
      documentTypeService.getDocumentTypes($scope.companyId).then(function(types){
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
          return field.key;
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
          var foundValue = _.findWhere($scope.newDoc.fields, {key:field.key});
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
    $scope.signatureCreatedDate = moment().format(DATE_FORMAT_STRING);

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
        $scope.signatureCreatedDate = moment(doc.signature.created_at).format(DATE_FORMAT_STRING);
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
  '$modal',
  '$controller',
  'profileSettings',
  'peopleRepository',
  'employmentAuthRepository',
  'employeeTaxRepository',
  'EmployeeProfileService',
  'EmploymentStatuses',
  'CompensationService',
  function($scope,
           $location,
           $stateParams,
           $modal,
           $controller,
           profileSettings,
           peopleRepository,
           employmentAuthRepository,
           employeeTaxRepository,
           EmployeeProfileService,
           EmploymentStatuses,
           CompensationService){

    // Inherit base modal controller for dialog window
    $controller('modalMessageControllerBase', {$scope: $scope});

    var compId = $stateParams.company_id;
    var employeeId = $stateParams.eid;
    $scope.isBroker = false;
    $scope.employee = {};
    $scope.showEditButton = false;
    $scope.terminateEmployeeButton = false;

    peopleRepository.ByUser.get({userId:employeeId})
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

          // Get the employee profile info that bound to this person
          EmployeeProfileService.getEmployeeProfileForPersonCompany(selfInfo.id, compId)
          .then(function(profile) {
            $scope.employee.employeeProfile = profile;
            $scope.$watch('employee.employeeProfile.employmentStatus',
              function(employmentStatus){
                $scope.terminateEmployeeButton = employmentStatus && employmentStatus !== EmploymentStatuses.terminated;
                $scope.terminateMessage = undefined;
                if(employmentStatus && employmentStatus === EmploymentStatuses.terminated){
                  $scope.terminateMessage = "Employment terminated";
                };
            });
            return profile.personId;
          }).then(function(personId) {
            CompensationService.getCompensationByPersonSortedByDate(personId, true)
            .then(function(response) {
              // Return sorted compensation records for the person
              $scope.compensations = response;
            });
          });
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

    var saveToTerminateEmployment = function(employeeProfileToSave){

      EmployeeProfileService.saveEmployeeProfile(employeeProfileToSave)
      .then(function(response){
        $scope.employee.employeeProfile = employeeProfileToSave;
      }, function(error){
        $scope.terminateMessage = "Error occurred during saving operation. Please verify " +
          "all the information enterred are valid. Message: " + error;
      });
    };

    $scope.terminateEmployment = function(){
      var modalInstance = $modal.open({
          templateUrl: '/static/partials/employee_record/terminate_confirmation.html',
          controller: 'confirmTerminateEmployeeModalController',
          size: 'md',
          backdrop: 'static',
          resolve: {
              employeeProfile: function () {
                  return angular.copy($scope.employee.employeeProfile);
              }
          }
      });
      modalInstance.result.then(function(employeeProfileConfirmed){
        saveToTerminateEmployment(employeeProfileConfirmed);
      });
    };

    $scope.editEmployeeProfile = function(){
        if (!$scope.employee.employeeProfile){
            return;
        }
        var modelCopy = angular.copy($scope.employee.employeeProfile);

        var modalInstance = $modal.open({
            templateUrl: '/static/partials/employee_record/modal_edit_employee_profile.html',
            controller: 'editEmployeeProfileModalController',
            size: 'lg',
            backdrop: 'static',
            resolve: {
                employeeProfileModel: function () {
                    return modelCopy;
                }
            }
        });

        modalInstance.result.then(function(updatedEmployeeProfile){
            var successMessage = "The employee profile has been saved successfully."
            $scope.showMessageWithOkayOnly('Success', successMessage);

            angular.copy(updatedEmployeeProfile, $scope.employee.employeeProfile)
        });
    };

    $scope.isFullTime = function(employee) {
      if (!employee.employeeProfile){
        return false;
      }
      return EmployeeProfileService.isFullTimeEmploymentType(employee.employeeProfile);
    };

    $scope.addCompensation = function() {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/employee_record/modal_edit_employee_compensation.html',
        controller: 'addEmployeeCompensationModalController',
        backdrop: 'static',
        resolve: {
          employeeProfile: function() {
            return angular.copy($scope.employee.employeeProfile);
          },
          currentSalary: function() {
            var currentCompensation = CompensationService.getCurrentCompensationFromViewList($scope.compensations);
            if (currentCompensation) {
              return currentCompensation.salary;
            } else {
              return null;
            }
          }
        }
      });

      modalInstance.result.then(function(newEmployeeCompensation) {
        var successMessage = "A new compensation record has been saved successfully.";
        $scope.showMessageWithOkayOnly('Success', successMessage);
        CompensationService.getCompensationByPersonSortedByDate($scope.employee.employeeProfile.personId, true)
        .then(function(response) {
          $scope.compensations = response;
        });
      });
    };

    $scope.backToDashboard = function(){
      $location.path('/admin');
    };

    $scope.backToList = function(){
      $location.path('/admin/employee/' + compId);
    }
}]);

var editEmployeeProfileModalController = employersController.controller('editEmployeeProfileModalController',
  ['$scope',
   '$modal',
   '$modalInstance',
   'EmployeeProfileService',
   'employeeProfileModel',
   'EmploymentStatuses',
    function($scope,
             $modal,
             $modalInstance,
             EmployeeProfileService,
             employeeProfileModel,
             EmploymentStatuses){

      $scope.errorMessage = null;
      $scope.employeeProfileModel = employeeProfileModel;
      $scope.employmentTypes = ['FullTime', 'PartTime', 'Contractor', 'Intern'];
      $scope.employmentStatusList = _.reject(
        _.values(EmploymentStatuses),
          function(status){
            return status === EmploymentStatuses.terminated;
          }
        );

      $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
      };

      $scope.save = function(employeeProfileToSave) {
        EmployeeProfileService.saveEmployeeProfile(employeeProfileToSave)
        .then(function(response){
          $modalInstance.close(response);
        }, function(error){
          $scope.errorMessage = "Error occurred during saving operation. Please verify " +
            "all the information enterred are valid. Message: " + error;
        });
      };

      $scope.updateEndDate = function(){
        $scope.employeeProfileModel.endDate = null;
      };
    }
  ]);

var addEmployeeCompensationModalController = employersController.controller(
  'addEmployeeCompensationModalController',
  ['$scope',
   '$modal',
   '$modalInstance',
   'CompensationService',
   'EmployeeProfileService',
   'employeeProfile',
   'currentSalary',
    function($scope,
             $modal,
             $modalInstance,
             CompensationService,
             EmployeeProfileService,
             employeeProfile,
             currentSalary){

      $scope.errorMessage = null;
      $scope.currentSalary = Number(currentSalary);
      $scope.isFullTime = EmployeeProfileService.isFullTimeEmploymentType(employeeProfile);
      var personId = employeeProfile.personId;
      var companyId = employeeProfile.companyId;


      $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
      };

      $scope.save = function(compensation) {
        if (!currentSalary && compensation.salary) {
          compensation.increasePercentage = null;
        }
        if(!compensation.salary && !compensation.hourly_rate && !compensation.increasePercentage){
          $scope.errorMessage = "You cannot save compensation record where both salary and increase percentage are empty!"
          return;
        }

        CompensationService.addCompensationByPerson(compensation, personId, companyId)
        .then(function(response){
          var newCompensation = CompensationService.mapToViewModel(response);
          $modalInstance.close(newCompensation);
        }, function(error){
          $scope.errorMessage = "Error occurred during saving operation. Please verify " +
            "all the information enterred are valid. Message: " + error;
        });
      };
    }
  ]);

var confirmTerminateEmployeeModalController = employersController.controller('confirmTerminateEmployeeModalController',[
  '$scope',
  '$modalInstance',
  'employeeProfile',
  'EmploymentStatuses',
  function($scope,
           $modalInstance,
           employeeProfile,
           EmploymentStatuses){

    $scope.employeeProfile = employeeProfile;
    $scope.endDateRequired = function(){
      return _.isNull($scope.employeeProfile.endDate) || _.isUndefined($scope.employeeProfile.endDate);
    };

    $scope.confirm = function(){
      $scope.employeeProfile.employmentStatus = EmploymentStatuses.terminated;
      $modalInstance.close($scope.employeeProfile);
    };

    $scope.cancel = function(){
      $modalInstance.dismiss();
    };
  }

])

var employerBenefitsSelected = employersController.controller('employerBenefitsSelected', [
  '$scope',
  '$location',
  '$state',
  '$stateParams',
  '$modal',
  'companyRepository',
  'CompanyEmployeeSummaryService',
  'CompanyBenefitEnrollmentSummaryService',
  'Company1095CService',
  function($scope,
           $location,
           $state,
           $stateParams,
           $modal,
           companyRepository,
           CompanyEmployeeSummaryService,
           CompanyBenefitEnrollmentSummaryService,
           Company1095CService){
    var company_id = $stateParams.company_id;
    $scope.employees = [];

    CompanyBenefitEnrollmentSummaryService.getEnrollmentSummary(company_id)
    .then(function(response){
      $scope.summary = response;
    });

    Company1095CService.get1095CByCompany(company_id).then(function(dataArray){
      $scope.sorted1095CData = dataArray;
    });

    $scope.viewNotStarted = function(){
      $scope.employees = $scope.summary.notStarted;
    };
    $scope.viewNotComplete = function(){
      $scope.employees = $scope.summary.notComplete;
    };
    $scope.viewCompleted = function(){
      $scope.employees = $scope.summary.completed;
    };

    $scope.viewDetails = function(employeeId){
        $state.go('admin_employee_benefit_selection', {company_id:company_id, employee_id:employeeId});
    };

    $scope.back = function(){
      $location.path('/admin');
    };

    $scope.backToDashboard = function(){
      $location.path('/admin');
    };

    $scope.exportCompanyEmployeeSummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryExcelUrl(company_id);
    $scope.exportCompanyEmployeeDirectDepositUrl = CompanyEmployeeSummaryService.getCompanyEmployeeDirectDepositExcelUrl(company_id);
    $scope.exportCompanyEmployeeLifeBeneficiarySummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl(company_id);
    $scope.exportCompanyBenefitsBillingSummaryUrl = CompanyEmployeeSummaryService.getCompanyBenefitsBillingReportExcelUrl(company_id);
    $scope.exportCompanyEmployeeSummaryPdfUrl = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryPdfUrl(company_id);
    $scope.companyHphcExcelUrl = CompanyEmployeeSummaryService.getCompanyHphcExcelUrl(company_id);

    $scope.getEmployee1095cUrl = function(employeeUserId) {
        return CompanyEmployeeSummaryService.getEmployee1095cUrl(employeeUserId);
    };

    $scope.valid1095C = function(){
      return Company1095CService.validate($scope.sorted1095CData);
    };

    $scope.open1095CModal = function(downloadUserId){
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/modal_company_1095_c.html',
        controller: 'company1095CModalController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
            CompanyId: function(){return company_id},
            Existing1095CData: function () {
                return angular.copy($scope.sorted1095CData);
            }
        }
      });
      modalInstance.result.then(function(saved1095CData){
        $scope.sorted1095CData = saved1095CData;
        if(downloadUserId && Company1095CService.validate($scope.sorted1095CData)){
          window.location = CompanyEmployeeSummaryService.getEmployee1095cUrl(downloadUserId);
        }
      });

    };
}]);

var employerViewUploads = employersController.controller('employerViewUploads', [
  '$scope',
  '$stateParams',
  'UploadService',
  'users',
  function($scope,
           $stateParams,
           UploadService,
           users){
    $scope.compId = $stateParams.company_id;
    $scope.uploads = [];
    UploadService.getEmployeeUploads($scope.compId, $stateParams.employee_id)
    .then(function(resp){
      $scope.uploads = resp;
    }, function(err){
      alert(err);
    });
    users.get({userId:$stateParams.employee_id})
    .$promise.then(function(resp){
      $scope.employee = resp.user;
    });
  }
]);

var employerEmployeeSelected = employersController.controller('employerEmployeeSelected', [
  '$scope',
  '$location',
  '$state',
  '$stateParams',
  'companyRepository',
  'peopleRepository',
  'employeeBenefits',
  'FsaService',
  'BasicLifeInsuranceService',
  'SupplementalLifeInsuranceService',
  'CompanyEmployeeSummaryService',
  'StdService',
  'LtdService',
  'HraService',
  function($scope,
           $location,
           $state,
           $stateParams,
           companyRepository,
           peopleRepository,
           employeeBenefits,
           FsaService,
           BasicLifeInsuranceService,
           SupplementalLifeInsuranceService,
           CompanyEmployeeSummaryService,
           StdService,
           LtdService,
           HraService){
    var company_id = $stateParams.company_id;
    $scope.employee = {id:$stateParams.employee_id};

    $scope.backToDashboard = function(){
      $location.path('/admin');
    };

    $scope.back = function(){
      $state.go('admin_benefit_elections', {company_id:company_id});
    };

    companyRepository.get({clientId: company_id})
    .$promise.then(function(response){
        $scope.company = response;

        peopleRepository.ByUser.get({userId:$scope.employee.id})
        .$promise.then(function(employeeDetail){
          $scope.employee.firstName = employeeDetail.first_name;
          $scope.employee.lastName = employeeDetail.last_name;
          $scope.employee.email = employeeDetail.email;
        });

        employeeBenefits.enroll().get({userId:$scope.employee.id, companyId:company_id})
          .$promise.then(function(response){
             $scope.employee.benefits = response.benefits;
             _.each($scope.employee.benefits, function(benefit){
              benefit.updateFormatted = moment(benefit.update_at).format(DATE_FORMAT_STRING);
             });
          });
        employeeBenefits.waive().query({userId:$scope.employee.id, companyId:company_id})
          .$promise.then(function(waivedResponse){
            if(waivedResponse.length > 0){
              $scope.employee.waivedBenefits = waivedResponse;
              _.each($scope.employee.waivedBenefits, function(waived){
                waived.updateFormatted = moment(waived.update_at).format(DATE_FORMAT_STRING);
             });
            }
          });

        // TODO: Could/should FSA information be considered one kind of benefit election
        //       and this logic of getting FSA data for an employee be moved into the
        //       BenefitElectionService?

        FsaService.getFsaElectionForUser($scope.employee.id, company_id).then(function(response) {
          $scope.employee.fsaElection = response;
        });

        // TODO: like the above comment for FSA, Life Insurance, or more generally speaking,
        //       all new benefits going forward, we should consider creating as separate
        //       entity and maybe avoid trying to artificially bundle them together.
        //       Also, once we have tabs working, we should split them into proper flows.
        BasicLifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser($scope.employee.id, $scope.company)
        .then(function(response){
          $scope.employee.basicLifeInsurancePlan = response;
        });

        SupplementalLifeInsuranceService.getPlanByUser($scope.employee.id, $scope.company).then(function(plan) {
          $scope.employee.supplementalLifeInsurancePlan = plan;
        });

        // STD
        StdService.getUserEnrolledStdPlanByUser($scope.employee.id, $scope.company.id).then(function(response){
          $scope.employee.userStdPlan = response;
        });

        // LTD
        LtdService.getUserEnrolledLtdPlanByUser($scope.employee.id, $scope.company.id).then(function(response){
          $scope.employee.userLtdPlan = response;
        });

        // HRA
        HraService.getPersonPlanByUser($scope.employee.id, $scope.company.id).then(function(plan) {
          $scope.employee.hraPlan = plan;
        });

    }, function(errorResponse){
      alert(errorResponse.content);
    });
  }
]);
