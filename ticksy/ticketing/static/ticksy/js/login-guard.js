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
                swal({
                    icon: "error",
                    title: "Internal server error!",
                    text: "HTTP Error code: '" + xhr.status + " " + error + "'"
                }).then(() => {
                    window.location = window.location
                });
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
                        swal({
                            title: "Confirmation",
                            text: "Are you sure you want to log out?",
                            icon: "warning",
                            buttons: true,
                            dangerMode: true,
                        }).then((willLogOut) => {
                            if (willLogOut) {
                                swal({
                                    icon: "success",
                                    title: "Logout successful!",
                                    text: "You have been logged out successfully!",
                                    button: false,
                                    closeOnEsc: false,
                                    closeOnClickOutside: false,
                                    timer: 1000
                                }).then(() => {
                                    $.ajax({
                                        url: '/login-api/logout_user=True',
                                        type: 'GET',
                                        error: function (xhr, status, error) {
                                            swal({
                                                icon: "error",
                                                title: "Internal server error!",
                                                text: "HTTP Error code: '" + xhr.status + " " + error + "'"
                                            }).then(() => {
                                                window.location = window.location
                                            });
                                        }
                                    });
                                    window.location = "/index/";
                                });
                            }
                        });
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
                    window.location = window.location
                });
            }
        });
    });
});