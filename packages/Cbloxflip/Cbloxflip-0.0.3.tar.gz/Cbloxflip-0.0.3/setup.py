from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Cbloxflip',
  version='0.0.3',
  description='a bloxflip api wrapper that you can use user.send or veiw your info',
  long_description="this is a bloxflip api wrapper made by culty and been nspired by his team first release 0.0.3",
  url='',  
  author='itsculty',
  author_email='sleepyculty@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['bloxflip', 'bloxflipApiWrapper', 'API'],
  packages=find_packages(),
  install_requires=['requests', 'websockets'] 
)
