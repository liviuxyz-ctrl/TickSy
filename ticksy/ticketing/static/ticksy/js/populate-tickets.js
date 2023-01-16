function generateTicketCard(ticket_json_response) {
    let ticket_id = ticket_json_response;

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
    '                                        <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">Costel Mihai</p><label class="form-label" for="service_name"><strong>Email:&nbsp;</strong></label>\n' +
    '                                        <p class="text-primary m-0 fw-normal fw-normal-rgreen" style="color: rgb(0,0,0)!important;">costel.mihai@nokia.com</p>\n' +
    '                                    </div>\n' +
    '                                </div>\n' +
    '                            </div>\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3">\n' +
    '                                    <div class="mb-3"></div>\n' +
    '                                </div>\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_name"><strong>Domain *</strong></label>\n' +
    '                                    <p class="text-primary m-0 fw-normal fw-normal-rgreen" style="color: rgb(0,0,0)!important;">Front-end</p>\n' +
    '                                </div>\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_name"><strong>To *</strong></label>\n' +
    '                                    <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">Andrei Popescu</p>\n' +
    '                                </div>\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_name"><strong>Team *</strong></label>\n' +
    '                                    <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">CSS-pros</p>\n' +
    '                                </div>\n' +
    '                            </div>\n' +
    '                        </div>\n' +
    '                        <div class="row">\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3"><label class="form-label" for="client_description"><strong>Description *</strong><br></label>\n' +
    '                                    <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">We need to center a div in the the login page.&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>\n' +
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
    '                                <p class="text-primary m-0 fw-bold" style="color: var(--bs-red)!important;">CRITICAL</p>\n' +
    '                            </div>\n' +
    '                            <div class="col">\n' +
    '                                <div class="mb-3"><label class="form-label" for="service_client_end_date"><strong>Dead Line *</strong><br></label></div>\n' +
    '                                <p class="text-primary m-0 fw-normal" style="color: rgb(0,0,0)!important;">02/05/2022 07:00 PM</p>\n' +
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
ticket_container.insertAdjacentHTML("beforeend", generateTicketCard(3));
ticket_container.insertAdjacentHTML("beforeend", generateTicketCard(4));
