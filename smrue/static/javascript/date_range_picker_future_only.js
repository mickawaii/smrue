$(function(){
	$('input.date-range-picker').daterangepicker({
		format: 'DD/MM/YYYY',
		startDate: moment(),
		endDate: moment().add(1, 'days'),
		minDate: moment(),
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
			'30 dias': [moment(), moment().add(30, 'days')],
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