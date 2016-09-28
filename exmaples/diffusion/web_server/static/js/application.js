
var inbox = new ReconnectingWebSocket('ws://' + location.host + "/zeromq");

inbox.onmessage = function(message) {
  var data = JSON.parse(message.data);
  console.log(data);
  draw_array(data.data);
  $('#time_step').html('ITERATION: ' + data.timestep);
};

var tmp = [];
for (var i=0; i<100; i++) {
  tmp.push([]);
  for (var j=0; j<100; j++) {
    tmp[i][j] = 10.0;
  }
}

console.log(tmp);

draw_array(tmp);

function draw_array(arr) {
  var canvas = $('#canvas')[0];
  var ctx = canvas.getContext("2d");
  // console.log(h, w);
  var color = d3.scaleLinear()
      .domain([0,6,12])
      .range(["blue", "green", "red"]);

  var img = ctx.getImageData(0, 0, arr.length, arr[0].length);
  for (var i=0, s=-1; i<arr.length; i++) {
    for (var j=0; j<arr[0].length; j++) {

      var c = d3.rgb(color(arr[i][j]));
      // if (c.g !== 0) console.log(c);
      img.data[++s] = c.r; // R
      img.data[++s] = c.g; // G
      img.data[++s] = c.b; // B
      img.data[++s] = 255;  // fully opaque

    }
  }
  ctx.putImageData(img, 0, 0);

}