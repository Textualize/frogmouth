"""Code for getting files from a forge."""

from __future__ import annotations

from httpx import URL, AsyncClient, HTTPStatusError

from .advertising import USER_AGENT


async def build_raw_forge_url(
    url_format: str,
    owner: str,
    repository: str,
    branch: str | None = None,
    desired_file: str | None = None,
) -> URL | None:
    """Attempt to get raw forge URL for the given file.

    Args:
        owner: The owner of the repository to look in.
        repository: The repository to look in.
        branch: The optional branch to look in.
        desired_file: Optional name of the file to go looking for.

    Returns:
        The URL for the file, or `None` if none could be guessed.

    If the branch isn't supplied then `main` and `master` will be tested.

    If the target file isn't supplied it's assumed that `README.md` is the
    target.
    """
    desired_file = desired_file or "README.md"
    async with AsyncClient() as client:
        for test_branch in (branch,) if branch else ("main", "master"):
            url = url_format.format(
                owner=owner,
                repository=repository,
                branch=test_branch,
                file=desired_file,
            )
            response = await client.head(
                url,
                follow_redirects=True,
                headers={"user-agent": USER_AGENT},
            )
            try:
                response.raise_for_status()
                return URL(url)
            except HTTPStatusError:
                pass
    return None


async def build_raw_github_url(
    owner: str,
    repository: str,
    branch: str | None = None,
    desired_file: str | None = None,
) -> URL | None:
    """Attempt to get the GitHub raw URL for the given file.

    Args:
        owner: The owner of the repository to look in.
        repository: The repository to look in.
        branch: The optional branch to look in.
        desired_file: Optional name of the file to go looking for.

    Returns:
        The URL for the file, or `None` if none could be guessed.

    If the branch isn't supplied then `main` and `master` will be tested.

    If the target file isn't supplied it's assumed that `README.md` is the
    target.
    """
    return await build_raw_forge_url(
        "https://raw.githubusercontent.com/{owner}/{repository}/{branch}/{file}",
        owner,
        repository,
        branch,
        desired_file,
    )


async def build_raw_gitlab_url(
    owner: str,
    repository: str,
    branch: str | None = None,
    desired_file: str | None = None,
) -> URL | None:
    """Attempt to get the GitLab raw URL for the given file.

    Args:
        owner: The owner of the repository to look in.
        repository: The repository to look in.
        branch: The optional branch to look in.
        desired_file: Optional name of the file to go looking for.

    Returns:
        The URL for the file, or `None` if none could be guessed.

    If the branch isn't supplied then `main` and `master` will be tested.

    If the target file isn't supplied it's assumed that `README.md` is the
    target.
    """
    return await build_raw_forge_url(
        "https://gitlab.com/{owner}/{repository}/-/raw/{branch}/{file}",
        owner,
        repository,
        branch,
        desired_file,
    )


async def build_raw_bitbucket_url(
    owner: str,
    repository: str,
    branch: str | None = None,
    desired_file: str | None = None,
) -> URL | None:
    """Attempt to get the BitBucket raw URL for the given file.

    Args:
        owner: The owner of the repository to look in.
        repository: The repository to look in.
        branch: The optional branch to look in.
        desired_file: Optional name of the file to go looking for.

    Returns:
        The URL for the file, or `None` if none could be guessed.

    If the branch isn't supplied then `main` and `master` will be tested.

    If the target file isn't supplied it's assumed that `README.md` is the
    target.
    """
    return await build_raw_forge_url(
        "https://bitbucket.org/{owner}/{repository}/raw/{branch}/{file}",
        owner,
        repository,
        branch,
        desired_file,
    )


async def build_raw_codeberg_url(
    owner: str,
    repository: str,
    branch: str | None = None,
    desired_file: str | None = None,
) -> URL | None:
    """Attempt to get the Codeberg raw URL for the given file.

    Args:
        owner: The owner of the repository to look in.
        repository: The repository to look in.
        branch: The optional branch to look in.
        desired_file: Optional name of the file to go looking for.

    Returns:
        The URL for the file, or `None` if none could be guessed.

    If the branch isn't supplied then `main` and `master` will be tested.

    If the target file isn't supplied it's assumed that `README.md` is the
    target.
    """
    return await build_raw_forge_url(
        "https://codeberg.org/{owner}/{repository}/raw//branch/{branch}/{file}",
        owner,
        repository,
        branch,
        desired_file,
    )
