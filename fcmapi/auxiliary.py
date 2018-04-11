
#---FCM-API-AUXILIARY-FUNCTIONS-&-CLASSES---#

import sys, os, io, contextlib, tempfile, _thread, time

#execute command (with specified map)
def execute(_map_,cmd,app):
    #disable interactive help
    cmd=cmd.replace("help()","help")
    #run command normally # TODO - run in thread with timeout to avoid freezing in infinite loop
    with stdoutIO() as s:
        #setup secure command context (available global builtins & local variables)
        global loc_vars
        loc_vars  = {"_map_":_map_,"functions":_map_.config.functions,"relations":_map_.config.relations}
        glob_vars = {'__builtins__': {"print":print,"dir":safe_dir,"help":help}}
        #catch and return errors when not debugging
        if not app.debug:
            try:
                try:
                    response=str(eval(cmd,glob_vars,loc_vars))+"\n"
                    if response=="None\n": response=s.getvalue()
                except SyntaxError:
                    exec(cmd,glob_vars,loc_vars)
                    response=s.getvalue()
                if response=="":
                    response=str(_map_)+"\n"
            except BaseException as error:
                print("Error:", error)
                response=s.getvalue()
        #do not catch errors when debugging since Flask will show full error traceback
        else:
            try:
                response=str(eval(cmd,glob_vars,loc_vars))+"\n"
                if response=="None\n": response=s.getvalue()
            except SyntaxError:
                exec(cmd,glob_vars,loc_vars)
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
    
#safe directory listing (without underscores)
loc_vars=[] # TODO - move to separate worker object
def safe_dir(d=None):
    if d:
        listing = [o for o in dir(d) if "_" not in o]
        if listing == []:
            print("[] - Empty listing. Printing help() instead:\n")
            return help(d)
        return listing
    else:
        return [o for o in loc_vars]

#link generator
def href_for(s):
    return "<a href='"+s+"'>"+s+"</a>"

#save handler class
class SaveHandler:

    interval = None
    directory = None
    files = None
    working = False
    
    def __init__(self, interval=10, directory="fcmservice"):
        self.interval = interval
        self.directory = os.path.join(tempfile.gettempdir(),directory)
        self.files = {}
        try: os.mkdir(self.directory)
        except: pass
        _thread.start_new_thread(self.__worker__,())
        
    def save(self, name, data):
        self.files[name]=data
        
    def delete(self, name):
        filepath = os.path.join(self.directory,name)
        while self.working:
            print("Warning. Waiting to remove file "+filepath)
        os.remove(filepath)
        if name in self.files:
            self.files.pop(name)
            
    def load(self):
        for file in os.listdir(self.directory):
            filepath = os.path.join(self.directory,file)
            try:
                f = open(filepath,"r",encoding="utf8")
                self.files[file]=f.read()
                f.close()
            except:
                print("Warning. Cannot open file "+filepath)
        return self.files
        
    def __worker__(self):
        while True:
            time.sleep(self.interval)
            self.working = True
            for name, data in self.files.items():
                filepath = os.path.join(self.directory,name)
                try:
                    f = open(filepath,"w",encoding="utf8")
                    f.write(data)
                    f.close()
                except:
                    print("Warning. Cannot create file "+filepath)
            self.working = False
            self.files.clear()
        