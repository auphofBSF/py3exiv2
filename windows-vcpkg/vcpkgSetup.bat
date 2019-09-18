set VCPKG=d:\vcpkg
set CUSTOM_VCPKG_PORTS_PATH=%cd%\vcpkg-custom
echo "---------------------------"
echo "CUSTOM_VCPKG_PORT_PATH: %CUSTOM_VCPKG_PORTS_PATH%"
echo
echo "----------------------------------------"
REM git clone https://github.com/Microsoft/vcpkg.git %VCPKG%
cd /D %VCPKG%
REM call .\bootstrap-vcpkg.bat

vcpkg install python3:x64-windows  --overlay-ports=%CUSTOM_VCPKG_PORTS_PATH%\ports\python3

vcpkg install boost-python:x64-windows
vcpkg install exiv2:x64-windows

cd /D  %CUSTOM_VCPKG_PORTS_PATH%  
cd ..


