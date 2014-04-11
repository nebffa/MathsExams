import sys
import subprocess
import os


script_path = sys.argv[1]
project_path = sys.argv[2]

script = os.path.relpath(script_path, project_path).replace('/', '.')

python_path = os.path.join(project_path, 'bin', 'python')

os.chdir(project_path)
subprocess.call([python_path, "-m", script])
