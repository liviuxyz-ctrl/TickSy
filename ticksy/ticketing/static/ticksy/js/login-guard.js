$( document ).ready(function() {
    $("#user_btn").ready(function () {
        $.ajax({
            url: '/user-state',
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                if (response) {
                    if (response.user_logged_in === false) {
                        $("#user_btn").html("LOGIN/REGISTER")
                    } else {
                        $("#user_btn").html("LOGOUT");
                        $("#ticket_creator_nav").show()
                        $("#ticket_list_nav").show()
                    }
                    $("#user_btn").show()
                } else {
                    console.log("Failed to retrieve user state using API!")
                }
            },
            error: function (xhr, status, error) {
                console.log(xhr.status);
                console.log(status);
                console.log(error)
            }
        });
    });

    $("#user_btn").click(function (event) {
        event.preventDefault();
        $.ajax({
            url: '/user-state',
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                if (response) {
                    if (response.user_logged_in === true) {
                        $.ajax({
                            url: '/login-api/logout_user=True',
                            type: 'GET',
                            error: function (xhr, status, error) {
                                console.log(xhr.status);
                                console.log(status);
                                console.log(error)
                            }
                        });
                        window.location = "/index/";
                    } else {
                        window.location = "/login/";
                    }
                } else {
                    console.log("Failed to retrieve user state using API!")
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
});