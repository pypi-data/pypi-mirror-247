import typing
import requests
from hashlib import md5, sha256

_base_github_raw_path = "https://raw.githubusercontent.com/{user_or_org}/{name}/{branch}/{path}"

def download_github_repo_file(
    user_or_org: str,
    name: str,
    branch: str = "master",
    path: str = None,
    checksum: str = None,
    checksum_format: typing.Literal["md5", "sha256"] = "md5",
    toFile: typing.Optional[str] = None
) -> bytes:
    """
    Download a file from a GitHub repository.

    Args:
        user_or_org (str): The username or organization name.
        name (str): The name of the repository.
        branch (str, optional): The branch name. Defaults to "master".
        path (str, optional): The path to the file. Defaults to None.
        checksum (str, optional): The expected checksum value. Defaults to None.
        checksum_format (typing.Literal["md5", "sha256"], optional): The format of the checksum. Defaults to "md5".
        toFile (typing.Optional[str], optional): The path to save the downloaded file. Defaults to None.

    Returns:
        bytes: The content of the downloaded file.
    """
    if path is None:
        raise ValueError("path cannot be None")

    url = _base_github_raw_path.format(
        user_or_org=user_or_org,
        name=name,
        branch=branch,
        path=path
    )

    req = requests.get(url)
    content = req.content

    if checksum is not None:
        if checksum_format == "md5":
            content_checksum = md5(content).hexdigest()
        elif checksum_format == "sha256":
            content_checksum = sha256(content).hexdigest()
        else:
            raise ValueError(f"Unsupported checksum format: {checksum_format}")

        if checksum != content_checksum:
            raise ValueError(f"Checksum mismatch: {checksum} != {content_checksum}")

    if toFile is not None:
        with open(toFile, 'wb') as f:
            f.write(content)

    return content
