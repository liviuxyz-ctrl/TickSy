let reset_register_form = function(){
    window.location = '/register/'
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
                    if (response.successful_registration) {
                        swal({
                            icon: "success",
                            title: "Registration successful!",
                            text: "Provided information is valid!",
                            button: false,
                            closeOnEsc: false,
                            closeOnClickOutside: false,
                            timer: 1000
                        }).then(() => {
                            window.location = '/index/'
                        });
                    } else {
                        if (!response.validator_error_messages[0]) {
                            $.each(response.validator_error_messages, function (key, field) {
                                $.each(field, function (key, val) {
                                    if (val.code === "blank") {
                                        swal({
                                            icon: "error",
                                            title: "Registration failed!",
                                            text: "Fields cannot be empty!"
                                        }).then(() => {
                                            reset_register_form();
                                        });
                                    }
                                });
                            });
                            if (response.validator_error_messages.email) {
                                $.each(response.validator_error_messages.email, function (key, val) {
                                    if (val.message === "employees with this email already exists." && val.code === "unique") {
                                        swal({
                                            icon: "error",
                                            title: "Registration failed!",
                                            text: "Account with the provided email already exists."
                                        }).then(() => {
                                            reset_register_form();
                                        });
                                        return false;
                                    }
                                    if (val.message === "Enter a valid email address." && val.code === "invalid") {
                                        swal({
                                            icon: "error",
                                            title: "Registration failed!",
                                            text: "Enter a valid email address."
                                        }).then(() => {
                                            reset_register_form();
                                        });
                                        return false;
                                    }
                                });
                            }
                            if (response.validator_error_messages.password) {
                                swal({
                                    icon: "error",
                                    title: "Registration failed!",
                                    text: response.validator_error_messages.password[0].message
                                }).then(() => {
                                    reset_register_form();
                                });
                            }
                            if (response.validator_error_messages.team_name) {
                                swal({
                                    icon: "error",
                                    title: "Registration failed!",
                                    text: response.validator_error_messages.team_name[0].message
                                }).then(() => {
                                    reset_register_form();
                                });
                            }
                            if (response.validator_error_messages.re_password) {
                                swal({
                                    icon: "error",
                                    title: "Registration failed!",
                                    text: response.validator_error_messages.re_password[0].message
                                }).then(() => {
                                    reset_register_form();
                                });
                            }
                        }
                    }
                }
            }
        },
        error: function (xhr, status, error) {
            swal({
                icon: "error",
                title: "Internal server error!",
                text: "HTTP Error code: '" + xhr.status + " " + error + "'"
            }).then(() => {
                reset_register_form();
            });
        }
    });
});