import ctypes
import sys
import os

if sys.platform == 'win32':
    binDir = "C:\\Program Files\\Inuitive\\InuDev\\bin"
    pythonAPIDir = "C:\\Users\\alexn\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\inu_api\\"
    cnnBinDir = "C:\\Program Files\\Inuitive\\InuDev\\config\\AI4000\\cnn_bins"
    myDll1 = ctypes.CDLL(os.path.join(binDir, "InuCommonUtilities.dll"))
    myDll2 = ctypes.CDLL(os.path.join(binDir, "InuStreamsd.dll"))
    myDll4 = ctypes.CDLL(os.path.join(pythonAPIDir, "InuStreamsPyth.pyd"))
elif sys.platform == 'linux':
    binDir = "/opt/Inuitive/InuDev/bin"
    cnnBinDir = "/opt/Inuitive/InuDev/config/AI4000/cnn_bins"
    myDll1 = ctypes.CDLL(os.path.join(binDir, "libInuCommonUtilities.so"))
    myDll2 = ctypes.CDLL(os.path.join(binDir, "libInuStreams.so"))
    import importlib.util


    def load_python_wrapper(module_name: str):
        # @brief    loadPythonWrapper
        #
        # The loadPythonWrapper function checks the Python version using sys.version_info and imports the appropriate
        #   module based on the version.
        # @param  iModuleName common module name
        # @return wrapper module
        python_version = sys.version_info
        print("Python version {}".format(python_version))
        if python_version >= (3, 10):
            specific_file_name = "lib" + module_name + "_3_10_12.so"
        elif python_version >= (3, 6):
            specific_file_name = "lib" + module_name + "_3_6_9.so"
        else:
            raise RuntimeError("Unsupported Python version")
        # Modify sys.path to include the directory containing the specific .so file
        sys.path.insert(0, binDir)
        try:
            spec = importlib.util.spec_from_file_location(module_name, specific_file_name)
            wrapper_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wrapper_module)
        except ImportError:
            raise ImportError(f"Failed to import module {specific_file_name}")
        # Remove the directory from sys.path after importing the module
        sys.path.pop(0)
        return wrapper_module

    # Load the appropriate Python wrapper
    inu_streams = load_python_wrapper("InuStreamsPyth")

# from InuStreamsPyth import *

