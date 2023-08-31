
#Before this there was another deployment file that copies this one to gcloud .... https://github.com/CoderRayMan/pythons/blob/master/AI/Resume_scanner/deploy.sh
#run that before this one
cat << 'EOF'
 _________________________________________ 
/                                         \
|                                         |
| We are starting the Main Deploy         |
| Script...... Please be patient ... this |
| may take some time                      |
|                                         |
| Patience is the Key                     |
|                                         |
\ -- Ankshuk Ray                          /
 ----------------------------------------- 
      \                    / \  //\
       \    |\___/|      /   \//  \\
            /0  0  \__  /    //  | \ \    
           /     /  \/_/    //   |  \  \  
           @_^_@'/   \/_   //    |   \   \ 
           //_^_/     \/_ //     |    \    \
        ( //) |        \///      |     \     \
      ( / /) _|_ /   )  //       |      \     _\
    ( // /) '/,_ _ _/  ( ; -.    |    _ _\.-~        .-~~~^-.
  (( / / )) ,-{        _      `-.|.-~-.           .~         `.
 (( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \
 (( /// ))      `.   {            }                   /      \  \
  (( / ))     .----~-.\        \-'                 .~         \  `. \^-.
             ///.----..>        \             _ -~             `.  ^-`  ^-_
               ///-._ _ _ _ _ _ _}^ - - - - ~                     ~-- ,.-~
                                                                  /.-~

EOF

echo """ 

Starting Build ... And Push

"""
set -e
echo "using docker Repo --- $1 " | docker login $1
docker rmi -f $1:$2 || true
docker build -t scanner:$2 app
docker tag scanner:$2 $1:$2
docker push $1:$2
docker rmi -f $1:$2 || true
docker rmi -f scanner:$2 || true
cat << 'EOF'


 _______________________________________ 
/                                       \
|                                       |
| I am just a nobody until you meet me. |
|                                       |
| --- Ankshuk The Boss                  |
|                                       |
| BTW I created the docker Image for    |
\ you!!!                                /
 --------------------------------------- 
\                             .       .
 \                           / `.   .' " 
  \                  .---.  <    > <    >  .---.
   \                 |    \  \ - ~ ~ - /  /    |
         _____          ..-~             ~-..-~
        |     |   \~~~\.'                    `./~~~/
       ---------   \__/                        \__/
      .'  O    \     /               /       \  " 
     (_____,    `._.'               |         }  \/~~~/
      `----.          /       }     |        /    \__/
            `-.      |       /      |       /      `. ,~~|
                ~-.__|      /_ - ~ ^|      /- _      `..-'   
                     |     /        |     /     ~-.     `-. _  _  _
                     |_____|        |_____|         ~ - . _ _ _ _ _>




EOF



gcloud run deploy scanner \
--image=$1:$2 \
--allow-unauthenticated \
--cpu=8 \
--memory=32Gi \
--timeout=1200 \
--min-instances=1 \
--max-instances=6 \
--execution-environment=gen2 \

cat << 'EOF'


MMMMMMMMMMMMMMMMMMMMMMMMMMMMWNXK0OxxxdddddxxxkO0KNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMWNKOkxoolc:::;;;;;;;;:::clodxk0XNMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMWXKOxdooc;'.......          .....',;codk0XWMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMN0xllodl;'. ...                       ..':llokKNMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMWKkoloxxl,.   ..    .                        .;clldOXMMMMMMMMMMMMMM
MMMMMMMMMMMWKxlldxd:..     .                                .,lllokXWMMMMMMMMMMM
MMMMMMMMMN0dloxxl,..       ......                             .,;:llxKWMMMMMMMMM
MMMMMMMNOoloxOkd'        ...   ..                                .cdlldKWMMMMMMM
MMMMMMNxloxkOOo'..       ...   .      ..         ... ...         .,ccollkWMMMMMM
MMMMMXxlokOOOx'...       ... ........................',,'...       ..:ollkNMMMMM
MMMW0olxOOOOOl....            ....'''''''''',,;;;;;::ccllc:,...     .;oxoldXWMMM
MMWOllxOOOOOk;. ...............,,;cccllllcc::::ccccccllllllcc;,.   ..cxxxoldKWMM
MM0lldOOOOOOo..  ... .......'.;:;ccloodooooooolllllllloollllll:,.   .:xxxxoloXMM
MXdldOOOOOOOc.     .......:lccc;,,;::::ccclodddddddddddddooolll:..  .:xkkxxolxWM
NdlokOOOOOOk,.      ..,:clddlcccc::;,'''',;:lodxxxxddoc:;;;;;;;:;.  'oxkkkxdllOW
0llxOOOOOOOx,.     ..;oxxxdoodxxddooolcccclloodxxxdoc;'....',,,',. .ckkkkxxxollK
xldOOOOOOOOk,..   ...cdxxddxxdollc::;:;;;:lodxxxxddl:;,,,;::cloc,. .okkkkxxxdllO
dldOOOOOOOOk;.  . ..'lddddddol:;;;'..,c:',:lodxxxdoc;'..',;;;;:cc. 'dkkkkkxxxolx
llxOOOOOOOOOl. .....,ldddddolc:::cc:;;c:;,:clloddol:,'....;;'',:c'.cxkkkkkxxxold
llxOOOOOOOOko,......:odddddooolllllcccccccllooodddol:;,,,;:::;;:c,'xkkkkkkxxxold
llxOOOOOOOOdloc;'..,lddxdxddddddddooooooddddddddxddocccc:::ccccll::xkkkkkxxxxold
olxOOOOOOOkdoxdlc;.:oddxxxxxxkkkkxxxddddxxdddddxxxxdlloooooooooolclkkkkkkxxxxolx
dldOOOOOOOkodxocod:codxxxkkkkOOkkkxxdddddddddxxkkxxxolodddddxxddoodkkkkkkxxxxolk
klokOOOOOOOxddclddllddxxxkkkkOOkkxxdoddxxxkxxxkOkkkxdoooooddxxxdooxkkkkkkxxxdll0
KlldOOOOOOOkxdooooddddxxxxkkkkkkxdooodxxxxdolldkkxxocloooooddddoodkkkkkkkxxxoldX
WkllxOOOOOOOkxxxxxxdddxkkkkkkkkxooodxxxxddddoooooollllooooooooolodkkkkkkkxxoloKW
MWxlokOOOOOOOkdcodolodxkkkkkxxxdodxxxxxxdddoooollllllllooolllllloxkkkkkkkxdllOWM
MMXdlokOOOOOOkc.':llodxxkkkkxxxdoollclodxxddodooolllcccllllllllldkkkkkkkxdllkNMM
MMMXdloOOOOOOk:.'clooddxkkkkkxxxoll;,:dxOO0OO0kkkxxdo;.':lllllldxkkkkkkkxllkWMMM
MMMMXxlokOOOOOo,,looooddxkkkkkxxxdxddoooddxxkkxkkxxdo:;clooolloxkkkkkkxdloONMMMM
MMMMMW0oldkOOko,;loooooddxxkkkxxxxxxxxxxxxxxdddddddollooooolloxkkkkkkxoloKMMMMMM
MMMMMMW0olodo:;,:ooddooooddxxkxxxxxxxxxkkxxdddooodddooooollldxkkkkkxdllxXWWMMMMM
MMMMMMMMNkocc:;;cooddddooooddxxxxxxxxxxxxxxxddddddddoooollldkkkkkkdolo0WMMMMMMMM
MMMMMMMMMWNOdlccclddddddddooooddxxxxxxxxxxxxxxxdddddoollloxkkkkxdoox0NMMMMMMMMMM
MMMMMMMMMMMMWKdlllodddxddddoooooddxxxkkkkkxxxxxxddddolloxkkkxdollkXMMMMMMMMMMMMM
MMMMMMMMMMMMMMWKkdlloddxxdddddddoodddxxxxxxdddddooollldkkxdolodOXWMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMWKkdllooddddoddddoooooooollllllcloodddoollxOXWMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWX0Okdolllooooooooollcccc:ccclooooxkOKNWMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMWNXKOkxxdoolllllllloodxkO0KXWMWMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMWMMMMMMMWNXK00OOOO00KNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM



 __        __             _  _   _                        _      _            
 \ \      / /___    __ _ | || | | |     ___ __   __ ___  | |__  (_) _ __ ___  
  \ \ /\ / // _ \  / _` || || | | |    / _ \\ \ / // _ \ | '_ \ | || '_ ` _ \ 
   \ V  V /|  __/ | (_| || || | | |___| (_) |\ V /|  __/ | | | || || | | | | |
    \_/\_/  \___|  \__,_||_||_| |_____|\___/  \_/  \___| |_| |_||_||_| |_| |_|
                                                                              
            _                                           _           
           | |__    ___   ___  __ _  _   _  ___   ___  | |__    ___ 
           | '_ \  / _ \ / __|/ _` || | | |/ __| / _ \ | '_ \  / _ \
           | |_) ||  __/| (__| (_| || |_| |\__ \|  __/ | | | ||  __/
           |_.__/  \___| \___|\__,_| \__,_||___/ \___| |_| |_| \___|
                                                                    
             _                                              _  _    
            | |  ___ __   __ ___  ___   _   _  ___    __ _ | || |   
            | | / _ \\ \ / // _ \/ __| | | | |/ __|  / _` || || |   
            | || (_) |\ V /|  __/\__ \ | |_| |\__ \ | (_| || || | _ 
            |_| \___/  \_/  \___||___/  \__,_||___/  \__,_||_||_|(_)



EOF

