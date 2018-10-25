function set_cookie(name,value)
{
    $.cookie(name ,value ,{path:'/'});
}

function get_cookie(name)
{
    return $.cookie(name);
}

function del_cookie(name)
{
    $.cookie(name ,null);
}


$(document).ready(function(){
    $('#login-modal').modal({
        dismissible: false
    });
    $('.modal').modal();
    $('.sidenav').sidenav();
    $('.dropdown-trigger').dropdown({
        hover: true,
        inDuration: 300,
        outDuration: 225,
        belowOrigin: true,
        alignment: 'right'
    });
    check_dark_mode();
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

function check_dark_mode(){
    var show_mode = get_cookie("show_mode");
    $('#body').removeAttr('class');

    if(show_mode == null){}else{
        if(show_mode == "dark-mode"){
            $('#dark-switch input').attr("checked",true)
        }else if(show_mode == "light-mode"){
            $('#dark-switch input').attr("checked",false)
        }
        $('#body').addClass(show_mode)
    }
}

function toggle_dark_mode() {
    var show_mode = get_cookie("show_mode");
    $('#body').removeAttr('class');

    if(show_mode == "dark-mode"){
        show_mode = "light-mode";

    }else{
        show_mode = "dark-mode";
    }
    $('#body').addClass(show_mode);
    set_cookie("show_mode",show_mode);
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
