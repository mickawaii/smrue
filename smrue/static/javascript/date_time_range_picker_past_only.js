$(function(){
  $('input.date-time-range-picker').daterangepicker({
    endDate: moment(),
    maxDate: moment(),
    timePicker: true,
    format: 'DD/MM/YYYY H:mm',
    timePickerIncrement: 60,
    timePicker12Hour: false,
    timePickerSeconds: false,
    timePickerMinutes: false,
    locale: {
      applyLabel: 'Ok',
      cancelLabel: 'Cancelar',
      fromLabel: 'De',
      toLabel: 'Até',
      customRangeLabel: 'Escolher',
      daysOfWeek: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex','Sab'],
      monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
      firstDay: 1
    },
    ranges: {
      '30 dias': [moment().subtract(30, 'days'), moment()],
      'Até o fim do mês': [moment(), moment().endOf('month')]
    }
  })

  $("form").submit(function(){
    var date_range = $("input.date-range-picker").val();
    var date_start = date_range.split(" - ")[0]
    var date_end = date_range.split(" - ")[1]
    
    $("input[name=yearmonth_start]").val(date_start)
    $("input[name=yearmonth_end]").val(date_end)
  });

});