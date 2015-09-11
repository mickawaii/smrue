$(function(){

	var dateTimeInputSelector = "input.date-time-range-picker";
	var dateInputSelector = "input.date-range-picker";
	var monthInputSelector = "input.year-month-range-picker-past";

	var integrateButtonSelector = "button.integrate";
	var unintegrateButtonSelector = "button.power";

	var hourlyPlotButtonSelector = "button.hourly-plot";
	var dailyPlotButtonSelector = "button.daily-plot";
	var monthlyPlotButtonSelector = "button.monthly-plot";

	var hourlyFromTimeSelector = "input.from-time";
	var hourlyToTimeSelector = "input.to-time";
	var unitSelecSelector =  "select.unit";
	var unit = $(unitSelecSelector).find(":selected").text();
	var valueIndex = 1;
	var dateIndex = 0;
	var data = null;
	var plot;
	
	var xFormat;


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

	var initialize = function(){

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
						title: dailyTitle,
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
									formatString: unit + '%.3f'
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

			console.log(data);
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

		$(hourlyPlotButtonSelector).click(function(){
			var newOptions = 
				{
					title: hourlyTitle,
					axes:{
						xaxis:{
							label: 'Horário',
						},
						yaxis:{
							label: 'Potência',
						}
					}
				};

			xFormat = '%H:%M';

			timeRange = "hourly";

			getTimeRangeAndGetData(dateTimeInputSelector, hourlyFromTimeSelector, hourlyToTimeSelector, newOptions);
		});

		$(dailyPlotButtonSelector).click(function(){
			var newOptions = 
			{
				title: dailyTitle,
				axes:{
					xaxis:{
						label: 'Data',
					},
					yaxis:{
						label: 'Potência',
					}
				}
			};

			xFormat = '%d-%m-%y';

			timeRange = "daily";

			getDateRangeAndGetData(dateInputSelector, newOptions);
		});

		$(monthlyPlotButtonSelector).click(function(){
			var newOptions = 
			{
				title: monthlyTitle,
				axes:{
					xaxis:{
						label: 'Data',
					},
					yaxis:{
						label: 'Potência',
					}
				}
			};

			xFormat = '%m-%y';

			timeRange = "monthly";

			getDateRangeAndGetData(monthInputSelector, newOptions);
		});

	}();

	var getTimeRangeAndGetData = function(datePickerSelector, fromTimePickerSelector, toTimePickerSelector, newOptions){
		var dateRange = $(datePickerSelector).val();
		var dateStart = dateRange.split(" - ")[0].split("/").join("-")
		var dateEnd = dateRange.split(" - ")[1] .split("/").join("-")

		changeDate(dateStart,dateEnd,newOptions,5);
			
	}

	var getDateRangeAndGetData = function(pickerSelector, newOptions){
		var dateRange = $(pickerSelector).val();
		var dateStart = dateRange.split(" - ")[0].split("/").join("-")
		var dateEnd = dateRange.split(" - ")[1] .split("/").join("-")

		changeDate(dateStart,dateEnd,newOptions,5);
	}

	//Passou de ser aplicado quando o daterangepicker eh okzado para quando um botao eh apertado.
	//comentado para futuras referencias
	// $(dateTimeInputSelector).on("apply.daterangepicker", function(event, picker){

	// 	var newOptions = 
	// 		{
	// 			title: hourlyTitle,
	// 			axes:{
	// 				xaxis:{
	// 					label: 'Horário',
	// 				},
	// 				yaxis:{
	// 					label: 'Potência',
	// 				}
	// 			}
	// 		};

	// 	xFormat = '%H:%M';

	// 	timeRange = "hourly";

	// 	getDateRangeAndGetData(dateTimeInputSelector, newOptions);
		
	// });


	var changeDate = function(xStart, xEnd, plotNewOptions, extraData){
		$("#chart").hide();
		$(".loading-gif").show();

		$.ajax({ 
			type: 'GET', 
			url: 'http://localhost:8000/consumption/ajaxPlot?', 
			dataType: 'json',
			data:
				{
					"xStart": xStart,
					"xEnd": xEnd,
					"extraData": extraData,
					"unit": unit,
					"timeRange": timeRange
				},
			success: function (response) { 

				var newPlotData = validatePlotData(response.plots);
				$(".loading-gif").hide();
				$("#chart").show();

				var newOptions = $.extend(
					plotNewOptions,
					{
						axes:{
							xaxis:{
								renderer:$.jqplot.DateAxisRenderer,
								tickOptions:{
									formatString: xFormat
								}
							},
							yaxis:{
								tickOptions:{
									formatString: unit.toUpperCase() + '%.3f'
								}
							}
						}
					}
				);

				data = newPlotData;

				console.log(data)
				plot = $.jqplot('chart', validatePlotData(newPlotData[0]), $.extend(defaultPlotOptions, plotNewOptions));
				plot.replot();
			}
		});
	
	};

	//--------------------------------------------Coisas novas

	var timeRange;
	var dailyTitle = 'Potência x Dia';
	var hourlyTitle = 'Potência x Hora';
	var monthlyTitle = 'Potência x Mes';

	/*
	Seletores dos inputs do form do gráfico. Usados como selectors do JQuery
	hiddenXStartInputSelector = input com a data de inicio.
	hiddenXEndInputSelector = input com a data de fim.
	hiddenFormatInputSelector = input com o formato que as datas estão.
	hiddenTimeRangeInputSelector = input que indica se é um gráfico por hora (hourly), dia (daily) ou mes (monthly)
	goalInputSelector = input do checkbox se os goals devem ser mostrados
	integrateInputSelector = input do checkbox se o gráfico deve ser integrado
	buttonSelector = botao que manda o form
	*/
	var hiddenXStartInputSelector = "";
	var hiddenXEndInputSelector = "";
	var hiddenFormatInputSelector = "";
	var hiddenTimeRangeInputSelector = "";
	var goalInputSelector = "";
	var integrateInputSelector = "";
	var buttonSelector = "";
	
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

	//Opcoes default do grafico
	var defaultPlotOptions = 	{
		animate: true,
		axesDefaults: {
			min: null,
					max: null
		},
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

	/*
	Entradas:
	xStart: data de inicio (String)
	xEnd: data de fim (String)
	goal: se o gráfico de metas deve ser mostrado (bool)
	integrate: se o grafico de medidas deve ser integrado (bool)
	format: o formato que as datas estao (string)
	timeRange: se o grafico será por hora ("hourly"), dias ("daily") ou meses ("monthly")
	*/
	var callApi = function(xStart, xEnd, goal, integrate, format){
		$.ajax({ 
			type: 'GET', 
			url: 'http://localhost:8000/consumption/ajaxPlot', 
			dataType: 'json',
			data: {
				"xStart": xStart,
				"xEnd": xEnd,
				"goal": goal,
				"integrate": integrate,
				"format": format
			},

			success: function (response) { 
				return response.plots;
			}
		});
	}

	var replotPlot = function(data, timeRange){
		var plotTitle = "";
		var xFormat = "";
		if(timeRange == "hourly"){
			plotTitle = hourlyTitle;
			xFormat = "%d-%m-%y %H:%M";
		} else if (timeRange == "daily") {
			plotTitle = dailyTitle;
			xFormat = "%d-%m-%y";
		} else if ("monthly") {
			plotTitle = monthlyTitle;
			xFormat = "%m-%y";
		};

		var newOptions = 
			{
				title: plotTitle,
				axes:{
					xaxis:{
						label: 'Data',
						renderer:$.jqplot.DateAxisRenderer,
						tickOptions:{
							formatString:xFormat
						}
					},
					yaxis:{
						label: 'Potência',
						tickOptions:{
							formatString: unit + '%.3f'
						}
					}
				}
			};

		plot = $.jqplot ('chart', validatePlotData(response.plots), $.extend(defaultPlotOptions, newOptions));
	}

	$(buttonSelector).click(function(){
		var xStart = $(hiddenXStartInputSelector).val();
		var xEnd = $(hiddenXEndInputSelector).val();
		var xFormat = $(hiddenFormatInputSelector).val();
		var yIntegrate = $(integrateInputSelector).is(":checked");
		var showGoals = $(goalInputSelector).is(":checked");
		var plots = callApi(xStart, xEnd, showGoals, yIntegrate, xFormat);

		var timeRange = $(hiddenTimeRangeInputSelector).val();
		replotPlot(plots, timeRange);
		
	});
})