from setuptools import setup, find_packages



setup(
  name='ClastEngine',
  version='0.5.1',
  author='0x402',
  author_email='romanhaziahmetov3@gmail.com',
  description='2D движок для создания простых игр',
  packages=find_packages(),
  url='https://qlcode.pythonanywhere.com',
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
#  keywords='example python',
#  project_urls={
#    'Documentation': 'link'
#  },
  python_requires='>=3.7'
)
