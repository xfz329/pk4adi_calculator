pyinstaller.exe  -i D:\UrgeData\Documents\Codes\Github\pk_gui\figures\pk.ico -Dw main.py -n PK4ADI
pyinstaller.exe  -i D:\UrgeData\Documents\Codes\Github\pk_gui\resource\images\logo.ico -Dw pk4adi_demo.py -n PK4ADI
cp -r D:\UrgeData\Documents\Codes\Github\pk_gui\resource\ D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI\resource
cp -r D:\UrgeData\Documents\Codes\Github\pk_gui\nsis\logs D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI
cp -r D:\UrgeData\Documents\Codes\Github\pk_gui\license D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI