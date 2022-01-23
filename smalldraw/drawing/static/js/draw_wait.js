function main(csrf_token, url, to_url, end_url) {
    setInterval(function() { wait(csrf_token, url, to_url, end_url); }, 1000);
}


function wait(csrf_token, url, to_url, end_url) {
    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        async: 'false',
        success: function (json) {
            var stage = json['message'];
            if (stage == 'End') {
                window.location.replace(end_url);
            }
            if (stage == 'Not ready') {
                window.location.replace(to_url);
            }
        }
    });
}
