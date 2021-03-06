(function($) {
  "use strict";

  function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 24));
    return {
      total: t,
      days: days,
      hours: hours,
      minutes: minutes,
      seconds: seconds
    };
  }
  var event_ids = [];
  $("input[type=hidden]").each(function() {
    event_ids.push($(this).attr("id"));
  });

  function initializeClock() {
    event_ids.forEach(function(event_id) {
      var event_datetime_arr = [];
      $("input[type=hidden]").each(function() {
        if (
          $(this).attr("name") == "timestamp-minute" &&
          $(this).attr("id") == event_id
        ) {
          event_datetime_arr[0] = $(this).val();
        }
        if (
          $(this).attr("name") == "timestamp-hour" &&
          $(this).attr("id") == event_id
        ) {
          event_datetime_arr[1] = $(this).val();
        }
        if (
          $(this).attr("name") == "timestamp-day" &&
          $(this).attr("id") == event_id
        ) {
          event_datetime_arr[2] = $(this).val();
        }
        if (
          $(this).attr("name") == "timestamp-month" &&
          $(this).attr("id") == event_id
        ) {
          event_datetime_arr[3] = $(this).val();
        }
        if (
          $(this).attr("name") == "timestamp-year" &&
          $(this).attr("id") == event_id
        ) {
          event_datetime_arr[4] = $(this).val();
        }
        if (
          event_datetime_arr[0] !== undefined &&
          event_datetime_arr[1] !== undefined &&
          event_datetime_arr[2] !== undefined &&
          event_datetime_arr[3] !== undefined &&
          event_datetime_arr[4] !== undefined
        ) {
          var name = ".event-" + event_id;
          var daysSpan = $(name + "> .days");
          var hoursSpan = $(name + "> .hours");
          var minutesSpan = $(name + "> .minutes");
          var secondsSpan = $(name + "> .seconds");

          function updateClock() {
            if (event_datetime_arr[0].length == 1) {
              event_datetime_arr[0] = event_datetime_arr[0] + "0";
            }
            if (event_datetime_arr[3].length == 1) {
              event_datetime_arr[3] = "0" + event_datetime_arr[3];
            }
            if (event_datetime_arr[2].length == 1) {
              event_datetime_arr[2] = "0" + event_datetime_arr[2];
            }
            if (event_datetime_arr[1].length == 1) {
              event_datetime_arr[1] = "0" + event_datetime_arr[1];
            }
            var t = getTimeRemaining(
              new Date(
                event_datetime_arr[4] +
                  "-" +
                  event_datetime_arr[3] +
                  "-" +
                  event_datetime_arr[2] +
                  "T" +
                  event_datetime_arr[1] +
                  ":" +
                  event_datetime_arr[0] +
                  ":" +
                  "00"
              )
            );
            daysSpan.html(t.days);
            hoursSpan.html(("0" + t.hours).slice(-2));
            minutesSpan.html(("0" + t.minutes).slice(-2));
            secondsSpan.html(("0" + t.seconds).slice(-2));

            if (t.total <= 0) {
              clearInterval(timeinterval);
            }
          }
          updateClock();
          var timeinterval = setInterval(updateClock, 1000);
        }
      });
    });
  }

  initializeClock();
})(jQuery);
