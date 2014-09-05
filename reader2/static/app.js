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
        }
    };
}]);

app.controller('bodyController', ['$scope','$timeout','$document','itemService','categoryService', function($scope,$timeout,$document,itemService,categoryService) {

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
}]);