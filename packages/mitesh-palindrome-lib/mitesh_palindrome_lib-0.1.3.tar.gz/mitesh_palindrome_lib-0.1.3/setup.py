from setuptools import setup, find_packages

readme = "# Introduction \n \
This is an experimentation library to check the palindrome. \n \
# Installation \n \
pip install mitesh_palindrome_lib \
"
setup(
    name = "mitesh_palindrome_lib",
    version = "0.1.3",
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

