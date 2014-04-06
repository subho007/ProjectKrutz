'use strict';

/* Controllers */

angular.module('androidApp.controllers', []).
  controller('AppController', function ($scope, $location) {

    $scope.isCollapsed = true;

    $scope.$on('$routeChangeSuccess', function() {
      $scope.isCollapsed = true;
    });

    $scope.getClass = function(path) {
      if (path === '/') {
        if ($location.path() === '/') {
          return 'active';
        } else {
          return '';
        }
      }

      if ($location.path().substr(0, path.length) === path) {
        return 'active';
      } else {
        return '';
      }
    }
    
  }).
  controller('DataController', function ($scope, $http) {

    // Rows of APK data from the database
    $http({
        method: 'GET',
        url: '/api/rows'
      }).
      success(function (data, status, headers, config) {
        $scope.rows = data;
        $scope.totalItems = $scope.rows.length;
      }).
      error(function (data, status, headers, config) {
        $scope.rows = 'Error!';
    });

    // Download format dropdown
    $scope.disabled = undefined;

    $scope.enable = function() {
      $scope.disabled = false;
    };

    $scope.disable = function() {
      $scope.disabled = true;
    };

    $scope.clear = function() {
      $scope.format.selected = undefined;
    };

    $scope.format = {};
    $scope.formats = [
      'XML',
      'JSON',
      'CSV'
    ];

    // Pagination
    $scope.totalItems = 1;
    $scope.currentPage = 1;
    $scope.itemsPerPage = 25;
    $scope.maxSize = 5;

    $scope.getPaginatedRows = function() {
      if ($scope.rows) {
        return $scope.rows.slice(($scope.currentPage - 1) * $scope.itemsPerPage, ($scope.itemsPerPage * $scope.currentPage) - 1);
      }
    };

  }).
  controller('AboutController', function ($scope) {

    $scope.message = 'About';

  });
