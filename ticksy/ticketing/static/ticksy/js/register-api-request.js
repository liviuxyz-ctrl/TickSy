let reset_login_form = function(){
    $( "#login_form_email_input" ).val('')
    $( "#login_form_password_input" ).val('')
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
                        if (response.successful_login) {
                            swal({
                                icon: "success",
                                title: "Login successful!",
                                text: "Provided credential are correct!",
                                button: false,
                                closeOnEsc: false,
                                closeOnClickOutside: false,
                                timer: 1000
                            }).then(() =>{
                                window.location = '/index/'
                            });
                        } else {
                            if (!response.email_exists) {
                                swal({
                                    icon: "error",
                                    title: "Login failed!",
                                    text: "Account with the provided email does not exist!"
                                }).then(() =>{
                                    reset_login_form();
                                });
                            }
                            else if(!response.successful_password_match){
                                swal({
                                icon: "error",
                                title: "Login failed!",
                                text: "Provided password is not correct!"
                                }).then(() =>{
                                    reset_login_form();
                                });
                            }
                        }
                    }
                    else{
                        swal({
                            icon: "error",
                            title: "Form completion error!",
                            text: response.validator_error_messages[0]
                        }).then(() =>{
                            reset_login_form();
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