#!/usr/bin/env python3

"""Utility to clean out unused stuff from docker.
"""

import argparse
import logging
import subprocess

# MARK: Local Utilities


def _run(command: str, directory: str = None):
    logging.debug("running: %s", command)
    with subprocess.Popen(f"{command}", shell=True, cwd=directory, stdout=subprocess.PIPE) as cmd:
        for line in cmd.stdout:
            print(f"  {line.decode('utf-8').strip()}")


def _process(command: str):
    logging.debug("Processing command: %s", command)
    with subprocess.Popen(
        f"{command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ) as pipe:
        for line in pipe.stdout:
            yield line.rstrip()
        pipe.communicate()
        if pipe.returncode != 0:
            raise subprocess.CalledProcessError(pipe.returncode, command)


# MARK: Application


def _remove_exited_processes():
    logging.info("Removing exited processes...")
    for line in _process("docker ps --all -q -f status=exited"):
        items = line.decode("utf-8").split()
        for item in items:
            print(f"  removing: {item}")
            subprocess.check_output(["docker", "rm", item])


def _remove_old_container_versions():
    logging.info("Removing old container versions...")
    images = {}

    for line in _process("docker image ls"):
        entry = line.decode("utf-8").split()
        if entry[0] == "REPOSITORY":
            continue

        name = entry[0]
        tag = entry[1]
        if tag == "latest":
            continue

        image_id = entry[2]
        if name in images:
            print(f"  removing {name}:{tag} ({image_id})")
            try:
                subprocess.check_output(["docker", "image", "rm", image_id])
            except subprocess.CalledProcessError:
                print(f"    WARNING: could not remove image {image_id}")
        else:
            images[name] = image_id


def _prune():
    logging.info("Pruning...")
    _run("docker system prune --force")
    _run("docker volume prune --force")


# MARK: Main Entry Point


def _parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Show debugging information")
    return parser.parse_args()


def _main():
    args = _parse_command_line()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    _remove_exited_processes()
    _remove_old_container_versions()
    _prune()


if __name__ == "__main__":
    _main()
