$(function(){
  $.ajax({ 
    type: 'GET', 
    url: 'http://localhost:8000/consumption/ajaxPlot', 
    dataType: 'json',
    success: function (data) { 
        console.log(data); // do anything you want with your parsed data
        $.jqplot ('chart', data.plot);
    }
  });
});