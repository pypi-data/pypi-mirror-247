from setuptools import setup

setup(
    name="zoomto",
    version="0.2",
    packages=[
        "zoomto", 
        "zoomto.core", 
        "zoomto._internal", 
        "zoomto._internal.img",
        "zoomto.tools",
    ],
    # include image files
    package_data={
        "": [
            "*.png",
        ]
    },
    install_requires=[
        "pyautogui",
        "pygetwindow",
        "screeninfo",
        "pywin32",
        "easyocr",
        "zrcl3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "zoomto=zoomto.tools.shell:runshell",
        ]
    }
)
