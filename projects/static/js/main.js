function name() {
    function save_name() {
        var textarea = $("#id_user");
        if (textarea.val() == "") {
            return false;
        }

        $.ajax({
            url: "/save_name/",
            type: "POST",
            cache: false,
            data: {"user_name": textarea.val()},
            success: function() {
                location.reload();
            }
        })

    }

    $("button").click(save_name);
    
    $("#id_user").keydown(function (e) {
        // Enter
        if (e.keyCode == 13) {
            save_name();
            e.preventDefault();
        }
    });
}

function activate_chat(thread_id, user_id, user_name) {
    $("#id_text").focus();

    function scroll_chat_window() {
        $("#chat-messages").scrollTop($("#chat-messages")[0].scrollHeight);
    }

    scroll_chat_window();

    var last_time = new Date().getTime();

    (function poll() {
        setTimeout(function() {
            $.ajax({
                url: "messages_view/",
                data: {'since': last_time},
                cache: false,
                success: function(html){  
                    $("#chat-messages").append(html);
                    scroll_chat_window();

                    last_time = new Date().getTime();
                },
                complete: poll
            });
        }, 1000);
    })();

    function send_message() {
        
        var textarea = $("#id_text");
        if (textarea.val() == "") {
            return false;
        }

        $.ajax({
            url: "send_message/",
            data: {"thread_id": thread_id, "user_id": user_id, "message": textarea.val()},
            type: "POST",
            cache: false,
        })

        textarea.val("");

    }

    $("button").click(send_message);

    $("#id_text").keydown(function (e) {
        // Enter
        if (e.keyCode == 13) {
            send_message();
            e.preventDefault();
        }
    });
}