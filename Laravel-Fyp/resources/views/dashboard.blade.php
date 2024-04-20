<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <div class="flex">
        <!-- Sidebar: Chat list -->
        <div class="w-1/4 p-4 text-white" style="background-color: rgb(229, 232, 243); color: black;">
            <div class="text-gray-900 dark:text-gray-100">
                <h2 class="text-lg font-bold mb-4">Chats</h2>
                <ul>
                    @foreach($chats as $chat)
                        <li class="py-2">
                            <a href="#" onclick="selectChat('{{ $chat->created_at->format('Y-m-d') }}', '{{ $chat->id }}')">
                                {{ $chat->created_at->format('Y-m-d') }}
                            </a>
                        </li>
                    @endforeach
                </ul>
            </div>
        </div>
        <!-- Main Content: Chat interface -->
        <div class="w-3/4 p-4">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg">
                    <!-- Chat Interface -->
                    <div class="p-6 text-gray-900 dark:text-gray-100">
                        <div class="flex justify-between mb-4">
                            <button onclick="clearConversation()" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">New Chat</button>
                            <button onclick="closeConversation()" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">Close Conversation</button>
                        </div>
                        <!-- Chat Container -->
                        <div class="chat-container" id="chatContainer">
                            <!-- Chat Messages will be displayed here -->
                        </div>
                        <!-- Input field and send button -->
                        <div class="input-container">
                            <input type="text" id="messageInput" class="w-full border rounded-md p-2" placeholder="Type your message here...">
                            <button onclick="sendMessage()" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Send</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>

</x-app-layout>
<!-- Include jQuery from a CDN -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
    function selectChat(date, chatId) {
    // Clear the chat container
    document.getElementById('chatContainer').innerHTML = '';
    var userData = {!! json_encode(Auth::user()) !!};
    // Make an Ajax request to fetch the selected chat messages
    $.ajax({
        url: "{{ route('fetchChatMessage') }}", // Assuming 'fetchChatMessages' is your route for fetching the chat messages
        type: "POST",
        data: {
            'date': date,
            'chatId': chatId,
            'userId': userData.id
        },
        success: function(response) {
            console.log(response);
            // Iterate over each chat message in the response
            response.forEach(function(message) {
                // Append each fetched chat message to the chat container
                appendMessage(message.name, message.message);
                appendMessage("ChatBot", message.chat_response); // Assuming 'chat_response' is the attribute for chat responses
            });
        },
        error: function(xhr) {
            // Handle error response
            console.error(xhr.responseText);
        }
    });
}

    // Function to handle clearing the conversation
    function closeConversation() {
        
        var userData = {!! json_encode(Auth::user()) !!};
        // Make an Ajax request to send the message to the controller
        $.ajax({
            url: "{{ route('closeConversation') }}", // Assuming 'sendQuestion' is your route for the sendQuestion function
            type: "POST",
            data: {
                'status': "0",
                'userId': userData.id // Include user ID in the data
            },
            success: function(response) {
               // Clear the chat container
                document.getElementById('chatContainer').innerHTML = '';
                console.log("Conversation cleared.");
            },
            error: function(xhr) {
                // Handle error response
                console.error(xhr.responseText);
            }
        });
    }
    function clearConversation() {
        // Clear the chat container
        document.getElementById('chatContainer').innerHTML = '';
        console.log("Conversation cleared.");
    }
    function sendMessage() {
        var message = document.getElementById("messageInput").value;
        // Assuming you're passing user data as JSON to a JavaScript variable
        var userData = {!! json_encode(Auth::user()) !!};

        // Now you can access the user's details
        console.log(userData.name); // Accessing name
        console.log(userData.id); // Accessing email
        // Append user's message to the chat container
        appendMessage('{{ explode(' ', Auth::user()->name)[0] }}', message);
        
        // Clear the input field after sending the message
        document.getElementById("messageInput").value = '';
        
        // Make an Ajax request to send the message to the controller
        $.ajax({
            url: "{{ route('sendQuestion') }}", // Assuming 'sendQuestion' is your route for the sendQuestion function
            type: "POST",
            data: {
                '_token': '{{ csrf_token() }}',
                'message': message,
                'userId': userData.id // Include user ID in the data
            },
            success: function(response) {
                console.log(response.response);
                // Append chatbot's response to the chat container
                appendMessage("Chatbot", response.response);
            },
            error: function(xhr) {
                // Handle error response
                console.error(xhr.responseText);
            }
        });
    }

    // Function to append a new message to the chat container
    function appendMessage(name, message) {
        var chatContainer = document.getElementById('chatContainer');
        var newChatMessage = document.createElement('div');
        newChatMessage.classList.add('chat-message');
        newChatMessage.innerHTML = `
            <div class="chat-name">${name}:</div>
            <div class="chat-body">${message}</div>
        `;
        chatContainer.appendChild(newChatMessage);
        // Scroll to the bottom of the chat container
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
</script>

<style>
    /* CSS for chat interface */
    .chat-container {
        display: flex;
        flex-direction: column;
        height:21rem;
        max-height: 400px; /* Adjust as needed */
        overflow-y: auto; /* Enable vertical scroll */
    }

    .chat-message {
        display: flex;
        margin-bottom: 10px;
    }

    .chat-name {
        flex: 0 0 100px; /* Adjust width of chat names column */
        font-weight: bold;
        padding-right: 10px;
    }

    .chat-body {
        flex: 1;
        background-color: #f0f0f0; /* Background color for chat messages */
        padding: 10px;
        border-radius: 10px;
    }

    /* CSS for input field and send button */
    .input-container {
        display: flex;
        margin-top: 20px;
    }

    .input-container input {
        flex: 1;
    }

    .input-container button {
        margin-left: 10px;
    }
</style>
