$(function() {
    $('button#on').bind('click', function() {
      $(this).toggleClass('btn-danger btn-secondary');
      var text=$('button#on').text();
      if(text === "Start"){
        $(this).html('Stop');
        $.getJSON('/startRecording',
          function(data) {
        //do nothing
      });
      } else{
        $(this).text('Start');
        $.getJSON('/stopRecording',
          function(data) {
            window.location.replace("http://localhost:5001/details")
        //go to details view
      });
      }
      return false;
    });
  });