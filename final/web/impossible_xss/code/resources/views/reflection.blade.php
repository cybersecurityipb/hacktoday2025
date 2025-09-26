<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Reflection Demo</title>

  <!-- Minimal CSS to make it readable -->
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial; background:#f8fafc; color:#0f1724; margin:2rem}
    .wrap{max-width:900px; margin:0 auto}
    textarea{width:100%; min-height:140px; padding:0.5rem; font-size:1rem; border-radius:6px; border:1px solid #d1d5db}
    button{padding:0.5rem 0.9rem; border-radius:6px; border:none; background:#2563eb; color:#fff; cursor:pointer}
    .card{background:#fff; border:1px solid #e6eef8; padding:1rem; border-radius:8px; margin-top:1rem}
    pre{white-space:pre-wrap; background:#f1f5f9; padding:0.6rem; border-radius:6px}
    .meta{color:#6b7280; font-size:0.9rem; margin-bottom:0.5rem}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Impossible XSS??</h1>
    <p class="meta">Enter text or simple HTML. Server sanitization is applied before reflection.</p>

    <div class="card">
      <form method="POST" action="{{ route('reflection.reflect') }}">
        @csrf

        <label for="user_input">Your input</label>
        <textarea id="user_input" name="user_input" placeholder="Type something...">{{ old('user_input', $input) }}</textarea>

        @error('user_input')
          <div style="color:#b91c1c; margin-top:0.5rem">{{ $message }}</div>
        @enderror

        <div style="margin-top:0.75rem">
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>

    <div class="card" style="margin-top:1rem">
      <div class="meta" style="margin-top:0.75rem">Sanitized output</div>

      <!-- We output sanitized HTML. If you prefer to show tags as text, replace {!! $safe !!} with {{ $safe }} -->
      <div style="padding:0.5rem; border-radius:6px; background:#ffffff;">
        {!! $safe !!}
      </div>
    </div>
  </div>
</body>
</html>
