var URL = 'http://127.0.0.1:8000/chatroom/api';

function sendChatToServer(username, message){
    // packages json object {username: , message: }
    // Post request -->  {% url 'chatApi' %}
    payload = {"username": username, "message": message};
    payloadReady = JSON.stringify(payload);
    $.ajax( {
        type:'POST',
        url: URL,
        data: payloadReady,
        dataType: 'json',
        success: function(response) { alert(response); }
    } );
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
