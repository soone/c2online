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
					std.loginDisplay(data['uInfo']);
					return false;
				}
			});
		});

		$('#logout').live('click', function(){
			std.active('logout');
			std.getJson('get', '/logged/logout/', {}, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('main', data['msg']);
					std.resetActive('logout');
					return false;
				}
				else
				{
					location.href = data['redirect'];
					return false;
				}
			});
		});

		$('#logset').live('click', function(){
			var setLists = '<ul class="breadcrumb"><li><a href="/">首页</a><span class="divider">/</span>用户设置</li></ul><table id="ulist"><thead><tr><th>#</th><th>用户名</th><th>状态</th><th>创建时间</th><th>操作</th></tr></thead><tbody></tbody></table>';
			$('#main').hide().fadeIn('slow').html(setLists);
			std.getJson('get', '/users', {}, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('main', data['msg']);
					return false;
				}
				else
				{
					var users = data['users'];
					var tbodys = [];
					for(var i = 0, j = users.length; i < j; i++)
					{
						var ts = '<tr><td>' + users[i].adm_id + '</td>';
						ts += '<td>' + users[i].adm_user + '</td><td>';
						ts += users[i].adm_status == 1 ? '<span class="label success">正常</span>&nbsp;' : '<span class="label warning">关闭</span>';
						ts += '</td>';
						ts += '<td>' + std.getLocalTime(users[i].adm_dateline) + '</td><td>';
						ts += '';
						ts += (data['curId'] == users[i].adm_id || (data['curId'] == users[i].adm_id && users[i].adm_auth == 1)) ? '&nbsp;<a href="javascript:;" id="setpass_' + users[i].adm_id + '" class="btn">修改密码</a>' : '';
						if(data['curId'] == users[i].adm_id && users[i].adm_auth == 1)
						{
							ts += users[i].adm_status == 1 ? '&nbsp;<a href="javascript:;" id="admstatus_' + users[i].adm_id + '_0" class="btn">设为关闭</a>' : '&nbsp;<a href="javascript:;" id="admstatus_' + users[i].adm_id + '_1" class="btn">设为打开</a>';
						}

						ts += '</td></tr>';
						tbodys.push(ts);
						ts = '';
					}

					$('#ulist > tbody').html(tbodys.join(''));
					return false;
				}
			});

			$('a[id^="setpass_"]').live('click', function(){
				var id = $(this).attr('id').split('_')[1];
			});

			$('a[id^="admstatus_"]').live('click', function(){
				var tArr = $(this).attr('id').split('_');
				var id = tArr[1];
				var sta = tArr[2];
			});
		});
	});

});
