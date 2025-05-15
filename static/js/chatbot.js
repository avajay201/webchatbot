(function (){
    const apiKey = document.currentScript?.getAttribute("data-api-key") || "";
    if (!apiKey){
        return;
    }

    const html = `
        <div class="chat-container" id="chatContainer">
            <button class="chat-icon" id="chatIcon" type="button">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="lucide lucide-message-circle">
                    <path
                        d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z">
                    </path>
                </svg>
            </button>

            <div class="chat-window" id="chatWindow">
                <div class="chat-header" id="chatHeader">
                    <h3 id="headerText">AI Bot</h3>
                    <button class="close-btn" id="closeChat" type="button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="lucide lucide-x">
                            <path d="M18 6 6 18"></path>
                            <path d="m6 6 12 12"></path>
                        </svg>
                    </button>
                </div>
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot-message">
                        <div class="message-content" id="welcomeMessage">Hello! How can I help you today?</div>
                    </div>
                </div>
                <div class="chat-input-container" id="inputContainer">
                    <input type="text" id="msgInput" placeholder="Type your message..." class="chat-input">
                    <button id="sendMessage" class="send-btn" type="button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="lucide lucide-send">
                            <path d="m22 2-7 20-4-9-9-4Z"></path>
                            <path d="M22 2 11 13"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        `;

    let botName;
    let chatbotUI;
    let loading;

    const initChatbot = () => {
        const wrapper = document.createElement("div");
        wrapper.innerHTML = html.trim();
        document.body.appendChild(wrapper.firstChild);

        const styles = `
        @media (min-width: 1024px) {
            .chat-container .flex .flex-col-reverse {
                flex-direction: row;
            }
        }

        .chat-container {
            position: fixed;
            bottom: 25px;
            right: 20px;
            z-index: 1000;
            font-family: ${chatbotUI.font_family};
        }

        .chat-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: ${chatbotUI.chat_icon_bg_color};
            color: ${chatbotUI.chat_icon_color};
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }

        .chat-icon:hover {
            transform: scale(1.05);
        }

        .chat-container .chat-window {
            position: absolute;
            bottom: 0;
            right: 0;
            width: 350px;
            height: 450px;
            background-color: white;
            border-radius: ${chatbotUI.border_radius + "px"};
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            display: none;
            transition: all 0.3s ease;
        }

        .chat-container .chat-header {
            background-color: ${chatbotUI.header_bg_color};
            color: ${chatbotUI.header_text_color};
            padding: 5px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-container .chat-header h3 {
            font-size: 16px;
            font-weight: 600;
        }

        .chat-container .close-btn {
            background: none;
            border: none;
            color: ${chatbotUI.chat_close_btn_color};
            cursor: pointer;
        }

        .chat-container .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            background-color: ${chatbotUI.msg_box_bg_color};
        }

        .chat-container .message {
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 18px;
            margin-bottom: 5px;
            word-wrap: break-word;
        }

        .chat-container .user-message {
            align-self: flex-end;
            background-color: ${chatbotUI.user_message_bg_color};
            color: ${chatbotUI.user_message_text_color};
            border-bottom-right-radius: 5px;
        }

        .chat-container .bot-message {
            align-self: flex-start;
            background-color: ${chatbotUI.bot_message_bg_color};
            color: ${chatbotUI.bot_message_text_color};
            border-bottom-left-radius: 5px;
        }

        .chat-container .message-content {
            font-size: 14px;
            line-height: 1.4;
        }

        .chat-container .chat-input-container {
            display: flex;
            padding: 10px;
        }

        .chat-container .chat-input {
            flex: 1;
            padding: 10px 15px;
            border: 1px solid ${chatbotUI.input_border_color};
            border-radius: 20px;
            outline: none;
            font-size: 14px;
            color: ${chatbotUI.input_color};
        }
        
        .chat-container .chat-input::placeholder {
            color: ${chatbotUI.input_placeholder_text};
        }

        .chat-container .send-btn {
            background: none;
            border: none;
            color: ${chatbotUI.send_btn_color};
            cursor: pointer;
            margin-left: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .chat-container #inputContainer {
            background-color: ${chatbotUI.input_container_bg_color};
        }
        
        .chat-container #chatMessages::-webkit-scrollbar {
            width: ${chatbotUI.scrollbar_width}px;
        }
        
        .chat-container #chatMessages::-webkit-scrollbar-thumb {
            background-color: ${chatbotUI.scrollbar_color};
            border-radius: 4px;
        }
        
        .chat-container #chatMessages {
            scrollbar-width: ${chatbotUI.scrollbar_width <= 8 ? 'thin' : 'auto'};
            scrollbar-color: ${chatbotUI.scrollbar_color} #f1f1f1;
        }

        @media (max-width: 480px) {
            .chat-container .chat-window {
                width: 300px;
                height: 400px;
                right: 0;
            }
        }
        `;

        const styleTag = document.createElement('style');
        styleTag.textContent = styles;
        document.head.appendChild(styleTag);

        const chatMessages = document.getElementById("chatMessages");
        const sendMessage = document.getElementById("sendMessage");
        const msgInput = document.getElementById("msgInput");
        const closeChat = document.getElementById("closeChat");
        const chatIcon = document.getElementById("chatIcon")
        const chatWindow = document.getElementById("chatWindow")
        const welcomeMessageEle = document.getElementById("welcomeMessage")

        welcomeMessageEle.textContent = chatbotUI.welcome_message;
        document.getElementById('headerText').textContent = botName;

        chatIcon.addEventListener("click", () => {
            chatWindow.style.display = "flex"
            chatIcon.style.display = "none"
        })

        closeChat.addEventListener("click", () => {
            chatWindow.style.display = "none"
            chatIcon.style.display = "flex"
        })

        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement("div")
            messageDiv.classList.add("message")
            messageDiv.classList.add(isUser ? "user-message" : "bot-message")

            const messageContent = document.createElement("div")
            messageContent.classList.add("message-content")
            messageContent.textContent = message

            messageDiv.appendChild(messageContent)
            chatMessages.appendChild(messageDiv)

            chatMessages.scrollTop = chatMessages.scrollHeight
        };

        sendMessage.addEventListener("click", () => {
            sendUserMessage()
        });

        msgInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                sendUserMessage()
            }
        });

        async function sendUserMessage() {
            const message = msgInput.value.trim()

            if (message !== "" && !loading) {
                loading = true;
                addMessage(message, true);

                msgInput.value = ""

                const res = await fetch("http://localhost:8000/api/chat-bot/chatbot-reply/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ api_key: apiKey, query: message }),
                });

                const result = await res.json();
                const reply = result.reply || 'Sorry, something went wrong.';
                addMessage(reply);
                loading = false;
            }
        }
    }

    const validateChatBot = async () => {
        const res = await fetch("http://localhost:8000/api/chat-bot/validate-chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ api_key: apiKey }),
        });
        const result = await res.json();
        if (result.name) {
            botName = result.name;
            chatbotUI = result.ui;
            initChatbot();
        }
    };

    validateChatBot();
})();
