from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='django_jquery_datatables',
    version='1.0.3',
    description='Python library that integrates the popular jQuery DataTables library with Django projects.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Salik Sheraz',
    author_email='salik.sheraz@it-masons.com',
    url='https://github.com/Saliksheraz/django_jquery_datatables.git',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0.0',
        'requests>=2.0.0',
        'django-rest-framework>=0.1.0'
    ],
)
