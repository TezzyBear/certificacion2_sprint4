setInterval(function(){
    $.ajax({
      type: 'GET',
      url: '/check_cam',
      dataType: 'json',
      success: function(data){
          //console.log(data)
          if(!data.available){
            $('#res').html("Por favor, muestra tu rosto!");  
          }else{
            $('#res').html("Todo bien"); 
          }    
        }
      });
    }, 500);