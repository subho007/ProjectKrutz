'use strict';

/* Filters */

angular.module('androidApp.filters', []).
  filter('interpolate', function (version) {
    return function (text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    };
  });
