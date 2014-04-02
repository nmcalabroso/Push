from cx_Freeze import setup, Executable

includefiles = ['avbin.dll','assets/']
includes = []
excludes = ['Tkinter']
packages = []

exe = Executable(script = "client_push.py",
				base = "Win32Gui",
				copyDependentFiles = True,
				icon = "favicon.ico",
				targetName = "push.exe")

setup(name = "Push",
	version = "0.1" ,
	description = "CS145 MP: Push",
	author = "Bunao;Calabroso;Mendoza",
	options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
	executables = [exe])