function download_csv(url) {
	window.location.href = url + URI(window.location.href).search();
}
function get_url_without_filter(name) {
	var url = URI(window.location.href).removeSearch(name);
	window.location.replace(url);
}
function add_filter_to_url(name,value,url) {
	var url = URI(window.location.href).removeSearch(name).addSearch(name,value);
	window.location.replace(url);
}
$(document).ready(function() {
	$('#daterange').daterangepicker(
		{
			ranges: {
				'Hoje': [moment(), moment()],
				'Ontem': [moment().subtract('days', 1), moment().subtract('days', 1)],
				'Últimos 7 dias': [moment().subtract('days', 6), moment()],
				'Últimos 30 dias': [moment().subtract('days', 29), moment()],
				'Mês Atual': [moment().startOf('month'), moment().endOf('month')],
				'Mês Passado': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
			},
			startDate: moment().subtract('days', 29),
			endDate: moment()
		},
		function(start, end) {
			$('#daterange').val((start.format('DD/MM/YYYY') + ' - ' + end.format('DD/MM/YYYY')));
		}
	);
	// Atribui valor inicial:
	parsed_url = URI(window.location.href).search(true);
	var daterange_from = (moment().subtract('days', 29)).format('DD/MM/YYYY');
	var daterange_to = (moment()).format('DD/MM/YYYY');
	if (parsed_url.daterange_from != undefined) {
		daterange_from = parsed_url.daterange_from;
	}
	if (parsed_url.daterange_to != undefined) {
		daterange_to = parsed_url.daterange_to;
	}
	$('#daterange').val((daterange_from + ' - ' + daterange_to));

	// Replace na URL:
	$('#daterange').on('apply.daterangepicker', function(ev, picker) {
		var url = URI(window.location.href).removeSearch('daterange_from').removeSearch('daterange_to').addSearch('daterange_from',picker.startDate.format('YYYY-MM-DD')).addSearch('daterange_to',picker.endDate.format('YYYY-MM-DD'))
		window.location.replace(url);
	});
});