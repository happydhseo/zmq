
var inbox = new ReconnectingWebSocket(location.host + "/receive");

inbox.onmessage = function(message) {
  var data = JSON.parse(message.data);
  console.log(data);
};

inbox.onclose = function(){
    console.log('inbox closed');
    this.inbox = new WebSocket(inbox.url);

};
