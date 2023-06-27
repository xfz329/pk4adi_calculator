; �ýű�ʹ�� HM VNISEdit �ű��༭���򵼲���

; ��װ�����ʼ���峣��
!define PRODUCT_NAME "PK4ADI������"
!define PRODUCT_VERSION "0.1.3.c"
!define PRODUCT_PUBLISHER "�㽭��ѧ����ѧԺ"
!define PRODUCT_WEB_SITE "http://www.cbeis.zju.edu.cn/main.htm"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; ------ MUI �ִ����涨�� (1.67 �汾���ϼ���) ------
!include "MUI.nsh"

; MUI Ԥ���峣��
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; ��ӭҳ��
!insertmacro MUI_PAGE_WELCOME
; ���Э��ҳ��
!insertmacro MUI_PAGE_LICENSE "D:\UrgeData\Documents\Codes\Github\pk_gui\license\license.txt"
; ��װĿ¼ѡ��ҳ��
!insertmacro MUI_PAGE_DIRECTORY
; ��װ����ҳ��
!insertmacro MUI_PAGE_INSTFILES
; ��װ���ҳ��
!define MUI_FINISHPAGE_RUN "$INSTDIR\PK4ADI.exe"
!insertmacro MUI_PAGE_FINISH

; ��װж�ع���ҳ��
!insertmacro MUI_UNPAGE_INSTFILES

; ��װ�����������������
!insertmacro MUI_LANGUAGE "SimpChinese"

; ��װԤ�ͷ��ļ�
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS
; ------ MUI �ִ����涨����� ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "D:\UrgeData\Documents\Codes\Github\pk_gui\nsis\PK4ADI_0.1.3.c_x64-setup.exe"
InstallDir "$PROGRAMFILES\PK4ADI"
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File /r "D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI\*.*"
  WriteUninstaller "$INSTDIR\uninst.exe"     ;---- ����������ж�س���
  CreateShortCut "$DESKTOP\PK4ADI.lnk" "$INSTDIR\PK4ADI.exe"
SectionEnd

Section -AdditionalIcons
  CreateDirectory "$SMPROGRAMS\PK4ADI"
  CreateShortCut "$SMPROGRAMS\PK4ADI\PK4ADI.lnk" "$INSTDIR\PK4ADI.exe"
  CreateShortCut "$SMPROGRAMS\PK4ADI\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

/******************************
 *  �����ǰ�װ�����ж�ز���  *
 ******************************/

Section Uninstall
  Delete "$INSTDIR\uninst.exe"

  Delete "$SMPROGRAMS\PK4ADI\PK4ADI.lnk"
  Delete "$SMPROGRAMS\PK4ADI\Uninstall.lnk"
  Delete "$DESKTOP\PK4ADI.lnk"

  RMDir "$SMPROGRAMS\PK4ADI"
  RMDir ""

  RMDir /r "$INSTDIR\tk"
  RMDir /r "$INSTDIR\tcl8"
  RMDir /r "$INSTDIR\tcl"
  RMDir /r "$INSTDIR\scipy.libs"
  RMDir /r "$INSTDIR\scipy"
  RMDir /r "$INSTDIR\qtpy"
  RMDir /r "$INSTDIR\qtpandas"
  RMDir /r "$INSTDIR\pytz"
  RMDir /r "$INSTDIR\PyQt5"
  RMDir /r "$INSTDIR\pandas"
  RMDir /r "$INSTDIR\numpy"
  RMDir /r "$INSTDIR\importlib_metadata-6.0.0.dist-info"
  RMDir /r "$INSTDIR\future"
  RMDir /r "$INSTDIR\figures"
  Delete   "$INSTDIR\*.*"
;  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd

#-- ���� NSIS �ű��༭�������� Function ���α�������� Section ����֮���д���Ա��ⰲװ�������δ��Ԥ֪�����⡣--#

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "��ȷʵҪ��ȫ�Ƴ� $(^Name) ���������е������" IDYES +2
  Abort
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) �ѳɹ��ش���ļ�����Ƴ���"
FunctionEnd
