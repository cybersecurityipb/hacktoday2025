#define UNICODE
#include <windows.h>
#include <map>
#include <string>
#include <cctype>
#include <vector>
#include "picosha2.h"

using namespace std;

const int MAX_INPUT = 60;
const string SECRET = "d1a451276fa47eded93b7db73edc98f8bbc143f5ce3894177abeb52cb79bfda4";

map<wchar_t, wstring> morseTable = {
    {L'y', L".-"},
    {L'e', L"-..."},
    {L'j', L"-.-."},
    {L'3', L"-.."},
    {L'?', L"."},
    {L'8', L"..-."},
    {L'0', L"--."},
    {L'6', L"...."},
    {L'.', L".."},
    {L'l', L".---"},
    {L'-', L"-.-"},
    {L'r', L".-.."},
    {L'_', L"--"},
    {L'f', L"-."},
    {L'4', L"---"},
    {L'a', L".--."},
    {L'u', L"--.-"},
    {L's', L".-."},
    {L'2', L"..."},
    {L'g', L"-"},
    {L'w', L"..-"},
    {L'h', L"...-"},
    {L'm', L".--"},
    {L'!', L"-..-"},
    {L'o', L"-.--"},
    {L'q', L"--.."},
    {L'9', L"-----"},
    {L'v', L".----"},
    {L'k', L"..---"},
    {L'p', L"...--"},
    {L'7', L"....-"},
    {L'i', L"....."},
    {L'b', L"-...."},
    {L'c', L"--..."},
    {L'#', L"---.."},
    {L'n', L"----."},
    {L'{', L".-.-.-"},
    {L'x', L"--..--"},
    {L'z', L"..--.."},
    {L'5', L"-.-.--"},
    {L'1', L"-....-"},
    {L'd', L"-..-."},
    {L't', L"-.--."},
    {L'}', L"-.--.-"}
};

#define ID_BUTTON_GEN     1
#define ID_BUTTON_SECRET  2
#define ID_INPUT_SECRET   3
#define ID_BUTTON_SUBMIT  4
#define ID_TEXT_RESULT    5

HWND hInput, hGenerateBtn, hSecretBtn, hLamp;
HWND hSecretInput, hSubmitBtn, hResultText;
HBRUSH hCurrBrush;
HBRUSH hBrushOn = CreateSolidBrush(RGB(255, 0, 0));
HBRUSH hBrushOff = CreateSolidBrush(RGB(30, 30, 30));

wstring ToLower(const wstring& s) {
    wstring res;
    for (wchar_t c : s)
        res += towlower(c);
    return res;
}

vector<int> StringToDelays(const wstring& input) {
    vector<int> delays;

    for (wchar_t c : input) {
        c = towlower(c);

        if (!morseTable.count(c))
            continue;

        const wstring& code = morseTable[c];

        for (wchar_t m : code) {
            if (m == L'.') {
                delays.push_back(65);
            } else if (m == L'-') {
                delays.push_back(85);
            } 
            delays.push_back(45);
        }
        delays.pop_back();
        delays.push_back(65);
    }

    return delays;
}


void EnableControls(HWND hwnd, BOOL enable) {
    EnableWindow(hInput, enable);
    EnableWindow(hGenerateBtn, enable);
    EnableWindow(hSecretBtn, enable);
    EnableWindow(hSecretInput, enable);
    EnableWindow(hSubmitBtn, enable);
}

void BlinkMorse(HWND hwnd, const vector<int>& delays) {
    EnableControls(hwnd, FALSE); 

    bool on = true;
    for (int duration : delays) {
        hCurrBrush = on ? hBrushOn : hBrushOff;
        InvalidateRect(hLamp, NULL, TRUE);
        UpdateWindow(hLamp);
        Sleep(duration);
        on = !on;
    }

    hCurrBrush = hBrushOff;
    InvalidateRect(hLamp, NULL, TRUE);
    UpdateWindow(hLamp);

    EnableControls(hwnd, TRUE); 
}


void ShowMorseFromInput(HWND parent) {
    wchar_t buf[MAX_INPUT + 1];
    GetWindowTextW(hInput, buf, MAX_INPUT);
    wstring input = ToLower(buf);
    vector<int> morse = StringToDelays(input);
    BlinkMorse(hLamp, morse);
}

void ShowMorseFromSecret() {
    vector<int> morse = {65, 45, 65, 45, 65, 45, 85, 65, 65, 45, 85, 45, 85, 45, 65, 65, 85, 45, 85, 45, 65, 45, 65, 45, 65, 65, 65, 45, 65, 45, 85, 45, 85, 45, 85, 65, 85, 45, 65, 45, 85, 45, 85, 45, 65, 65, 85, 45, 65, 45, 85, 45, 85, 65, 85, 45, 65, 45, 65, 45, 85, 45, 65, 65, 65, 45, 85, 45, 85, 45, 65, 65, 65, 45, 85, 65, 65, 45, 85, 45, 65, 45, 85, 45, 65, 45, 85, 65, 65, 45, 85, 45, 65, 65, 65, 45, 85, 45, 85, 45, 85, 65, 85, 45, 65, 45, 65, 45, 65, 65, 85, 45, 65, 45, 65, 45, 65, 65, 65, 45, 65, 45, 65, 45, 85, 45, 85, 65, 85, 45, 85, 65, 65, 45, 85, 45, 65, 65, 65, 45, 85, 45, 85, 45, 85, 65, 85, 45, 65, 45, 65, 45, 65, 65, 85, 45, 65, 45, 65, 45, 65, 65, 65, 45, 65, 45, 65, 45, 85, 45, 85, 65, 85, 45, 85, 65, 65, 45, 85, 45, 65, 65, 65, 45, 85, 45, 85, 45, 85, 65, 85, 45, 65, 45, 65, 45, 65, 65, 85, 45, 65, 45, 65, 45, 65, 65, 65, 45, 65, 45, 65, 45, 85, 45, 85, 65, 85, 45, 85, 65, 65, 45, 85, 45, 85, 45, 85, 65, 85, 45, 85, 45, 65, 45, 85, 65, 85, 45, 85, 65, 65, 45, 85, 45, 85, 45, 65, 65, 65, 45, 65, 45, 65, 45, 85, 45, 85, 65, 65, 45, 85, 45, 85, 45, 65, 65, 85, 45, 85, 65, 85, 45, 65, 45, 65, 45, 65, 45, 65, 65, 65, 45, 85, 45, 85, 45, 65, 65, 65, 45, 85, 65, 65, 45, 65, 45, 65, 45, 65, 45, 65, 65, 85, 45, 85, 65, 85, 45, 65, 45, 85, 45, 85, 45, 65, 65, 65, 45, 65, 45, 65, 45, 65, 45, 65, 65, 85, 45, 65, 45, 65, 45, 85, 45, 65, 65, 85, 45, 85, 45, 65, 45, 85, 65, 65, 45, 85, 45, 65, 45, 65, 65, 85, 45, 85, 65, 65, 45, 85, 45, 65, 65, 65, 45, 65, 45, 65, 45, 65, 45, 65, 65, 65, 45, 85, 45, 85, 45, 65, 65, 85, 45, 85, 45, 85, 45, 85, 45, 65, 65, 85, 65, 65, 65, 85, 45, 65, 45, 85, 45, 85, 45, 65, 45, 85, 65};
    BlinkMorse(hLamp, morse);
}

WNDPROC originalEditProc;

LRESULT CALLBACK EditInputProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (msg == WM_CHAR) {
        wchar_t c = (wchar_t)wParam;

        if (c == VK_BACK || c == VK_RETURN || 
            c == L'.' || c == L'_' || c == L'!' ||
            c == L'?' || c == L'#' || c == L'{' || 
            c == L'}' || c == L' ' || c == L'-') {
            return CallWindowProc(originalEditProc, hwnd, msg, wParam, lParam);
        }

        if (iswlower(c) || iswdigit(c)) {
            return CallWindowProc(originalEditProc, hwnd, msg, wParam, lParam);
        }

        return 0;
    }
    
    return CallWindowProc(originalEditProc, hwnd, msg, wParam, lParam);
}

WNDPROC originalSecretProc;

LRESULT CALLBACK EditSecretProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (msg == WM_CHAR) {
        wchar_t c = (wchar_t)wParam;

        if (c == VK_BACK || c == VK_RETURN || 
            c == L'.' || c == L'_' || c == L'!' ||
            c == L'?' || c == L'#' || c == L'{' || 
            c == L'}' || c == L' ' || c == L'-') {
            return CallWindowProc(originalSecretProc, hwnd, msg, wParam, lParam);
        }

        if (iswlower(c) || iswdigit(c)) {
            return CallWindowProc(originalSecretProc, hwnd, msg, wParam, lParam);
        }

        return 0;
    }

    return CallWindowProc(originalSecretProc, hwnd, msg, wParam, lParam);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
    case WM_CREATE:
        hInput = CreateWindowW(L"EDIT", L"", WS_CHILD | WS_VISIBLE | WS_BORDER,
            20, 20, 400, 25, hwnd, NULL, NULL, NULL);
        
        originalEditProc = (WNDPROC)SetWindowLongPtr(hInput, GWLP_WNDPROC, (LONG_PTR)EditInputProc);
        
        hGenerateBtn = CreateWindowW(L"BUTTON", L"Generate Message", WS_CHILD | WS_VISIBLE,
            430, 20, 130, 25, hwnd, (HMENU)ID_BUTTON_GEN, NULL, NULL);

        hSecretInput = CreateWindowW(L"EDIT", L"", WS_CHILD | WS_VISIBLE | WS_BORDER,
            20, 60, 400, 25, hwnd, (HMENU)ID_INPUT_SECRET, NULL, NULL);

        originalSecretProc = (WNDPROC)SetWindowLongPtr(hSecretInput, GWLP_WNDPROC, (LONG_PTR)EditSecretProc);

        hSubmitBtn = CreateWindowW(L"BUTTON", L"Submit Guess", WS_CHILD | WS_VISIBLE,
            430, 60, 130, 25, hwnd, (HMENU)ID_BUTTON_SUBMIT, NULL, NULL);

        hResultText = CreateWindowW(L"STATIC", L"", WS_CHILD | WS_VISIBLE,
            570, 60, 150, 25, hwnd, (HMENU)ID_TEXT_RESULT, NULL, NULL);

        hSecretBtn = CreateWindowW(L"BUTTON", L"Secret Message", WS_CHILD | WS_VISIBLE,
            20, 100, 130, 25, hwnd, (HMENU)ID_BUTTON_SECRET, NULL, NULL);

        hLamp = CreateWindowW(L"STATIC", L"", WS_CHILD | WS_VISIBLE | SS_CENTER, 350, 140, 100, 100, hwnd, NULL, NULL, NULL);
        hCurrBrush = hBrushOff;

        break;
    case WM_CTLCOLORSTATIC:
        if ((HWND)lParam == hLamp) {
            HDC hdcStatic = (HDC)wParam;
            SetBkMode(hdcStatic, TRANSPARENT);
            return (INT_PTR)hCurrBrush;
        }
        break;

    case WM_COMMAND:
        switch (LOWORD(wParam)) {
        case ID_BUTTON_GEN:
            ShowMorseFromInput(hwnd);
            break;
        case ID_BUTTON_SECRET:
            ShowMorseFromSecret();
            break;
        case ID_BUTTON_SUBMIT: {
            wchar_t guess[MAX_INPUT + 1];
            GetWindowTextW(hSecretInput, guess, MAX_INPUT);
            wstring wsGuess(guess);
            string sGuess(wsGuess.begin(), wsGuess.end());
            string hash = picosha2::hash256_hex_string(sGuess);
            
            if (hash == SECRET) {
                SetWindowTextW(hResultText, L"Correct!");
            } else {
                SetWindowTextW(hResultText, L"Wrong!");
            }
            break;
        }
        }
        break;

    case WM_DESTROY:
        PostQuitMessage(0);
        break;

    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    const wchar_t CLASS_NAME[] = L"MorseLikeCode";

    WNDCLASS wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0, CLASS_NAME, L"Message Visualizer",
        WS_OVERLAPPEDWINDOW ^ WS_THICKFRAME ^ WS_MAXIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 760, 300,
        NULL, NULL, hInstance, NULL
    );

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}
