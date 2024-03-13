pyinstaller main.spec
mkdir game
cd dist
move main.exe ..
cd ..
move main.exe game
butler push "game/" marctho8/slimery:windows