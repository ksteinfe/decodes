:: here we set a variable to the current decodes release number
set dc=decodes-0.0.1
python setup.py sdist
python setup.py bdist_msi

echo the name is "%dc%"

:: requires 7-zip http://www.7-zip.org/download.html (get command line version and put .exe file in C:\Windows directory)
7za x dist/%dc%.zip -odist -y


:choice
::set /P c=Install to Python Directory[Y/N]?
::if /I "%c%" EQU "Y" goto :install_python
::if /I "%c%" EQU "N" goto :all_done
::goto :choice

:install_python
::python dist/%dc%/setup.py install

:all_done
::echo all done!
