from pathlib import Path

from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v0.0.16')
print('     setup: module :  accurate_timed_loop')

# @formatter:off
setup(
    description='Accurate timed loop',
    keywords=['accurate loop', 'utility'],
    install_requires=[
        'pytest-ver',
        'pytest',
        'on_the_fly_stats',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='accurate-timed-loop',
    packages=find_packages(include='./accurate_timed_loop*', ),
    include_package_data=True,
    exclude_package_data={'./accurate_timed_loop/lib': ['.gitignore']},
    version='0.0.16',
    license='MIT',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    author='JA',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/accurate-timed-loop/src/master',
    download_url='https://bitbucket.org/arrizza-public/accurate-timed-loop/get/master.zip',
)
# @formatter:on

print('     setup: done')
