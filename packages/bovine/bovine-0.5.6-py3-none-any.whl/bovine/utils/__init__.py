from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple

from bs4 import BeautifulSoup


GMT_STRING = "%a, %d %b %Y %H:%M:%S GMT"


@dataclass
class JrdLink:
    """Dataclass representing a JRD link

    See [RFC 7033](https://www.rfc-editor.org/rfc/rfc7033.html).

    :param rel: e.g. "self"
    :param href: the url
    :param type: e.g. "application/activity+json"
    """

    rel: str | None = None
    href: str | None = None
    type: str | None = None

    def build(self) -> dict:
        """Transforms the JrdLink into a dict"""
        return {key: value for key, value in asdict(self).items() if value}


@dataclass
class JrdData:
    """Dataclass representing a JRD Object

    See [RFC 7033](https://www.rfc-editor.org/rfc/rfc7033.html).

    :param subject: Subject of the JrdData
    :param links: List of links
    """

    subject: str | None = None
    links: list[JrdLink] = field(default_factory=list)

    def build(self) -> dict:
        """Transforms JrdData to dict

        :return: Appropriate document"""
        result = {}
        if self.subject:
            result["subject"] = self.subject

        if len(self.links) > 0:
            result["links"] = [x.build() for x in self.links]

        return result


def webfinger_response_json(account: str, url: str) -> dict:
    """helper to generate a webfinger response"""
    return JrdData(
        subject=account,
        links=[JrdLink(href=url, rel="self", type="application/activity+json")],
    ).build()


def parse_fediverse_handle(account: str) -> Tuple[str, Optional[str]]:
    """Splits fediverse handle in name and domain Supported forms are:

    * user@domain -> (user, domain)
    * @user@domain -> (user, domain)
    * acct:user@domain -> (user, domain)
    """
    if account[0] == "@":
        account = account[1:]
    account = account.removeprefix("acct:")

    if "@" in account:
        user, domain = account.split("@", 1)
        return user, domain
    return account, None


def now_isoformat() -> str:
    """Returns now in Isoformat, e.g. "2023-05-31T18:11:35Z", to be used as the value
    of published"""
    return (
        datetime.now(tz=timezone.utc).replace(microsecond=0, tzinfo=None).isoformat()
        + "Z"
    )


def activity_pub_object_id_from_html_body(body: str) -> str | None:
    """Determines the object identifier from the html body
    by parsing it and looking for link tags with rel="alternate"
    and type application/activity+json"""

    soup = BeautifulSoup(body, features="lxml")
    element = soup.find(
        "link", attrs={"rel": "alternate", "type": "application/activity+json"}
    )
    if not element:
        return None

    return element.attrs.get("href")


def get_gmt_now() -> str:
    """Returns the current time in UTC as a GMT formatted string as used
    in the HTTP Date header"""
    return datetime.now(tz=timezone.utc).strftime(GMT_STRING)


def parse_gmt(date_string: str) -> datetime:
    """Parses a GMT formatted string as used in HTTP Date header"""
    return datetime.strptime(date_string, GMT_STRING).replace(tzinfo=timezone.utc)


def check_max_offset_now(dt: datetime, minutes: int = 5) -> bool:
    """Checks that offset of a datetime to now to be less than minutes"""

    now = datetime.now(tz=timezone.utc)

    if dt > now + timedelta(minutes=minutes):
        return False

    if dt < now - timedelta(minutes=minutes):
        return False

    return True
