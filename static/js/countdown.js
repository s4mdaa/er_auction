// Wait for the document to be ready
$(document).ready(function () {
  function getAuctionOrders(auctionCode) {
    $.ajax({
      url: '/auction_orders',
      method: 'GET',
      data: { auctionCode: auctionCode },
      success: function (response) {
        var response = JSON.parse(response)
        var orders = response.orders;
        var table = document.getElementById('orderbookTable');

        // Clear existing rows from the table
        while (table.rows.length > 1) {
          table.deleteRow(1);
        }

        // Iterate over the orders and create rows in the table
        for (var i = 0; i < orders.length; i++) {
          var order = orders[i];

          // Create a new row
          var newRow = table.insertRow(i + 1);

          // Insert cells for each order property
          var datetimeCell = newRow.insertCell(0);
          datetimeCell.textContent = order.date;

          var accountCell = newRow.insertCell(1);
          accountCell.textContent = order.account;

          var volumeCell = newRow.insertCell(2);
          volumeCell.textContent = order.volume;

          var priceCell = newRow.insertCell(3);
          priceCell.textContent = order.price;
        }

        $("#instrument").empty();
        $("#instrument").val(response.auctionCode);
        $("#auctionId").val(response.auctionCode);


        var accounts = response.accounts;

        // Clear existing options from the select element
        $("#accountSelection").empty();

        // Loop through the accounts array and append options to the select element
        for (var i = 0; i < accounts.length; i++) {
          var account = accounts[i];
          var option = $("<option>").val(account.code).text(account.code);
          $("#accountSelection").append(option);
        }
      },
      error: function (xhr, status, error) {
        // Handle any errors that occur during the request
        console.log(error);
      }
    });
  }


  $('table tr').click(function () {
    $("#orderbook").css("display", "block");
    var auctionCode = $(this).data('auction-id');
    getAuctionOrders(auctionCode);
    // You can perform further actions with the auctionId here
  });

  $('#close_popup_btn').click(function () {
    // Hide the popup
    $('#popup').hide();
  });

  // Handle button click
  $('#place_bid_btn').click(function () {
    // Show the popup element
    $('#popup').show();
  });
  // Get the text content of the element with the ID "close_time"
  var closeTime = $("#close_time").text();

  // Set the date and time for the countdown (assuming closeTime is defined)
  var countdownDate = new Date(closeTime).getTime();

  // Update the countdown every second
  var countdownTimer = setInterval(function () {
    // Get the current date and time
    var now = new Date().getTime();

    // Calculate the time remaining
    var timeRemaining = countdownDate - now;

    // Calculate days, hours, minutes, and seconds
    var days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    var hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

    // Display the countdown in the Odoo web template
    $('#countdown').text(days + "d " + hours + "h " + minutes + "m " + seconds + "s ");

    // If the countdown is finished, display a message
    if (timeRemaining < 0) {
      clearInterval(countdownTimer);
      $('#countdown').text("Countdown has ended.");
    }
  }, 1000);
});