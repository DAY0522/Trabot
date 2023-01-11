// == 연산자: 서로 다른 유형 "값" 비교
// === 연산자: 서로 다른 유형 "값" "자료형" 비교

// variables
let userName = localStorage.getItem("userName");
let state = 'SUCCESS';

// functions
function Message(arg) {
    this.text = arg.text;
    this.message_side = arg.message_side;

    this.draw = function (_this) {
        return function () {
            let $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.message_side).find('.text').html(_this.text);
            $('.messages').append($message);

            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
}

function getMessageText() { //최근 입력한 메시지 내용(?)을 저장
    let $message_input;
    $message_input = $('.message_input');
    return $message_input.val();
}

function sendMessage(text, message_side) {
    let $messages, message;
    $('.message_input').val('');
    $messages = $('.messages');
    message = new Message({ //새롭게 입력받은 메시지를 저장하는 듯
        text: text,
        message_side: message_side
    });
    message.draw(); //Message함수 안의 draw함수? 이용
    $messages.animate({scrollTop: $messages.prop('scrollHeight')}, 300);
    //prop(): js의 property를 취급
    //scrollTop: scroll바 위치를 위에서 300px로 정함
    //scrollHeight: scroll 시키지 않았을 때 전체 높이
}

function greet() { //챗봇 처음 실행될 때, 인사하는 함수
    if(userName !== null) return setUserName(userName)
    setTimeout(function () {
        return sendMessage("TRABOT 방문을 환영합니다~!", 'left');
    }, 1000); //1초후에 띄움

    setTimeout(function () {
        return sendMessage("저는 여행지를 추천해주는 트래봇입니다!", 'left');
    }, 2000);

    setTimeout(function () {
        return sendMessage("사용할 닉네임을 알려주세요!", 'left');
    }, 3000);

}

function onClickAsEnter(e) {
    if (e.keyCode === 13) { //enter 쳤을때 전송됐다는 표시를 해줘야 함
        onSendButtonClicked()
    }
}

function setUserName(username) { //사용자 이름 설정 함수
    if (username !== null && username.replace(" ", "" !== "")) {
        setTimeout(function () {
            return sendMessage("반갑습니다." + username + "님", 'left');
        }, 1000);

        setTimeout(function () {
           return sendMessage("원하는 여행 정보에 대한 키워드를 입력하세요! <br> 1.지역 2. 근처 3.테마 ", 'left');
        }, 2000);

        return username; //사용자 이름을 반환

    } else { //user 이름을 입력받지 못할 때
        setTimeout(function () {
            return sendMessage("올바른 닉네임을 이용해주세요.", 'left');
        }, 1000);

        return null; //입력받지 못했으므로 기본값을 반환
    }
}

function requestChat(messageText, url_pattern) {
    $.ajax({
        url: "http://127.0.0.1:8080/" + url_pattern + '/' + userName + '/' + messageText,
        type: "GET",
        dataType: "json",
        success: function (data) {
            state = data['state'];

            if (state === 'SUCCESS') {
                //모든 entity가 정상적으로 입력된 경우
                return sendMessage(data['answer'], 'left');
                //
            } else if (state === 'REQUIRE_LOCATION')
               //기본값이 없는 엔티티가 입력되지 않음
                     if(messageText==('1')) {
                       setTimeout(function () {
                return sendMessage("기상정보에 대해 알려드릴게요! 무엇이든 물어보세요~", 'left');
            }, 1000);
            }
                     else if(messageText==('2')) {
                       setTimeout(function () {
                return sendMessage("여행지 추천 또는 맛집에 대해 알려드릴게요! 무엇이든 물어보세요~", 'left');
            }, 1000);
}
                   else if(messageText==('3')) {
                       setTimeout(function () {
                return sendMessage("여행지 코스를 추천해드릴게요! 무엇이든 물어보세요~", 'left');
            }, 1000);
    }
               // return sendMessage('어느 지역을 알려드릴까요?', 'left');
             else {
                return sendMessage('죄송합니다. 무슨말인지 잘 모르겠어요.', 'left');
            }
        },

        error: function (request, status, error) {
            console.log(error);

            return sendMessage('죄송합니다. 서버 연결에 실패했습니다.', 'left');
        }
    });
}

function onSendButtonClicked() {
    let messageText = getMessageText();
    sendMessage(messageText, 'right');

    if (userName == null) {
        localStorage.setItem("userName",messageText);
        userName = localStorage.getItem("userName");
        setUserName(userName)
    }

    else {

    if (messageText.includes('안녕')) {
            setTimeout(function () {
                return sendMessage("안녕하세요. 저는 트래봇입니다~!", 'left');
            }, 1000);
    }
    else if (messageText.includes('고마워')) {
            setTimeout(function () {
                return sendMessage("천만에요. 더 물어보실 건 없나요?", 'left');
            }, 1000);
    }
    else if (messageText.includes('없어')) {
            setTimeout(function () {
                return sendMessage("아쉽네요ㅠㅠ 알겠습니다!", 'left');
            }, 1000);


    }
    else if (state.includes('REQUIRE')) {
            return requestChat(messageText, 'fill_slot');
            //사용자에게 되묻고 기존 딕셔너리에 추가
        }
    else {
            return requestChat(messageText, 'request_chat');
        }
    }

    }

//let inputValue = document.getElementByClassName('message_input')[0].value