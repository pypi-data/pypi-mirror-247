from distutils.core import setup
setup(
    name='HSsound',
    packages=['HSsound'],
    version='1.1.5',
    license='MIT',
    description='Package to perform calculations on sound measurements',
    author='Jacob Vestergaard',
    author_email='jacobvestergaard95@gmail.com',
    url='https://github.com/jacobv95/HSsound',
    download_url='https://github.com/jacobv95/HSsound/archive/refs/tags/v1.tar.gz',
    keywords=['python', 'sound', 'measurement', 'HS'],
    install_requires=[            # I get to this in a second
        'pyees', 'matplotlib'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
    ],
)
