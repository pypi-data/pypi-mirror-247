from setuptools import setup, find_packages

setup(
    name = "mitesh_palindrome_lib",
    version = "0.1.1",
    author="mitesh gupta",
    author_email="mitesh51294@gmail.com",
    description="This lib will help you validate a palindrome ",
    packages=(),
    entry_points={
        'console_scripts': [
            'executable_test_script = mitesh_palindrome_lib.validate_palindrome:main',
        ],
    },
)

