from subprocess import CompletedProcess, run


class Agent:
    def build_image(self, **args):
        pass

    def create_container(self, **args):
        pass

    def start_container(self, **args):
        pass

    def stop_container(self, **args):
        pass

    def remove_container(self, **args):
        pass

    def remove_image(self, **args):
        pass


class DockerAgent(Agent):
    def _execute(self, *args) -> CompletedProcess:
        return run(args, capture_output=True, check=True)

    def build_image(self, image_name: str, image_type: str) -> CompletedProcess:
        return self._execute("docker", "build", "-f", f"containers/{image_type}/Dockerfile", "-t", f"{image_name}", ".")

    def stop_container(self, name: str) -> CompletedProcess:
        return self._execute("docker", "container", "stop", f"{name}")

    def start_container(self, name: str) -> CompletedProcess:
        return self._execute("docker", "start", f"{name}")

    def remove_container(self, name: str) -> CompletedProcess:
        return self._execute("docker", "container", "rm", f"{name}")

    def remove_image(self, name: str) -> CompletedProcess:
        return self._execute("docker", "image", "rm", f"{name}")

    def create_container(
        self, image_name: str, container_name: str, exposed_port: int, container_port: int
    ) -> CompletedProcess:
        return self._execute(
            "docker", "create", "-p", f"{exposed_port}:{container_port}", "--name", f"{container_name}", f"{image_name}"
        )
