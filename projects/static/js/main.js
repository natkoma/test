
function getXmlHttpRequest(){
    var xmlhttp;
    try {
        xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
        try {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (E) {
            xmlhttp = false;
        }
    }
    if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
        xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
}


function name() {
    function save_name() {
        var textarea = $("input#id_user");
        if (textarea.val() == "") {
            return false;
        }

        var data = "user_name="+textarea.val();

        var http_request = new getXmlHttpRequest();
        http_request.open('POST', '/save_name/', true);
        http_request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded, charset=utf-8');
        http_request.onreadystatechange = function() { // Ждём ответа от сервера
            if (http_request.readyState == 4) { // Ответ пришёл
                if(http_request.status == 200) { // Сервер вернул код 200 (что хорошо)
                    // location.reload();
                }
            }
        };
        http_request.send(data);

    }

    $("button").click(save_name);
    
    $("input#id_user").keydown(function (e) {
        // Enter
        if (e.keyCode == 13) {
            save_name();
        }
    });
}

function activate_chat(thread_id, user_id, user_name) {
    $("div#chat form#chat-form div#compose input#id_text").focus();

    function scroll_chat_window() {
        $("div#chat div#chat-messages").scrollTop($("div#chat div#chat-messages")[0].scrollHeight);
    }

    scroll_chat_window();

    var chat_messages_html;

    function show() {  
        $.ajax({  
            url: "messages_view/?limit=20",
            type:"GET",
            async: false,
            cache: false,  
            success: function(html){  
                if (chat_messages_html != html){
                    $("div#chat div#chat-messages").html(html);
                    scroll_chat_window();
                    chat_messages_html = html;
                };
            }  
        });  
    }  
  
    $(document).ready(function(){  
        setInterval(show, 3000);  
    });

    function send_message() {
        
        var textarea = $("input#id_text");
        if (textarea.val() == "") {
            return false;
        }

        var data = "";

        data = "thread_id="+thread_id+"&";
        data += "user_id="+user_id+"&";
        data += "message="+textarea.val();

        textarea.val("");

        var http_request = new getXmlHttpRequest();
        http_request.open('POST', '/send_message/', true);
        http_request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded, charset=utf-8');
        http_request.onreadystatechange = function() { // Ждём ответа от сервера
            if (http_request.readyState == 4) { // Ответ пришёл
                if(http_request.status == 200) { // Сервер вернул код 200 (что хорошо)
                    textarea.val(""); // Выводим ответ сервера
                }
            }
        };

        http_request.send(data);
        show();
        scroll_chat_window();
    }


    $("div#chat form#chat-form div#compose button").click(send_message);

    $("input#id_text").keydown(function (e) {
        // Enter
        if (e.keyCode == 13) {
            send_message();
        }
    });
}