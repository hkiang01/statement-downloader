from .schwab import Schwab


def main(download_dir: str = "./schwab"):
    """Downloads Schwab statements

    Parameters
    ----------
    download_dir : str, optional
        Where to download them,
        by default ./schwab
    """
    schwab = Schwab(download_dir=download_dir)
    schwab.login()
    schwab.download_statements()
