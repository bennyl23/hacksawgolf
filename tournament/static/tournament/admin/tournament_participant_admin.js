django.jQuery(document ).ready(function() {

	/*
		Tournament participant admin
		- golfer select change event
	*/
	django.jQuery("#id_golfer").change(function(){

		// get the id of the golfer selected
		var golfer_id = django.jQuery(this).val();

		// get the default salary of the golfer selected
		django.jQuery.ajax({
			url: '/tournament/getgolfersalary/' + golfer_id + '/',
			success: function(data) {
				django.jQuery('#id_salary').val(data);
			},
			failure: function(data) {
				return false;
			}
		});

	});
});