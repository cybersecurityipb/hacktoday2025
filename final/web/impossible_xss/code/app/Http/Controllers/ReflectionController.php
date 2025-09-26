<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use voku\helper\AntiXSS;

class ReflectionController extends Controller
{
    public function show()
    {
        return view('reflection', ['input' => null, 'safe' => null]);
    }

    public function reflect(Request $request)
    {
        $data = $request->validate([
            'user_input' => 'required|string|max:5000', 
        ]);

        $raw = $data['user_input'];
        $antiXss = new AntiXSS();
        $clean = $antiXss->xss_clean($raw);
        return view('reflection', ['input' => $raw, 'safe' => $clean]);
    }
}
