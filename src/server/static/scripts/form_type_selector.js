$(document).ready(function() {

  $("#period_div").hide();
  $("#delta_div").hide();
  $("#quota_div").hide();

  // On Select option changed
  $("#id_sampling_type").change(function() {
    // Check if current value is "PR" or "APR"
    if ($(this).val() === "PERIODIC") {
      // Show input field

      $("#period_div").show();

      $("#delta_div").hide();

    } else if ($(this).val() === "APERIODIC") {
      // Hide input field
      $("#delta_div").show();

      $("#period_div").hide();

    } else {
      //hide on default
      $("#delta_div").hide();
      $("#period_div").hide();
    }
  });


  $("#id_sending_type").change(function() {
    // Check if current value is "PR" or "APR"
    if ($(this).val() === "INSTANT") {
      // Show input field

      $("#quota_div").hide();

    } else if ($(this).val() === "BATCH") {
      // Hide input field
      $("#quota_div").show();

    } else {
      //hide on default
      $("#quota_div").hide();
    }
  });


});
