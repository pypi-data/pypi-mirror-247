from setuptools import setup, find_packages

readme = "# Introduction \
This is an experimentation library to check the palindrome.\
# Installation \
pip install mitesh_palindrome_lib \
"
setup(
    name = "mitesh_lib_for_palindrome",
    version = "0.1.0",
    author="mitesh gupta",
    author_email="mitesh51294@gmail.com",
    description="This lib will help you validate a palindrome ",
    long_description=readme,
    packages=(),
    # entry_points={
    #     'console_scripts': [
    #         'executable_test_script = mitesh_palindrome_lib.validate_palindrome:main',
    #     ],
    # },
)

