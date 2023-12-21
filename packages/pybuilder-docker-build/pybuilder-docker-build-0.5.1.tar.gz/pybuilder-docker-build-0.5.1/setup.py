#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-docker-build',
        version = '0.5.1',
        description = 'A Docker build plugin for PyBuilder',
        long_description = 'PyBuilder Docker Build Plugin\n=============================\n\nSummary\n-------\n\nThis project is a plugin for [PyBuilder](https://pybuilder.io) that will perform a\ndocker build for a Python package.  _PyBuilder Docker Build Plugin_ attempts to use\nsane defaults so that in most cases you only need add a `Dockerfile` to your\nproject base directory and a docker image will be built when you call\nthe appropriate task.\n\nUsage\n-----\n\nTo use this plugin in your `build.py` file add the following line to the\nplugins section:\n\n```python\nuse_plugin(\'pypi:pybuilder_docker_build\')\n```\n\nThis will add the following tasks to your build:\n\n| Task         | Description                               |\n|--------------|-------------------------------------------|\n| docker_build | Performs docker build                     |\n| docker_save  | Saves docker image to dist dir            |\n| docker_push  | Pushes docker image upstream to your repo |\n\nThe following properties are available:\n\n| Property              | Value        | Default            | Usage                                                               |\n|-----------------------|--------------|--------------------|---------------------------------------------------------------------|\n| docker_cli            | True / False | False              | Use docker cli to do build                                          |\n| docker_path           | str          | docker             | Path to docker executable                                           |\n| docker_build_path     | str          | `basedir` property | Path to docker build directory                                      |\n| docker_build_file     | str          | Dockerfile         | Dockerfile to use for build, relative path from `docker_build_path` |\n| docker_build_force_rm | True / False | False              | Use the force rm feature of docker build                            |\n| docker_image_repo     | str          | `project.name`     | The name of the image repository                                    |\n| docker_image_tag      | str          | latest             | A tag to apply to the repository                                    |\n| docker_build_args     | dict         | None               | A dict of build args                                                |\n| docker_registry_auth  | dict         | None               | A dict containing `username` and `password` for login / auth        |\n| docker_registry       | str          | None               | A http / https URL of registry for authentication and push          |\n\nBy default there are several build args that are supplied to the docker build, additional args can\nbe added with the `docker_build_args` property.  The default build args are:\n\n| Argument             | Value                                                                  |\n|----------------------|------------------------------------------------------------------------|\n| PROJECT_NAME         | `project.name`                                                         |\n| PROJECT_VERSION      | `project.version`                                                      |\n| PROJECT_DIST_VERSION | `project.dist_version`                                                 |\n| PROJECT_DIST_DIR     | The relative path from the `docker_build_path` property to `$dir_dist` |\n\nAuthentication\n--------------\n\nIf you need to push images to a registry then you probably need to set credentials.  Don\'t\ndo this directly in your build file but rather look them up from environment or use some other\nmethod for passing secrets to code.  The following is an extract from the `hello-world` sample\nproject in the `samples` directory:\n\n```python\n@init\ndef set_properties(project: Project):\n    project.set_property("docker_build_args", {"EXTRA_ARG": "Extra build arg"})\n    project.set_property("docker_image_repo", "dockerhubusername/hello-world")\n    # Don\'t put your credentials in code, look them up from environment or\n    # use some other way to pass secrets to your code\n    project.set_property(\n        "docker_registry_auth",\n        {\n            "username": os.getenv("DOCKER_HUB_USERNAME"),\n            "password": os.getenv("DOCKER_HUB_PASSWORD")\n        }\n    )\n```',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'Jeffrey Sheehan',
        author_email = 'jeff.sheehan7@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT License',

        url = 'https://github.com/jlsheehan/pybuilder-docker-build',
        project_urls = {},

        scripts = [],
        packages = ['pybuilder_docker_build'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['docker'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
