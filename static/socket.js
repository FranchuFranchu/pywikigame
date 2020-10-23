Game.socket = new WebSocket("ws://" + window.location.host + "/socket");


String.prototype.limited_split = function(separator, n) {

    var split = this.split(separator);
    if (split.length <= n)
        return split;
    var out = split.slice(0,n-1);
    out.push(split.slice(n-1).join(separator));
    return out;
}
    

Game.socket.onopen = function(e) {
    Cookies.set
    Game.socket.send_data("match_list", {})
};

Game.socket.send_data = function(action, data) {
    Game.socket.send(action + " " + JSON.stringify(data))
}

Game.socket.onmessage = function(event) {
    console.debug(`[message] Data received from server: ${event.data}`);
    console.log(event.data)
    action = event.data.split(' ')[0]
    args = event.data.limited_split(' ', 2)[1]

    data = JSON.parse(args)

    Game.message_handlers[action](data)
};

Game.socket.onclose = function(event) {
    if (event.wasClean) {
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.error('[close] Connection died');
    }
};

Game.socket.onerror = function(error) {
    console.error(`[error] ${error.message}`);
};
