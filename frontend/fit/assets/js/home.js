(function(){
    var app = angular.module('fitapp', []);
    // session doc: https://medium.com/opinionated-angularjs/techniques-for-authentication-in-angularjs-applications-7bbf0346acec

    app.constant('AUTH_EVENTS', {
        loginSuccess: 'auth-login-success',
        loginFailed: 'auth-login-failed',
        logoutSuccess: 'auth-logout-success',
        sessionTimeout: 'auth-session-timeout',
        notAuthenticated: 'auth-not-authenticated',
        notAuthorized: 'auth-not-authorized'
    });


    app.constant('USER_ROLES', {
        user: 'user',
        guest: 'guest'
    });


    app.controller('HomeController', ['$scope', 'USER_ROLES', 'AuthService', function ($scope, USER_ROLES, AuthService){
        $scope.currentUser = null;
        $scope.userRoles = USER_ROLES;
        $scope.isAuthorized = AuthService.isAuthorized;
        $scope.setCurrentUser = function(user){
            $scope.currentUser = user;
        };
    }]);


    app.controller('LoginController', ['$scope', '$rootScope', 'AUTH_EVENTS', 'AuthService', function ($scope, $rootScope, AUTH_EVENTS, AuthService) {
        $scope.credentials = {
            username: '',
            password: ''
        };
        $scope.login = function (credentials) {
            AuthService.login(credentials).then(function (user) {
                $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
                $scope.setCurrentUser(user);
            }, function () {
                $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
            });
        };
    }]);


    app.factory('AuthService', ['$http', 'Session', function ($http, Session){
        var serviceSite = "http://servicedev.justinerictaylor.com"
        var authService = {};
        authService.login = function(credentials){
            credentials.grant_type = "password";
            
            return $http
                .post(serviceSite+"/login", credentials)
                .then(function(res) {
                    debugger;
                    Session.create(res.data);
                    return res.data.user
                })
        };
        authService.isAuthenticated = function(){
            return !!Session.userId;
        };
        authService.isAuthorized = function (authorizedRoles){
            if (!angular.isArray(authorizedRoles)) {
                authorizedRoles = [authorizedRoles];
            }
            return (authService.isAuthenticated() && authorizedRoles.indexOf(Session.userRole) !== -1);
        };

        return authService;        
    }]);


    app.service('Session', function(){
        this.create = function(data){
            this.id = data.sessionId;
            this.userId = data.userId;
            this.userName = data.userName;
            this.userRole = data.userRole;
        };
        this.destroy = function(){
            this.id = null;
            this.userId = null;
            this.userName = null;
            this.userRole = null;
        };
        return this;
    });


})();