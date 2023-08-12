pyinstaller.exe  -i D:\UrgeData\Documents\Codes\Github\pk_gui\resource\images\logo.ico -Dw pk4adi_demo.py -n PK4ADI --noconfirm
cp -r D:\UrgeData\Documents\Codes\Github\pk_gui\resource\ D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI\resource
cp -r D:\UrgeData\Documents\Codes\Github\pk_gui\nsis\logs D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI
md D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI\license
cp D:\UrgeData\Documents\Codes\Github\pk_gui\LICENSE D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI\license\LICENSE