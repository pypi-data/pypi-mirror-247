import os
from pathlib import Path
from typing import Generator

import pytest
from docker.models.images import Image

from tomodachi_testcontainers import EphemeralDockerImage
from tomodachi_testcontainers.utils import get_docker_image


@pytest.fixture(scope="session")
def testcontainers_docker_image() -> Generator[Image, None, None]:
    if image_id := os.getenv("TOMODACHI_TESTCONTAINER_IMAGE_ID"):
        yield get_docker_image(image_id)
    else:
        dockerfile = (
            Path(os.environ["TOMODACHI_TESTCONTAINER_DOCKERFILE_PATH"])
            if os.getenv("TOMODACHI_TESTCONTAINER_DOCKERFILE_PATH")
            else None
        )
        context = (
            Path(os.environ["TOMODACHI_TESTCONTAINER_DOCKER_BUILD_CONTEXT"])
            if os.getenv("TOMODACHI_TESTCONTAINER_DOCKER_BUILD_CONTEXT")
            else None
        )
        target = os.getenv("TOMODACHI_TESTCONTAINER_DOCKER_BUILD_TARGET")
        with EphemeralDockerImage(dockerfile=dockerfile, context=context, target=target) as image:
            yield image
