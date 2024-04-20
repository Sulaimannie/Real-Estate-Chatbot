<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http; // Add this line to import the Http facade
use App\Models\Chat; // Assuming you have a Chat model
use Illuminate\Support\Facades\Auth; // Import the Auth facade
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Log;

class ChatController extends Controller
{
    public function sendQuestion(Request $request)
    {
        // Retrieve the message from the Ajax request
        $userMessage = $request->input('message');
        $user_id = $request->input('userId');

        // Save the user message to the database
        $user = "1";
        $chat = new Chat();
        $chat->user_id = $user_id; // Assuming you're using authentication
        $chat->user_message = $userMessage;
        $chat->save();

        // Define the question as an associative array
        $question = [
            'question' => $userMessage
        ];
        
        // Send the question as a JSON request to the external API
        $response = Http::withHeaders([
            'Accept' => 'application/json',
            'Content-Type' => 'application/json',
        ])->post('http://127.0.0.1:5000/chatbot', $question);

        Log::info('Response Body: ' . $response->body());
        Log::info('Response Headers: ', $response->headers());
     

        // Check if the request was successful
        if ($response->successful()) {
            // Process the response
            $apiResponse = $response->json();
           
            // Save the chatbot response to the database
            $chat->chat_response = $apiResponse;
            $chat->save();

            // Do something with the API response
            return response()->json($apiResponse);
        } else {
            // Handle the error
            return response()->json(['error' => 'Failed to send question'], 400);
        }
    }
    public function closeConversation(Request $request){
        $status = $request->input('status');
        $user_id = $request->input('userId');

        Chat::where('user_id','=',$user_id)
        ->update([
            'status' => "0"
         ]);
        return response()->json(['message' => 'status updated to close conversation'], 200);
    }
    public function fetchChatMessage(Request $request){
        $date = $request->input('date');
        // $chat_id = $request->input('chatId');
        $user_id = $request->input('userId');
    
        // Fetch the chat message based on date, chat ID, and user ID
        $chat = Chat::whereDate('created_at', $date)
                    // ->where('id', $chat_id)
                    ->where('user_id', $user_id) // Assuming user is logged in
                    ->get();
                   
    
        if ($chat->isNotEmpty()) { // Check if the collection is not empty
            // Return the fetched chat message
            $chatMessages = $chat->map(function ($message) {
                return [
                    'name' => $message->user->name, // Assuming you have a relationship to the User model
                    'message' => $message->user_message,
                    'chat_response' =>$message->chat_response,
                ];
            });
    
            return response()->json($chatMessages);
        } else {
            // Return a 404 response if chat message is not found
            return response()->json(['error' => 'Chat message not found.'], 404);
        }
    }
    

}
