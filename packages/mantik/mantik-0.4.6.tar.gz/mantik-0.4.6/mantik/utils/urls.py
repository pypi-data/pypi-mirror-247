import re
import urllib.parse


def remove_double_slashes_from_path(url: str, ensure_https: bool = True) -> str:
    """Ensure that a URL uses HTTPS and does not contain `//` in its path."""
    u = urllib.parse.urlparse(url)
    path = u.path.replace("//", "/")
    url = f"{u.netloc}{path}".replace("//", "/")
    if ensure_https:
        return f"https://{url}"
    return f"{u.scheme}://{url}"


def replace_first_subdomain(url: str, replace_with: str) -> str:
    regex = re.compile(r"^https?:\/\/(www\.)?(.*?)(\..*)$")
    return regex.sub(rf"https://\1{replace_with}\3", url)
