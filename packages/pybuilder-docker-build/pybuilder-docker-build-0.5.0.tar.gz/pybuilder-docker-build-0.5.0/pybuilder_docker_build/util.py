import os
import posixpath
from docker import DockerClient
from pybuilder.core import Project, Logger

docker_client_singleton = None


def _full_image_tag(project):
    return "{docker_image_repo}:{docker_image_tag}".format(
        docker_image_repo=project.get_property("docker_image_repo"),
        docker_image_tag=project.get_property("docker_image_tag")
    )


def _build_args(project: Project, logger: Logger):
    build_args_dict = {
        "PROJECT_NAME": project.name,
        "PROJECT_VERSION": project.version,
        "PROJECT_DIST_VERSION": project.dist_version,
        "PROJECT_DIST_DIR": posixpath.join(os.path.relpath(project.expand_path(project.get_property("dir_dist")), start=project.get_property("docker_build_path")))
    }
    if project.has_property("docker_build_args"):
        build_args_dict.update(project.get_property("docker_build_args"))
    logger.debug("Created build args: %s", build_args_dict)
    return build_args_dict


def _get_docker_client():
    global docker_client_singleton
    if docker_client_singleton is None:
        docker_client_singleton = DockerClient.from_env()
    return docker_client_singleton


