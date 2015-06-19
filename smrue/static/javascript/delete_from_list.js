$(function(){
  $(".delete-button").click(function(){
    var button = this;
    $("#delete-form").attr("action", button.value);
  });
});