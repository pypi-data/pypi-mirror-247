from setuptools import setup, find_packages

str_version = '1.0.2'

setup(name='UCTool-1.0',
      version=str_version,
      description='UCTool-1.0',
      author='xiejunwei',
      author_email='xiejunwei@qq.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires= ['pypinyin', 'opencv-python'],
      python_requires='>=3')

