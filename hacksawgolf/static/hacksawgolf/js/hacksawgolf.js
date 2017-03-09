var selected_golfer_list = [];
var num_golfer_selections;

$( document ).ready(function($) {

	/* LISTENERS */

	/*
		- my team page
		- toggle chevron arrow on collapsible pick selection panel
	*/
	$('#my_team_selections').on('shown.bs.collapse', function () {
	   $("#my_team_selections_chevron").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
	});

	$('#my_team_selections').on('hidden.bs.collapse', function () {
	   $("#my_team_selections_chevron").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
	});


	/*
		- scores page
		- fetch team for selected team name and append response html
	*/
	/* COLLAPSIBLE/EXPANDABLE TEAMS NOT NEEDED FOR RIGHT NOW
	$("div[id^='team_score_content_']").on('shown.bs.collapse', function () {
		var user_id_for_scores = $(this).attr('data-user-id');
		var tournament_id_for_scores = $("#tournament_id").val();
		var team_score_list_div = $("#team_score_list_" + user_id_for_scores);

		// as long as the user has not clicked on a team (element has no children), go get the team and display it
		if (team_score_list_div.children().length == 0) {

			// get the team of golfers for the selected user team
			$.ajax({
				url: '/tournament/getteamforuserfortournament/' + user_id_for_scores + '/' + tournament_id_for_scores + '/',
				success: function(data) {
					// append the user team html
					team_score_list_div.append(data.team_html);
				},
				failure: function(data) {
					return false;
				}
			});

		}
	});
	*/

	/*
		- standings page
		- set sorting on standings table
	*/
	$('#standings_table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "bAutoWidth": false,
		"bProcessing": false,
		"aaSorting": [[ 2, "desc"]],
		"aoColumns": [null, null, null, null]
	});

	/*
		- standings page
		- set sorting on standings table
	*/
	$('#standings_detail_table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "bAutoWidth": false,
		"bProcessing": false,
		"aaSorting": [],
		"aoColumns": [null, null]
	});

	/*
		- breakdown page
		- set sorting on breakdown table
	*/
	$('#breakdown_table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "bAutoWidth": false,
		"bProcessing": false,
		"aaSorting": [[ 1, "desc"]],
		"aoColumns": [null, null, null, null]
	});

	/* END LISTENERS*/


	/*
		- my team page
		- set the selected golfer list array
	*/
	selected_golfer_list = [];
	var selected_golfer_id;
	// loop over each selected golfer row
	$.each($("div[id^='selected_golfer_row_']"), function(){
		// get the values of the selected_golfer_id and selected_golfer_salary hidden inputs
		selected_golfer_id = $(this).find("input[name^=selected_golfer_id_]")[0].value;
		selected_golfer_salary = $(this).find("input[name^=selected_golfer_salary_]")[0].value;

		// convert values to int
		selected_golfer_id = parseInt(selected_golfer_id);
		selected_golfer_salary = parseInt(selected_golfer_salary);

		// add an object that holds the golfer_id and salary to the selected_golfer_list array
		selected_golfer_list.push({golfer_id:selected_golfer_id, golfer_salary:selected_golfer_salary});
	});

	/*
		- my team page
		- set the num_golfer_selections variable
		- used to keep track of the number of times golfers have been selected in order to append a new golfer row to the selected
		golfers section
	*/
	num_golfer_selections = selected_golfer_list.length;

	/*
		- my team page
		- show the info message in the golfer selection section if no golfers have been selected
	*/
	if (!selected_golfer_list.length) {
		$("#selected_golfer_info_message").removeClass("hidden").addClass("show");
	}



	/*
		- my team page
		- select a golfer
	*/
	btnGolferSelect_click = function(golfer_id) {
		var tournament_id = $("#tournament_id").val();
		var next_golfer_row = num_golfer_selections + 1;
		var salary_total = parseInt($("#salary_total").html());

		// show the too many golfers selected modal if number of golfers already selected is >= 6
		if (selected_golfer_list.length >= 6) {
			$("#info_modal_text").empty().html('You cannot select more than 6 golfers');
			$("#info_modal").modal("show");
			return false;
		}

		// get the data for the selected golfer
		$.ajax({
			url: '/team/getgolferfortournament/' + tournament_id + '/' + golfer_id + '/' + next_golfer_row + '/',
			success: function(data) {

				// set a boolean holding whether or not the selected golfer_id is in the selected_golfer_list array
				var golfer_id_in_list = false;
				for (var i=0; i<selected_golfer_list.length; i++){
					if (selected_golfer_list[i].golfer_id == data.golfer_id){
						golfer_id_in_list = true;
						break;
					}
				}

				/*
					Continue only if the golfer_id is not in the selected_golfer_list array.
					This can happen when the user clicks the add golfer button for a particular golfer once and then again quickly before
					the button fades out.
				*/
				if (!golfer_id_in_list){

					// add an object holding the golfer_id and golfer_salary to the selected_golfer_list array
					selected_golfer_list.push({golfer_id:data.golfer_id, golfer_salary:data.salary});

					// set the num_golfer_selections variable to the current row number
					num_golfer_selections = next_golfer_row;

					// fade/hide the row for the selected golfer in the main golfer list
					$("#add_golfer_row_" + data.golfer_id).fadeOut("slow", function(){
						$("#add_golfer_row_" + data.golfer_id).addClass("hidden");
					});

					// add the golfer's salary to the salary total
					salary_total = salary_total + parseInt(data.salary);
					$("#salary_total").empty().html(salary_total);

					// change the number of golfers badge
					$("#num_golfers_selected").empty().html(selected_golfer_list.length);

					// add the golfer row
					$("#selected_golfer_form_container").append(data.golfer_html);

					// show the selected golfer column headers if necessary
					if ($("#selected_golfer_headings").hasClass("hidden")) {
						$("#selected_golfer_headings").removeClass("hidden").addClass("show");
						$("#selected_golfer_info_message").removeClass("show").addClass("hidden");
					}

					// if at least 1 golfer selected, show the continue button, but keep it disabled
					if (selected_golfer_list.length > 0){
						$("#continue_onto_confirmation_button").removeClass("hidden").addClass("show");
						if (!($("#continue_onto_confirmation_button").hasClass("disabled"))){
							$("#continue_onto_confirmation_button").addClass("disabled");
						}
						// if 6 golfers selected, enable the continue button
						if (selected_golfer_list.length == 6){
							$("#continue_onto_confirmation_button").removeClass("disabled");
							$("#continue_onto_confirmation_button").removeAttr("disabled");
						}
					}
				}
			},
			failure: function(data) {
				return false;
			}
		});
	}


	/*
		- my team page
		- remove a golfer from the selected golfer list
	*/
	btnGolferRemove_click = function(selected_golfer_row) {
		var salary_total = parseInt($("#salary_total").html());

		// get the golfer_id for the golfer being removed
		var golfer_id = parseInt($("#selected_golfer_id_" + selected_golfer_row).val());

		var golfer_id_in_list = false;
		// get the index of the golfer_id in the selected_golfer_list array
		for (var i=0; i<selected_golfer_list.length; i++){
			if (selected_golfer_list[i].golfer_id == golfer_id){
				var golfer_index = i;
				golfer_id_in_list = true;
				break;
			}
		}

		/*
			Continue only if the selected golfer_id is in the selected_golfer_list array.
			This can happen when the user clicks the remove golfer button for a particular golfer once and then again quickly before
			the button fades out.
		*/
		if (!golfer_id_in_list) {
			return false;
		}

		// get the salary of the golfer being removed
		var golfer_salary = parseInt(selected_golfer_list[golfer_index].golfer_salary);
		// subtract the golfer's salary from the total salary
		salary_total = salary_total - golfer_salary;
		$("#salary_total").empty().html(salary_total);

		// remove the golfer_id from the selected_golfer_list array
		selected_golfer_list.splice(golfer_index, 1);

		// change the number of golfers badge
		$("#num_golfers_selected").empty().html(selected_golfer_list.length);

		// if all golfers have been removed, hide the continue button
		if (selected_golfer_list.length == 0){
			$("#continue_onto_confirmation_button").removeClass("show").addClass("hidden");
		}
		// if less than 6 golfers selected, disable the continue button
		else {
			$("#continue_onto_confirmation_button").attr("disabled", "disabled");
			if (!($("#continue_onto_confirmation_button").hasClass("disabled"))){
				$("#continue_onto_confirmation_button").addClass("disabled");
			}
		}

		// fade/remove the row for the golfer being removed from the team
		$("#selected_golfer_row_" + selected_golfer_row).fadeOut("slow", function(){
			$("#selected_golfer_row_" + selected_golfer_row).remove();

			// remove hidden class and fade in the row to the main golfer list
			$("#add_golfer_row_" + golfer_id).removeClass("hidden");
			$("#add_golfer_row_" + golfer_id).fadeIn("fast");

			// if all golfers have been removed, hide the column headings and show the info message
			if (selected_golfer_list.length == 0) {
				$("#selected_golfer_headings").removeClass("show").addClass("hidden");
				$("#selected_golfer_info_message").removeClass("hidden").addClass("show");
			}
		});

	}


	/*
		- my team page
		- continue button click
	*/
	btnContinueOntoConfirm_click = function() {

		var tournament_id = $("#tournament_id").val();
		var oTeam = {tournament: tournament_id, selected_golfers: selected_golfer_list};
		var oTeam_json = JSON.stringify(oTeam);

		// post the selected_golfer_list array for validation
		$.ajax({
			url: '/team/validateteamselect/',
			type: 'POST',
			contentType: 'application/json',
			data: oTeam_json,
			success: function(validate_response) {
				// if validation errors
				if (!validate_response.successful){
					$("#error_modal_text").empty().html(validate_response.error);
					$("#error_modal").modal("show");
				}
				// if no validation errors, go to team verification page
				else {
					$("form#team_selection_form").submit();
				}
			},
			failure: function(response) {
				return false;
			}
		});
	}


	/*
		- verify team page
		- submit team button click
	*/
	btnSubmitTeam_click = function() {
		// check if save button has been disabled, if so, then the user double-clicked
		if ($("#submit_team_button").hasClass("disabled")){
			return false;
		}

		// disable the save button so they don't double click it
		$("#submit_team_button").addClass("disabled");

		var tournament_id = $("#tournament_id").val();
		var oData = {tournament_id: tournament_id};
		var oData_json = JSON.stringify(oData);

		// save the user's selected team
		$.ajax({
			url: '/team/save/',
			type: 'POST',
			contentType: 'application/json',
			data: oData_json,
			success: function(response) {
				// if  errors
				if (!response.successful){
					$("#error_modal_text").empty().html(response.error);
					$("#error_modal").modal("show");
					// enable the save button if an error occurs
					$("#submit_team_button").removeClass("disabled");
				}
				// if no errors, go to the home page
				else {
					window.location.href = '/home/';
				}
			},
			failure: function(response) {
				// enable the save button if an error occurs
				$("#submit_team_button").removeClass("disabled");
				return false;
			}
		});
	}

});