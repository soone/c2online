define(function(require, exports, module){
    var $ = require('jquery');
	var std = require('std');
    var main = '';//主框架缓存变量
    var createpro = '<ul class="breadcrumb"><li><a href="#">项目管理</a><span class="divider">/</span></li><li class="active">创建项目</li></ul><form class="form-stacked" id="proform"> <fieldset><div class="clearfix"><label for="pname">名称</label><div class="input"><input type="text" id="pname" class="xlarge" size="30" name="pname" /></div></div><div class="clearfix"><label for="vcspath">版本控制地址</label><div class="input"><input type="text" id="vcspath" class="span8" size="256" name="vcspath" /><span class="help-block">比如：svn://192.168.1.253:4000/code/v2/branches/pangu/</span></div></div><div class="clearfix"><label for="user">版本控制用户名</label><div class="input"><input type="text" id="user" name="user" /></div></div><div class="clearfix"><label for="pass">版本控制密码</label><div class="input"><input type="password" id="pass" name="pass" /></div></div></fieldset><div class="actions"><button id="prosubmit" class="btn primary">提交</button>&nbsp;<button class="btn" id="cancel">取消</button></div></form>';
	var cancel = 0;//是否点击了取消
	exports.init = function(){
        $('#createpro').live('click', function(){//显示创建表单
			main = std.cacheMain();
			$('#main').hide().fadeIn('slow').html(createpro);
        });

		$('#cancel').live('click', function(){//点击取消按钮
			cancel = std.cancel('main', main);
		});

		$('#proform').live('submit', function(){//提交创建表单
			std.active($('#prosubmit'));
			$('#prosubmit').attr('disabled', true);
			var postData ={};
			postData.pname = $('#pname').val();
			postData.vcs = $('#vcspath').val();
			postData.vcsuser = $('#user').val();
			postData.vcspass = $('#pass').val();
			if(std.validAllNotEmpty(postData) == false)
			{
				std.alertErrorBox('proform', '各项都不能为空');
				std.resetActive($('#prosubmit'));
				return false;
			}

			std.getJson('post', '/project/create/', postData, function(data){
				alert(data['pname']);
				std.resetActive($('#prosubmit'));
			});

			return false;
		});
	};
});
