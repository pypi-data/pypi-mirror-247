'''Setup script to create the python AdHawk SDK
Usage:
To create the package, ensure all required files are in MANIFEST.in and run `python setup.py sdist`
pip install the resulting package and run adhawkdemo
'''

import setuptools

setuptools.setup(
    name='adhawk',
    version='5.11.4',
    description='AdHawk Microsystems SDK',
    url='http://www.adhawkmicrosystems.com/',
    author='AdHawk Microsystems',
    author_email='info@adhawkmicrosystems.com',
    packages=['adhawkapi', 'adhawkapi.frontend', 'frontend'],
    license="Proprietary",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy'
    ],
    entry_points={
        'gui_scripts': [
            'adhawkdemo=frontend.frontend_diag:main',
            'adhawk_video_demo=frontend.frontend_gaze_in_image:main',
        ],
        'console_scripts': [
            'adhawkipd=frontend.frontend_ipd:main',
        ]
    },
)