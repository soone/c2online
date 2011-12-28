define(function(require, exports, module){
    var $ = require('jquery');
	var std = require('std');
	var main = std.cacheMain();//主框架缓存变量
    var createser = '<ul class="breadcrumb"><li><a href="/servers">服务器管理</a><span class="divider">/</span></li><li class="active">创建服务器</li></ul><form class="form-stacked" id="serform"><fieldset><div class="clearfix"><label for="pid">所属项目*</label><div class="input"><select name="pid" id="pid"><option value="">请选择</option></select></div></div><div class="clearfix"><label for="sname">名称*</label><div class="input"><input type="text" id="sname" class="xlarge" size="30" name="sname" /></div></div><div class="clearfix"><label for="pdir">生产地址*</label><div class="input"><input type="text" id="pdir" class="span8" size="256" name="pdir" /><span class="help-block">比如：/data/wwwV2/</span></div></div><div class="clearfix"><label for="pdir">备份地址*</label><div class="input"><input type="text" id="bdir" class="span8" size="256" name="bdir" /><span class="help-block">比如：/data/release/</span></div></div><div class="clearfix"><label for="spath">Host地址*</label><div class="input"><input type="text" id="spath" class="span8" size="256" name="spath" /><span class="help-block">比如：192.168.1.253</span></div></div><div class="clearfix"><label for="suser">用户名*</label><div class="input"><input type="text" id="suser" name="suser" /></div></div><div class="clearfix"><label for="spass">密码*</label><div class="input"><input type="password" id="spass" name="spass" /></div></div><div class="clearfix"><label for="vpnpro">vpn网关</label><div class="input"><select name="vpnpro" class="mini"><option value="1">PPTP</option></select>&nbsp;<input type="text" placeholder="192.168.1.253" id="svpn" class="span5" size="256" name="svpn" /></div></div><div class="clearfix"><label for="vpnname">vpn帐号</label><div class="input"><input type="text" id="vpnname" name="vpnname" /></div></div><div class="clearfix"><label for="vpnpass">vpn密码</label><div class="input"><input type="password" id="vpnpass" name="vpnpass" /></div></div></fieldset><div class="actions"><button class="btn primary" id="sersubmit">提交</button>&nbsp;<button class="btn" id="cancel">取消</button></div></form>';

	exports.init = function(){
		//显示创建表单
        $('#createser').live('click', function(){
			$('#main').hide().fadeIn('slow').html(createser);
			//取得服务器列表
			$.getJSON('/project/shortlist/', function(data){
				if(data['res'] == 1)
				{
					for(var i = 0, j = data['list'].length; i < j; i++)
					{
						$('#pid').append('<option value="' + data['list'][i].p_id + '">' + data['list'][i].p_name + '</option>');
					}
				}
				else
					std.alertErrorBox('serform', data['msg']);
			});
		});
		//点击取消按钮
		$('#cancel').live('click', function(){var cancel = std.cancel('main', main);});
		//提交创建表单
		$('#serform').live('submit', function(){
			std.active('sersubmit');
			$('#sersubmit').attr('disabled', true);
			var postData ={};
			postData.sname = $('#sname').val();
			postData.pdir = $('#pdir').val();
			postData.bdir= $('#bdir').val();
			postData.spath = $('#spath').val();
			postData.suser = $('#suser').val();
			postData.spass = $('#spass').val();
			postData.pid = $('#pid').val();
			if(std.validAllNotEmpty(postData) == false)
			{
				std.alertErrorBox('serform', '带*号不能为空');
				std.resetActive('sersubmit');
				return false;
			}

			postData.svpn = $('#svpn').val();
			postData.svpnname = $('#vpnname').val();
			postData.svpnpass = $('#vpnpass').val();

			std.getJson('post', '/servers/create/', postData, function(data){
				if(data['res'] == 0)
				{
					std.alertErrorBox('serform', data['msg']);
					std.resetActive('sersubmit');
					return false;
				}
				else
				{
					location.href = "/servers/";
					return false;
				}
			});

			return false;
		});

		//设置服务器列表信息为可编辑
		$('span[id^="ser"]').live('dblclick', function(){
			var val = $(this).text();
			var id = $(this).attr('id');
			$(this).html('<input type="text" value="' + val + '" id="edit_' + id + '" />');
			$('#edit_' + id).focus();
		});

		//保存服务器列表编辑项
		$('input[id^="edit_"]').live('blur', function(){
			var val = $(this).val();
			var id = $(this).attr('id');
			if(!val){
				std.alertErrorBox('tlist', '该值不能为空');
				return false;
			}

			var p = id.split('_');
			std.getJson('post', '/servers/update/', {name: p[2], id: p[3], val: val}, function(data){
				if(!data['res'])
					std.alertErrorBox('slist', data['msg']);
				else
					$('#'+id).parent().html(val);
			});
		});

		//服务器列表状态修改函数
		function changeStatus(obj, status){
			var id = $(obj).attr('id');
			std.active(id);
			var checkboxs = $('input[name="scheck"]:checked');
			if(!checkboxs.length)
			{
				std.alertErrorBox('slist', '请至少选择一项');
				std.resetActive(id);
				return false;
			}

			var sValues = new Array();
			checkboxs.each(function(){sValues.push($(this).val());});
			std.getJson('post', '/servers/change/', {checkboxs: sValues.join('|'), status: status}, function(data){
				if(!data['res'])
				{
					std.alertErrorBox('slist', data['msg']);
					std.resetActive(id);
				}
				else
					location.href = "/servers/";
			});
		};

		//服务器状态开启关闭操作
		$('#sopen').live('click', function(){changeStatus(this, 1)});
		$('#sclose').live('click', function(){changeStatus(this, 2)});

		//显示项目已经打包的列表
		$('a[id^="packlist_"]').live('click', function(){
			var pInfo = $(this).attr('id').split('_');
			showPackList(pInfo[2], pInfo[1]);
		});
	};
});
