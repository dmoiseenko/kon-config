import subprocess


def execute_bash_script(instructions_array):
    script = "\n".join(instructions_array)
    subprocess.run(script, shell=True, check=True)
