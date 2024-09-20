import docker
import os

def build_and_run_docker_image(dockerfile_path, image_name, container_name, ports):
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

if __name__ == "__main__":
    # Path to the directory containing your Dockerfile
    dockerfile_path = os.path.abspath(".")  # Use the current directory or adjust it
    
    # Name for the Docker image and container
    image_name = "simple_image"
    container_name = "simple_container"
    
    # Map container ports to host ports
    ports = {'8000/tcp': 8000}  # Example: expose port 8000

    build_and_run_docker_image(dockerfile_path, image_name, container_name, ports)
