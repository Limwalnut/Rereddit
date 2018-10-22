function set_cookie(name,value)
{
    var Days = 1;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days*24*60*60*1000);
    document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}

function get_cookie(name)
{
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

function del_cookie(name)
{
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval=getCookie(name);
    if(cval!=null)
        document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}

$(document).ready(function(){
    $('#login-modal').modal({
        dismissible: false
    });
    $('.dropdown-trigger').dropdown({
        hover: true,
        inDuration: 300,
        outDuration: 225,
        belowOrigin: true,
        alignment: 'right'
    });
    var show_mode = get_cookie("show_mode");
    var html_body = document.getElementById("body");

    if(show_mode == "dark-mode"){
        show_mode = "dark-mode";
        html_body.className = show_mode;
        $('#dark-switch input').attr("checked",true)

    }else{
        show_mode = "light-mode";
        html_body.className = show_mode;
        $('#dark-switch input').attr("checked",false)

    }
});

//open login modal
function login_button_click(){
    $('#login-modal').modal('open')
}

//close login modal
function login_modal_close(){
    $('#login-modal').modal('close')
}

//check username or password at frontend side (it will check at backend twice)
function on_login_submit(){
    if ($('#username').val() == 0 || $('#password').length == 0){
        //show alert
        $('#login-alert').css('display','initial');
        return false;
    }else{
        $('#login-modal').modal('close')
        return true;
    }
}

function toggle_dark_mode() {
    var html_body = document.getElementById("body");
    var show_mode = get_cookie("show_mode") == "dark-mode" ? "light-mode" : "dark-mode";
    html_body.className = show_mode;
    set_cookie("show_mode", show_mode);
}

function on_ginup_submit(){
    if($('#password1').val() == $('#password2').val()){
        $('#password2').removeClass('invalid');
        $('#password2').addClass('valid');
        return true;
    }else {
        $('#password2').removeClass('valid');
        $('#password2').addClass('invalid');
        return false
    }
}
