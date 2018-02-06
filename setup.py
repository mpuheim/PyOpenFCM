from setuptools import setup

setup(name='fcmlib',
      version='0.2.20',
      description='Open Fuzzy Cognitive Maps Library',
      url='https://github.com/mpuheim/PyOpenFCM',
      author='M.Puheim',
      author_email='puheim@gmail.com',
      license='GPL 3.0',
      package_dir={
            'fcmlib': 'fcmlib',
            'fcmlib.relations': 'fcmlib/relations',
            'fcmlib.functions': 'fcmlib/functions',
            'fcmapi': 'fcmapi',
            'fcmapi.templates': 'fcmapi/templates'},
      packages=[
            'fcmlib',
            'fcmlib.relations',
            'fcmlib.functions',
            'fcmapi',
            'fcmapi.templates'],
      scripts=['fcmapi/fcmapi_app.py','fcmapi/fcmapi_debug.bat','fcmapi/fcmapi_service.bat'],
      install_requires=['flask'],
      dependency_links=['https://github.com/jsonpickle/jsonpickle.git'],
      include_package_data=True,
      zip_safe=False)