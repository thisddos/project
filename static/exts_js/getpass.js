$(document).ready(function(){
  $('#alert-box').hide();
});

function off(){
    $('#alert-box').fadeToggle('slow');
}

var form_info;

$('#form').submit(function(e){
  e.preventDefault();
  form_info = $('#form').serialize();

  $.ajax({
    type:'POST',
    url:location.pathname,
    dataType:'json',
    data: form_info,
    success: function(data){
      // if change
      if(data.msg == 'change'){
        window.location.href='/login/';
      }
      // else it
      else{
        $('#alert-box').fadeToggle('slow');
        $('.info').text(' ' + data.msg);
      }},

    error: function(xhr,){
      $('#alert-box').fadeToggle('slow');
      $('.info').text(' ' + '网络不佳～～ 请稍后重试!');}
  });

});
