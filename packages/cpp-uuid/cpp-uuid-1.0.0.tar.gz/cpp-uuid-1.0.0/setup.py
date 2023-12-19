import os

from setuptools import Extension, dist, setup


class BinaryDistribution(dist.Distribution):
    def has_ext_modules(self):
        return super().has_ext_modules()


def read_readme(path: str) -> str:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), path)) as file:
        return file.read()


setup(
    name='cpp-uuid',
    version='1.0.0',
    package_dir={'': 'src'},
    long_description=read_readme('README.rst'),
    long_description_content_type='text/x-rst',
    zip_safe=False,
    ext_modules=[
        Extension(
            'cpp_uuid',
            sources=['src/cpp_uuid/uuid.cpp'],
            include_dirs=['src/cpp_uuid/include'],
            extra_compile_args=['-Ofast', '-march=native'],
        )
    ],
    distclass=BinaryDistribution,
)
