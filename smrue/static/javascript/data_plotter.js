$(function(){

	$(".loading-gif").show();
	$("#chart").hide();


	$.ajax({ 
		type: 'GET', 
		url: 'http://localhost:8000/consumption/ajaxPlot', 
		dataType: 'json',
		success: function (data) { 

			$(".loading-gif").hide();
			$("#chart").show();

			plot = $.jqplot ('chart', [data.plot], 
				{
					title: 'Título',
					animate: true,
					animation: {
						speed: 100
					},
					series:[
						{
							rendererOptions: {
								// Speed up the animation a little bit.
								// This is a number of milliseconds.  
								// Default for bar series is 3000.  
								animation: {
									speed: 2000
								},
							}
						}
					],
					axes:{
						xaxis:{
							label: 'Data',
							renderer:$.jqplot.DateAxisRenderer,
							tickOptions:{
								formatString:'%d-%m-%y'
							}
						},
						yaxis:{
							label: 'Potência',
							tickOptions:{
								formatString:'W%.2f'
							}
						}
					},
					highlighter: {
						show: true,
						sizeAdjust: 7.5
					},
					cursor: {
						show: false
					}
				}
			);
		}
	});
});