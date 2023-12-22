
import typing
import py7zr
import os
import numpy as np

def crack_password(
    path: str,
    possibilities: typing.Union[typing.Generator, typing.List],
    excluded_list_path: str = None
) -> str:
    """
    Crack a password using a list of potential passwords.

    Parameters
    ----------
    path : str
        Path to the file containing the password to crack.
    possibilities : Iterator[str]
        Iterator over potential passwords.
    excluded_list_path : str, optional
        Path to a file containing a list of passwords to exclude from the
        potential passwords, by default None.

    Returns
    -------
    str
        The cracked password.
    """
    if excluded_list_path is not None:
        if not os.path.exists(excluded_list_path):
            open(excluded_list_path, "w").close()

        with open(excluded_list_path, "r") as f:
            tried = np.array(f.read().splitlines(), dtype=str)

    for password in possibilities:
        print(f"trying {password}", end="")
        if excluded_list_path and password in tried:
            print(" (already tried)")
            continue
        else:
            print()

        try:
            with py7zr.SevenZipFile(path, mode="r", password=password) as archive:
                archive.files
                return password
        except py7zr.Bad7zFile:
            if excluded_list_path is None:
                continue
            tried = np.append(tried, password)
            with open(excluded_list_path, "a") as f:
                f.write(password + "\n")

            continue
        except Exception as e:
            if "_lzma.LZMAError" not in str(type(e)):
                raise e
            if excluded_list_path is None:
                continue
            tried = np.append(tried, password)
            with open(excluded_list_path, "a") as f:
                f.write(password + "\n")

            continue

    if excluded_list_path is not None:
        with open(excluded_list_path, "w") as f:
            f.write("\n".join(tried))

    return None
    