import os

from docker import DockerClient
from pybuilder.core import task, Project, Logger, init, depends

from pybuilder_docker_build import util
from pybuilder_docker_build.util import _full_image_tag, _build_args, _get_docker_client


@init
def init_docker_build(project: Project):
    project.set_property_if_unset("docker_cli", False)
    project.set_property_if_unset("docker_path", "docker")
    project.set_property_if_unset("docker_build_file", "Dockerfile")
    project.set_property_if_unset("docker_build_path", project.get_property("basedir"))
    project.set_property_if_unset("docker_build_force_rm", False)
    project.set_property_if_unset("docker_image_repo", project.name)
    project.set_property_if_unset("docker_image_tag", "latest")


@task(description="Perform docker build to create a docker image")
@depends("publish")
def docker_build(project: Project, logger: Logger):
    if project.get_property("docker_cli", False):
        docker_command = ("{docker_path} "
                          "build "
                          "-t {image_tag} "
                          "-f {docker_build_file} "
                          "{forcerm}"
                          "{build_args} "
                          "{docker_build_path}".format(
                                docker_path=project.get_property("docker_path"),
                                docker_build_path=project.get_property("docker_build_path"),
                                image_tag=_full_image_tag(project),
                                build_args=" ".join([f'--build-arg {k}="{v}"' for k, v in _build_args(project, logger).items()]),
                                docker_build_file=project.get_property("docker_build_file"),
                                forcerm="--force-rm " if project.get_property("docker_build_force_rm") else ""))
        logger.debug("Executing %s", docker_command)
        os.system(docker_command)
    else:
        logger.debug("docker build path %s", project.get_property("docker_build_path"))
        docker_client: DockerClient = _get_docker_client()
        docker_image, docker_logs = docker_client.images.build(
            path=project.get_property("docker_build_path"),
            dockerfile=project.get_property("docker_build_file"),
            buildargs=_build_args(project, logger),
            tag=_full_image_tag(project),
            forcerm=project.get_property("docker_build_force_rm")
        )
        for line_dict in docker_logs:
            if "stream" in line_dict:
                logger.debug(line_dict["stream"].strip())


@task(description="Save built docker image to local dist directory")
@depends("docker_build")
def docker_save(project: Project, logger: Logger):
    docker_image_dir = project.expand_path(project.get_property("dir_dist"), "image")
    docker_image_file = os.path.join(docker_image_dir, f"{project.name}-{project.version}.tar")
    logger.debug("Writing docker image to %s", docker_image_file)
    os.mkdir(docker_image_dir)

    if project.get_property("docker_cli"):
        docker_save_command = "{docker_path} save -o {docker_image_file} {docker_full_image_tag}".format(
            docker_path=project.get_property("docker_path"),
            docker_image_file=docker_image_file,
            docker_full_image_tag=_full_image_tag(project)
        )
        logger.debug("Executing %s", docker_save_command)
        os.system(docker_save_command)
    else:
        docker_client: DockerClient = _get_docker_client()
        docker_image = docker_client.images.get(_full_image_tag(project))
        with open(docker_image_file, 'wb') as f:
            for chunk in docker_image.save():
                f.write(chunk)
        logger.info("Wrote docker image to %s", docker_image_file)


@task(description="Push built docker image to registry")
@depends("docker_build")
def docker_push(project: Project, logger: Logger):
    if project.get_property("docker_cli", False):
        if project.has_property("docker_registry_auth"):
            docker_login_command = ("{docker_path} login "
                                    "--username {docker_username} "
                                    "--password {docker_password} "
                                    "{docker_registry}"
                                    ).format(
                docker_path=project.get_property("docker_path"),
                docker_username=project.get_property("docker_registry_auth")["username"],
                docker_password=project.get_property("docker_registry_auth")["password"],
                docker_registry=project.get_property("docker_registry") if project.has_property("docker_registry") else ""
            )
            logger.debug("Running command %s", docker_login_command)
            os.system(docker_login_command)
        docker_push_command = ("{docker_path} push {image_tag}".format(
            docker_path=project.get_property("docker_path"),
            image_tag=_full_image_tag(project)
        ))
        logger.debug("Executing %s", docker_push_command)
        os.system(docker_push_command)
    else:
        docker_client: DockerClient = _get_docker_client()
        docker_logs = docker_client.images.push(
            project.get_property("docker_image_repo"),
            tag=project.get_property("docker_image_tag"),
            auth_config=project.get_property("docker_registry_auth", None),
            stream=True,
            decode=True)
        for line in docker_logs:
            logger.debug(line)
    logger.info("Completed docker push")