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
        },
        addFeed: function(id,feedId) {
            return $http.patch('api/categories/' + id + '/', {'feedId': feedId});
        }
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

    $scope.editable = false;

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

    $scope.showCreateCategoryForm = function() {
        $scope.form.$setPristine();
        $scope.formSubmitted = false;

        $scope.formId = false;
        $scope.formData = {}

        $('#category-form-modal').modal('show');
    };

    $scope.submitCreateCategoryForm = function(isValid) {
        $scope.formSubmitted = true;
        if (isValid) {
            categoryService.createCategory($scope.formData).success(function(data) {
                $scope.categories.push(data);
                $('#category-form-modal').modal('hide');
            });
        }
    };

    $scope.showUpdateCategoryForm = function(categoryId) {
        $scope.form.$setPristine();
        $scope.formSubmitted = false;

        var category = $filter('filter')($scope.categories, {id: categoryId}, true)[0];
        $scope.formId = category.id;
        $scope.formData = {
            'title': category.title
        };

        $('#category-form-modal').modal('show');
    };

    $scope.submitUpdateCategoryForm = function(isValid) {
        $scope.formSubmitted = true;
        if (isValid) {
            categoryService.updateCategory($scope.formId,$scope.formData).success(function(data) {
                var category = $filter('filter')($scope.categories, {id: $scope.formId}, true)[0];
                category.title = data.title;
                $('#category-form-modal').modal('hide');
            });
        }
    };

    $scope.showDeleteCategoryForm = function(categoryId) {
        $scope.formType = 'category';
        $scope.formId = categoryId;

        $('#delete-form-modal').modal('show');
    };

    $scope.submitDeleteCategoryForm = function(isValid) {
        categoryService.deleteCategory($scope.formId).success(function() {
            var category = $filter('filter')($scope.categories, {id: $scope.formId}, true)[0];
            var index = $scope.categories.indexOf(category);
            if (index != -1) {
                $scope.categories.splice(index, 1);
            }
            $('#delete-form-modal').modal('hide');
        });
    };

    // feed form

    $scope.showCreateFeedForm = function() {
        $scope.form.$setPristine();
        $scope.formSubmitted = false;

        $scope.formId = false;
        $scope.formData = {}

        $('#feed-form-modal').modal('show');
    };

    $scope.submitCreateFeedForm = function(isValid) {
        $scope.feedFormSubmitted = true;
        if (isValid) {
            var categoryId = parseInt($scope.formData.categoryId);
            var category = $filter('filter')($scope.categories, {id: categoryId}, true)[0];

            feedService.createFeed($scope.formData).success(function(data) {
                category.feeds.push(data);
                $('#feed-form-modal').modal('hide');
            });
        }
    };

    $scope.showUpdateFeedForm = function(categoryId,feedId) {
        $scope.form.$setPristine();
        $scope.formSubmitted = false;

        var category = $filter('filter')($scope.categories, {id: categoryId}, true)[0];
        var feed = $filter('filter')(category.feeds, {id: feedId}, true)[0];

        $scope.formId = feedId;
        $scope.formCategoryId = categoryId;
        $scope.formData = {
            'title':feed.title,
            'htmlUrl': feed.htmlUrl,
            'xmlUrl': feed.xmlUrl,
            'categoryId': categoryId
        };

        $('#feed-form-modal').modal('show');
    };

    $scope.submitUpdateFeedForm = function(isValid) {
        $scope.feedFormSubmitted = true;
        if (isValid) {
            var categoryId = parseInt($scope.formData.categoryId);
            var category = $filter('filter')($scope.categories, {id: categoryId}, true)[0];

            feedService.updateFeed($scope.formId,$scope.formData).success(function(data) {
                var feed = $filter('filter')(category.feeds, {id: $scope.formId}, true)[0];
                if (typeof feed === 'undefined') {
                    // we switched categories
                    category.feeds.push(data);

                    // get rid of the old feed
                    var oldCategory = $filter('filter')($scope.categories, {id: $scope.formCategoryId}, true)[0];
                    var oldFeed = $filter('filter')(oldCategory.feeds, {id: $scope.formId}, true)[0];
                    var index = oldCategory.feeds.indexOf(oldFeed);
                    if (index != -1) {
                        oldCategory.feeds.splice(index, 1);
                    }
                } else {
                    feed.title = data.title;
                    feed.htmlUrl = data.htmlUrl;
                    feed.xmlUrl = data.xmlUrl;
                }
                $('#feed-form-modal').modal('hide');
            });
        }
    };

    $scope.showDeleteFeedForm = function(categoryId,feedId) {
        $scope.formType = 'feed';
        $scope.formId = feedId;
        $scope.formCategoryId = categoryId;
        $('#delete-form-modal').modal('show');
    };

    $scope.submitDeleteFeedForm = function(isValid) {
        feedService.deleteFeed($scope.formId).success(function() {
            var category = $filter('filter')($scope.categories, {id: $scope.formCategoryId}, true)[0];
            var feed = $filter('filter')(category.feeds, {id: $scope.formId}, true)[0];

            var index = category.feeds.indexOf(feed);
            if (index != -1) {
                category.feeds.splice(index, 1);
            }
            $('#delete-form-modal').modal('hide');
        });
    };
}]);
