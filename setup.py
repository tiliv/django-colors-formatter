from setuptools import setup, find_packages
setup(
    name = "DjangoColorsFormatter",
    version = "1.0",
    packages = find_packages(),
    exclude_package_data = { 'djangocolors_formatter': ['*.pyc'] },

    # metadata for upload to PyPI
    author = "Tim Valenta",
    author_email = "tonightslastsong@gmail.com",
    description = "Zero-config logging formatter that uses the built-in DJANGO_COLORS setting",
    license = "BSD",
    keywords = "django colors logging formatter DJANGO_COLORS",
    url = "https://github.com/tiliv/django-colors-formatter",
)
