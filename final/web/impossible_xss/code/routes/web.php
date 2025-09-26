<?php

use App\Http\Controllers\ReflectionController;
use Illuminate\Support\Facades\Route;

Route::get('/', [ReflectionController::class, 'show'])->name('reflection.show');
Route::post('/reflect', [ReflectionController::class, 'reflect'])->name('reflection.reflect');
