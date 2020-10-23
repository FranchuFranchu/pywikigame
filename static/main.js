Game = {

}
Game.player = {}
Game.current_page = window.location.hash.slice(1)


if (!Game.current_page) {
    Game.current_page = "T-shirt"
}

Game.go_to_section = function(section) {
    $(".mw-headline").each((idx, e) => {
        console.log(e.innerText, section.replace(/_/g, ' '), section.replace(/_/g, ' ') == e.innerText)
        if (section.replace(/_/g, ' ') == e.innerText) {
            e.scrollIntoView()
        }
    })
}

Game.change_page = function() {
    let main = $("html > body > main")
    $.getJSON("https://en.wikipedia.org/w/api.php?action=parse&page=" + Game.current_page + "&format=json&callback=?&origin=*", (data) => {
        main
            .html(data.parse.text["*"])

        main.find("*[src]").each((idx, e) => {
            $(e).attr("src", "https:" + $(e).attr("src"))
        })

        main.find("*[href]").each((idx, e) => {
            $(e).attr("href", window.location.origin + "#" + $(e).attr("href"))
        })
        window.scrollTo(0,0)    

    })
}
// dec2hex :: Integer -> String
// i.e. 0-255 -> '00'-'ff'
function dec2hex (dec) {
  return dec < 10
    ? '0' + String(dec)
    : dec.toString(16)
}

// generateId :: Integer -> String
function generateId (len) {
  var arr = new Uint8Array((len || 40) / 2)
  window.crypto.getRandomValues(arr)
  return Array.from(arr, dec2hex).join('')
}


if (Cookies.get("uid") == undefined ){
    Cookies.set("uid", generateId())
}

$().ready(() => {
    Game.change_page()

    $("#create-button").on('click', (ev) => {
        Game.socket.send_data("create_match", {
            wikipedia_base: $("*[name=wikipedia_base]").val(), 
            name: $("*[name=match_name]").val()
        })
    })
    $("#leave-button").on('click', (ev) => {

        $("#pre-login").show()
        $("#lobby")    .hide()
        $("#in-game")  .hide()
        Game.socket.send_data("leave_match", {
        })
    })
    $("#ready-button").on('click', (ev) => {
        Game.player.fields.ready = !Game.player.fields.ready
        Game.socket.send_data("set_ready", {
            ready: !Game.player.fields.ready
        })
        $("#ready-button").text(Game.player.fields.ready ? "Set ready" : "Set not ready")
    })
})

Game.join_match_w = function(ev) {
    Game.join_match(ev.target.getAttribute('data-pk'))
}

Game.join_match = function(pk) {
    Game.socket.send_data('join_match', {
        pk: pk,
        name: $("*[name=player_name]").val(),
    })
}
Game.deliberate_hash = false
$(window).on('hashchange', (ev) => {
    let page = window.location.hash.slice(1).split("/wiki/")[1]
    Game.deliberate_hash = true
    if (page === undefined) {
        if (window.location.hash[1] === "#") {
            Game.current_page = Game.current_page.split("#")[0]
            page = window.location.hash.slice(1)
            Game.go_to_section(page.slice(1))
            page = Game.current_page + page
            Game.current_page = page
            Game.deliberate_hash = true
            window.history.replaceState( {} , Game.current_page, window.location.origin + "#" + Game.current_page );
            return;
        }
    }
    if (page === Game.current_page) {
        return;
    }
    Game.current_page = page

    window.history.replaceState( {} , Game.current_page, window.location.origin + "#" + Game.current_page );
    console.log("Page: " + page)
    Game.change_page()

})
