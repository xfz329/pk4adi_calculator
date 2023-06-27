; 该脚本使用 HM VNISEdit 脚本编辑器向导产生

; 安装程序初始定义常量
!define PRODUCT_NAME "PK4ADI计算器"
!define PRODUCT_VERSION "0.1.3.c"
!define PRODUCT_PUBLISHER "浙江大学生仪学院"
!define PRODUCT_WEB_SITE "http://www.cbeis.zju.edu.cn/main.htm"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; ------ MUI 现代界面定义 (1.67 版本以上兼容) ------
!include "MUI.nsh"

; MUI 预定义常量
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; 欢迎页面
!insertmacro MUI_PAGE_WELCOME
; 许可协议页面
!insertmacro MUI_PAGE_LICENSE "D:\UrgeData\Documents\Codes\Github\pk_gui\license\license.txt"
; 安装目录选择页面
!insertmacro MUI_PAGE_DIRECTORY
; 安装过程页面
!insertmacro MUI_PAGE_INSTFILES
; 安装完成页面
!define MUI_FINISHPAGE_RUN "$INSTDIR\PK4ADI.exe"
!insertmacro MUI_PAGE_FINISH

; 安装卸载过程页面
!insertmacro MUI_UNPAGE_INSTFILES

; 安装界面包含的语言设置
!insertmacro MUI_LANGUAGE "SimpChinese"

; 安装预释放文件
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS
; ------ MUI 现代界面定义结束 ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "D:\UrgeData\Documents\Codes\Github\pk_gui\nsis\PK4ADI_0.1.3.c_x64-setup.exe"
InstallDir "$PROGRAMFILES\PK4ADI"
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File /r "D:\UrgeData\Documents\Codes\Github\pk_gui\dist\PK4ADI\*.*"
  WriteUninstaller "$INSTDIR\uninst.exe"     ;---- 这里是生成卸载程序
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
 *  以下是安装程序的卸载部分  *
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

#-- 根据 NSIS 脚本编辑规则，所有 Function 区段必须放置在 Section 区段之后编写，以避免安装程序出现未可预知的问题。--#

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "你确实要完全移除 $(^Name) ，及其所有的组件？" IDYES +2
  Abort
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) 已成功地从你的计算机移除。"
FunctionEnd
