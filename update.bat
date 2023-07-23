pyinstaller --onefile main.py
mkdir game
cd dist
move main.exe ..
cd ..
move main.exe game
butler push "game/" marctho8/slimery:windows
del game
del dist
del build
del main.spec
