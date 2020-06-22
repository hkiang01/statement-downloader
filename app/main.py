import os

import fire

from schwab import Schwab

DEFAULT_DIR = os.path.join(os.getcwd(), "statements")


def download_statements(download_dir: str):
    """Downloads Schwab statements

    Parameters
    ----------
    download_dir : str, optional
        Where to download them,
        by default ./schwab
    """
    os.makedirs(download_dir, exist_ok=True)
    schwab = Schwab(download_dir=download_dir)
    schwab.login()
    schwab.download_statements()


if __name__ == "__main__":
    fire.Fire()
