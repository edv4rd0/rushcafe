function urlify(text) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    })
}

$(function() {
    
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new WebSocket(ws_scheme + '://' + window.location.host + "/cafe/ws/chat/");
    // var chatsock = new WebSocket("wss://echo.websocket.org/")
    // var chatsock = new WebSocket(ws_scheme + '://127.0.0.1:8000/cafe/ws/chat/');    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var css_class = data.is_bot ? "bot" : "me";

        chat.append(
            $("<li class='" + css_class + "'></li>").append(urlify(data.message.toString()))
        )
        chat.scrollTop(chat.height())
    };

    function send(event) {
        var message = $('#message').val();
        var chat = $("#chat")
        chat.append($("<li class='me'></li>").text("You: " + message));
        chat.scrollTop(chat.height())
        chatsock.send(JSON.stringify({
            'message': message}));
        $("#message").val('').focus();
        return false;
    }

    $("#sendMessage").on("click", (event) =>{send(event)});
    $("#message").keyup(function(event) {
        if (event.keyCode === 13) {
            send(event);
        }
    });
    

});