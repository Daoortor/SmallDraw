function main(csrf_token, url, to_url) {
    setInterval(function() { wait(csrf_token, url, to_url); }, 1000);
}


function wait(csrf_token, url, to_url) {
    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        async: 'false',
        success: function (json) {
            var stage = json['message'];
            if (stage == 'Not ready') {
                window.location.replace(to_url);
            }
        }
    });
}
