let reset_create_ticket_form = function(){
    window.location = '/create-ticket/'
};

$( "#ticket_create_form" ).submit(function( event ) {
    event.preventDefault();
    let ticket_create_form_data = $(this).serialize()
    $.ajax({
        url: '/create-ticket-api/',
        data: ticket_create_form_data,
        processData: false,
        type: 'POST',
        dataType: 'json',
        success: function (response) {
            if (response) {
                if (response.create_ticket_deny) {
                    window.location = '/index/'
                } else {
                    if (response.ticket_successful_create) {
                        swal({
                            icon: "success",
                            title: "Ticket create successful!",
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
                                            reset_create_ticket_form();
                                        });
                                    }
                                });
                            });
                            if (response.validator_error_messages.user_email) {
                                $.each(response.validator_error_messages.user_email, function (key, val) {
                                    if (val.message === "Enter a valid email address." && val.code === "invalid") {
                                        swal({
                                            icon: "error",
                                            title: "Ticket creation failed!",
                                            text: "Enter a valid email address."
                                        }).then(() => {
                                            reset_create_ticket_form();
                                        });
                                        return false;
                                    }
                                });
                            }
                            if (response.validator_error_messages.responsible_team_id) {
                                swal({
                                    icon: "error",
                                    title: "Ticket creation failed!",
                                    text: response.validator_error_messages.responsible_team_id[0].message
                                }).then(() => {
                                    reset_create_ticket_form();
                                });
                            }
                            if (response.validator_error_messages.responsible_employee_id) {
                                swal({
                                    icon: "error",
                                    title: "Ticket creation failed!",
                                    text: response.validator_error_messages.responsible_employee_id[0].message
                                }).then(() => {
                                    reset_create_ticket_form();
                                });
                            }
                            if (response.validator_error_messages.due_datetime) {
                                swal({
                                    icon: "error",
                                    title: "Ticket creation failed!",
                                    text: response.validator_error_messages.due_datetime[0].message
                                }).then(() => {
                                    reset_create_ticket_form();
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
                reset_create_ticket_form();
            });
        }
    });
});