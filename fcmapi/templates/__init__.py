from pkgutil import get_data

#html templates
index_template = str(get_data("fcmapi","templates/index.html"), 'utf-8')
maplogin_template = str(get_data("fcmapi","templates/maplogin.html"), 'utf-8')
session_template = str(get_data("fcmapi","templates/session.html"), 'utf-8')
missing_template = str(get_data("fcmapi","templates/missing.html"), 'utf-8')
webcli_template = str(get_data("fcmapi","templates/webcli.html"), 'utf-8')
webgui_template = str(get_data("fcmapi","templates/webgui.html"), 'utf-8')
d3v4_template = str(get_data("fcmapi","templates/d3.v4.min.js"), 'utf-8')