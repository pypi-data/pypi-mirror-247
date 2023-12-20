import io
import os
import shutil
import tempfile
import setuptools

current_dir = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(current_dir, "README.md"), encoding="utf-8") as fd:
    desc = fd.read()

# env_dir = tempfile.mkdtemp(prefix="fingerscan-install-")  # 创建一个临时目录，目录名以"fingerscan-install-"为前缀
# shutil.copytree(os.path.abspath(os.getcwd()), os.path.join(env_dir, "fingerscan"))  # 将当前工作目录的内容复制到临时目录的"fingerscan"文件夹中
# os.chdir(env_dir)  # 改变当前工作目录到临时目录
setuptools.setup(
    name="fingerscan",
    license='',
    version="1.1.5",
    long_description=desc,
    long_description_content_type="text/markdown",
    description="指纹识别开发测试版本",
    author="zhizhuo",
    author_email="zhizhuoshuma@163.com",
    url='https://github.com/expzhizhuo',
    # 定义入口点，即命令行脚本
    entry_points={
        'console_scripts': [
            'fingerscan=fingerscan.fingerscan:main',
        ],
    },
    package_data={"fingerscan": ["*", "export/config/*"]},
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "colorama",
        "mmh3",
        "urllib3",
        "pyfiglet",
        "termcolor",
        "openpyxl",
        "poc-tool",
        "alive-progress",
        "pyOpenSSL"
    ],
    python_requires=">=3.8",
)
