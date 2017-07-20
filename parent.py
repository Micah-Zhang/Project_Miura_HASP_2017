import subprocess as sp

p = sp.Popen(["./child.py", "arg1", "arg2"], stdout=sp.PIPE, stderr=sp.PIPE)
out, err = p.communicate()
result = p.returncode
