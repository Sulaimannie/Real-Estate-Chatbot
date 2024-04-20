<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ChatController;
use Illuminate\Support\Facades\Http;
/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('/sendQuestion', [ChatController::class, 'sendQuestion'])->name('sendQuestion');

// Route protected by auth:sanctum middleware
Route::get('/userDetails', [ChatController::class, 'userDetails'])->name('userDetails');
Route::post('/fetchChatMessage', [ChatController::class, 'fetchChatMessage'])->name('fetchChatMessage');
Route::post('/closeConversation', [ChatController::class, 'closeConversation'])->name('closeConversation');


