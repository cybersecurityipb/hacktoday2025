const express = require("express");

const app = express();
const PORT = 54321;

const allowedRegex = /^[\x20-\x7E]*$/;
const arr = {
  '0': 'D',
  '1': '1',
  '2': '#',
  '3': 'M',
  '4': 'x',
  '5': '&',
  '6': 'N',
  '7': 'h',
  '8': 'J',
  '9': ']',
  ' ': '0',
  '!': '>',
  '"': '9',
  '#': '5',
  '$': '6',
  '%': '/',
  '&': "'",
  "'": '<',
  '(': 'r',
  ')': ')',
  '*': '.',
  '+': 'g',
  ',': '[',
  '-': ',',
  '.': 'K',
  '/': '2',
  ':': '_',
  ';': 'p',
  '<': 't',
  '=': '}',
  '>': 'W',
  '?': 'C',
  '@': 'i',
  A: 'U',
  B: '`',
  C: 'O',
  D: 'P',
  E: '!',
  F: 'e',
  G: 'H',
  H: '$',
  I: 'w',
  J: 'y',
  K: 'I',
  L: '^',
  M: 'R',
  N: 'G',
  O: 'F',
  P: 'E',
  Q: ';',
  R: '%',
  S: '"',
  T: 'X',
  U: '-',
  V: 'k',
  W: 'd',
  X: '~',
  Y: '8',
  Z: ':',
  '[': '+',
  '\\': 'z',
  ']': 'T',
  '^': 'l',
  _: 'Q',
  '`': '{',
  a: 'j',
  b: 'f',
  c: '3',
  d: 'c',
  e: ' ',
  f: '4',
  g: '|',
  h: 's',
  i: 'Z',
  j: 'B',
  k: 'b',
  l: '\\',
  m: 'A',
  n: 'n',
  o: 'v',
  p: '@',
  q: 'q',
  r: 'Y',
  s: 'a',
  t: 'o',
  u: '(',
  v: 'S',
  w: '7',
  x: '=',
  y: 'L',
  z: '?',
  '{': 'V',
  '|': 'm',
  '}': 'u',
  '~': '*'
}

function encode(str, arr) {
  return str.split("").map(ch => arr[ch] || ch).join("");
}

function isValidInput(str) {
  return allowedRegex.test(str);
}

app.get("/", (req, res) => {
  res.send(`
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Flag Checker</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #000000, #0f3d2e);
      color: #e0ffe0;
    }
    .card {
      max-width: 400px;
      width: 100%;
      background: rgba(0, 0, 0, 0.85);
      border: 1px solid #1db954;
      border-radius: 15px;
      color: #e0ffe0;
    }
    .btn-custom {
      background-color: #1db954;
      border: none;
      font-weight: bold;
      transition: 0.3s;
    }
    .btn-custom:hover {
      background-color: #17a34a;
    }
  </style>
</head>
<body>
  <div class="card shadow p-4">
    <h3 class="text-center mb-3">Flag Checker</h3>
    <form action="/check" method="get">
      <div class="mb-3">
        <input type="text" class="form-control" name="flag" placeholder="input the flag" required>
      </div>
      <div class="d-grid">
        <button type="submit" class="btn btn-custom">CHECK</button>
      </div>
    </form>
  </div>
</body>
</html>
  `);
});

app.get("/check", (req, res) => {
  const teks = req.query.flag;

  if(!isValidInput(teks)){
    res.send(`
      <div style="
        display:flex;align-items:center;justify-content:center;
        height:100%;background:linear-gradient(135deg,#000000,#330000);color:#ff4d4d;
        font-family:sans-serif;">
        <h2 style="font-size:2rem;">❌ Invalid Characters! Try Again.</h2>
      </div>
    `);
  }

  const encoded = Buffer.from(encode(teks, arr), "utf-8").toString("base64");

  if (encoded === "c2ozYm92Y2pMVmNaYShZKHNRYlpufFEobnZRZihqb1FhdmpcUVxqfFp1") {
    res.send(`
      <div style="
        display:flex;align-items:center;justify-content:center;
        height:100%;background:linear-gradient(135deg,#000000,#0f3d2e);color:#1db954;
        font-family:sans-serif;">
        <h2 style="font-size:2rem;">✅ Correct! ${teks}.</h2>
      </div>
    `);
  } else {
    res.send(`
      <div style="
        display:flex;align-items:center;justify-content:center;
        height:100%;background:linear-gradient(135deg,#000000,#330000);color:#ff4d4d;
        font-family:sans-serif;">
        <h2 style="font-size:2rem;">❌ Wrong! Try Again.</h2>
      </div>
    `);
  }
});

const server = app.listen(PORT, () => {
  console.log(`Flag Checker -> http://localhost:${PORT}`);
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(`⚠️ Port ${PORT} is already in use`);
    process.exit(1);
  } else {
    console.error(err);
  }
});