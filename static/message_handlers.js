Game.message_handlers = {
    match_list: function(data) {
        $("tbody#match-tbody").empty()
        data.forEach((e) => { 
            Game.message_handlers.create_match(e)
        })
    },
    success_join_match: function (data) {
        $("#pre-login").hide()
        $("#lobby")    .show()
        $("#in-game")  .hide()
    },
    error: function (data) {
        console.error(data)
    },
    create_match: function(e) {

        $("tbody#match-tbody")
            .append($("<tr></tr>")
                .addClass("match-row")
                .attr('data-pk', e.pk)
                .append($("<td></td>")
                    .addClass("match-name")
                    .on('click', Game.join_match_w)
                    .attr('data-pk', e.pk)
                    .text(e.fields.name))
                .append($("<td></td>")
                    .text(e.fields.started ? "Started" : "Waiting"))

                
            )     
    },
    success_create_match: function (data) {
        Game.message_handlers.create_match(data[0])
    },

    this_player: function(data) {
        Game.player = data[0]
        $("*[name=player_name]").val(data[0].fields.name)
    },
    this_match: function(data) {
        if (data[0].fields.started) {
            $("#pre-login").hide()
            $("#lobby")    .hide()
            $("#in-game")  .show()
        } else {
            $("#pre-login").hide()
            $("#lobby")    .show()
            $("#in-game")  .hide()
        }
        $(".match-name-field").text(data[0].fields.name)
        $(".match-base-field").text(data[0].fields.wikipedia_base)
    },
    not_logged_in: function(data) {

    },
    add_player: function(data) {
        let e = data[0]
        let row = $("<tr></tr>")
            .attr('data-pk', e.pk)
            .addClass("player-row")
                .append($("<td></td>")
                    .addClass("player-name")
                    .attr('data-pk', e.pk)
                    .text(e.fields.name))
                .append($("<td></td>")
                    .text(e.fields.ready ? "Ready" : "Not ready")
                )

        $("tr.player-row[data-pk=" + e.pk + "]").remove()
        $("tbody#lobby-player-tbody, tbody#game-player-tbody")    
            .append(row)
        
    },
    delete_player: function(data) {
        let e = data[0]
        $("tr.player-row[data-pk=" + e.pk + "]").remove()
    },
    delete_match: function(data) {
        let e = data[0]
        $("tr.match-row[data-pk=" + e.pk + "]").remove()
    },
}
