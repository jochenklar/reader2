var app = angular.module('reader', ['ngSanitize','infinite-scroll','duScroll']);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory('itemService', ['$http', function($http) {
    return {
        getItems: function(params) {
            return $http.get('api/items/', {params: params});
        },
        activateItem: function(id) {
            return $http.patch('api/items/' + id + '/', {'visited': true});
        }
    };
}]);

app.factory('categoryService', ['$http', function($http) {
    return {
        getCategories: function () {
            return $http.get('api/categories/');
        },
        createCategory: function(data) {
            return $http.post('api/categories/', data);
        },
        updateCategory: function(id, data) {
            return $http.put('api/categories/' + id + '/', data);
        },
        deleteCategory: function(id, data) {
            return $http.delete('api/categories/' + id + '/', data);
        }
    };
}]);

app.factory('subscriptionService', ['$http', function($http) {
    return {
        createSubscription: function (data) {
            return $http.post('api/subscriptions/', data);
        },
        updateSubscription: function (id, data) {
            return $http.put('api/subscriptions/' + id + '/', data);
        },
        deleteSubscription: function (id, data) {
            return $http.delete('api/subscriptions/' + id + '/', data);
        },
    };
}]);

app.controller('bodyController', ['$scope','$timeout','$filter','$document','itemService','categoryService','subscriptionService', function($scope,$timeout,$filter,$document,itemService,categoryService,subscriptionService) {

    $scope.activeFeed = -1;

    $scope.activeItem = -1;

    $scope.canScroll = false;

    $scope.editable = false;

    $scope.sidebarVisible = false;

    $scope.toogleSidebar = function() {
        $scope.sidebarVisible = !$scope.sidebarVisible;
    };

    $scope.firstItem = function() {
        $scope.setActiveItem(0);
    };

    $scope.prevItem = function() {
        $scope.setActiveItem($scope.activeItem - 1);
    };
    
    $scope.nextItem = function() {
        $scope.setActiveItem($scope.activeItem + 1);
    };

    $scope.thisItem = function(i) {
        if ($scope.activeItem == i) {
            $scope.setActiveItem(-1);
        } else {
            $scope.setActiveItem(i);
        }
    };

    $scope.setActiveFeed = function(id) {
        $scope.activeFeed = id;
        $scope.activeItem = -1;

        itemService.getItems({
            'page_size': 30,
            'feed': $scope.activeFeed
        }).success(function(data) {
            $scope.items = data.results;
            $scope.canScroll = true;
        });
    };

    $scope.setActiveItem = function(i) {
        if (i > -1) {

            $scope.activeItem = i;

            if ($scope.items[i].visited === false) {
                $scope.items[i].visited = true;
                itemService.activateItem($scope.items[i].id);
            }

            $timeout(function() {
                var element = angular.element('.active');
                $document.scrollToElement(element, 100, 300);
            }, 100);

        } else {
            $scope.activeItem = -1;
        }
    };

    $scope.loadMoreItems = function() {
        if ($scope.canScroll){
            $scope.canScroll = false;

            var page = $scope.items.length / 5;

            itemService.getItems({
                'page_size': 10,
                'page': ($scope.items.length / 10) + 1,
                'feed': $scope.activeFeed
            }).success(function(data) {
                $scope.items = $scope.items.concat(data.results);
                $scope.canScroll = true;
            });
        }
    };

    categoryService.getCategories().success(function(data) {
        $scope.categories = data;
    });
    
    itemService.getItems({
        'page_size': 30
    }).success(function(data) {
        $scope.items = data.results;
        $scope.canScroll = true;
    });

    // category form

    $scope.showCreateCategoryForm = function() {
        $scope.categoryForm.$setPristine();
        $scope.categoryFormSubmitted = false;

        $scope.categoryFormItem = false;
        $scope.categoryFormData = {};

        $('#category-form-modal').modal('show');
    };

    $scope.submitCreateCategoryForm = function(isValid) {
        $scope.categoryFormSubmitted = true;

        if (isValid) {
            categoryService.createCategory($scope.categoryFormData).success(function(data) {
                $scope.categories.push(data);
                $('#category-form-modal').modal('hide');
            });
        }
    };

    $scope.showUpdateCategoryForm = function(category) {
        $scope.categoryForm.$setPristine();
        $scope.categoryFormSubmitted = false;

        $scope.categoryFormItem = category;
        $scope.categoryFormData = {
            'title': category.title
        };

        $('#category-form-modal').modal('show');
    };

    $scope.submitUpdateCategoryForm = function(isValid) {
        $scope.categoryFormSubmitted = true;
        if (isValid) {
            categoryService.updateCategory($scope.categoryFormItem.id,$scope.categoryFormData).success(function(data) {
                $scope.categoryFormItem.title = data.title;
                $('#category-form-modal').modal('hide');
            });
        }
    };

    $scope.showDeleteCategoryForm = function(category) {
        $scope.deleteFormType = 'category';
        $scope.deleteFormItem = category;

        $('#delete-form-modal').modal('show');
    };

    $scope.submitDeleteCategoryForm = function(isValid) {
        categoryService.deleteCategory($scope.deleteFormItem.id).success(function() {
            var index = $scope.categories.indexOf($scope.deleteFormItem);
            if (index != -1) {
                $scope.categories.splice(index, 1);
            }
            $('#delete-form-modal').modal('hide');
        });
    };

    // subscription form

    $scope.showCreateSubscriptionForm = function() {
        $scope.subscriptionForm.$setPristine();
        $scope.subscriptionFormSubmitted = false;

        $scope.subscriptionFormItem = false;
        $scope.subscriptionFormData = {};
        $scope.subscriptionFormError = false;

        $('#subscription-form-modal').modal('show');
    };

    $scope.submitCreateSubscriptionForm = function(isValid) {
        $scope.subscriptionFormSubmitted = true;
        if (isValid) {
            var categoryId = parseInt($scope.subscriptionFormData.categoryId);
            var category = $filter('filter')($scope.categories, {id: categoryId}, true)[0];

            subscriptionService.createSubscription($scope.subscriptionFormData).success(function(data) {
                category.subscriptions.push(data);
                $('#subscription-form-modal').modal('hide');
            }).error(function(data) {
                $scope.subscriptionFormError = 'Feed not available.';
            });
        }
    };

    $scope.showUpdateSubscriptionForm = function(subscription) {
        $scope.subscriptionForm.$setPristine();
        $scope.subscriptionFormSubmitted = false;

        $scope.subscriptionFormItem = subscription;
        $scope.subscriptionFormData = {
            'categoryId': subscription.category.id,
            'xmlUrl': subscription.feed.xmlUrl
        };
        $scope.subscriptionFormError = false;

        $('#subscription-form-modal').modal('show');
    };

    $scope.submitUpdateSubscriptionForm = function(isValid) {
        $scope.feedFormSubmitted = true;

        if (isValid) {
            subscriptionService.updateSubscription($scope.subscriptionFormItem.id,$scope.subscriptionFormData).success(function(data) {

                // see if we switched categories
                if (data.category.id != $scope.subscriptionFormItem.category.id) {
                    // remove subscription from the old category
                    var oldCategory = $filter('filter')($scope.categories, {id: $scope.subscriptionFormItem.category.id}, true)[0];
                    var index = oldCategory.subscriptions.indexOf($scope.subscriptionFormItem);
                    if (index != -1) {
                        oldCategory.subscriptions.splice(index, 1);
                    }

                    var newCategory = $filter('filter')($scope.categories, {id: data.category.id}, true)[0];
                    newCategory.subscriptions.push(data);
                } else {
                    $scope.subscriptionFormItem.feed = data.feed;
                }

                $('#subscription-form-modal').modal('hide');
            }).error(function(data) {
                $scope.subscriptionFormError = 'Feed not available.';
            });
        }
    };

    $scope.showDeleteSubscriptionForm = function(subscription) {
        $scope.deleteFormType = 'subscription';
        $scope.deleteFormItem = subscription;
        $('#delete-form-modal').modal('show');
    };

    $scope.submitDeleteSubscriptionForm = function(isValid) {
        subscriptionService.deleteSubscription($scope.deleteFormItem.id).success(function() {
            // remove subscription from the old category
            var category = $filter('filter')($scope.categories, {id: $scope.deleteFormItem.category.id}, true)[0];
            var index = category.subscriptions.indexOf($scope.deleteFormItem);
            if (index != -1) {
                category.subscriptions.splice(index, 1);
            }
            $('#delete-form-modal').modal('hide');
        });
    };
}]);
