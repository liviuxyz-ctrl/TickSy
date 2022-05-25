$( "#login_form" ).submit(function( event ) {
    event.preventDefault();
    let login_form_data = $(this).serialize()
    $.ajax({
      url: '/login-api/',
      data: login_form_data,
      processData: false,
      type: 'POST',
      dataType: 'json',
      success: function ( response ) {
          if(response){
              if(response.login_deny === true){
                  window.location = '/index/'
              }
              else{
                  if(response.successful_login){
                      window.location = '/index/'
                  }
              }
          }
      },
      error: function(xhr, status, error) {
        console.log(xhr.status);
        console.log(status);
        console.log(error)
      }
    });
});