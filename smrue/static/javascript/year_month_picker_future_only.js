$(function(){

  $('input.year-month-range-picker-future').daterangepicker({
    startDate: moment(),
    minDate: moment(),
    showDropdowns: true,
    singleDatePicker: true,
    locale: {
      applyLabel: 'Ok',
      cancelLabel: 'Cancelar',
      fromLabel: 'De',
      toLabel: 'Até',
      customRangeLabel: 'Escolher',
      daysOfWeek: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex','Sab'],
      monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
      firstDay: 1,
      format: 'MM/YYYY'
    }
  }).on('show.daterangepicker', function(ev, picker){
    $(".daterangepicker:visible").addClass("monthly-range-picker");

    $(".monthly-range-picker .calendar select").on("change", function(){
      var fromMonth = $(".monthly-range-picker .calendar.left select.monthselect").val()
      var fromYear = $(".monthly-range-picker .calendar.left select.yearselect").val()
      $('.year-month-range-picker-future').data('daterangepicker').setStartDate((parseInt(fromMonth) + 1).toString() + "/" + fromYear);

      var toMonth = $(".monthly-range-picker .calendar.right select.monthselect").val()
      var toYear = $(".monthly-range-picker .calendar.right select.yearselect").val()
      $('.year-month-range-picker-future').data('daterangepicker').setEndDate((parseInt(toMonth) + 1).toString() + "/" + toYear);

    });

  });

  $("form").submit(function(){
    var date_range = $("input.year-month-range-picker-future").val();
    var date_range_moment = moment("01/" + date_range, "DD/MM/YYYY");

    var date_start = date_range_moment.startOf("month").format("DD/MM/YYYY");
    var date_end = date_range_moment.endOf("month").format("DD/MM/YYYY");
    
    $("input[name=yearmonth_start]").val(date_start)
    $("input[name=yearmonth_end]").val(date_end)
  });

});