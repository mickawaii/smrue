$(function(){
  

  $('input.year-month-range-picker-past').daterangepicker({
    endDate: moment(),
    maxDate: moment(),
    showDropdowns: true,
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
      $('.year-month-range-picker-past').data('daterangepicker').setStartDate((parseInt(fromMonth) + 1).toString() + "/" + fromYear);

      var toMonth = $(".monthly-range-picker .calendar.right select.monthselect").val()
      var toYear = $(".monthly-range-picker .calendar.right select.yearselect").val()
      $('.year-month-range-picker-past').data('daterangepicker').setEndDate((parseInt(toMonth) + 1).toString() + "/" + toYear);

    });

  });

});