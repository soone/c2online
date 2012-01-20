seajs.config({
    alias:{
        'jquery':'jquery-1.7.1.min.js',
    }
});

define(function(require, exports, module){
	$ = require('jquery');
	std = require('std');
	$(document).ready(function(){
		var qString = std.queryString();
		if(qString == 'login' || qString['login'])
		{
			if($('#loginwarning').length == 0)
			{
				std.alertErrorBox('main', 'Oops...请先登录，谢谢!!');
				$('#loginwarning').fadeOut(600).fadeIn(600);
			}
			$('#loginuserinput').focus();
		}

		$('#loginsubmit').live('click', function(){
			std.active('loginsubmit');
			var postData ={};
			postData.user = $('input[name="username"]').val();
			postData.pass = $('input[name="password"]').val();
			if(std.validAllNotEmpty(postData) == false)
			{
				std.alertErrorBox('main', 'Oops...请填写正确的用户名和密码');
				std.resetActive('loginsubmit');
				return false;
			}

			std.getJson('post', '/logged/login/', postData, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('main', data['msg']);
					std.resetActive('loginsubmit');
					return false;
				}
				else
				{
					//location.href = "/servers/";
					return false;
				}
			})
		})
	});

});
