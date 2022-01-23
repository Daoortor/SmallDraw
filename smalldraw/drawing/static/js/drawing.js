var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    BB = 0,
    dot_flag = false;

var x = "black",
    y = 2;

function init() {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext("2d");
    w = canvas.width;
    h = canvas.height;
    window.timer = document.getElementById("timer");
    window.time_elapsed = 0;
    window.context = canvas.getContext('2d');

    canvas.addEventListener("mousemove", function (e) {
        findxy('move', e)
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        findxy('down', e)
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        findxy('up', e)
    }, false);
    canvas.addEventListener("mouseout", function (e) {
        findxy('out', e)
    }, false);
    setInterval(function() { updateTime(timer); }, 1000);
}

function draw() {
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = x;
    ctx.lineWidth = y;
    ctx.stroke();
    ctx.closePath();
}

function findxy(res, e) {
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        BB = canvas.getBoundingClientRect();
        currX = 0.86 * (e.clientX - BB.left);
        currY = 0.76 * (e.clientY - BB.top);

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (res == 'up' || res == "out") {
        flag = false;
    }
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            BB = canvas.getBoundingClientRect();
            currX = 0.86 * (e.clientX - BB.left);
            currY = 0.76 * (e.clientY - BB.top);
            draw();
        }
    }
}

function updateTime() {
    window.time_elapsed += 1;
    window.timer.innerHTML = "Time elapsed: " + time_elapsed + " sec.";
}


function clearCanvas() {
    window.context.clearRect(0, 0, canvas.width, canvas.height);
}

function send(url, to_url, csrf_token) {
    var pic = document.getElementById("canvas").toDataURL("image/png");
    $.ajax({
        url: url,
        type: 'post',
        async: 'false',
        data: {'picture': pic, 'time_elapsed': window.time_elapsed, 'csrfmiddlewaretoken': csrf_token},
        success: function (data) {
            window.location.replace(to_url);},
        failure: function (data) {alert('ejnrej')},
    });
}