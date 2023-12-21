from setuptools import setup, find_packages

setup(
  name='ktro_asm',
  version='0.0.1',
  packages=find_packages(),
  entry_points={
    'console_scripts': [
      'ktroasm=ktro_asm.ktroasm:main'
    ]
  },
  install_requires=[
      'lark',
      # other dependencies...
  ]
)