define(function(require, exports, module){
    var $ = require('jquery');
	var std = require('std');
    var main = '';//主框架缓存变量
    var createpro = '<ul class="breadcrumb"><li><a href="/project/">项目管理</a><span class="divider">/</span></li><li class="active">创建项目</li></ul><form class="form-stacked" id="proform"> <fieldset><div class="clearfix"><label for="pname">名称</label><div class="input"><input type="text" id="pname" class="xlarge" size="30" name="pname" /></div></div><div class="clearfix"><label for="vcspath">版本控制地址</label><div class="input"><input type="text" id="vcspath" class="span8" size="256" name="vcspath" /><span class="help-block">比如：svn://192.168.1.253:4000/code/v2/branches/pangu/</span></div></div><div class="clearfix"><label for="user">版本控制用户名</label><div class="input"><input type="text" id="user" name="user" /></div></div><div class="clearfix"><label for="pass">版本控制密码</label><div class="input"><input type="password" id="pass" name="pass" /></div></div></fieldset><div class="actions"><button id="prosubmit" class="btn primary">提交</button>&nbsp;<button class="btn" id="cancel">取消</button></div></form>';
	var successs = '';
	var cancel = 0;//是否点击了取消
	var packlist = '<ul class="breadcrumb"><li><a href="/project/">项目管理</a><span class="divider">/</span></li><li><a href="/project/">项目列表</a><span class="divider">/</span></li><li><span id="pname"></span><span class="divider">/</span></li><li class="active">打包</li></ul><input type="text" id="vids" name="vno" placeholder="输入版本号，多个版本号用空格隔开"/>&nbsp;<input type="hidden" id="pcurid" /><a href="javascript:;" id="govcs" class="btn primary">提交</a>';
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
				if(data['res'] == 0)
				{
					std.alertErrorBox('proform', data['msg']);
					std.resetActive($('#prosubmit'));
					return false;
				}
				else
				{
					location.href = "/project/";
					return false;
				}
			});

			return false;
		});

		$('td[id^="vcs"]').live('dblclick', function(){
			var val = $(this).text();
			var id = $(this).attr('id');
			$(this).html('<input type="text" value="' + val + '" id="edit_' + id + '" />');
			$('#edit_' + id).focus();
		});

		$('input[id^="edit_"]').live('blur', function(){
			var val = $(this).val();
			var id = $(this).attr('id');
			if(!val){
				std.alertErrorBox('tlist', '该值不能为空');
				return false;
			}

			var p = id.split('_');
			std.getJson('post', '/project/update/', {name: p[1], id: p[2], val: val}, function(data){
				if(!data['res'])
					std.alertErrorBox('tlist', data['msg']);
				else
					$('#'+id).parent().html(val);
			});
		});

		function changeStatus(obj, status){
			std.active(obj);
			var checkboxs = $('input[name="pcheck[]"]:checked');
			if(!checkboxs.length)
			{
				std.alertErrorBox('tlist', '请至少选择一项1');
				std.resetActive(obj);
				return false;
			}

			var sValues = new Array();
			checkboxs.each(function(){sValues.push($(this).val());});
			std.getJson('post', '/project/change/', {checkboxs: sValues.join('|'), status: status}, function(data){
				if(!data['res'])
				{
					std.alertErrorBox('tlist', data['msg']);
					std.resetActive(obj);
				}
				else
					location.href = "/project/";
			});
		};

		$('#popen').live('click', function(){changeStatus(this, 1)});
		$('#pclose').live('click', function(){changeStatus(this, 2)});

		$('a[id^="package_"]').live('click', function(){
			var pInfo = $(this).attr('id').split('_');
			main = std.cacheMain();
			$('#main').hide().fadeIn('slow').html(packlist);
			$('#pname').html(pInfo[2]);
			$("#pcurid").val(pInfo[1]);
		});

		$('#govcs').live('click', function(){
			std.active(this);
			var vIds = $('#vids').val();
			var vIdsArr = vIds.split(' ');
			var vIdLen = vIdsArr.length;
			if(!vIdLen)
			{
				std.alertErrorBox('vids', '请输入版本号，多个版本号用空格隔开');
				std.resetActive(this);
				return false;
			}

			for(var i = 0; i < vIdLen; i++)//判断版本合法性
			{
				if(isNaN(vIdsArr[i]))
				{
					std.alertErrorBox('vids', '请输入纯数字版本号');
					std.resetActive(this);
					return false;
				}
			}

			vIds = vIds.split(' ').join('|');
			std.getJson('post', '/project/vcslist/', {vids: vIds}, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('vids', data['msg']);
					std.resetActive($('#govcs'));
					return false;
				}
				else
				{
					alert(data['text']);
				}
			});
		});
	};
});
