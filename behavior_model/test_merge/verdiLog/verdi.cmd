debImport "+v2k" "-sverilog" "+incdir+../srcs+./" "-f" "filelist.f"
debLoadSimResult /mnt/c/git/nvcim-comm/behavior_model/test_merge/wave.fsdb
wvCreateWindow
wvRestoreSignal -win $_nWave2 "./wcfg/cfg1.rc" -overWriteAutoAlias on
verdiDockWidgetDisplay -dock widgetDock_WelcomePage
