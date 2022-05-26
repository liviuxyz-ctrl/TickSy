let reset_register_form = function(){
    $( "#register_form_full_name_input" ).val('')
    $( "#register_form_email_input" ).val('')
    $( "#register_form_password_input" ).val('')
    $( "#register_form_verify_password_input" ).val('')
    $( "#register_form_department_name_input" ).val('')
    $( "#register_form_team_name_input" ).val('')
};

$( "#register_form" ).submit(function( event ) {
    event.preventDefault();
    let register_form_data = $(this).serialize()
    $.ajax({
        url: '/register-api/',
        data: register_form_data,
        processData: false,
        type: 'POST',
        dataType: 'json',
        success: function (response) {
            if (response) {
                if (response.register_deny) {
                    window.location = '/index/'
                } else {
                    if (!response.validator_error_messages[0]) {
                        if (response.successful_registration) {
                            swal({
                                icon: "success",
                                title: "Register successful!",
                                text: "Provided credential are correct!",
                                button: false,
                                closeOnEsc: false,
                                closeOnClickOutside: false,
                                timer: 1000
                            }).then(() =>{
                                window.location = '/index/'
                            });
                        } else {
                            if (response.email_exists) {
                                swal({
                                    icon: "error",
                                    title: "Register failed!",
                                    text: "Account with the provided email already exist!"
                                }).then(() =>{
                                    reset_register_form();
                                });
                            }
                            else if(!response.team_exists){
                                swal({
                                icon: "error",
                                title: "Register failed!",
                                text: "Team name is not correct!"
                                }).then(() =>{
                                    reset_register_form();
                                });
                            }
                            else if(!response.successful_pwd_match){
                                swal({
                                icon: "error",
                                title: "Register failed!",
                                text: "Passwords don't match!"
                                }).then(() =>{
                                    reset_register_form();
                                });
                            }
                        }
                    }else{
                        swal({
                            icon: "error",
                            title: "Form completion error!",
                            text: response.validator_error_messages[0]
                        }).then(() =>{
                            reset_register_form();
                        });
                    }
                }
            }
        },
        error: function (xhr, status, error) {
            console.log(xhr.status);
            console.log(status);
            console.log(error)
        }
    });
});