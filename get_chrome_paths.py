from __future__ import print_function
import os
import os.path
import platform
import sys


def filter_existing_paths(paths):
    return [p for p in paths if os.path.isfile(p)]


def get_chrome_paths():
    system = platform.system()
    chrome_paths = set()

    if system == 'Windows':
        if sys.version_info < (3,):
            import _winreg as winreg
        else:
            import winreg

        software_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software", 0, winreg.KEY_ENUMERATE_SUB_KEYS)
        index = 0
        while True:
            try:
                # Use EnumKey to get the subkey name by index
                subkey_name = winreg.EnumKey(software_key, index)
                index += 1
            except OSError:
                # EnumKey raises an OSError when all subkeys have been enumerated
                break

            try:
                subkey = winreg.OpenKey(software_key, subkey_name)
                value = winreg.QueryValueEx(subkey, "InstallerSuccessLaunchCmdLine")[0]
                winreg.CloseKey(subkey)
            except OSError:
                # QueryValueEx raises an OSError if InstallerSuccessLaunchCmdLine is not a valid value
                continue

            try:
                # Assuming that the value a string similar to:
                # "C:\Users\USER\AppData\Local\Google\Chrome\Application\chrome.exe" --from-installer
                browser_path = value.split('"', maxsplit=2)[1]
                if not os.path.isfile(browser_path):
                    continue
                chrome_paths.add(browser_path)
            except TypeError:
                # Raise error if value is not a string
                continue

        winreg.CloseKey(software_key)

    elif system == 'Darwin':
        common_paths = [
            # Google Chrome
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta',
            '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
            '/Applications/Google Chrome Dev.app/Contents/MacOS/Google Chrome Dev',
            # Chromium
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            # Microsoft Edge
            '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
            '/Applications/Microsoft Edge Beta.app/Contents/MacOS/Microsoft Edge Beta',
            '/Applications/Microsoft Edge Canary.app/Contents/MacOS/Microsoft Edge Canary',
            '/Applications/Microsoft Edge Dev.app/Contents/MacOS/Microsoft Edge Dev',
        ]

        chrome_paths.update(filter_existing_paths(common_paths))

    elif system == 'Linux':
        common_paths = [
            # Google Chrome
            '/usr/bin/google-chrome',
            '/snap/bin/google-chrome',
            # Chromium
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium',
            # Microsoft Edge
            '/usr/bin/microsoft-edge',
        ]

        chrome_paths.update(filter_existing_paths(common_paths))

    return chrome_paths


if __name__ == '__main__':
    for chrome_path in get_chrome_paths():
        print(chrome_path)
