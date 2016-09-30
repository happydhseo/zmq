
ws = new ReconnectingWebSocket("ws://"  + location.host + '/zeromq')

ws.onmessage = function(message) {
  // onsole.log(message);
  payload = JSON.parse(message.data);
  draw_array(payload.data);
  $('#time_step').html('<h2> ITERATION: ' + payload.timestep + '</h2>');
};

function draw_array(arr) {
  var canvas = $('#canvas')[0];
  canvas.width = 500;
  canvas.height = 500;
  var ctx = canvas.getContext("2d");
  ctx.webkitImageSmoothingEnabled = false;
  ctx.mozImageSmoothingEnabled = false;
  ctx.imageSmoothingEnabled = false;
  var color = d3.scaleLinear()
      .domain([0,6,12])
      .range(["blue", "green", "red"]);

  var img = ctx.getImageData(0, 0, arr.length, arr[0].length);
  // var idata = ctx.createImageData(100, 100);
  for (var i=0, s=-1; i<arr.length; i++) {
    for (var j=0; j<arr[0].length; j++) {
      var c = d3.rgb(color(arr[i][j]));
      img.data[++s] = c.r; // R
      img.data[++s] = c.g; // G
      img.data[++s] = c.b; // B
      img.data[++s] = 255;  // fully opaque

    }
  }
  
  // rescale/ redraw to make it look pixellated 
  ctx.putImageData(img, 0, 0);
  ctx.drawImage(canvas, 0, 0, 100, 100, 0, 0, canvas.width, canvas.height);
}