function generateTicketCard(ticket_json_response) {
    let ticket_id = ticket_json_response.ticket_id;
    let name = ticket_json_response.user_full_name;
    let email = ticket_json_response.user_email;
    let responsible_name = ticket_json_response.responsible_employee_name;
    let team_name = ticket_json_response.responsible_team_name;
    let description = ticket_json_response.description;
    let priority_name = ticket_json_response.importance;
    let ticket_deadline = ticket_json_response.due_datetime;
    let ticket_creation_date = ticket_json_response.created_at;

    const ticket_template = '<div class="row">\n' +
    '    <div class="col-md-12">\n' +
    '        <div>\n' +
    '                <div class="card shadow mb-3">\n' +
    '                    <div class="card-header py-3" data-aos="fade" data-aos-duration="500">\n' +
    `                        <p class="text-primary m-0 fw-bold">${ticket_id}</p>\n` +
    '                    </div>\n' +
    '                    <div class="card-body">\n' +
    '                        <div class="row">\n' +
    '                            <div class="col-sm-12 col-md-8 col-lg-8">\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_name"><strong>Name:&nbsp;</strong></label>\n' +
    '                                    <div>\n' +
    `                                        <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">${name}</p><label class="form-label" for="service_name"><strong>Email:&nbsp;</strong></label>\n` +
    `                                        <p class="text-primary m-0 fw-normal fw-normal-rgreen" style="color: rgb(0,0,0)!important;">${email}</p>\n` +
    '                                    </div>\n' +
    '                                </div>\n' +
    '                            </div>\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3">\n' +
    '                                    <div class="mb-3"></div>\n' +
    '                                </div>\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_name"><strong>To *</strong></label>\n' +
    `                                    <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">${responsible_name}</p>\n` +
    '                                </div>\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_name"><strong>Team *</strong></label>\n' +
    `                                    <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">${team_name}</p>\n` +
    '                                </div>\n' +
    '                            </div>\n' +
    '                        </div>\n' +
    '                        <div class="row">\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3"><label class="form-label" for="client_description"><strong>Description *</strong><br></label>\n' +
    `                                    <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">${description}</p>\n` +
    '                                    <div class="mb-3"></div>\n' +
    '                                </div>\n' +
    '                            </div>\n' +
    '                        </div>\n' +
    '                        <div class="mb-3">\n' +
    '                            <div class="form-group mb-3">\n' +
    '                                <div class="col-sm-12 col-md-8 col-lg-8">\n' +
    '                                    <div class="mb-3"></div>\n' +
    '                                </div>\n' +
    '                            </div>\n' +
    '                        </div>\n' +
    '                        <div class="row mb-2">\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_client_start_date"><strong>Priority</strong><br></label></div>\n' +
    `                                <p class="text-primary m-0 fw-bold" style="color: var(--bs-red)!important;">${priority_name}</p>\n` +
    '                            </div>\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_client_end_date"><strong>Dead Line *</strong><br></label></div>\n' +
    `                                <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">${ticket_deadline}</p>\n` +
    '                            </div>\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_client_end_date"><strong>Created At *</strong><br></label></div>\n' +
    `                                <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">${ticket_creation_date}</p>\n` +
    '                            </div>\n' +
    '                        </div>\n' +
    '                        <div class="mb-3"></div>\n' +
    '                    </div>\n' +
    '                </div>\n' +
    '                <div class="text-end mb-3"></div>\n' +
    '        </div>\n' +
    '    </div>\n' +
    '</div>'

    return ticket_template;
}

ticket_container = document.getElementById("ticket_container")

$.ajax({
        url: '/ticket-count',
        processData: false,
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            if (response.number_of_tickets !== 0) {
                for(let ticket_id=1 ; ticket_id<= response.number_of_tickets; ticket_id++){
                $.ajax({
                    url: `/ticket/${ticket_id}`,
                    processData: false,
                    type: 'GET',
                    dataType: 'json',
                    success: function (ticket_information_response) {
                        if (ticket_information_response) {
                            ticket_container.insertAdjacentHTML("beforeend", generateTicketCard(ticket_information_response));
                        }
                        else{
                        swal({
                            icon: "error",
                            title: "Could not load ticket!",
                            text: `Could not load ticket with ID '${ticket_id}'!`
                        })
                        }
                    },
                    error: function (xhr, status, error) {
                    swal({
                        icon: "error",
                        title: "Internal server error!",
                        text: "HTTP Error code: '" + xhr.status + " " + error + "'"
                    })
                }
                })
                }
            }
            else {
                        swal({
                            icon: "error",
                            title: "No tickets found!",
                            text: "No tickets found in database!"
                        }).then(() =>{
                            window.location = '/index/'
                        });
            }
        }
})



