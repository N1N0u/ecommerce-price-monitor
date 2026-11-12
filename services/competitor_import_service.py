from urllib.parse import urlsplit, urlunsplit

from database.models import Competitor


class CompetitorImportService:

    def __init__(self, db):
        self.db = db

    def normalize_url(self, url):
        """
        Validate and normalize a competitor website URL.
        """

        url = url.strip()

        if not url:
            raise ValueError("Empty URL")

        if "://" not in url:
            url = "https://" + url

        parsed = urlsplit(url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError("Only HTTP and HTTPS URLs are supported")

        if not parsed.hostname:
            raise ValueError("Invalid website URL")

        if parsed.username or parsed.password:
            raise ValueError("URLs containing credentials are not allowed")

        # Keep the website's hostname and port.
        # Remove paths, query strings and fragments.
        normalized_url = urlunsplit((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            "",
            "",
            ""
        ))

        return normalized_url.rstrip("/")

    def get_competitor_name(self, url):
        """
        Generate a competitor name from its domain.
        """

        hostname = urlsplit(url).hostname

        name = hostname.removeprefix("www.")
        name = name.split(".")[0]

        return name.replace("-", " ").title()

    def import_from_text(self, content):
        """
        Import competitor websites from TXT content.
        One website URL per line.
        """

        results = {
            "imported": [],
            "duplicates": [],
            "invalid": []
        }

        seen_urls = set()

        lines = content.splitlines()

        for line_number, line in enumerate(lines, start=1):

            line = line.strip()

            # Ignore blank lines and comments.
            if not line or line.startswith("#"):
                continue

            try:
                url = self.normalize_url(line)

                # Avoid duplicates inside the uploaded file.
                if url in seen_urls:
                    results["duplicates"].append(url)
                    continue

                seen_urls.add(url)

                # Check whether the competitor already exists.
                existing = (
                    self.db.query(Competitor)
                    .filter(Competitor.website_url == url)
                    .first()
                )

                if existing:
                    results["duplicates"].append(url)
                    continue

                competitor = Competitor(
                    name=self.get_competitor_name(url),
                    website_url=url
                )

                self.db.add(competitor)

                results["imported"].append({
                    "name": competitor.name,
                    "website_url": url
                })

            except Exception as error:
                results["invalid"].append({
                    "line": line_number,
                    "value": line,
                    "error": str(error)
                })

        try:
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return results