var employersController = angular.module('benefitmyApp.employers.controllers',[]);


var employerHome = employersController.controller('employerHome',
                                                  ['$scope',
                                                  '$location',
                                                  'employerRepository',
                                                  'currentUser',
                                                  'clientListRepository',
                                                  'documentRepository',
                                                  'templateRepository',
                                                  'employerWorkerRepository',
                                                  'benefitListRepository',
  function employerHome($scope,
                        $location,
                        employerRepository,
                        currentUser,
                        clientListRepository,
                        documentRepository,
                        templateRepository,
                        employerWorkerRepository,
                        benefitListRepository){

    $scope.employeeCount = 0;
    $scope.brokerCount = 0;
    $scope.benefitCount = 0;
    $scope.templateCountArray = [];

   var getDocumentTypes = function(company){
      documentRepository.type.get({companyId:company.Id}).$promise.then(function(response){
        $scope.documentTypes = response.document_types;
      });
    }
    var getTemplates = function(company){
      templateRepository.byCompany.get({companyId:company.id}).$promise.then(function(response){
        $scope.templateArray = response.templates;
      });
    }
    var getWorkerCount = function(company){
      employerWorkerRepository.get({companyId:company.id})
        .$promise.then(function(response){
            _.each(response.user_roles, function(role){
              if(role.type=='employee')
              {
                $scope.employeeCount++;
              }
              else if(role.type=='broker')
              {
                $scope.brokerCount++;
              }
            })
        });
    };

    var getBenefitCount = function(company){
      benefitListRepository.get({clientId:company.id})
        .$promise.then(function(response){
            var benefitNameArray = [];
            _.each(response.benefits, function(benefit){
              var name = _.findWhere(benefitNameArray, {benefit_name:benefit.benefit_name});
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
          _.each(response.templates, function(template){
            if(!$scope.templateCountArray[template.document_type])
            {
              $scope.templateCountArray[template.document_type] = 1;
            }
            else
            {
              $scope.templateCountArray[template.document_type] ++;
            }
          });
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
            getDocumentTypes($scope.company);
            getTemplates($scope.company);
            getWorkerCount($scope.company);
            getBenefitCount($scope.company);
            getTemplateCount($scope.company);
            return false;
          }
          return true;
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
       $location.path('/admin/generate_template/'+ companyId).search({type:docType.name});
    }
  }
]);

var employerUser = employersController.controller('employerUser',
                                                  ['$scope',
                                                  '$location',
                                                  '$routeParams',
                                                  'employerWorkerRepository',
                                                  'usersRepository',
                                                  'documentRepository',
  function employerUser($scope,
                        $location,
                        $routeParams,
                        employerWorkerRepository,
                        usersRepository,
                        documentRepository){
      var compId = $routeParams.company_id;
      $scope.employees=[];
      $scope.addUser = {};
      $scope.brokers = [];
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

      var gotoUserView = function(userType){
        $location.path('/admin/' + userType + '/' + compId);
      }

      var mapToAPIUser = function(viewUser, userType){
        var apiUser = {};
        apiUser.company = compId;
        apiUser.company_user_type = userType;
        apiUser.user = {};
        apiUser.user.email = viewUser.email;
        apiUser.user.first_name = viewUser.name;
        apiUser.user.last_name = 'Default';
        if(viewUser.phone)
        {
            //input phone to the apiModel here
        }
        return apiUser;
      }

      var validateAddUser = function(addUser){
        if(addUser.name && addUser.email)
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
        var sendEmail = $scope.addUser.send_email;
        if(validateAddUser($scope.addUser))
        {
          usersRepository.save(mapToAPIUser($scope.addUser, userType), function(){
              gotoUserView(userType);
            }, function(){
                $scope.saveSucceeded = false;
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
        documentRepository.byUser.get({userId:employeeId, companyId:compId})
        .$promise.then(function(response){
          var doc = _.findWhere(response.documents, {document_type:docType});
          var pathKey = 'create_letter';
          if(doc)
          {
            pathKey='view_letter';
          }
          $location.path('/admin/' + pathKey + '/' +compId +'/'+employeeId).search({type:docType});
        });

      }
  }
]);

var employerBenefits = employersController.controller('employerBenefits', ['$scope', '$location', '$routeParams', 'benefitListRepository',
  function employerBenefits($scope, $location, $routeParams, benefitListRepository){
    var compId = $routeParams.company_id;
    benefitListRepository.get({clientId:compId})
        .$promise.then(function(response){
            $scope.companyBenefitsArray = [];
            _.each(response.benefits, function(benefit){
                insertIntoBenefitArray($scope.companyBenefitsArray, benefit);
            });
        });
    var insertIntoBenefitArray = function(companyBenefitsArray, benefit)
    {
        var benefitType = benefit.benefit_plan.benefit_type.name;
        var array = _.findWhere(companyBenefitsArray, {type:benefitType});
        if(!array)
        {
            array = {type:benefitType, benefitList:[]};
            companyBenefitsArray.push(array);
        }
        var sameBenefit = _.findWhere(array.benefitList, {name:benefit.benefit_name})
        if(!sameBenefit)
        {
          var sameNameBenefit = {};
          sameNameBenefit.name = benefit.benefit_plan.name;
          sameNameBenefit.options = [];
          sameNameBenefit.options.push({
              optionType:benefit.benefit_option_type,
              totalCost:benefit.total_cost_per_period,
              employeeCost: benefit.employee_cost_per_period
            });
          array.benefitList.push(sameNameBenefit);
        }
        else
        {
          sameBenefit.options.push({
              optionType:benefit.benefit_option_type,
              totalCost:benefit.total_cost_per_period,
              employeeCost: benefit.employee_cost_per_period
          });
        }

    }
  }
]);

var employerLetterTemplate = employersController.controller('employerLetterTemplate', ['$scope', '$location', '$route', '$routeParams', 'templateRepository', 'documentRepository',
  function employerLetterTemplate($scope, $location, $route, $routeParams, templateRepository, documentRepository){
    $scope.documentType = $routeParams.type;
    $scope.addMode = $routeParams.add;
    $scope.companyId = $routeParams.company_id;
    $scope.viewTitle = 'Create ' + $scope.documentType + ' Template';
    $scope.showCreateButton = $scope.addMode;
    $scope.showEditButton = false;
    $scope.existingTemplateList = [];

    var updateWithExistingTemplate = function(template)
    {
      if(template)
      {
        $scope.templateContent = template.content;
        $scope.templateName = template.name;
        $scope.showCreateButton = false;
        $scope.showEditButton = true;
      }
    }
    if(!$scope.addMode)
    {
      templateRepository.byCompany.get({companyId:$routeParams.company_id})
        .$promise.then(function(response){
          $scope.existingTemplateList = _.sortBy(_.where(response.templates, {document_type:$scope.documentType}), function(elm){return elm.id;}).reverse();
          if(!_.isEmpty($scope.existingTemplateList))
          {
            $scope.viewTitle = 'Manage ' + $scope.documentType + ' Template';
          }
          else
          {
            $scope.addMode=true;
            $scope.showCreateButton = true;
          }
        });
    };
    $scope.modifyExistingTemplate = function(template){
      updateWithExistingTemplate(template);
    };
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
                                                          '$routeParams',
                                                          'documentRepository',
                                                          'templateRepository',
  function employerCreateLetter($scope,
                                $location,
                                $routeParams,
                                documentRepository,
                                templateRepository){
    $scope.companyId = $routeParams.company_id;
    var employeeId = $routeParams.employee_id;
    $scope.documentType = $routeParams.type;
    $scope.newDoc = {document_type:$scope.documentType};

    templateRepository.byCompany.get({companyId:$scope.companyId})
      .$promise.then(function(response){
        $scope.templateArray = _.sortBy(_.where(response.templates, {document_type:$scope.documentType}), function(elm){return elm.id;}).reverse();
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
      var postObj={company:$scope.companyId, user:employeeId, template:curTemplate.id, document:$scope.newDoc};
      documentRepository.create.save(postObj, function(response){
        $location.path('/admin/view_letter/' + $scope.companyId + '/' + employeeId).search({type:$scope.documentType});
      }, function(errResponse){
        $scope.createFailed = true;
      });
    }
  }]);

var employerViewLetter = employersController.controller('employerViewLetter',
                                                          ['$scope',
                                                          '$location',
                                                          '$routeParams',
                                                          'documentRepository',
  function employerViewLetter($scope,
                              $location,
                              $routeParams,
                              documentRepository){
    $scope.companyId = $routeParams.company_id;
    var employeeId = $routeParams.employee_id;
    $scope.documentType = $routeParams.type;
    $scope.documentList = [];


    documentRepository.byUser.get({userId:employeeId, companyId:$scope.companyId})
      .$promise.then(function(response){
        $scope.documentList = _.sortBy(_.where(response.documents, {document_type:$scope.documentType}), function(elm){return elm.id;}).reverse();
      });

    $scope.viewExistingLetter = function(doc){
      $scope.curDocument = doc;
    };

    $scope.createNewLetter = function(){
      $location.path('/admin/create_letter/'+ $scope.companyId +'/' + employeeId).search({type:$scope.documentType});
    };

    $scope.viewEmployeesLink = function(){
      $location.path('/admin/employee/' + $scope.companyId);
    };
  }]);
