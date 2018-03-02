import datetime, sys, io, contextlib
from fcmlib import FCM
from fcmapi.templates import *
from flask import Flask, session, redirect, url_for, request

#create service application
app = Flask(__name__)

#app secret key - keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #TODO - use generator or file

#service index
@app.route("/")
def index():
    return index_template

#-CLIENT-SIDE-API-----------------------------------------------#
    
@app.route('/cs/')
def cs_index():
    if 'client_name' in session:
        return cs_index_template.replace("{R}",session['client_name'])
    return redirect(url_for('cs_login'))

@app.route('/cs_login/', methods=['GET', 'POST'])
def cs_login():
    if request.method == 'POST':
        map=FCM()
        map.name=request.form['mapname']
        session['client_map'] = map.serialize()
        session['client_name'] = map.name
        return redirect(url_for('cs_index')+session['client_name'])
    return cs_maplogin_template

@app.route('/cs_logout/')
def cs_logout():
    # remove the map from the session if it's there
    session.pop('client_map', None)
    session.pop('client_name', None)
    return redirect(url_for('cs_index'))

@app.route('/cs/<mapname>/')
def cs_session(mapname):
    if 'client_name' in session and session['client_name']==mapname:
        return cs_session_template.replace("{R}",session['client_name'])
    if 'client_name' not in session:
        return redirect(url_for('cs_login'))
    return cs_missing_template.replace("{R1}",mapname).replace("{R2}",session['client_name'])

@app.route('/cs/<mapname>/execute/<command>')
def cs_process(mapname,command):
    if 'client_name' in session and session['client_name']==mapname:
        #processing start time
        st=datetime.datetime.now()
        #secure command (no underlines)
        cmd=command.replace("_","")
        #fix dictionary in JSON object (if any)
        cmd=cmd.replace('"dict":','"__dict__":')
        #create FCM object
        _map_=FCM(session['client_map'])
        #use FCM object in command
        cmd=cmd.replace(session['client_name'],"_map_")
        #execute secured command
        response=execute(_map_,cmd)
        response=response.replace("_map_",session['client_name'])
        #update client FCM cookie
        session['client_map']=_map_.serialize()
        #processing end time
        et=datetime.datetime.now()
        #processing duration (ms)
        dt=(et-st).total_seconds()*1000
        #generate response
        ret=">>> "+command+"\n"
        ret+="-------------------------------------\n"
        ret+=response
        ret+="-------------------------------------\n"
        ret+="Processed in "+str(dt)+"ms."
        ret="<pre style='white-space:pre-wrap;'>"+ret+"</pre>"
        return ret
    if 'client_name' not in session:
        return redirect(url_for('cs_login'))
    return cs_missing_template.replace("{R1}",mapname).replace("{R2}",session['client_name'])
    
@app.route('/cs/<mapname>/cli/', methods=['GET', 'POST'])
def cs_webcli(mapname):
    if 'client_name' in session and session['client_name']==mapname:
        if request.method == 'POST' and 'command' in request.form:
            command=request.form['command']
            return webcli_template.replace("{R1}",href_for('cs_index')+mapname+"/cli/").replace("{R2}",cs_process(mapname,command))
        return webcli_template.replace("{R1}",href_for('cs_index')+mapname+"/cli/").replace("{R2}","")
    if 'client_name' not in session:
        return redirect(url_for('cs_login'))
    return cs_missing_template.replace("{R1}",mapname).replace("{R2}",session['client_name'])

@app.route('/cs/<mapname>/gui/')
def cs_webgui(mapname):
    if 'client_name' in session and session['client_name']==mapname:
        return webgui_template.replace("{R1}",url_for('cs_index')+mapname+"/cli/").replace("{R2}",FCM(session['client_map']).serialize(indent=0));
    if 'client_name' not in session:
        return redirect(url_for('cs_login'))
    return cs_missing_template.replace("{R1}",mapname).replace("{R2}",session['client_name'])

@app.route('/cs/<mapname>/gui/d3.v3.min.js')
def serve_d3_js(mapname):
    return d3_template;
    
@app.route('/cs/<mapname>/serialize/')
def cs_serialize(mapname):
    if 'client_name' in session and session['client_name']==mapname:
        _map_=FCM(session['client_map'])
        return _map_.serialize()
    if 'client_name' not in session:
        return redirect(url_for('cs_login'))
    return cs_missing_template.replace("{R1}",mapname).replace("{R2}",session['client_name'])

#-SERVER-SIDE-API-----------------------------------------------#

ss_maps={}
    
@app.route('/ss/', methods=['GET', 'POST'])
def ss_index():
    if request.method == 'POST':
        #work with existing FCM
        if 'name' in request.form:
            mapname = request.form['name']
            if mapname in ss_maps:
                return redirect(url_for('ss_index')+mapname)
            return ss_missing_template.replace("{R}",mapname)
        #create new FCM
        if 'logname' in request.form:
            mapname = request.form['logname']
            return redirect(url_for('ss_index')+mapname+"/login/")
        #delete existing FCM
        if 'remname' in request.form:
            mapname = request.form['remname']
            return redirect(url_for('ss_index')+mapname+"/logout/")
        #get FCM as JSON
        if 'getname' in request.form:
            mapname = request.form['getname']
            return redirect(url_for('ss_index')+mapname+"/serialize/")
        #command line interface
        if 'cliname' in request.form:
            mapname = request.form['cliname']
            return redirect(url_for('ss_index')+mapname+"/cli/")
    return ss_index_template

@app.route('/ss/<mapname>/login/', methods=['GET', 'POST'])
def ss_login(mapname):
    if request.method == 'POST':
        ss_maps[mapname]=FCM()
        ss_maps[mapname].name=mapname
        return redirect(url_for('ss_index')+mapname)
    if mapname not in ss_maps:
        ss_maps[mapname]=FCM()
        ss_maps[mapname].name=mapname
        return redirect(url_for('ss_index')+mapname)
    return ss_maplogin_template.replace("{R}",mapname)
        
@app.route('/ss/<mapname>/logout/')
def ss_logout(mapname):
    # remove the map from the list if it's there
    ss_maps.pop(mapname, None)
    return redirect(url_for('ss_index'))
    
@app.route('/ss/<mapname>/')
def ss_session(mapname):
    print("session")
    if mapname in ss_maps:
        return ss_session_template.replace("{R}",mapname)
    return ss_missing_template.replace("{R}",mapname)
    
@app.route('/ss/<mapname>/execute/<command>')
def ss_process(mapname,command):
    if mapname in ss_maps:
        #processing start time
        st=datetime.datetime.now()
        #secure command (no underlines)
        cmd=command.replace("_","")
        #fix dictionary in JSON object (if any)
        cmd=cmd.replace('"dict":','"__dict__":')
        #get FCM object
        _map_=ss_maps[mapname]
        #use FCM object in command
        cmd=cmd.replace(mapname,"_map_")
        #execute secured command
        response=execute(_map_,cmd)
        response=response.replace("_map_",mapname)
        #processing end time
        et=datetime.datetime.now()
        #processing duration (ms)
        dt=(et-st).total_seconds()*1000
        #generate response
        ret=">>> "+command+"\n"
        ret+="-------------------------------------\n"
        ret+=response
        ret+="-------------------------------------\n"
        ret+="Processed in "+str(dt)+"ms."
        ret="<pre style='white-space:pre-wrap;'>"+ret+"</pre>"
        return ret
    return ss_missing_template.replace("{R}",mapname)
    
@app.route('/ss/<mapname>/cli/', methods=['GET', 'POST'])
def ss_webcli(mapname):
    if mapname not in ss_maps:
        return ss_missing_template.replace("{R}",mapname)
    if request.method == 'POST' and 'command' in request.form:
        command=request.form['command']
        return webcli_template.replace("{R1}",href_for('ss_index')+mapname+"/cli/").replace("{R2}",ss_process(mapname,command))
    return webcli_template.replace("{R1}",href_for('ss_index')+mapname+"/cli/").replace("{R2}","")
    
@app.route('/ss/<mapname>/serialize/')
def ss_serialize(mapname):
    if mapname in ss_maps:
        return ss_maps[mapname].serialize()
    return ss_missing_template.replace("{R}",mapname)
    
@app.route('/ss_list/')
def ss_list():
    ret=""
    for m in ss_maps:
        lnk=url_for('ss_index')+m
        ret+="<a href='"+lnk+"'>"+lnk+"</a><br/>"
    if ret=="": return "None"
    return ret

#-AUXILIARY----------------------------------------------------#

#execute command (with specified map)
def execute(_map_,cmd):
    #disable interactive help
    cmd=cmd.replace("help()","help")
    #run command normally
    with stdoutIO() as s:
        #catch and return errors when not debugging
        if not app.debug:
            try:
                try:
                    response=str(eval(cmd,{'__builtins__': {"print":print,"dir":dir,"help":help}},{"_map_":_map_}))+"\n"
                    if response=="None\n": response=s.getvalue()
                except SyntaxError:
                    exec(cmd,{'__builtins__': {"print":print,"dir":dir,"help":help}},{"_map_":_map_})
                    response=s.getvalue()
                if response=="":
                    response=str(_map_)+"\n"
            except BaseException as error:
                print("Error:", error)
                response=s.getvalue()
        #do not catch errors when debugging since Flask will show full error traceback
        else:
            try:
                response=str(eval(cmd,{'__builtins__': {"print":print,"dir":dir,"help":help}},{"_map_":_map_}))+"\n"
                if response=="None\n": response=s.getvalue()
            except SyntaxError:
                exec(cmd,{'__builtins__': {"print":print,"dir":dir,"help":help}},{"_map_":_map_})
                response=s.getvalue()
            if response=="":
                response=str(_map_)+"\n"
    return response
    
#web output context manager
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = io.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
    
#link generator
def href_for(s):
    l=url_for(s)
    return "<a href='"+l+"'>"+l+"</a>"

#--------------------------------------------------------------#

# entry point for the application
if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
