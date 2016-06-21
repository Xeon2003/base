#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, datetime, binascii

cwd = os.getcwd()
dirs = []
files = {}

for dirname, dirnames, filenames in os.walk("."):
	if dirname == ".":
		for ignore in [".idea", ".git", "server"]:
			if ignore in dirnames:
				dirnames.remove(ignore)

		for ignore in ["README.md", "mksetup.py", ".gitignore", ".gitmodules"]:
			if ignore in filenames:
				filenames.remove(ignore)

		dirname = ""
	elif dirname.startswith("./"):
		dirname = dirname[2:]

	for dir in dirnames:
		dirs.append(((dirname + "/") if dirname else "") + dir)

	for file in filenames:
		filename = ((dirname + "/") if dirname else "") + file
		if filename == "viur_server.py":
			tfilename = "{{app_id}}.py"
		elif filename == "start.bat":
			tfilename = "{{app_id}}.bat"
		else:
			tfilename = filename

		f = open(filename, "rb")
		files[tfilename] = binascii.hexlify(f.read())
		f.close()

out = ""
out += "#!/usr/bin/env python\n"
out += "# -*- coding: utf-8 -*-\n"
out += "# THIS FILE WAS GENERATED WITH %s ON %s\n" % (__file__, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
out += "# DO NOT EDIT THIS FILE PERMANENTLY - IT WILL GO AWAY!\n\n"

out += "import os, sys, binascii, datetime\n\n"

out += "dirs = %s\n" % dirs
out += "files = %s\n\n" % files

out += """

print('''
                iii
               iii
              iii

          vvv iii uu      uu rrrrrrrr
         vvvv iii uu      uu rr     rr
  v     vvvv  iii uu      uu rr     rr
 vvv   vvvv   iii uu      uu rr rrrrr
vvvvv vvvv    iii uu      uu rr rrr
 vvvvvvvv     iii uu      uu rr  rrr
  vvvvvv      iii  uu    uu  rr   rrr
   vvvv       iii   uuuuuu   rr    rrr

  I N F O R M A T I O N    S Y S T E M

Welcome to the raw setup utility!
''')

def prompt(quest = None):
	if quest:
		sys.stdout.write(quest)

	try:
		return raw_input()
	except NameError:
		return input()

def confirm(quest):
	answ = prompt(quest)
	return answ.lower() in ["y","yes"]

cwd = os.getcwd()
prgc = sys.argv[0]

if prgc.startswith("/") or prgc[1] == ":":
    path = os.path.dirname(prgc)
else:
    path = os.path.abspath(os.path.dirname(os.path.join(cwd, prgc)))

path = os.path.abspath( os.path.join( path , ".." ) )
os.chdir(path)
appid = path[path.rfind(os.path.sep) + 1:].strip()

nappid = prompt("Please enter your desired application name [default=%s]" % appid)
if nappid:
	appid = nappid

if not confirm("This will setup the application '%s' in '%s' - continue [y/N]?" % (appid, path)):
	print("Setup aborted.")
	sys.exit(0)

for folder in dirs:
	folder = os.path.join(path, *folder.split("/"))
	if not os.path.exists(folder):
		print("Creating %s..." % folder)
		os.mkdir(folder)

# Replacement variables
vars = {
	"app_id": appid,
	"path": path,
	"timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
}

try:
	import getpass
	vars["whoami"] = getpass.getuser()
except:
	vars["whoami"] = "Bernd"

# Extract files.
for name, content in files.items():
	if content:
		content = binascii.unhexlify(content)

	if isinstance(content, str):
		for k, v in vars.items():
			name = name.replace("{{%s}}" % k, v)
			content = content.replace("{{%s}}" % k, v)

	name = os.path.join(*name.split("/"))

	if os.path.exists(name):
		if not confirm("The file %s already exists - Override [y/N]?" % name):
			print("Skipping %s!" % name)
			continue

	sys.stdout.write("Writing %s..." % name)
	open(name, "w+").write(content)
	print("Done")
"""

print(out)
