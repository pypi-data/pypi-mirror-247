from setuptools import setup

with open("README.rst", encoding='utf-8') as f:
    long_description = f.read()

setup(name='FreeWorkUT',  # 包名
      version='0.1.4',  # 版本号
      description='这是个测试版，正式版请检索FreeWork！',
      long_description=long_description,
      author='Jhonie King(王骏诚)',
      author_email='queenelsaofarendelle2022@gmail.com',
      license='MIT License',
      packages=["FreeWork"],
      keywords=['python', 'Office', 'Excle', 'Word', 'File\'s operation'],
      install_requires=['openpyxl', 'python-docx', 'pytest-shutil'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
