from distutils.core import setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
    f.close()

setup(
    name='crispy-parser',
    version='2.1.0',
    packages=['crispy'],
    url='https://github.com/fybx/crispy',
    license='GNU LGPL-v2.1',
    author='F. Y. BALABAN, <fyb@fybx.dev>',
    author_email='fyb@fybx.dev',
    description='Crispy is a simple command line argument parser, ready to be integrated to any project of any size!',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires=">=3.7"
)
