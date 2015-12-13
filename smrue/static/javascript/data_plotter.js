$(function(){
	var timeRange;
	var callApiRequest;
	var chartId = "chart";
	var loadingGif = "<div class='loading-gif'></div>";

	/*
	Seletores dos inputs do form do gráfico. Usados como selectors do JQuery
	xStartInputSelector = input com a data de inicio.
	xEndInputSelector = input com a data de fim.
	formatInputSelector = input com o formato que as datas estão.
	timeRangeInputSelector = input que indica se é um gráfico por hora (hourly), dia (daily) ou mes (monthly)
	goalInputSelector = input do checkbox se os goals devem ser mostrados
	integrateInputSelector = input do checkbox se o gráfico deve ser integrado
	buttonSelector = botao que manda o form
	*/
	var dateInputSelector = ".tab-pane.active .date-input";
	var measurementInputSelector = ".unit";
	var equipmentSelector = ".equipment";
	var timeRangeInputSelector = ".tab-pane.active";
	var goalInputSelector = "#boolean-goal";
	var integrateInputSelector = "#boolean-integrate";
	
	var buttonSelector = ".plot-button";
	var plotUrl = $(buttonSelector).data("url");
	
	var validatePlotData = function(plotsData){
		var blankPlotData = [[[]]];

		try{
			for(var i = 0; i < plotsData.length; i++){
				if(!(plotsData[i][0][0] && plotsData[i][0][1]))
					return blankPlotData
			}
			console.log("plotsData on validate");
			console.log(plotsData);
			return plotsData
		}catch(err){
			console.log(err);
			return blankPlotData
		}
	};

	//Opcoes default do grafico
	var defaultPlotOptions = {
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

	var validateConfig = function(){
		$(integrateInputSelector).change(function(){
			if($(this).is(":checked")){
				$(measurementInputSelector).find("option[value='money']").removeAttr("disabled");
			} else {
				$(measurementInputSelector).find("option:first").attr("selected", "selected	");
				$(measurementInputSelector).find("option[value='money']").attr("disabled", "disabled");
			}
		})
	}

	/*
	data:
	xStart: data de inicio (String)
	xEnd: data de fim (String)
	goal: se o gráfico de metas deve ser mostrado (bool)
	integrate: se o grafico de medidas deve ser integrado (bool)
	format: o formato que as datas estao (string)
	timeRange: se o grafico será por hora ("hourly"), dias ("daily") ou meses ("monthly")
	*/
	var callApi = function(options){
		$("#"+chartId).html(loadingGif);
		callApiRequest = $.ajax({ 
			type: 'GET', 
			url: plotUrl, 
			dataType: 'json',
			data: options, 
			success: function(data) {
		    	return data;
		    }
		});
	}

	var translate = function(name){
		var translation;
		var dictionary = {"all": "Todos", "goal": "Meta"};
		if (!(name in dictionary)) {
			translation = name;
		} else {
			translation = dictionary[name];
		}
		return translation;	
	}

	var replotPlot = function(plots, timeRange){
		var plotTitle = "";
		var xFormat = "";
		var label = $(measurementInputSelector).find("option:selected").val();
		if($(integrateInputSelector).is(":checked")){
			label += "h";
		}
		var yFormat = $(measurementInputSelector).find("option:selected").data("yformat");

		plotTitle = label+" x Data";
		if(timeRange == "hourly"){
			xFormat = "%d/%m/%y %H:%M";
		} else if (timeRange == "daily") {
			xFormat = "%d/%m/%y";
		} else if (timeRange == "monthly") {
			xFormat = "%m/%y";
		} else if (timeRange == "test"){
			xFormat = "%H:%M:%S";
		};

		// desempacotar os dados...
		var data = [];
		var legends = [];
		var tempData = [];
		for(var key in plots){
			legends.push(translate(key));
			for(var i = 0; i < plots[key].length; i++){
				tempData.push([plots[key][i][0], plots[key][i][1]]);
			}
			data.push(tempData);
			tempData = [];
		}

		var newOptions = 
			{
				title: plotTitle,
				axes:{
					xaxis:{
						tickInterval : '1 second',
						pad: 1.0,
						label: 'Data',
						renderer: $.jqplot.DateAxisRenderer,
						tickOptions:{
							formatString: xFormat
						}
					},
					yaxis:{
						label: label,
						tickOptions:{
							formatString: yFormat
						}
					}
				},
				legend: {
					show: true,
					labels: legends
				}
			};
		plot = $.jqplot(chartId, data, $.extend(defaultPlotOptions, newOptions));
	}

	var hasData = function(responseData){
		return Object.keys(responseData).length > 0;
	}

	$(buttonSelector).click(function(){
		var dateRangeInput = $(dateInputSelector).val();
		var measurement = $(measurementInputSelector).val();
		if(dateRangeInput != undefined){
			var xStart = dateRangeInput.split(" - ")[0].split("/").join("-");
			var xEnd = dateRangeInput.split(" - ")[1].split("/").join("-");
		}
		var timeRange = $(timeRangeInputSelector).data("type");
		var yIntegrate = $(integrateInputSelector).is(":checked");
		var showGoals = $(goalInputSelector).is(":checked");
		var equipmentId = $(equipmentSelector).val();
		var noDataMessage = "<p class='chart-error'>Não há dados de consumo para o equipamento ou período selecionado.</p>"

		var equipmentId = [];
		$(equipmentSelector + ":checked").each(function() {
			equipmentId.push($(this).val());
		});
		data = {
			"xStart": xStart,
			"xEnd": xEnd,
			"timeRange": timeRange,
			"goal": showGoals,
			"integrate": yIntegrate,
			"measurement": measurement,
			"equipmentId": equipmentId
		}
		callApi(data);
		callApiRequest.success(function(response){
			if (!hasData(response.plots)){
				$("#"+chartId).html(noDataMessage);
			} else {
				replotPlot(response.plots, timeRange);
			}
		});
		
	});

	// $(".date-time-range-picker").val("01/04/2015 0:00 - 02/04/2015 18:00");
	// $("div#hour").removeClass("active");
	// $("div#month").addClass("active");
	// $(".year-month-range-past").val("11/2015 - 12/2015");
	// $(".date-range-picker").val("01/11/2015 - 07/11/2015");
	// $(".equipment[value='']").attr("checked","checked");
	// $(".equipment[value='1']").attr("checked","checked");
	// $(".equipment[value='2']").attr("checked","checked");

	// $(".unit").val("money");

	validateConfig();
	$(buttonSelector).click();
})

