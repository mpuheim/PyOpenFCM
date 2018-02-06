from pkgutil import get_data

#html templates
index_template = str(get_data("fcmapi","templates/index.html"), 'utf-8')
cs_index_template = str(get_data("fcmapi","templates/cs_index.html"), 'utf-8')
cs_maplogin_template = str(get_data("fcmapi","templates/cs_maplogin.html"), 'utf-8')
cs_session_template = str(get_data("fcmapi","templates/cs_session.html"), 'utf-8')
cs_missing_template = str(get_data("fcmapi","templates/cs_missing.html"), 'utf-8')
ss_index_template = str(get_data("fcmapi","templates/ss_index.html"), 'utf-8')
ss_maplogin_template = str(get_data("fcmapi","templates/ss_maplogin.html"), 'utf-8')
ss_session_template = str(get_data("fcmapi","templates/ss_session.html"), 'utf-8')
ss_missing_template = str(get_data("fcmapi","templates/ss_missing.html"), 'utf-8')
webcli_template = str(get_data("fcmapi","templates/webcli.html"), 'utf-8')