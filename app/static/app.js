/**
 * Created by huangjianting on 2018/1/5.
 */

var app = angular.module('myApp', ['ngSanitize']);
app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.controller('myCtrl', function($scope, $http) {
    // source
    $scope.app_get = function (url_data, param, callback, error_call_back) {
        var url = '/api/' + url_data;
        $http(
            {
                method: 'GET',
                url: url,
                params: param
            }
        ).success(function(data, status, headers, config) {
            if(data.state===1){
                callback(data);
            }else{
                error_call_back();
                alert(url + '\n' +data.message);
            }
        }).error(function(data, status, headers, config){
            error_call_back();
            alert(status);
        });
    };
    $scope.app_post = function (url, post_data, callback, error_callback) {
        $http.post(url, post_data).then(
            function successCallback(response) {
                if(response.data.state===1){
                    callback(response);
                }else{
                    error_callback(response);
                    alert(url + '\n' + JSON.stringify(post_data) + '\n' + response.data.message);
                }
                // callback(response);
            },
            function errorCallback(response) {
                console.log(response);
                    if(response.status===500){
                        alert('500 服务器异常')
                    }else if(response.status===404){
                        alert('404 页面不存在')
                    }else{
                        alert(response.status + '与服务器连接中断')
                    }
                error_callback(response);
            }
        );
    };
    $scope.api_post = function (url_data, post_data, callback, error_callback) {
        var url = '/api/' + url_data;
        $scope.app_post(url, post_data, callback, error_callback);
    };
    // win_service
    $scope.win_service_list_reset = function () {
        $scope.win_service_list_now = [];
        $scope.win_service_list = [];
        $scope.win_service_10_list = [];
        $scope.win_service_20_list = [];
        $scope.win_service_other_list = [];
    };
    $scope.get_win_service_list = function () {
        $scope.win_service_list_reset();
        $scope.win_service_reload_loading = 'loading';
        $scope.app_get(
            "win_service",
            {},
            // function (data) {$scope.win_service_list = data.data;}
            function (data) {
                $scope.win_service_list = data.data;
                $scope.win_service_split();
                $scope.check_win_service_radio();
                $scope.win_service_reload_loading = '';
            },
            function () {
                $scope.win_service_reload_loading = '';
            }
        )
    };
    $scope.get_win_service_one = function(win_service_index){
        $scope.app_get(
            "win_service",
            {name: $scope.win_service_list_now[win_service_index].name},
            function (data) {
                $scope.win_service_list_now[win_service_index].service_state = data.data[0].service_state;
                $scope.win_service_list_now[win_service_index].is_reloading = '';
                if($scope.win_service_list_now[win_service_index].service_state!=="1  STOPPED "
                    && $scope.win_service_list_now[win_service_index].service_state!=="4  RUNNING "){
                        $scope.win_service_all_loading(win_service_index, 1);
                        setTimeout(function(){$scope.get_win_service_one(win_service_index)}, 2000);
                }else{
                    $scope.win_service_all_loading(win_service_index, 0);
                }
            },
            function () {
                $scope.win_service_list_now[win_service_index].is_reloading = '';
            }
        )
    };
    // $scope.start_win_service_one = function(win_service_index){
    //     $scope.api_post(
    //         "win_service",
    //         {name: $scope.win_service_list_now[win_service_index].name, method: "start"},
    //         function (data) {
    //             // console.log(data);
    //             $scope.win_service_list_now[win_service_index].service_state = data.data.data[0].service_state;
    //             // $scope.win_service_list_now[win_service_index].is_starting = '';
    //             $scope.win_service_all_loading(win_service_index, 1);
    //             $scope.get_win_service_one(win_service_index);
    //         },
    //         function () {
    //             // $scope.win_service_all_loading(win_service_index, 0);
    //             $scope.get_win_service_one(win_service_index);
    //         }
    //     )
    // };
    // $scope.stop_win_service_one = function(win_service_index){
    //     $scope.api_post(
    //         "win_service",
    //         {name: $scope.win_service_list_now[win_service_index].name, method: "stop"},
    //         function (data) {
    //             // console.log(data);
    //             $scope.win_service_list_now[win_service_index].service_state = data.data.data[0].service_state;
    //             // $scope.win_service_list_now[win_service_index].is_starting = '';
    //             $scope.win_service_all_loading(win_service_index, 1);
    //             $scope.get_win_service_one(win_service_index);
    //         },
    //         function () {
    //             // $scope.win_service_all_loading(win_service_index, 0);
    //             $scope.get_win_service_one(win_service_index);
    //         }
    //     )
    // };
    $scope.post_win_service_one = function(win_service_index, method){
        $scope.api_post(
            "win_service",
            {name: $scope.win_service_list_now[win_service_index].name, method: method},
            function (data) {
                // console.log(data);
                $scope.win_service_list_now[win_service_index].service_state = data.data.data[0].service_state;
                // $scope.win_service_list_now[win_service_index].is_starting = '';
                $scope.win_service_all_loading(win_service_index, 1);
                $scope.get_win_service_one(win_service_index);
            },
            function () {
                // $scope.win_service_all_loading(win_service_index, 0);
                $scope.get_win_service_one(win_service_index);
            }
        )
    };
    $scope.win_service_all_loading = function (win_service_index, load_type) {
        if(load_type===1){
            $scope.win_service_list_now[win_service_index].is_reloading = "loading";
            $scope.win_service_list_now[win_service_index].is_starting = "loading";
            $scope.win_service_list_now[win_service_index].is_stoping = "loading";
        }else{
            $scope.win_service_list_now[win_service_index].is_reloading = "";
            $scope.win_service_list_now[win_service_index].is_starting = "";
            $scope.win_service_list_now[win_service_index].is_stoping = "";
        }
    };
    $scope.win_service_split = function () {
        $scope.win_service_10_list = [];
        $scope.win_service_20_list = [];
        $scope.win_service_other_list = [];
        for(var i=0;i<$scope.win_service_list.length;i++) {
            $scope.win_service_list[i].is_reloading = "";
            $scope.win_service_list[i].is_starting = "";
            $scope.win_service_list[i].is_stoping = "";
            if($scope.win_service_list[i].service_type === "10  WIN32_OWN_PROCESS  "){
                $scope.win_service_10_list.push($scope.win_service_list[i]);
            }else if($scope.win_service_list[i].service_type === "20  WIN32_SHARE_PROCESS  "){
                $scope.win_service_20_list.push($scope.win_service_list[i]);
            }else{
                $scope.win_service_other_list.push($scope.win_service_list[i]);
            }
        }
    };
    $scope.check_win_service_radio = function () {
        var win_service_selected=$('input:radio[name="win_service_radio"]:checked').val();
        if(win_service_selected==="10"){
            $scope.win_service_list_now = $scope.win_service_10_list;
        }else if(win_service_selected==="20"){
            $scope.win_service_list_now = $scope.win_service_20_list;
        }else{
            $scope.win_service_list_now = $scope.win_service_other_list;
        }
    };
    $scope.win_service_reload_one = function (win_service_index) {
        // $scope.win_service_list_now[win_service_index].is_reloading = 'loading';
        $scope.win_service_all_loading(win_service_index, 1);
        $scope.get_win_service_one(win_service_index);
    };
    $scope.win_service_start_one = function (win_service_index) {
        // $scope.win_service_list_now[win_service_index].is_starting = 'loading';
        $scope.win_service_all_loading(win_service_index, 1);
        // $scope.start_win_service_one(win_service_index)
        $scope.post_win_service_one(win_service_index, 'start')
    };
    $scope.win_service_stop_one = function (win_service_index) {
        // $scope.win_service_list_now[win_service_index].is_stoping = 'loading';
        $scope.win_service_all_loading(win_service_index, 1);
        // $scope.stop_win_service_one(win_service_index)
        $scope.post_win_service_one(win_service_index, 'stop')
    };
    // iis
    $scope.get_iis_list = function () {
        // $scope.win_service_list_reset();
        $scope.iis_list = [];
        $scope.iis_reload_loading = 'loading';
        $scope.app_get(
            "iis",
            {},
            // function (data) {$scope.win_service_list = data.data;}
            function (data) {
                $scope.iis_list = data.data;
                for(var i=0;i<$scope.iis_list.length;i++) {
                    $scope.iis_list[i].is_reloading = '';
                    $scope.iis_list[i].is_starting = '';
                    $scope.iis_list[i].is_stoping = '';
                }
                $scope.iis_reload_loading = '';
            },
            function () {
                $scope.iis_reload_loading = '';
            }
        )
    };
    $scope.get_iis_one = function(iis_index){
        $scope.app_get(
            "iis",
            {name: $scope.iis_list[iis_index].name},
            function (data) {
                $scope.iis_list[iis_index] = data.data[0];
                // $scope.iis_list[iis_index].is_reloading = '';
                // $scope.iis_list[iis_index].is_starting = '';
                // $scope.iis_list[iis_index].is_stoping = '';
                $scope.iis_all_loading(iis_index, 0);
            },
            function () {
                $scope.iis_all_loading(iis_index, 0);
            }
        )
    };
    $scope.post_iis_one = function(iis_index, method){
        $scope.api_post(
            "iis",
            {name: $scope.iis_list[iis_index].name, method: method},
            function (data) {
                console.log(data);
                $scope.iis_all_loading(iis_index, 1);
                alert(data.data.data);
                $scope.get_iis_one(iis_index);
            },
            function (data) {
                // alert(data.data.data);
                $scope.get_iis_one(iis_index);
            }
        )
    };
    $scope.iis_all_loading = function (iis_index, type) {
        if (type===1){
            $scope.iis_list[iis_index].is_reloading = 'loading';
            $scope.iis_list[iis_index].is_starting = 'loading';
            $scope.iis_list[iis_index].is_stoping = 'loading';
        }else{
            $scope.iis_list[iis_index].is_reloading = '';
            $scope.iis_list[iis_index].is_starting = '';
            $scope.iis_list[iis_index].is_stoping = '';
        }
    };
    $scope.iis_reload_one = function (iis_index) {
        $scope.iis_all_loading(iis_index, 1);
        $scope.get_iis_one(iis_index);
    };
    $scope.iis_start_one = function (iis_index) {
        $scope.iis_all_loading(iis_index, 1);
        $scope.post_iis_one(iis_index, 'start')
    };
    $scope.iis_stop_one = function (iis_index) {
        $scope.iis_all_loading(iis_index, 1);
        $scope.post_iis_one(iis_index, 'stop')
    };
});

app.filter('win_service_state', function(){
    return function(value){
        if(value === "1  STOPPED "){return "ui inverted red table";}
        else if(value === "4  RUNNING "){return "ui inverted green table";}
        else{return "ui inverted yellow table";}
    }
});
app.filter('win_service_state2', function(){
    return function(value){
        if(value === "1  STOPPED "){return "negative";}
        else if(value === "4  RUNNING "){return "positive";}
        else{return "warning";}
    }
});
app.filter('iis_state', function(){
    return function(value){
        if(value === "Stopped"){return "negative";}
        else if(value === "Started"){return "positive";}
        else{return "warning";}
    }
});