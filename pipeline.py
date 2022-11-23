import random
import string
import sys

import anyio
from dagger import Config, Connection
from dagger.api.gen import Client, DirectoryID


def random_string(n: int) -> str:
    return "".join(
        random.choices(
            string.ascii_lowercase + string.digits, k=n
        )
    )


async def job_a(client: Client):
    cnt_mnt_dir = f"/{random_string(8)}-src"

    await (
        client.container().
        from_("python:alpine").
        exec(["python", "-c", "from time import sleep; sleep(5); \"print('Hello world')\""])
    ).exit_code()


async def job_b(client: Client, src_dir_id: DirectoryID):
    cnt_mnt_dir = f"/{random_string(8)}-src"

    await (
        client.container().
        from_("alpine:latest").
        with_mounted_directory(cnt_mnt_dir, src_dir_id).
        with_workdir(cnt_mnt_dir).
        exec(["cat", "LICENSE"])
    ).exit_code()


async def main():
    async with Connection(Config(log_output=sys.stdout)) as client:
        src_dir_id = await client.host().workdir().id()

        async with anyio.create_task_group() as tg:
            tg.start_soon(job_a, client)
            tg.start_soon(job_b, client, src_dir_id)

if __name__ == "__main__":
    anyio.run(main)
