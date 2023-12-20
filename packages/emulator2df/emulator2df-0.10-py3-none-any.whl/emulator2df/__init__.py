import ctypes
import platform
import re
import shutil
import subprocess
import sys
from functools import cache
from time import sleep
import psutil
import pandas as pd

compiledregex = re.compile(r"^[A-Z]:\\", flags=re.I)

iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    user32 = windll.user32
    kernel32 = windll.kernel32
    GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
    CloseHandle = windll.kernel32.CloseHandle
    GetExitCodeProcess.argtypes = [
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_ulong),
    ]
    CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
    GetExitCodeProcess.restype = ctypes.c_int
    CloseHandle.restype = ctypes.c_int

    GetWindowRect = user32.GetWindowRect
    GetClientRect = user32.GetClientRect
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
else:
    invisibledict = {}


@cache
def get_short_path_name(long_name):
    try:
        if not iswindows:
            return long_name
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        return long_name


@staticmethod
def connect_to_all_tcp_devices_windows(adb_path, convert_to_83=True):
    allprocs = []
    if convert_to_83:
        adb_path = get_short_path_name(adb_path)
    netstatexe = shutil.which("netstat.exe")
    p = subprocess.run(
        [netstatexe, "-a", "-b", "-n", "-o", "-p", "TCP"],
        capture_output=True,
        **invisibledict,
    )

    for ip, port in re.findall(
            rb"^\s*TCP\s*((?:127.0.0.1)|(?:0.0.0.0)):(\d+).*LISTENING",
            p.stdout,
            flags=re.M,
    ):
        allprocs.append(
            subprocess.Popen(
                [adb_path, "connect", ip.decode() + ":" + port.decode()]
            )
        )
        sleep(0.1)
    pde = subprocess.run([adb_path, "devices", "-l"], capture_output=True)
    print(pde.stdout.splitlines())
    for pr in allprocs:
        try:
            pr.kill()
        except Exception:
            pass
    ou = [
        y
        for y in [
            q.split(maxsplit=2) for q in pde.stdout.decode("utf-8").splitlines()
        ]
        if len(y) == 3 and "devices attached" not in y
    ]
    return ou


def find_procs_by_name(names):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(['name']):
        if p.info['name'] in names:
            ls.append(p)
    return ls


def all_emulators_as_df(adb=r"adb.exe"
                        , emulator_exe=('Ld9BoxHeadless.exe', 'MEmuHeadless.exe', 'HD-Player.exe', 'NoxVMHandle.exe')):
    r"""
        Provides a function to gather information about all running ANDROID emulators and their connections
        by creating a pandas DataFrame for Windows-specific operations.

        Functionality:
        - Connects to all TCP devices using the provided ADB path and retrieves their IP addresses and port numbers.
        - Identifies processes associated with various emulator executables.
        - Matches the connections between ADB and emulators based on IP addresses and port numbers.
        - Constructs a pandas DataFrame containing details about each identified connection between ADB and emulators.

        Dependencies:
        - pandas
        - psutil

        Parameters:
            adb (str): Path to the ADB executable. Default is set to a standard location for Windows.
            emulator_exe (tuple): Tuple of emulator executable names (e.g., 'Ld9BoxHeadless.exe', 'MEmuHeadless.exe').
                                  Defaults to ('Ld9BoxHeadless.exe', 'MEmuHeadless.exe', 'HD-Player.exe', 'NoxVMHandle.exe').

        Returns:
            pandas.DataFrame: A DataFrame containing detailed information about all identified connections between
                             ADB and emulators. The columns of the DataFrame are prefixed with 'aa_'.

        Note: This function is specifically designed for Windows and relies on Windows-specific functionalities.

        Example:

            from emulator2df import all_emulators_as_df

            df = all_emulators_as_df(adb=r"C:\ProgramData\anaconda3\envs\ldbot\platform-tools\adb.exe"
                         , emulator_exe=('Ld9BoxHeadless.exe', 'MEmuHeadless.exe', 'HD-Player.exe', 'NoxVMHandle.exe'))

            # df
            # Out[3]:
            #                                           aa_threads  ...                                          aa_PSUTIL
            # 0  [(19956, 0.765625, 0.71875), (8484, 0.0, 0.0),...  ...  psutil.Process(pid=1292, name='HD-Player.exe',...
            # 1  [(22392, 0.03125, 0.015625), (12392, 0.0, 0.0)...  ...  psutil.Process(pid=22188, name='NoxVMHandle.ex...
            # 2  [(22392, 0.03125, 0.015625), (12392, 0.0, 0.0)...  ...  psutil.Process(pid=22188, name='NoxVMHandle.ex...
            # 3  [(22392, 0.03125, 0.015625), (12392, 0.0, 0.0)...  ...  psutil.Process(pid=22188, name='NoxVMHandle.ex...
            # 4  [(22392, 0.03125, 0.015625), (12392, 0.0, 0.0)...  ...  psutil.Process(pid=22188, name='NoxVMHandle.ex...
            # 5  [(22392, 0.03125, 0.015625), (12392, 0.0, 0.0)...  ...  psutil.Process(pid=22188, name='NoxVMHandle.ex...
            # 6  [(22392, 0.03125, 0.015625), (12392, 0.0, 0.0)...  ...  psutil.Process(pid=22188, name='NoxVMHandle.ex...
"""
    alld = connect_to_all_tcp_devices_windows(adb_path=adb, convert_to_83=True)

    adbproc = find_procs_by_name(names=['adb.exe'])
    emulatorexe = find_procs_by_name(names=emulator_exe)
    allconnections = []
    for adbpr in adbproc:
        for q in adbpr.connections():
            try:
                ipaddress = q.raddr.ip
                portnumber = q.raddr.port
                allconnections.append((ipaddress, portnumber))
            except Exception as fe:
                continue
    foundconnections = []
    allreadydone = set()
    for emulatorex in emulatorexe:
        for q in emulatorex.connections():
            try:

                ipaddress = q.laddr.ip
                portnumber = q.laddr.port
                if (ipaddress, portnumber) in allconnections and (ipaddress, portnumber) not in allreadydone:
                    asdi = emulatorex.as_dict()
                    asdi['ADB_IP_ADDRESS'] = ipaddress
                    asdi['PORT_NUMBER'] = portnumber
                    asdi['ALL_CHILDREN'] = emulatorex.children()
                    asdi['PSUTIL'] = emulatorex
                    foundconnections.append(asdi)
                    allreadydone.add((ipaddress, portnumber))
            except Exception as fe:
                pass

    df = pd.DataFrame(foundconnections)
    df.columns = [f'aa_{x}' for x in df.columns]
    return df


