import asyncio
import builtins
import contextlib
import json
import logging
import os
import random
import subprocess
import time
import typing as tp
from pathlib import Path

from huggingface_hub import model_info, snapshot_download


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


def resolve_task_name(huggingface_model_id: str):
    info = model_info(huggingface_model_id)
    if info.pipeline_tag is not None:
        if info.library_name == "transformers":
            task = info.pipeline_tag
        elif info.library_name == "sentence-transformers":
            # TODO - maybe support multiple tasks here for sbert (sentence similarity, feature extraction, etc.)
            task = "sentence-transformers-feature-extraction"
    else:
        raise ValueError(
            "'task' kwarg must be specified if it cannot be inferred from the huggingface model's metadata."
        )

    logger.debug(
        f"Inferring task from huggingface model metadata...\nHF Model ID: {huggingface_model_id}\nTask: {task}\n"
    )
    return task


class Logger:
    def __init__(self, marker: str = "predict-timings"):
        self.marker = marker + "%s" % random.randint(0, 1000000)
        self.start = time.time()
        self.last = self.start

    def log(self, *args):
        current_time = time.time()
        elapsed_since_start = current_time - self.start
        elapsed_since_last_log = current_time - self.last

        message = " ".join(str(arg) for arg in args)
        timings = f"{elapsed_since_start:.2f}s since start, {elapsed_since_last_log:.2f}s since last log"

        print(f"{self.marker}: {message} - {timings}")
        self.last = current_time

    def info(self, *args):
        self.log(*args)


def get_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.new_event_loop()


def download_file(file, local_filename):
    print(f"Downloading {file} to {local_filename}")
    if os.path.exists(local_filename):
        os.remove(local_filename)
    if "/" in local_filename:
        if not os.path.exists(os.path.dirname(local_filename)):
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)

    command = ["pget", file, local_filename]
    subprocess.check_call(command, close_fds=True)


async def download_file_with_pget(remote_path, dest_path, pget_concurrency="10"):
    # Create the subprocess
    print("Downloading ", remote_path)
    if remote_path.endswith("json"):
        info = "%{filename_effective} took %{time_total}s (%{speed_download} bytes/sec)\n"
        args = ["curl", "-w", info, "-sLo", dest_path, remote_path]
    else:
        args = ["pget", "-c", pget_concurrency, remote_path, dest_path]
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        close_fds=True,
    )

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Print what the subprocess output (if any)
    if stdout:
        print(f"[stdout]\n{stdout.decode()}")
    if stderr:
        print(f"[stderr]\n{stderr.decode()}")


async def download_files_with_pget(remote_path: str, path: str, files: list[str]) -> None:
    download_jobs = "\n".join(f"{remote_path}/{f} {path}/{f}" for f in files)
    print(download_jobs)
    args = ["pget", "multifile", "-", "-f", "--max-conn-per-host", "100"]
    process = await asyncio.create_subprocess_exec(*args, stdin=-1, close_fds=True)
    # Wait for the subprocess to finish
    await process.communicate(download_jobs.encode())


def list_remote_filenames(remote_path):
    """
    Given a remote bucket path, return a list of all files in the bucket.

    Example:

    ```
    >>> list_remote_filenames("gs://my-bucket/username/roberta-base")
    ["config.json", "pytorch_model.bin", "tokenizer.json", "vocab.json"]

    >>> list_remote_filenames("https://storage.googleapis.com/my-bucket/username/roberta-base")
    ["config.json", "pytorch_model.bin", "tokenizer.json", "vocab.json"]
    ```
    """
    try:
        from google.cloud import storage
    except ImportError:
        raise ImportError(
            "google-cloud-storage is not installed. Can't infer remote filenames without it. "
            "Please either install it or pass in remote_filenames kwarg."
        )
    bucket_name, *prefixes = remote_path.replace("https://storage.googleapis.com/", "").replace("gs://", "").split("/")
    prefix = "/".join(prefixes)
    print("bucket name", bucket_name)
    print("prefix", prefix)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    remote_filenames = [blob.name[len(prefix) + 1 :] for blob in blobs]
    print(f"Found {len(remote_filenames)} files in {remote_path}:\n{remote_filenames}")
    return remote_filenames


def maybe_pget_weights(
    path,
    remote_path: tp.Optional[str] = None,
    remote_filenames: tp.Optional[tp.List[str]] = None,
    logger: tp.Optional[Logger] = None,
):
    """
    Downloads files from remote_path to path if they are not present in path. File paths are constructed
    by concatenating remote_path and remote_filenames. If remote_path is None, files are not downloaded.

    Args:
        path (str): Path to the directory where files should be downloaded
        remote_path (str): Path to the directory where files should be downloaded from
        remote_filenames (List[str]): List of file names to download
        logger (Logger): Logger object to log progress

    Returns:
        path (str): Path to the directory where files were downloaded

    Example:

        maybe_pget_weights(
            path="models/roberta-base",
            remote_path="gs://my-bucket/username/roberta-base",
            remote_filenames=["config.json", "pytorch_model.bin", "tokenizer.json", "vocab.json"],
            logger=logger
        )
    """

    if remote_path:
        remote_path = remote_path.rstrip("/")
        remote_path = remote_path.replace("gs://replicate-hf-weights/", "https://weights.replicate.delivery/hf/")
        remote_path = remote_path.replace("gs://", "https://storage.googleapis.com/")

        if remote_filenames is None:
            remote_filenames = list_remote_filenames(remote_path)

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            missing_files = remote_filenames
        else:
            local_files = os.listdir(path)
            missing_files = [file for file in remote_filenames if file not in local_files]

        get_loop().run_until_complete(download_files_with_pget(remote_path, path, missing_files))

    return path


@contextlib.contextmanager
def delay_prints(REALLY_EAT_MY_PRINT_STATEMENTS: bool = False) -> tp.Iterator[tp.Callable]:
    lines = []

    def delayed_print(*args: tp.Any, **kwargs: tp.Any) -> None:
        lines.append((args, kwargs))

    if REALLY_EAT_MY_PRINT_STATEMENTS:
        builtins.print, _print = delayed_print, builtins.print
    try:
        yield delayed_print
    finally:
        if REALLY_EAT_MY_PRINT_STATEMENTS:
            builtins.print = _print
        for args, kwargs in lines:
            print(*args, **kwargs)

    return delay_prints


def prefix_exists(bucket_name, prefix, project_name: tp.Optional[str] = None):
    """Given bucket name, and a prefix (e.g. "hf_model_id/hf_model_sha"), return whether the prefix exists.)"""
    try:
        from google.cloud import storage
    except ImportError:
        raise ImportError(
            "google-cloud-storage is not installed. Can't infer remote filenames without it. "
            "Please either install it or pass in remote_filenames kwarg."
        )
    storage_client = storage.Client(project=project_name)
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, max_results=1)
    return any(blobs)


def mirror_weights(
    hf_model_id: str,
    gcp_bucket_name: str,
    gcp_bucket_prefix: str = "{hf_model_id}/{hf_model_sha}",
    gcp_project_name: tp.Optional[str] = None,
    overwrite: bool = False,
    hf_model_sha: tp.Optional[str] = None,
    config_save_path: tp.Optional[str] = None,
    **kwargs,
):
    """Mirror weights from huggingface.co to a GCP bucket.

    Args:
        hf_model_id (str): Huggingface model ID (e.g. "bert-base-uncased")
        gcp_bucket_name (str): Name of the GCP bucket to mirror to
        overwrite (bool): Whether to overwrite existing weights in the bucket
        hf_model_sha (str): Huggingface model SHA (e.g. "b5a5d9a8a9a8")
        config_save_path (str): Path to save config file to, if specified.
        **kwargs: Additional kwargs to pass to snapshot_download
    """
    hf_model_id = hf_model_id.lower()
    task = resolve_task_name(hf_model_id)

    gcp_bucket_uri = f"gs://{gcp_bucket_name}".rstrip("/")
    info = model_info(hf_model_id, revision=hf_model_sha)
    hf_model_sha = info.sha
    remote_filenames = [x.rfilename for x in info.siblings]

    gcp_bucket_prefix = gcp_bucket_prefix.format(hf_model_id=hf_model_id, hf_model_sha=hf_model_sha)
    weights_uri = f"{gcp_bucket_uri}/{gcp_bucket_prefix}"
    print("gcp_bucket_name", gcp_bucket_name)
    print("gcp_bucket_prefix", gcp_bucket_prefix)
    print("gcp_project_name", gcp_project_name)
    mirror_exists = prefix_exists(gcp_bucket_name, gcp_bucket_prefix, gcp_project_name)
    print("mirror_exists", mirror_exists)

    do_mirror = False if mirror_exists and not overwrite else True
    if mirror_exists and not overwrite:
        print(f"Found non-empty weights URI: {weights_uri}. Not overwriting.")
    elif mirror_exists and overwrite:
        print(f"Found non-empty weights URI: {weights_uri}, but overwrite=True. Overwriting.")
    else:
        print(f"No files found in destination URI: {weights_uri}. Mirroring.")

    if do_mirror:
        cache_dir = snapshot_download(repo_id=hf_model_id, revision=hf_model_sha, **kwargs)

        cmd = f"gsutil -m cp -r {cache_dir}/* {weights_uri}"
        print("Running gsutil cp command:\n", cmd, "\n")
        subprocess.check_output(cmd.split(), close_fds=True)

    if config_save_path:
        config = {
            "hf_model_id": hf_model_id,
            "task": task,
            "gcp_bucket_weights": weights_uri,
            "trust_remote_code": True,
            "remote_filenames": remote_filenames,
        }
        Path(config_save_path).write_text(json.dumps(config, indent=2))

    return weights_uri
