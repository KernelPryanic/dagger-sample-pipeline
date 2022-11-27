import random
import string
import sys

import anyio
from dagger import Config, Connection
from dagger.api.gen import Client, Directory


def random_string(n: int) -> str:
    return "".join(
        random.choices(
            string.ascii_lowercase + string.digits, k=n
        )
    )


async def job_a(client: Client, src_dir: Directory):
    cnt_mnt_dir = f"/{random_string(8)}-src"

    await (
        client.container().
        from_("python:3.11-alpine").
        with_mounted_directory(cnt_mnt_dir, src_dir).
        with_workdir(cnt_mnt_dir).
        exec(["cat", "LICENSE"])
    ).exit_code()


async def job_b(client: Client, src_dir: Directory):
    cnt_mnt_dir = f"/{random_string(8)}-src"

    await (
        client.container().
        from_("ghcr.io/kernelpryanic/dagger-debug:debugging").
        with_mounted_directory(cnt_mnt_dir, src_dir).
        with_workdir(cnt_mnt_dir).
        exec(["cat", "LICENSE"])
    ).exit_code()


async def main():
    async with Connection(Config(log_output=sys.stdout)) as client:
        src_dir = client.host().workdir()

        await job_a(client, src_dir)
        await job_b(client, src_dir)

if __name__ == "__main__":
    anyio.run(main)
