var app = angular.module('reader', ['ngSanitize','infinite-scroll']);

app.factory('itemService', ['$http', function($http) {
    return {
        getItems: function(params) {
            return $http.get('api/items/', {params: params});
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

app.controller('bodyController', ['$scope', 'itemService', 'categoryService', function($scope,itemService,categoryService) {

    $scope.activeFeed = -1;

    $scope.activeItem = -1;

    $scope.canScroll = false;

    $scope.first = function() {
        $scope.activeItem = 0;
    };

    $scope.prev = function() {
        if ($scope.activeItem >= 0) {
            $scope.activeItem -= 1;
        }
    };
    
    $scope.next = function() {
        $scope.activeItem += 1;
    };

    $scope.setActiveFeed = function(id) {
        $scope.activeFeed = id;
        $scope.activeItem = -1;

        itemService.getItems({
            'feed': $scope.activeFeed
        }).success(function(data) {
            $scope.items = data;
            $scope.canScroll = true;
        });
    };

    $scope.setActiveItem = function(i) {
        if ($scope.activeItem == i) {
            $scope.activeItem = -1;
        } else {
            $scope.activeItem = i;
        }
    };

    $scope.loadMoreItems = function() {
        if ($scope.canScroll){
            itemService.getItems({
                'begin': $scope.items.length + 1,
                'nrows': 5,
                'feed': $scope.activeFeed
            }).success(function(data) {
                if (data.length > 0) {
                    $scope.items = $scope.items.concat(data);
                } else {
                    // everything is here, disabling infinite scroll
                    $scope.canScroll = false;
                }
            });
        }
    };

    categoryService.getCategories().success(function(data) {
        $scope.categories = data;
    });
    
    itemService.getItems().success(function(data) {
        $scope.items = data;
        $scope.canScroll = true;
    });
}]);