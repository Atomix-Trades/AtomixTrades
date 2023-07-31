document.addEventListener("DOMContentLoaded", function() {
    var socket = new WebSocket("ws://localhost:5000/ws");
  
    socket.onmessage = function(event) {
      var message = JSON.parse(event.data);
      if (message.type === "profit") {
        updateProfit(message.value);
      } else if (message.type === "trade") {
        addTradeHistory(message.trade);
      }
    };
  
    function updateProfit(profit) {
      var profitValue = document.getElementById("profit-value");
      profitValue.textContent = profit.toFixed(2);
    }
  
    function addTradeHistory(trade) {
      var tradeHistoryBody = document.getElementById("trade-history-body");
      var row = document.createElement("tr");
      row.innerHTML = `
        <td>${trade.date}</td>
        <td>${trade.type}</td>
        <td>${trade.amount}</td>
        <td>${trade.price}</td>
      `;
      tradeHistoryBody.insertBefore(row, tradeHistoryBody.firstChild);
    }
  });
  