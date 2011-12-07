define(function(require, exports, module){
    var $ = require('jquery');
    var main = '';
    var createpro = '<ul class="breadcrumb"><li><a href="#">项目管理</a><span class="divider">/</span></li><li class="active">创建项目</li></ul><form class="form-stacked"> <fieldset><div class="clearfix"><label for="pname">名称</label><div class="input"><input type="text" id="pname" class="xlarge" size="30" name="pname" /></div></div><div class="clearfix"><label for="vcspath">版本控制地址</label><div class="input"><input type="text" id="vcspath" class="span8" size="256" name="vcspath" /><span class="help-block">比如：svn://192.168.1.253:4000/code/v2/branches/pangu/</span></div></div><div class="clearfix"><label for="user">版本控制用户名</label><div class="input"><input type="text" id="user" name="user" /></div></div><div class="clearfix"><label for="pass">版本控制密码</label><div class="input"><input type="password" id="pass" name="pass" /></div></div></fieldset><div class="actions"><button class="btn primary" type="submit">提交</button>&nbsp;<a class="btn" id="cancel">取消</a></div></form>';
    exports.show = function(id){
        if(id == 'createpro') id = createpro;
        main = $('#main').html();
        $('#main').hide().show('slow').html(id);
        //$('#main').show('slow');
    };

    exports.cancel = function(){
        $('#main').hide().show('slow').html(main);    
    };

});
