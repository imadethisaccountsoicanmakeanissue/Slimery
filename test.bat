pyinstaller main.spec
mkdir game
cd dist
move main.exe ..
cd ..
move main.exe game
cd game
main.exe
cd ..
