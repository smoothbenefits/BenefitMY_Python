var employersController = angular.module('benefitmyApp.employers.controllers',[]);

var employerHome = employersController.controller('employerHome',
  ['$scope',
  '$location',
  '$state',
  'employerRepository',
  'currentUser',
  'clientListRepository',
  'TemplateService',
  'benefitListRepository',
  'countRepository',
  'documentTypeService',
  'CompanyBenefitEnrollmentSummaryService',
  function ($scope,
            $location,
            $state,
            employerRepository,
            currentUser,
            clientListRepository,
            TemplateService,
            benefitListRepository,
            countRepository,
            documentTypeService,
            CompanyBenefitEnrollmentSummaryService){

    $scope.employeeCount = 0;
    $scope.brokerCount = 0;
    $scope.benefitCount = 0;
    $scope.benefitEnrollCount = 0;
    $scope.templateCount = 0;

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

            getWorkerCount($scope.company);
            getBenefitCount($scope.company);
            TemplateService.getTemplateCount($scope.company.id)
            .then(function(templateCount){
              $scope.templateCount = templateCount;
            });
            getBenefitElectionCount($scope.company);
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
    };

    $scope.viewDocumentTemplate = function(companyId){
       $state.go('document_templates', {company_id: companyId});
    };

    $scope.addDocumentTemplate = function(companyId){
      $state.go('document_templates_edit', {company_id: companyId});
    }

    $scope.viewBenefitElection = function(companyId)
    {
      $location.path('/admin/benefit/election/'+companyId);
    }

    $scope.viewAcaReports = function(companyId) {
      $state.go('aca_report', {company_id: companyId});
    };
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
   'TemplateService',
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
                        TemplateService,
                        DocumentService,
                        CompensationService,
                        EmployerEmployeeManagementService){
      var compId = $stateParams.company_id;
      $scope.employees=[];
      $scope.brokers = [];
      $scope.templateFields = [];
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
          $scope.annualSalaryNotAvailable = false;
        } else {
          $scope.isHourlyRate = true;
          $scope.annualSalaryNotAvailable = true;
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
                DocumentService.getDocumentsToUserEntry(employee.user.id)
                .then(function(docEntry) {
                    employee.docEntry = docEntry;
                });
            });
        });

      TemplateService.getAllTemplateFields(compId)
      .then(function(fields){
        $scope.templateFields = fields;
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

      $scope.syncBenefitStartDate = function(){
        if($scope.addUser.date_of_hire){
          $scope.addUser.benefit_start_date = moment($scope.addUser.date_of_hire).format('MM/DD/YYYY');
        }
      };

      $scope.$watch('addUser.date_of_hire', $scope.syncBenefitStartDate);

      $scope.addLink = function(userType)
      {
        $location.path('/admin/'+ userType + '/add/'+compId)
      };

      $scope.createUser = function(userType) {
        if(!$scope.addUser.send_email &&
           !$scope.validatePassword($scope.addUser.password, $scope.addUser.password_confirm)){
          alert('Password validation failed. Please re-enter the passwords');
          return false;
        };
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
        var pathKey = 'create';
        if(docEntry.hasDocument())
        {
            pathKey='view';
        }

        $location.path('/admin/documents/' + pathKey + '/' +compId +'/'+employeeId);
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
  'CommuterService',
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
            CommuterService,
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

    CommuterService.getPlansForCompany($stateParams.company_id).then(function(response) {
      $scope.commuterPlans = response;
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
  ['$scope', '$state', '$stateParams', 'TemplateService',
  function employerLetterTemplate($scope, $state, $stateParams, TemplateService){
    $scope.companyId = $stateParams.company_id;
    $scope.existingTemplateList = [];

    TemplateService.getTemplates($stateParams.company_id)
    .then(function(templates){
      $scope.existingTemplateList = _.sortBy(
          templates,
          function(elm){return elm.id;}
        ).reverse();
    });

    $scope.modifyExistingTemplate = function(template){
      $state.go('document_templates_edit', {company_id:$scope.companyId, template_id: template.id});
    };

    $scope.isTemplateUpload = function(template) {
        return template.contentType == TemplateService.contentTypes.upload;
    };

    $scope.goToBatchDocumentCreationView = function(template) {
        $state.go('employer_batch_create_documents', {company_id:$scope.companyId, template_id: template.id});
    };

    $scope.viewDashboard = function(){
      $state.go('/admin');
    };
  }
]);

var employerModifyTemplate = employersController.controller('employerModifyTemplate',
  ['$scope', '$state', '$stateParams', 'TemplateService',
  function employerModifyTemplate($scope, $state, $stateParams, TemplateService){
    $scope.companyId = $stateParams.company_id;
    $scope.templateId = $stateParams.template_id;
    
    var templateTypes = {
        'Text': 'Text',
        'Upload': 'Upload'
    };

    $scope.templateType = templateTypes.Text;

    if($scope.templateId){
      $scope.viewTitle = 'View/Edit Template';
      TemplateService.getTemplateById($scope.templateId)
      .then(function(template){
        $scope.template = template;

        $scope.templateType = $scope.template.upload 
                            ? templateTypes.Upload
                            : templateTypes.Text;
      });
    }
    else{
      $scope.viewTitle = 'Create Template';
      $scope.template = {};
    };

    $scope.onUploadAdded = function(upload) {
        $scope.template.upload = upload;
    };

    $scope.onUploadDeleted = function(upload) {
        $scope.template.upload = null;
    };

    $scope.inTextMode = function() {
        return $scope.templateType == templateTypes.Text;
    };

    $scope.inUploadMode = function() {
        return $scope.templateType == templateTypes.Upload;
    };

    $scope.hasCompleteData = function() {
        return $scope.template
            && $scope.template.name
            && ($scope.template.upload 
                || $scope.template.content);
    };

    var cleanTemplateForSave = function() {
        if ($scope.inTextMode()) {
            $scope.template.upload = null;
        } else if ($scope.inUploadMode()) {
            $scope.template.content = null;
        }
    };

    $scope.saveTemplateChanges = function(){
      cleanTemplateForSave();
      $scope.template.id = $scope.templateId;
      TemplateService.updateTemplate($scope.companyId, $scope.template)
      .then(function(savedTemplate){
        $scope.template = savedTemplate;
        alert('Template Saved');
        $scope.goBack();
      }, function(errorResponse){
        alert('Template save failure with reason: ' + errorResponse);
      });
    };

    $scope.viewDashboard = function(){
      $location.path('/admin');
    };

    $scope.createTemplate = function(){
      if($scope.template.name 
         && ($scope.template.content
             || $scope.template.upload))
      {
        cleanTemplateForSave();
        
        TemplateService.createNewTemplate($scope.companyId, $scope.template)
        .then(function(savedTemplate){
          $scope.template = savedTemplate;
          alert('Template "' + $scope.template.name + '" successfully created');
          $scope.goBack();
        }, function(errorResponse){
          alert('Template creation failure: ' + errorResponse);
        });
      }
    };
    $scope.goBack = function(){
      $state.go('document_templates', {company_id:$scope.companyId});
    };
  }
]);

var employerCreateDocument = employersController.controller('employerCreateDocument',
                                                          ['$scope',
                                                          '$location',
                                                          '$stateParams',
                                                          'DocumentService',
                                                          'TemplateService',
  function employerCreateDocument($scope,
                                $location,
                                $stateParams,
                                DocumentService,
                                TemplateService){
    $scope.companyId = $stateParams.company_id;
    var employeeId = $stateParams.employee_id;
    $scope.newDoc = {};

    TemplateService.getTemplates($scope.companyId)
    .then(function(templates){
      $scope.templateArray = _.sortBy(templates, function(template){
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

    $scope.inTextMode = function() {
        return $scope.selectedTemplate 
            && $scope.selectedTemplate.contentType == TemplateService.contentTypes.text;
    };

    $scope.inUploadMode = function() {
        return $scope.selectedTemplate 
            && $scope.selectedTemplate.contentType == TemplateService.contentTypes.upload;
    };

    $scope.doCreateLetter = function()
    {
      var curTemplate = $scope.selectedTemplate;
      $scope.newDoc.upload = curTemplate.upload
                            ? curTemplate.upload.id
                            : null;
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

      DocumentService.createDocument($scope.companyId, employeeId, curTemplate.id, '', $scope.newDoc)
      .then(function(response){
        $location.search({type:$scope.documentType}).path('/admin/documents/view/' + $scope.companyId + '/' + employeeId);
      }, function(errResponse){
        $scope.createFailed = true;
      });
    }
  }]);

var employerBatchCreateDocuments = employersController.controller('employerBatchCreateDocuments',
                                                          ['$scope',
                                                          '$state',
                                                          '$stateParams',
                                                          'TemplateService',
                                                          'DocumentService',
  function employerBatchCreateDocuments($scope,
                                        $state,
                                        $stateParams,
                                        TemplateService,
                                        DocumentService){
    $scope.companyId = $stateParams.company_id;
    $scope.documentsCreationData = {};
    
    TemplateService.getTemplateById($stateParams.template_id).then(function(template) {
        $scope.template = template;
        $scope.documentsCreationData.documentName = template.name;
        $scope.documentsCreationData.templateId = template.id;
    });

    $scope.createDocuments = function()
    {
        DocumentService.batchCreateDocuments($scope.companyId, $scope.documentsCreationData)
        .then(function(resultDocs) {
            alert('Documents have been successfully created for ' + resultDocs.length + ' employees!');
            $scope.goBackToViewTemplates();
        }, 
        function(errors) {
            alert('There were problems creating documents. Please try again later or contact support.');
        });
    };

    $scope.goBackToViewTemplates = function(){
      $state.go('document_templates', {company_id:$scope.companyId});
    };
  }]);

var employerViewDocument = employersController.controller('employerViewDocument',
                                                          ['$scope',
                                                          '$location',
                                                          '$state',
                                                          '$stateParams',
                                                          'DocumentService',
  function employerViewDocument($scope,
                              $location,
                              $state,
                              $stateParams,
                              DocumentService){
    $scope.companyId = $stateParams.company_id;
    var employeeId = $stateParams.employee_id;
    $scope.documentList = [];
    $scope.activeDocument = {};
    $scope.signaturePresent = false;

    DocumentService.getAllDocumentsForUser(employeeId)
        .then(function(response){
            $scope.documentList = _.sortBy(response, function(elm){return elm.id;}).reverse();
        });

    $scope.deleteExistingLetter = function(doc){
      DocumentService.deleteDocumentById(doc.id)
        .then(function(response){
          alert("Deleted document " + doc.name);
          $state.reload();
        });
    };

    $scope.updateExistingLetter = function(){
      var doc = $scope.activeDocument;
      DocumentService.updateDocumentById(doc.id, doc)
        .then(function(response){
          alert("Successful update " + response.name);
        });
    }

    $scope.anyActiveDocument = function(){
      return typeof $scope.activeDocument.name !== 'undefined';
    }

    $scope.inTextMode = function() {
        return $scope.activeDocument 
            && $scope.activeDocument.contentType == DocumentService.contentTypes.text;
    };

    $scope.inUploadMode = function() {
        return $scope.activeDocument
            && $scope.activeDocument.contentType == DocumentService.contentTypes.upload;
    };

    $scope.viewExistingLetter = function(doc){
      $scope.activeDocument = doc;
      if (doc.signature && doc.signature.signature){
        $scope.signaturePresent = true;
        $scope.signatureId = doc.signature.id;
      } else {
        $scope.signaturePresent = false;
        $scope.signatureId = null;
      }
    };

    $scope.createNewLetter = function(){
      $location.path('/admin/documents/create/'+ $scope.companyId +'/' + employeeId);
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

    var saveToTerminateEmployment = function(terminationData){

      EmployeeProfileService.terminateEmployee(terminationData)
      .then(function(response){
        $scope.employee.employeeProfile = response;
      }, function(error){
        $scope.terminateMessage = "Error occurred during saving operation. Please verify " +
          "all the information enterred are valid. Message: " + error;
      });
    };

    $scope.terminateEmployment = function(){
      var terminationData = {
        companyId: $scope.employee.employeeProfile.companyId,
        personId: $scope.employee.employeeProfile.personId
      };
      var modalInstance = $modal.open({
          templateUrl: '/static/partials/employee_record/terminate_confirmation.html',
          controller: 'confirmTerminateEmployeeModalController',
          size: 'md',
          backdrop: 'static',
          resolve: {
              terminationData: function () {
                  return terminationData;
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
      $scope.employmentTypes = ['FullTime', 'PartTime', 'Contractor', 'Intern', 'PerDiem'];
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

      $scope.useHourlyRate = function() {
        return !$scope.isFullTime || $scope.getHourlyPaid;
      };

      $scope.useAnnualSalary = function(){
        return $scope.isFullTime && !$scope.getHourlyPaid;
      };

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
  'terminationData',
  function($scope,
           $modalInstance,
           terminationData){

    $scope.terminationData = terminationData;

    $scope.endDateRequired = function(){
      return _.isNull($scope.terminationData.endDate) || _.isUndefined($scope.terminationData.endDate);
    };

    $scope.confirm = function(){
      $modalInstance.close($scope.terminationData);
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
  '$controller',
  'companyRepository',
  'CompanyEmployeeSummaryService',
  'CompanyBenefitEnrollmentSummaryService',
  'Company1095CService',
  function($scope,
           $location,
           $state,
           $stateParams,
           $modal,
           $controller,
           companyRepository,
           CompanyEmployeeSummaryService,
           CompanyBenefitEnrollmentSummaryService,
           Company1095CService){

    $controller('modalMessageControllerBase', {$scope: $scope});

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
        templateUrl: '/static/partials/aca/modal_company_1095_c.html',
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

    $scope.editEmployeeSafeHarborCode = function(employeeId) {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/aca/modal_employee_1095_c.html',
        controller: 'employee1095CModalController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          CompanyId: function() { return company_id; },
          EmployeeId: function() { return employeeId; },
          Company1095CData: function() {
            return angular.copy($scope.sorted1095CData);
          }
        }
      });

      modalInstance.result.then(function(saved1095CData) {
        $scope.showMessageWithOkayOnly('Success', 'Employee safe harbor code has been saved successfully.');
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
  'CommuterService',
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
           HraService,
           CommuterService){
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

        // Commuter
        CommuterService.getPersonPlanByUser($scope.employee.id, $scope.company.id).then(function(plan) {
          $scope.employee.commuterPlan = plan;
          $scope.employee.commuterPlan.calculatedTotalTransitAllowance = CommuterService.computeTotalMonthlyTransitAllowance($scope.employee.commuterPlan);
          $scope.employee.commuterPlan.calculatedTotalParkingAllowance = CommuterService.computeTotalMonthlyParkingAllowance($scope.employee.commuterPlan);
        });

    }, function(errorResponse){
      alert(errorResponse.content);
    });
  }
]);

var employerAcaReport = employersController.controller('employerAcaReport', [
  '$scope', '$state', '$stateParams', '$modal', '$controller', 'Company1094CService',
  function($scope, $state, $stateParams, $modal, $controller, Company1094CService) {
    $controller('modalMessageControllerBase', {$scope: $scope});

    var companyId = $stateParams.company_id;

    Company1094CService.Get1094CEligibilityCertification().then(function(data) {
      $scope.eligibilityCertification = data;
    });

    Company1094CService.Get1094CByCompany(companyId).then(function(data) {
      $scope.sorted1094CData = data;
    });

    $scope.getCompany1094CUrl = function() {
      return Company1094CService.GetCompany1094CUrl(companyId);
    };

    $scope.edit1094CInfo = function() {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/aca/modal_company_1094_c.html',
        controller: 'Company1094CModalController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          CompanyId: function() { return companyId; },
          EligibilityCertification: function() { return $scope.eligibilityCertification; },
          Company1094CData: function() {
            return angular.copy($scope.sorted1094CData);
          }
        }
      });

      modalInstance.result.then(function(saved1094CData) {
        $scope.sorted1094CData = saved1094CData;
        $scope.showMessageWithOkayOnly('Success', 'Company 1094C data has been saved successfully.');
      });
    };

  }
]);
