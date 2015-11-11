$(function(){
  var date_start = moment().startOf("month").format("DD/MM/YYYY");
  var date_end = moment().endOf("month").format("DD/MM/YYYY");
  
  $("input[name=yearmonth_start]").val(date_start);
  $("input[name=yearmonth_end]").val(date_end);
});