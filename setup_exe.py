from cx_Freeze import setup, Executable

executables = [
    Executable('client.py')
]

setup(name='client',
      version='0.1',
      description='client',
      executables=executables
      )
