$(function(){

	var initializePlot = function(){
		$(".loading-gif").show();
		$("#chart").hide();

		$.ajax({ 
			type: 'GET', 
			url: 'http://localhost:8000/consumption/ajaxPlot', 
			dataType: 'json',
			success: function (response) { 

				$(".loading-gif").hide();
				$("#chart").show();

				var newOptions = 
					{
						title: 'Título',
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
						}
					};


				plot = $.jqplot ('chart', validatePlotData(response.plots), $.extend(defaultPlotOptions, newOptions));
			}
		});
	}();

	$("input.date-range-picker").on("apply.daterangepicker", function(event, picker){

		var newOptions = 
			{
				title: 'Título',
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
				}
			};

		var dateRange = $("input.date-range-picker").val();
		var dateStart = dateRange.split(" - ")[0].split("/").join("-")
		var dateEnd = dateRange.split(" - ")[1] .split("/").join("-")
		console.log(dateStart)
		console.log(dateEnd)

		replot(1,dateStart,dateEnd,4,5);
	});

	var validatePlotData = function(plotsData){
		var blankPlotData = [[[]]];

		try{
			for(var i = 0; i < plotsData.length; i++){
				if(!(plotsData[i][0][0] && plotsData[i][0][1]))
					return blankPlotData
			}
			return plotsData
		}catch(err){
			return blankPlotData
		}
	};

	var defaultPlotOptions = {
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
					highlighter: {
						show: true,
						sizeAdjust: 7.5
					},
					cursor: {
						show: false
					}
	
				};


	var replot = function(yUnit, xStart, xEnd, plotNewOptions, extraData){
		$("#chart").hide();
		$(".loading-gif").show();

		$.ajax({ 
			type: 'GET', 
			url: 'http://localhost:8000/consumption/ajaxPlot?', 
			dataType: 'json',
			data:
				{
					"yUnit": yUnit,
					"xStart": xStart,
					"xEnd": xEnd,
					"extraData": extraData
				},
			success: function (response) { 

				var newPlotData = validatePlotData(response.plots);
				$(".loading-gif").hide();
				$("#chart").show();

				var newOptions = {
					data: newPlotData[0]
				} 

				plot.replot($.extend(defaultPlotOptions, newOptions));
		}
	});

	
	};
});