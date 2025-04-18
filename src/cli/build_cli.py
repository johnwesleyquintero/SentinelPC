# 1. PyInstaller Packaging Script (build_cli.py)
import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "SentinelPC_cli_v2.py",
        "--name=sysopt",  # Final executable name
        "--onefile",  # Single binary output
        # Explicitly include custom modules
        "--hidden-import=config_manager_v2",
        "--hidden-import=performance_optimizer_v2",
        # Bundle configuration files
        "--add-data=config/*.ini:config",
        "--clean",  # Clear previous builds
        "--icon=favicon_ico/favicon.ico",  # Optional icon
    ]
)
