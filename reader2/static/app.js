var app = angular.module('reader', ['ngSanitize']);

app.factory('itemService', ['$http', function($http) {
    return {
        getItems: function (feedId) {
            if (typeof feedId === 'undefined') {
                return $http.get('api/items/');
            } else {
                return $http.get('api/items/?feedId=' + feedId);
            }
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

    $scope.activeItem = -1;

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

    $scope.activateItem = function(i) {
        if ($scope.activeItem == i) {
            $scope.activeItem = -1;
        } else {
            $scope.activeItem = i;
        }
    };

    $scope.getItems = function(feedId) {
        itemService.getItems(feedId).success(function(data) {
            console.log(data.length);
            $scope.items = data;
        });
        $scope.activeItem = -1;
    };

    $scope.getCategories = function() {
        categoryService.getCategories().success(function(data) {
            $scope.categories = data;
        });
    };

    $scope.getItems();
    $scope.getCategories();
}]);