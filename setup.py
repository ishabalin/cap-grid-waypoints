try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='cap-grid-waypoints',
    version='0.1',
    author='ishabalin',
    url='https://github.com/ishabalin/cap-grid-waypoints',
    description='CAP grid waypoint generator',
    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python',
    ],
    license='Public Domain',
    py_modules=['cap_grid_waypoints'],
    scripts=['cap_grid_waypoints.py'],
    packages=find_packages(exclude=['ez_setup', 'tests']),
    zip_safe=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cap-grid-waypoints=cap_grid_waypoints:main',
        ],
    },
)
