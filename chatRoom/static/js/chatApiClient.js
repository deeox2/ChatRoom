var URL = 'https://morning-headland-7475.herokuapp.com/chatroom/api';

function main(){
    constructChatRoom(10);
        setInterval(function() { fetchChatLog(populateChatRoom); }, 1000);
        USERNAME = prompt("What is your name?");
        $("div#username").append(USERNAME+":");
        $("button#send").on('click', function() { submitChatText(); } );
        $("input#chatText").on('keydown', function(e) {
            if (e.keyCode == 13) { submitChatText(); } 
        } );
}

function submitChatText(){
    var message = $("input#chatText").val();
    sendChatToServer(message);
    $("input#chatText").val("");
}

function sendChatToServer(message){
    // packages json object {username: , message: }
    // Post request -->  {% url 'chatApi' %}
    var csrftoken = $.cookie('csrftoken');
    var payload = {"username": USERNAME, "message": message};
    payloadReady = JSON.stringify(payload);
    $.ajax( {
        type:'POST',
        url: URL,
        data: payloadReady,
        dataType: 'json',
        beforeSend: function(xhr, settings){
            if (!csrfSafeMethod(settings.type) && !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function(response) { alert(response); }
    } );

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
}

function parseChatLog(chatLogJSON){
    // input: Json object  from server that includes vital information: username and message
    // Able to handle input {username: none, message: none}. This occurs when the DB is empty
    // output:  array = ['<username>: <message>', ...]
    var chatLog = [];
    var chatLogArrayDict = chatLogJSON['chatLog'];
    if(chatLogArrayDict  == 'none'){
        console.log("There are no chat records stored in the DB at this moment.");
    }
    else{
        chatLogArrayDict.forEach( function(dict){
            chatLine = dict['username'] + ': ' + dict['message'];
            chatLog.push(chatLine);
        } );
        return chatLog;
    }
}

function populateChatRoom(chatLogArr){
    chatLogArr.forEach( function(eachMessage, idx){
        $('li.chatRoom').eq(idx).text(eachMessage);
    });
}

function constructChatRoom(num){
    for(i=0; i < num; i++){
        var newLi = $('<li class="chatRoom">');
        $('ul#chatRoom').append(newLi);
    }
}

function fetchChatLog(callback){
    // this function will perform an ajax get request.
    // after successful request, ajax will... parseChatLog and populateChat
    // parseChatLog(chatLogJSON) returns chatLogArray
    // populateChatRoom(chatLogArray)  --> 
    $.ajax({
        type:'GET',
        url: URL,
        dataType:'json',
        success: function(response){
            var chatLogArray = parseChatLog(response);
            callback(chatLogArray);
        }
    });
}
