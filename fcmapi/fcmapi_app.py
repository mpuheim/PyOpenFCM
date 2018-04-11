import datetime
from fcmlib import FCM
from fcmapi.templates import *
from fcmapi.auxiliary import *
from flask import Flask, make_response, redirect, abort, url_for, request

#create service application
app = Flask(__name__)

#initialize service maps
_maps_  = {}
_saver_ = SaveHandler()
for file, data in _saver_.load().items():
    map=FCM(data)
    _maps_[map.name]=map

#-SERVER-SIDE-API-----------------------------------------------#
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #work with existing FCM
        if 'name' in request.form:
            mapname = request.form['name']
            if mapname in _maps_:
                return redirect(url_for('index')+mapname)
            return missing_template.replace("{R}",mapname)
        #create new FCM
        if 'logname' in request.form:
            mapname = request.form['logname']
            return redirect(url_for('index')+mapname+"/login/")
        #delete existing FCM
        if 'remname' in request.form:
            mapname = request.form['remname']
            return redirect(url_for('index')+mapname+"/logout/")
        #get FCM as JSON
        if 'getname' in request.form:
            mapname = request.form['getname']
            return redirect(url_for('index')+mapname+"/serialize/")
        #command line interface
        if 'cliname' in request.form:
            mapname = request.form['cliname']
            return redirect(url_for('index')+mapname+"/cli/")
        #graphical user interface
        if 'guiname' in request.form:
            mapname = request.form['guiname']
            return redirect(url_for('index')+mapname+"/gui/")
    return index_template

@app.route('/<mapname>/login/', methods=['GET', 'POST'])
def login(mapname):
    if (mapname not in _maps_) or (request.method == 'POST'):
        _maps_[mapname]=FCM()
        _maps_[mapname].name=mapname
        _saver_.save(mapname+".json",_maps_[mapname].serialize(2))
        return redirect(url_for('index')+mapname)
    return maplogin_template.replace("{R}",mapname)
        
@app.route('/<mapname>/logout/')
def logout(mapname):
    # remove the map from the list if it's there
    if mapname in _maps_:
        _maps_.pop(mapname)
        _saver_.delete(mapname+".json")
    return redirect(url_for('index'))
    
@app.route('/<mapname>/')
def session(mapname):
    if mapname in _maps_:
        return session_template.replace("{R}",mapname)
    return missing_template.replace("{R}",mapname)
    
@app.route('/<mapname>/run/', methods=['POST'])
def runpost(mapname):
    if request.method == 'POST' and 'command' in request.form:
        command=request.form['command']
        return run(mapname,command)
    return abort(404)
    
@app.route('/<mapname>/run/<command>', methods=['GET'])
def run(mapname,command):
    if mapname not in _maps_:
        return abort(404)
    #secure command (no underlines)
    cmd=command.replace("_","")
    #fix dictionary in JSON object (if any)
    cmd=cmd.replace('"dict":','"__dict__":')
    #get FCM object
    _map_=_maps_[mapname]
    #use FCM object in command
    cmd=cmd.replace(mapname,"_map_")
    #execute secured command
    response=execute(_map_,cmd,app)
    response=response.replace("_map_",mapname)
    #fix map name (if changed to _map_)
    if _map_.name=="_map_":
        _map_.name=mapname
    #rename on server (if renamed)
    if _map_.name != mapname:
        _maps_[_map_.name]=_maps_.pop(mapname)
        _saver_.delete(mapname+".json")
    #save map on server
    _saver_.save(_map_.name+".json",_map_.serialize(2))
    #return response
    return response
    
@app.route('/<mapname>/execute/<command>')
def process(mapname,command):
    if mapname in _maps_:
        #processing start time
        st=datetime.datetime.now()
        #secure command (no underlines)
        cmd=command.replace("_","")
        #fix dictionary in JSON object (if any)
        cmd=cmd.replace('"dict":','"__dict__":')
        #get FCM object
        _map_=_maps_[mapname]
        #use FCM object in command
        cmd=cmd.replace(mapname,"_map_")
        #execute secured command
        response=execute(_map_,cmd,app)
        response=response.replace("_map_",mapname)
        #fix map name (if changed to _map_)
        if _map_.name=="_map_":
            _map_.name=mapname
        #rename on server (if renamed)
        if _map_.name != mapname:
            _maps_[_map_.name]=_maps_.pop(mapname)
            _saver_.delete(mapname+".json")
        #save map on server
        _saver_.save(_map_.name+".json",_map_.serialize(2))
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
    return missing_template.replace("{R}",mapname)
    
@app.route('/<mapname>/cli/', methods=['GET', 'POST'])
def webcli(mapname):
    if mapname not in _maps_:
        return missing_template.replace("{R}",mapname)
    if request.method == 'POST' and 'command' in request.form:
        command=request.form['command']
        return webcli_template.replace("{R1}",href_for(url_for('index')+mapname)+"/cli/").replace("{R2}",process(mapname,command))
    return webcli_template.replace("{R1}",href_for(url_for('index')+mapname)+"/cli/").replace("{R2}","")
    
@app.route('/<mapname>/gui/')
def webgui(mapname):
    if mapname not in _maps_:
        return missing_template.replace("{R}",mapname)
    ret=webgui_template
    ret=ret.replace("{R1}",url_for('index')+mapname+"/cli/")
    ret=ret.replace("{R2}",url_for('index')+mapname+"/serialize/")
    ret=ret.replace("{R3}",_maps_[mapname].serialize(indent=0))
    return ret;
    
@app.route('/<mapname>/gui/d3.v4.min.js')
def serve_d3v4_js(mapname):
    return d3v4_template;
    
@app.route('/<mapname>/serialize/')
def serialize(mapname):
    if mapname in _maps_:
        return _maps_[mapname].serialize()
    return missing_template.replace("{R}",mapname)
    
@app.route('/list/')
def list():
    ret=""
    for m in _maps_:
        lnk=url_for('index')+m
        ret+="<a href='"+lnk+"'>"+lnk+"</a><br/>"
    if ret=="": return "None"
    return ret

#--------------------------------------------------------------#

# entry point for the application
if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
