import docker
import sys
import subprocess
import os

""" def stream_container_logs(container):
    # Stream and print the container's stdout in real-time
    for log_chunk in container.logs(stream=True, stdout=True, stderr=False):
        print(log_chunk.decode(), end='') """

def download_models(container):
    try:
        # Run MFA commands inside the Docker container
        mfa_command = [
            "mfa",
            "model",
            "download",
            "acoustic",
            "english_us_arpa"
        ]
        exec_result = container.exec_run(mfa_command)
        print("Command output:", exec_result.output.decode())

        mfa_command = [
            "mfa",
            "model",
            "download",
            "dictionary",
            "english_us_arpa"
        ]
        exec_result = container.exec_run(mfa_command)
        print("Command output:", exec_result.output.decode())

    except subprocess.CalledProcessError as e:
        print(f"Error executing MFA command: {e}")
        # Handle the error as needed

def validate_data(container, container_data_directory):
    try:
        # Run MFA commands inside the Docker container
        mfa_command = [
            "mfa",
            "validate",
            container_data_directory,
            "english_us_arpa",
            "english_us_arpa"
        ]
        exec_result = container.exec_run(mfa_command)
        print("Command output:", exec_result.output.decode())

    except subprocess.CalledProcessError as e:
        print(f"Error executing MFA command: {e}")
        # Handle the error as needed

def align_data(container, container_data_directory, container_aligned_data_directory):
    try:
        # Run MFA commands inside the Docker container
        mfa_command = [
            "mfa",
            "align",
            container_data_directory,
            "english_us_arpa",
            "english_us_arpa",
            container_aligned_data_directory
        ]
        exec_result = container.exec_run(mfa_command)
        print("Command output:", exec_result.output.decode())

    except subprocess.CalledProcessError as e:
        print(f"Error executing MFA command: {e}")
        # Handle the error as needed

def run_mfa(trial_directory, verbose=False):
    if verbose:
        print("RUNNING MFA")

    local_data_directory = os.path.join(trial_directory, "trials")
    local_aligned_data_directory = os.path.join(trial_directory, "textgrids")

    os.mkdir(local_aligned_data_directory)

    # Create a Docker client
    client = docker.from_env()

    # Specify the image name and tag
    image_name = "mmcauliffe/montreal-forced-aligner"
    image_tag = "latest"

    # Pull the Docker image
    client.images.pull(image_name, tag=image_tag)

    container_data_directory = "/data"
    container_aligned_data_directory = "/aligned"
    
    volume_mapping = {
        local_data_directory: {'bind': container_data_directory, 'mode': 'rw'},
        local_aligned_data_directory: {'bind': container_aligned_data_directory, 'mode': 'rw'}
    }

    # Run the Docker container
    container = client.containers.run(
        f"{image_name}:{image_tag}",
        command="/bin/bash",  # You can customize the command if needed
        volumes=volume_mapping,
        stdin_open=True,
        tty=True,
        detach=True
    )

    download_models(container)

    validate_data(container, container_data_directory)

    align_data(container, container_data_directory, container_aligned_data_directory)

    # Stop and remove the Docker container
    container.stop()
    container.remove()

    if (verbose):
        print("MFA COMPLETE")

    return local_aligned_data_directory
