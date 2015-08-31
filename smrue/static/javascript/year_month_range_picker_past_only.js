$(function(){
  

  // $('input.year-month-range-picker-past').daterangepicker({
  //   endDate: moment(),
  //   maxDate: moment(),
  //   showDropdowns: true,
  //   locale: {
  //     applyLabel: 'Ok',
  //     cancelLabel: 'Cancelar',
  //     fromLabel: 'De',
  //     toLabel: 'Até',
  //     customRangeLabel: 'Escolher',
  //     daysOfWeek: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex','Sab'],
  //     monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
  //     firstDay: 1,
  //     format: 'MM/YYYY'
  //   }
  // }).on('show.daterangepicker', function(ev, picker){
  //   $(".daterangepicker:visible").addClass("monthly-range-picker");

  //   $(".monthly-range-picker .calendar select").on("change", function(){
  //     var fromMonth = $(".monthly-range-picker .calendar.left select.monthselect").val()
  //     var fromYear = $(".monthly-range-picker .calendar.left select.yearselect").val()
  //     $('.year-month-range-picker-past').data('daterangepicker').setStartDate((parseInt(fromMonth) + 1).toString() + "/" + fromYear);

  //     var toMonth = $(".monthly-range-picker .calendar.right select.monthselect").val()
  //     var toYear = $(".monthly-range-picker .calendar.right select.yearselect").val()
  //     $('.year-month-range-picker-past').data('daterangepicker').setEndDate((parseInt(toMonth) + 1).toString() + "/" + toYear);

  //   });

  // });

  $('.year-month-range-picker-past input.start').datepicker({
    changeMonth: true,
    changeYear: true,
    showButtonPanel: true,
    format: 'mm/yyyy',
    minViewMode: 'months',
    endDate: 'today'
    
  }).on('changeDate', function() { 
      var date_range = $("input.year-month-range-past").val();
      if(date_range == ""){
        var date_range_array = ["", " - ", ""];
      }else{
        var date_range_array = date_range.split(" - ");
        date_range_array = [date_range_array[0], " - ", date_range_array[1]];
      }
      var date_range_moment = moment("01/" + $(this).val(), "DD/MM/YYYY");

      date_range_array[0] = date_range_moment.startOf("month").format("DD/MM/YYYY");
      console.log(date_range_array.join(""))
      $('input.year-month-range-past').val(date_range_array.join(""))
    })

  $('.year-month-range-picker-past  input.end').datepicker({
    changeMonth: true,
    changeYear: true,
    showButtonPanel: true,
    format: 'mm/yyyy',
    minViewMode: 'months',
    endDate: 'today'
    
  }).on('changeDate', function() { 
      var date_range = $("input.year-month-range-past").val();
      if(date_range == ""){
        var date_range_array = ["", " - ", ""];
      }else{
        var date_range_array = date_range.split(" - ");
        date_range_array = [date_range_array[0], " - ", date_range_array[1]];
      }
      var date_range_moment = moment("01/" + $(this).val(), "DD/MM/YYYY");

      date_range_array[2] = date_range_moment.endOf("month").format("DD/MM/YYYY");
      console.log(date_range_array.join(""))
      $('input.year-month-range-past').val(date_range_array.join(""))
    })
});