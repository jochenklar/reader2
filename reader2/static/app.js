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
        createCategory: function (data) {
            return $http.post('api/categories/', data);
        },
        updateCategory: function (id, data) {
            return $http.put('api/categories/' + id + '/', data);
        },
        deleteCategory: function (id, data) {
            return $http.delete('api/categories/' + id + '/', data);
        },
    };
}]);

app.factory('feedService', ['$http', function($http) {
    return {
        createFeed: function (data) {
            return $http.post('api/feeds/', data);
        },
        updateFeed: function (id, data) {
            return $http.put('api/feeds/' + id + '/', data);
        },
        deleteFeed: function (id, data) {
            return $http.delete('api/feeds/' + id + '/', data);
        },
    };
}]);

app.controller('bodyController', ['$scope','$timeout','$filter','$document','itemService','categoryService','feedService', function($scope,$timeout,$filter,$document,itemService,categoryService,feedService) {

    $scope.activeFeed = -1;

    $scope.activeItem = -1;

    $scope.canScroll = false;

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
            var page = $scope.items.length / 5;

            itemService.getItems({
                'page_size': 5,
                'page': ($scope.items.length / 5) + 1,
                'feed': $scope.activeFeed
            }).success(function(data) {
                $scope.items = $scope.items.concat(data.results);
            }).error(function(data) {
                // everything is here, disabling infinite scroll
                $scope.canScroll = false;
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

    $scope.categoryFormData = {};
    $scope.categoryFormSubmitted = false;

    $scope.showCategoryForm = function(categoryId) {
        $scope.categoryForm.$setPristine();
        $scope.categoryFormSubmitted = false;

        if (typeof categoryId === 'undefined') {
            $scope.categoryFormId = null;
            $scope.categoryFormData = {};
        } else {
            var category = $filter('filter')($scope.categories, {id: categoryId}, true)[0];
            $scope.categoryFormId = category.id;
            $scope.categoryFormData = {
                'title': category.title
            };
        }

        $('#category-form-modal').modal('show');
    };

    $scope.submitCategoryForm = function(isValid) {
        $scope.categoryFormSubmitted = true;
        if (isValid) {
            if ($scope.categoryFormId === null) {
                categoryService.createCategory($scope.categoryFormData).success(function(data) {
                    $scope.categories.push(data);
                    $('#category-form-modal').modal('hide');
                });
            } else {
                categoryService.updateCategory($scope.categoryFormId,$scope.categoryFormData).success(function(data) {
                    var category = $.grep($scope.categories, function(e){return e.id == data.id;})[0];
                    category.title = data.title;
                    $('#category-form-modal').modal('hide');
                });
            }
        }
    };

    // feed form

    $scope.feedFormData = {};
    $scope.feedFormSubmitted = false;

    $scope.showFeedForm = function(feedId) {
        $scope.feedForm.$setPristine();
        $scope.feedFormSubmitted = false;

        if (typeof feedId === 'undefined') {
            $scope.feedFormId = null;
            $scope.feedFormData = {};
        } else {
            var feed = $filter('filter')($scope.categories, {id: feedId}, true)[0];
            $scope.feedFormId = feed.id;
            $scope.feedFormData = {
                // 'title': feed.title,
                // 'htmlurl': feed.title,
                // 'xmlurl': feed.title,
                // 'category': feed.title,
            };
        }

        $('#feed-form-modal').modal('show');
    };

    $scope.submitFeedForm = function(isValid) {
        $scope.feedFormSubmitted = true;
        if (isValid) {
            if ($scope.feedFormId === null) {
                feedService.createFeed($scope.feedFormData).success(function(data) {
                    $scope.categories.push(data);
                    $('#feed-form-modal').modal('hide');
                });
            } else {
                feedService.updateFeed($scope.feedFormId,$scope.feedFormData).success(function(data) {
                    var feed = $.grep($scope.categories, function(e){return e.id == data.id;})[0];
                    feed.title = data.title;
                    $('#feed-form-modal').modal('hide');
                });
            }
        }
    };

    // delete form

    $scope.showDeleteForm = function(type,id) {
        $scope.deleteFormType = type;
        $scope.deleteFormId = id;
        $('#delete-form-modal').modal('show');
    };

    $scope.submitDeleteForm = function(isValid) {
        if ($scope.deleteFormType === "category") {
            categoryService.deleteCategory($scope.deleteFormId).success(function() {
                var category = $filter('filter')($scope.categories, {id: $scope.deleteFormId}, true)[0];
                var index = $scope.categories.indexOf(category);
                if (index != -1) {
                    $scope.categories.splice(index, 1);
                }
                $('#delete-form-modal').modal('hide');
            });
        } else if ($scope.deleteFormType === "feed") {
            feedService.deleteFeed($scope.deleteFormId).success(function() {
                var feed = $filter('filter')($scope.categories, {id: $scope.deleteFormId}, true)[0];
                var index = $scope.categories.indexOf(feed);
                if (index != -1) {
                    $scope.categories.splice(index, 1);
                }
                $('#delete-form-modal').modal('hide');
            });
        }
    };

    $scope.editable = true;
}]);
