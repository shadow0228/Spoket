$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var socket_url = ws_scheme + '://' + window.location.host + "/youPotify" + window.location.pathname + "/websocket"
    // var socket_url = ws_scheme + '://' + window.location.host + window.location.pathname
    console.log(socket_url)

    var song_socket = new ReconnectingWebSocket(socket_url);
    
    song_socket.onmessage = function(message) {
        console.log('>>> callback!!!!!!')
        var data = JSON.parse(message.data);
        var sender = data['sender']
        var msg = data['message']
        var songId = data['songId']

        var url = "https://api.spotify.com/v1/tracks/" + songId

        var userAjax = $.get('/getUser')

        songAjax = $.get(url)

        $.when(userAjax, songAjax).done(function(userData, songData) {
            console.log(userData[0].user)
            console.log(sender)
            songName = songData[0].name
            if(userData[0].user != sender) {
                var notificationIcon = $("#notificationIcon")
                var html = "<a id='notificationIcon'><span class='glyphicon glyphicon-bell' style='color:red' onclick=\"notification('" + String(sender) + "', '" + String(msg) + "','" + String(songName) + "')" + "\" ></span></a>"
                var icon = $(html);
                notificationIcon.replaceWith(icon);
            }
        });
            
    };
});