
#---FCM-API-AUXILIARY-FUNCTIONS-&-CLASSES---#

import sys, os, io, contextlib, tempfile, _thread, time

#execute command (with specified map)
def execute(_map_,cmd,app):
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
    return "<a href='"+s+"'>"+s+"</a>"

#save handler class
class SaveHandler:

    interval = None
    directory = None
    files = None
    working = False
    
    def __init__(self, interval=1, directory="fcmservice"):
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
        