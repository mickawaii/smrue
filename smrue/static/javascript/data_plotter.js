$(function(){

	var dateTimeInputSelector = "input.date-time-range-picker";
	var dateInputSelector = "input.date-range-picker";
	var integrateButtonSelector = "button.integrate";
	var unintegrateButtonSelector = "button.power";
	var unitSelecSelector =  "select.unit";
	var unit = "W";
	var valueIndex = 1;
	var dateIndex = 0;
	var data = null;
	var plot;

	var plotDataCopy = function(plotArray){
		var copy = [];
		for(var i = 0; i < plotArray[0][0].length; i ++){
			copy.push([plotArray[0][0][i][0], plotArray[0][0][i][1]]);
		}
		return copy;
	}

	var integrate = function(plotArray){
		var dataCopy = plotDataCopy(plotArray);
		var referenceValue = 0;

		for(var i = 0; i < dataCopy.length; i ++){
			if(i == 0){
				referenceValue = dataCopy[i][valueIndex];
			}else{
				dataCopy[i][valueIndex] += referenceValue;
				referenceValue = dataCopy[i][valueIndex];
			}
		}


		return [[dataCopy]];
	};

	var initializePlot = function(){

		$(".loading-gif").show();
		$("#chart").hide();

		$(unintegrateButtonSelector).hide();
		$(integrateButtonSelector).show();

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
									formatString:'W%.3f'
								}
							}
						}
					};


				data = response.plots;
				plot = $.jqplot ('chart', validatePlotData(response.plots), $.extend(defaultPlotOptions, newOptions));
			}
		});

		$(unitSelecSelector).change(function(){
			unit = $(this).val();
		});

		$(integrateButtonSelector).click(function(){


			var integratedData = integrate(data);

			var newOptions = {
				data: integratedData[0]
			}

			plot.replot($.extend(defaultPlotOptions, newOptions));
			$(unintegrateButtonSelector).show();
			$(integrateButtonSelector).hide();
		});

		$(unintegrateButtonSelector).click(function(){

			var newOptions = {
				data: data[0]
			}
			plot.replot($.extend(defaultPlotOptions, newOptions));
			$(unintegrateButtonSelector).hide();
			$(integrateButtonSelector).show();
		});

	}();

	var getDateRangeAndGetData = function(pickerSelector){
		var dateRange = $(pickerSelector).val();
		var dateStart = dateRange.split(" - ")[0].split("/").join("-")
		var dateEnd = dateRange.split(" - ")[1] .split("/").join("-")

		changeDate(1,dateStart,dateEnd,4,5);
	}

	$(dateTimeInputSelector).on("apply.daterangepicker", function(event, picker){

		var newOptions = 
			{
				title: 'Título',
				axes:{
					xaxis:{
						label: 'Data',
						renderer:$.jqplot.DateAxisRenderer,
						tickOptions:{
							formatString:'%I:%M'
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

		getDateRangeAndGetData(dateTimeInputSelector);
		
	});

	$(dateInputSelector).on("apply.daterangepicker", function(event, picker){

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
			
		getDateRangeAndGetData(dateInputSelector);
		
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


	var changeDate = function(yUnit, xStart, xEnd, plotNewOptions, extraData){
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
					"extraData": extraData,
					"unit": unit
				},
			success: function (response) { 

				var newPlotData = validatePlotData(response.plots);
				$(".loading-gif").hide();
				$("#chart").show();

				var newOptions = {
					data: newPlotData[0]
				} 

				data = newPlotData;
				plot.replot($.extend(defaultPlotOptions, newOptions));
		}
	});
	
	};
});