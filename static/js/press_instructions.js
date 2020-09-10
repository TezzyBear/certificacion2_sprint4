function mouseUp() {    
    $('#instrucciones').hide();
  }
  function mouseDown() {
    $('#instrucciones').show();
  }

  $(function() {
    $('button#on').bind('click', function() {
      $(this).toggleClass('btn-danger btn-secondary');
      var text=$('button#on').text();
      if(text === "Iniciar"){
        $(this).html('Detener');
        $.getJSON('/startRecording',
          function(data) {
        //do nothing
      });
      } else{
        $(this).text('Iniciar');
        $.getJSON('/stopRecording',
          function(data) {
            window.location.replace("http://localhost:5001/details")
        //go to details view
      });
      }
      return false;
    });
  });