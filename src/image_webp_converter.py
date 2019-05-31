


import os

def search_import_file(a):
    liste, liste2= [], []
    for i in os.listdir(os.path.curdir):
        liste.append(i)
    for file in liste: 
        curdir = os.path.abspath(os.path.curdir)
        path_to_file = os.path.join(curdir,file)
        liste2.append(path_to_file)
        print("found",path_to_file)
    return liste2

os.chdir('/home/hugo/Development/la_petite_portugaise/static/images/icons')
liste = search_import_file('DS')
os.system("sudo apt install webp -Y")

for i in liste:
    if os.path.isfile(i):
        fname = (os.path.basename(i))
        base = (os.getcwd())
        nfname = (os.path.splitext(i)[0])
        os.system("cwebp -q 60 {} -o {}".format(i, os.path.join(base,nfname+".webp")))