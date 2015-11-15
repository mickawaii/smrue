
$(function(){

  var goalInputSelector = "#boolean-goal";
  var integrateInputSelector = "#boolean-integrate";

  $(integrateInputSelector).change(function(){
    if(this.checked == true){
      $(goalInputSelector).prop('disabled', false);
    }else{
      $(goalInputSelector).prop('disabled', true);
    }
  });
});