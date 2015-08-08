$(function(){
  $("input.time-picker").datetimepicker({
    format: 'HH:mm',
  });
})

// $(function(){
//   $('input.time-picker').daterangepicker({
//         timePicker: true,
//         timePickerIncrement: 60,
//         singleDatePicker: true,
//         locale: {
//           applyLabel: 'Ok',
//           cancelLabel: 'Cancelar',
//           fromLabel: 'De',
//           toLabel: 'Até',
//           customRangeLabel: 'Escolher',
//           daysOfWeek: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex','Sab'],
//           monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
//           firstDay: 1
//         }
//     }).on("show.daterangepicker", function(ev, picker){
//       $("div.daterangepicker:visible").addClass("time-picker");
//     });
// ;
// });