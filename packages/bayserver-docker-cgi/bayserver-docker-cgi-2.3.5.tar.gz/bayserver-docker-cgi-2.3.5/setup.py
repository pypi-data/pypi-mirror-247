from setuptools import setup, find_packages

print("packages: " + str(find_packages()))

setup(
    name='bayserver-docker-cgi',
    version='2.3.5',
    packages=find_packages(),
    package_data={
        '': ['LICENSE.BAYKIT', 'README.md'],
    },  
    install_requires=[
      "bayserver-core==2.3.5",
    ],
    author='Michisuke-P',
    author_email='michisukep@gmail.com',
    description='CGI Docker for BayServer',
    license='MIT',
    python_requires=">=3.7",
    url='https://baykit.yokohama/',
)

