define(function(require, exports, module){
    var $ = require('jquery');
	var std = require('std');
    var main = '';//主框架缓存变量
    var createpro = '<ul class="breadcrumb"><li><a href="/project/">项目管理</a><span class="divider">/</span></li><li class="active">创建项目</li></ul><form class="form-stacked" id="proform"> <fieldset><div class="clearfix"><label for="pname">名称</label><div class="input"><input type="text" id="pname" class="xlarge" size="30" name="pname" /></div></div><div class="clearfix"><label for="vcspath">版本控制地址</label><div class="input"><input type="text" id="vcspath" class="span8" size="256" name="vcspath" /><span class="help-block">比如：svn://192.168.1.253:4000/code/v2/branches/pangu</span></div></div><div class="clearfix"><label for="user">版本控制用户名</label><div class="input"><input type="text" id="user" name="user" /></div></div><div class="clearfix"><label for="pass">版本控制密码</label><div class="input"><input type="password" id="pass" name="pass" /></div></div></fieldset><div class="actions"><button id="prosubmit" class="btn primary">提交</button>&nbsp;<button class="btn" id="cancel">取消</button></div></form>';
	var successs = '';
	var cancel = 0;//是否点击了取消
	var goPack = '<ul class="breadcrumb"><li><a href="/project/">项目管理</a><span class="divider">/</span></li><li><a href="/project/">项目列表</a><span class="divider">/</span></li><li><span id="pname"></span><span class="divider">/</span></li><li class="active">打包</li></ul><input type="text" id="vids" name="vno" placeholder="输入版本号，多个版本号用半角逗号隔开"/>&nbsp;<input type="hidden" id="pcurid" /><a href="javascript:;" id="govcs" class="btn primary">提交</a>';
	var listTable = '<table><thead><th class="span1"><input type="checkbox" id="alltotal" name="all" /></th><th>vcs号</th><th>文件</th></thead><tbody></tbody></table><div class="well"><input type="text" name="version" id="version" class="normal" placeholder="请填写对外版本号"/>&nbsp;<a href="javascript:;" id="startpack" class="btn danger">开始打包</a><span class="help-block">如：2.0.15.r5798或者2.0.16.r5799.p15(补丁的版本号规则)</span>';
	var packList = '<ul class="breadcrumb"><li><a href="/project/">项目管理</a><span class="divider">/</span></li><li><a href="/project/">项目列表</a><span class="divider">/</span></li><li><span id="pname"></span><span class="divider">/</span></li><li class="active">包列表</li></ul><table id="listtable"><thead><tr><th>#</th><th>版本号</th><th>创建时间</th><th>状态</th><th>最后发布服务器</th><th>最后发布时间</th><th>操作</th></tr></thead><tbody></tbody><tfoot></tfoot></table></table>';

	exports.init = function(){
		//显示创建表单
        $('#createpro').live('click', function(){
			main = std.cacheMain();
			$('#main').hide().fadeIn('slow').html(createpro);
        });

		//点击取消按钮
		$('#cancel').live('click', function(){
			cancel = std.cancel('main', main);
		});

		//提交创建表单
		$('#proform').live('submit', function(){
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

		//设置项目列表信息为可编辑
		$('td[id^="vcs"]').live('dblclick', function(){
			var val = $(this).text();
			var id = $(this).attr('id');
			$(this).html('<input type="text" value="' + val + '" id="edit_' + id + '" />');
			$('#edit_' + id).focus();
		});

		//保存项目列表编辑项
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

		//项目列表状态修改函数
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

		//项目状态开启关闭操作
		$('#popen').live('click', function(){changeStatus(this, 1)});
		$('#pclose').live('click', function(){changeStatus(this, 2)});

		//显示打包操作
		$('a[id^="package_"]').live('click', function(){
			var pInfo = $(this).attr('id').split('_');
			main = std.cacheMain();
			$('#main').hide().fadeIn('slow').html(goPack);
			$('#pname').html(pInfo[2]);
			$("#pcurid").val(pInfo[1]);
		});

		//根据版本号显示项目打包的文件信息
		$('#govcs').live('click', function(){
			std.active(this);
			var vIds = $('#vids').val();
			var vIdsArr = vIds.split(',');
			var vIdLen = vIdsArr.length;
			var pro = $('#pcurid').val();
			if(!vIdLen)
			{
				std.alertErrorBox('vids', '请输入版本号，多个版本号用半角逗号隔开');
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

			vIds = vIds.split(',').join('|');
			std.getJson('post', '/project/vcslist/', {pro: pro, vids: vIds}, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('vids', data['msg']);
					std.resetActive($('#govcs'));
					return false;
				}
				else
				{
					if($('#main > table').length == 0) $('#main').append(listTable);
					$('#main > table > tbody').html('');
					var tbodys = [];
					for(var i = 0, j = data['logs'].length; i < j; i++)
					{
						var files = [];
						for(var x = 0, y = data['logs'][i][1].length; x < y; x++)
						{
							files.push('<li><input type="checkbox" name="vf[]" id="vf_' + data['logs'][i][0] + '_' + x + '" value="' + data['logs'][i][0] + '::' + data['logs'][i][1][x][0] + '::' + data['logs'][i][1][x][1] + '"/><span class="help-inline">' + data['logs'][i][1][x][0] + ' ' +  data['logs'][i][1][x][1] + '</span></li>');
						}

						$('#main > table > tbody').append('<tr><td><input type="checkbox" id="total_' + data['logs'][i][0] + '" name="all" /></td><td><p>r' + data['logs'][i][0] + '</p></td><td><ul class="unstyled packhide">' + files.join('') + '</ul></td></tr>');
					}

					std.resetActive($('#govcs'));
				}
			});
		});

		//项目打包文件选项操作开始
		$('input[id^="total_"]').live('click', function(){
			var id = $(this).attr('id').split('_')[1];
			var val = $(this).attr('checked');
			var checked = val == 'checked' ?  true : false;
			$('input[id^="vf_'+id+'"]').each(function(){$(this).attr('checked', checked)});
		});

		$('#alltotal').live('click', function(){
			var val = $(this).attr('checked');
			var checked = val == 'checked' ?  true : false;
			$('input[id^="total_"]').each(function(){$(this).attr('checked', checked)});
			$('input[id^="vf_"]').each(function(){$(this).attr('checked', checked)});
		});

		$('input[id^="vf_"]').live('click', function(){
			var id = $(this).attr('id');
			var idArr = id.split('_');
			var totalId = 'total_' + idArr[1];
			var vfIds = idArr[0] + '_' + idArr[1];
			var val = $(this).attr('checked');
			if(val != 'checked')
			{
				$('#' + totalId).attr('checked', false);
				$('#alltotal').attr('checked', false);
			}
			else if($('input[id^="' + vfIds + '"]:checked').length == $('input[id^="' + vfIds + '"]').length)
					$('#' + totalId).attr('checked', true);
		});
		//项目打包文件选项操作结束

		//打版本号操作
		$('#startpack').live('click', function(){
			var isSub = $(this).attr('class').indexOf('disabled');
			std.active(this);
			var checkboxs = $('input[id^="vf_"]:checked');
			var version = $('#version').val();
			if(!checkboxs.length || !version)
			{
				std.alertErrorBox('version', '请填写版本号并且至少选择一个文件');
				std.resetActive(this);
				return false;
			}

			if(isSub > -1) return false;
			//组织数据发送服务器
			var pro = $('#pcurid').val();
			var cVals = [];
			checkboxs.each(function(){cVals.push($(this).val())});
			std.getJson('post', '/project/package/', {verno : version, pro : pro, vals : cVals.join('|')}, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('version', data['msg']);
					std.resetActive($('#startpack'));
					return false;
				}
				else
					showPackList($('#pname').text(), pro);
			});
		});

		//显示项目已经打包的列表
		$('a[id^="packlist_"]').live('click', function(){
			var pInfo = $(this).attr('id').split('_');
			showPackList(pInfo[2], pInfo[1]);
		});

		function showPackList(pName, pId)
		{
			$('#main').hide().fadeIn('slow').html(packList);
			$('#pname').html(pName);
			$('#listtable').ready(function(){
				$('#listtable tbody').html('<tr><td colspan="7" style="text-align:center">正在读取,请稍候...</td></tr>');
				//std.getJson('GET', '/project/packlist/?pro=' + pId, {}, function(data){
				$.getJSON('/project/packlist/?pro='+pId, {pro : pId}, function(data){
					if(data['res'] == 1)
					{

						return false;
					}
					else
						$('table[id="listtable"] > tbody > tr > td').html(data['msg']);
				});
			});
		}
	};
});
