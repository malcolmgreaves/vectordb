[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/malcolmgreaves/vectordb)

# vectordb

Explores embedding generation, storage, retrieval, and k-NN with vector databases.

## Using

To add and install this package as a dependency of your project, run `poetry add vectordb`.

### qdrant setup

Follow the [quickstart guide](https://qdrant.tech/documentation/quick-start/):
```shell
docker pull qdrant/qdrant
```

then:
```shell
docker run -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

and use the client:

Either (1) [run this file](./src/vectordb/qdrant/quickstart.py) via `poetry run python -m vectordb.qdrant.quickstart`
or (2) copy and paste the following code into your REPL:
```python
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import CollectionStatus
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import UpdateStatus
from qdrant_client.http.models import Filter, FieldCondition, MatchValue


def sep(n: int = 20) -> None:
    print("-" * n)


client = QdrantClient("localhost", port=6333)

create_response = client.recreate_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)
print(f"{create_response=}")
sep()

collection_info = client.get_collection(collection_name="test_collection")
print(f"{collection_info=}")
assert collection_info.status == CollectionStatus.GREEN
assert collection_info.vectors_count == 0
sep()


operation_info = client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": ["Berlin", "London"]}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": ["Berlin", "Moscow"]}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": ["London", "Moscow"]}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"count": [0]}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44]),
    ],
)
print(f"{operation_info=}")
assert operation_info.status == UpdateStatus.COMPLETED
sep()


search_result = client.search(collection_name="test_collection", query_vector=[0.2, 0.1, 0.9, 0.7], limit=3)
print(f"{search_result=}")
sep(2)
assert len(search_result) == 3
print(f"{search_result[0]=}")
# ScoredPoint(id=4, score=1.362, ...)
print(f"{search_result[1]=}")
# ScoredPoint(id=1, score=1.273, ...)
print(f"{search_result[2]=}")
# ScoredPoint(id=3, score=1.208, ...)
sep()


filtered_search_result = client.search(
    collection_name="test_collection",
    query_vector=[0.2, 0.1, 0.9, 0.7],
    query_filter=Filter(must=[FieldCondition(key="city", match=MatchValue(value="London"))]),
    limit=3,
)
assert len(filtered_search_result) == 2
print(f"{filtered_search_result=}")
sep(2)
print(f"{filtered_search_result[0]=}")
# ScoredPoint(id=4, score=1.362, ...)
print(f"{filtered_search_result[1]=}")
# ScoredPoint(id=2, score=0.871, ...)
sep()

```


## Contributing

<details>
<summary>Prerequisites</summary>

<details>
<summary>1. Set up Git to use SSH</summary>

1. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) and [add the SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
1. Configure SSH to automatically load your SSH keys:
    ```sh
    cat << EOF >> ~/.ssh/config
    Host *
      AddKeysToAgent yes
      IgnoreUnknown UseKeychain
      UseKeychain yes
    EOF
    ```

</details>

<details>
<summary>2. Install Docker</summary>

1. [Install Docker Desktop](https://www.docker.com/get-started).
    - Enable _Use Docker Compose V2_ in Docker Desktop's preferences window.
    - _Linux only_:
        - [Configure Docker to use the BuildKit build system](https://docs.docker.com/build/buildkit/#getting-started). On macOS and Windows, BuildKit is enabled by default in Docker Desktop.
        - Export your user's user id and group id so that [files created in the Dev Container are owned by your user](https://github.com/moby/moby/issues/3206):
            ```sh
            cat << EOF >> ~/.bashrc
            export UID=$(id --user)
            export GID=$(id --group)
            EOF
            ```

</details>

<details>
<summary>3. Install VS Code or PyCharm</summary>

1. [Install VS Code](https://code.visualstudio.com/) and [VS Code's Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). Alternatively, install [PyCharm](https://www.jetbrains.com/pycharm/download/).
2. _Optional:_ install a [Nerd Font](https://www.nerdfonts.com/font-downloads) such as [FiraCode Nerd Font](https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/FiraCode) and [configure VS Code](https://github.com/tonsky/FiraCode/wiki/VS-Code-Instructions) or [configure PyCharm](https://github.com/tonsky/FiraCode/wiki/Intellij-products-instructions) to use it.

</details>

</details>

<details open>
<summary>Development environments</summary>

The following development environments are supported:

1. ⭐️ _GitHub Codespaces_: click on _Code_ and select _Create codespace_ to start a Dev Container with [GitHub Codespaces](https://github.com/features/codespaces).
1. ⭐️ _Dev Container (with container volume)_: click on [Open in Dev Containers](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/malcolmgreaves/vectordb) to clone this repository in a container volume and create a Dev Container with VS Code.
1. _Dev Container_: clone this repository, open it with VS Code, and run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Dev Containers: Reopen in Container_.
1. _PyCharm_: clone this repository, open it with PyCharm, and [configure Docker Compose as a remote interpreter](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#docker-compose-remote) with the `dev` service.
1. _Terminal_: clone this repository, open it with your terminal, and run `docker compose up --detach dev` to start a Dev Container in the background, and then run `docker compose exec dev zsh` to open a shell prompt in the Dev Container.

</details>

<details>
<summary>Developing</summary>

- Run `poe` from within the development environment to print a list of [Poe the Poet](https://github.com/nat-n/poethepoet) tasks available to run on this project.
- Run `poetry add {package}` from within the development environment to install a run time dependency and add it to `pyproject.toml` and `poetry.lock`. Add `--group test` or `--group dev` to install a CI or development dependency, respectively.
- Run `poetry update` from within the development environment to upgrade all dependencies to the latest versions allowed by `pyproject.toml`.

</details>
