# Android emulators to DataFrame

## pip install emulator2df

### Tested against Windows / Python 3.11 / Anaconda


```python

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
```