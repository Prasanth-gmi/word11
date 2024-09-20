import docker
import os
from crewai_tools import tool

def build_and_run_docker_image(dockerfile_path, image_name, container_name, ports, dockerhub_username, dockerhub_password, repo_name, tag):
    client = docker.from_env()

    # Build Docker image
    try:
        print(f"Building Docker image '{image_name}' from path '{dockerfile_path}'...")
        image, logs = client.images.build(path=dockerfile_path, tag=image_name)
        for log in logs:
            if 'stream' in log:
                print(log['stream'].strip())
    except Exception as e:
        print(f"Error while building image: {e}")
        return

    # Check if container with the same name is already running and stop it
    try:
        container = client.containers.get(container_name)
        print(f"Stopping existing container '{container_name}'...")
        container.stop()
        container.remove()
    except docker.errors.NotFound:
        print(f"No existing container named '{container_name}' found.")

    # Run Docker container
    try:
        print(f"Running Docker container '{container_name}'...")
        container = client.containers.run(
            image_name,
            name=container_name,
            ports=ports,
            detach=True
        )
        print(f"Container '{container_name}' is running.")
    except Exception as e:
        print(f"Error while running container: {e}")

    # Log in to Docker Hub
    try:
        print(f"Logging into Docker Hub as '{dockerhub_username}'...")
        client.login(username=dockerhub_username, password=dockerhub_password)
        print("Login successful.")
    except Exception as e:
        print(f"Error logging in to Docker Hub: {e}")
        return

    # Tag the image for Docker Hub
    try:
        full_image_name = f"{dockerhub_username}/{repo_name}:{tag}"
        print(f"Tagging image '{image_name}' as '{full_image_name}'...")
        image.tag(f"{dockerhub_username}/{repo_name}", tag)
    except Exception as e:
        print(f"Error tagging image: {e}")
        return

    # Push the image to Docker Hub
    try:
        print(f"Pushing image '{full_image_name}' to Docker Hub...")
        push_logs = client.images.push(f"{dockerhub_username}/{repo_name}", tag=tag, stream=True, decode=True)
        for log in push_logs:
            if 'status' in log:
                print(log['status'])
    except Exception as e:
        print(f"Error pushing image to Docker Hub: {e}")

# if __name__ == "__main__":
#     # Path to the directory containing your Dockerfile
@tool
def DockerAutomationTool(image_name: str, container_name: str, ports: str, dockerhub_username: str, dockerhub_password: str, repo_name: str, tag: str):
    """
    A custom tool to automate Docker tasks: building, running, and pushing an image to DockerHub.
    
    Args:
    - image_name: Set the docker image_name. It should be same agents.py file image_name value.
    - container_name: Set the docker container_name. It should be same agents.py file container_name value.
    - ports: Set the docker ports. It should be same agents.py file ports value.
    - dockerhub_username: This dockerhub_username for login use. It should be same agents.py file dockerhub_username value.
    - dockerhub_password: This dockerhub_password for login use. It should be same agents.py file dockerhub_password value.
    - repo_name: Set the docker repo_name. It should be same agents.py file repo_name value.
    - tag: Set the docker tag. It should be same agents.py file tag value.
    
    Returns:
    - A report detailing the success or failure of each Docker operation.
    """
    dockerfile_path = os.path.abspath(".")  # Adjust if necessary
    
    # # Name for the Docker image and container
    # image_name = "simple_image"
    # container_name = "simple_container"
    
    # # Map container ports to host ports
    # ports = {'8000/tcp': 8000}  # Example: expose port 8000

    # # Docker Hub credentials and repo details
    # dockerhub_username = "prasanth046"
    # dockerhub_password = "Su6yalun@"
    # repo_name = "simple"  # Docker Hub repo name
    # tag = "latest"  # Tag for the Docker image

    build_and_run_docker_image(dockerfile_path, image_name, container_name, ports, dockerhub_username, dockerhub_password, repo_name, tag)
