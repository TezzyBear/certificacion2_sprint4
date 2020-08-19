setInterval(function(){
    $.ajax({
      type: 'GET',
      url: '/has_cam',
      dataType: 'json',
      success: function(data){
          console.log(data)
          if(data.available){
            $("#main-text").html("¿Habilitas el acceso a tu cámara?"); 
            $(".btn").removeClass("invisible")
          }else{
            $("#main-text").html("Por favor, conecta tu cámara!"); 
            $(".btn").addClass("invisible")
          }            
        }
      });
    }, 3000);