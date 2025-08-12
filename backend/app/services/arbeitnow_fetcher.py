import requests
from typing import Dict, Any, List, Optional

BASE_URL = "https://www.arbeitnow.com/api/job-board-api"

def fetch_arbeitnow_jobs(
    page_url: Optional[str] = None,
    remote: Optional[bool] = None,
    visa_sponsorship: Optional[bool] = None,
    query: Optional[str] = None,
    limit_pages: int = 1,
    timeout: int = 20,
) -> List[Dict[str, Any]]:
    """
    Fetch jobs from Arbeitnow API with optional filters and follow pagination up to limit_pages.
    If page_url is given, it takes precedence; otherwise builds from BASE_URL with query params.
    Returns a flat list of jobs.
    """
    jobs: List[Dict[str, Any]] = []
    pages_fetched = 0
    url = page_url or BASE_URL

    # Build querystring on first call if no page_url provided
    params = {}
    if page_url is None:
        if remote is not None:
            params["remote"] = str(remote).lower()
        if visa_sponsorship is not None:
            params["visa_sponsorship"] = str(visa_sponsorship).lower()
        if query:
            params["search"] = query  # documented on the API blog; use to narrow results

    while pages_fetched < limit_pages and url:
        resp = requests.get(url, params=params if pages_fetched == 0 and page_url is None else None, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Expected structure: {"data": [...], "links": {"next": "...", "prev": "..."}, "meta": {...}}
        page_jobs = data.get("data", [])
        for j in page_jobs:
            # Normalize minimal fields for downstream
            jobs.append({
                "source": "arbeitnow",
                "title": j.get("title", ""),
                "company": j.get("company_name", ""),
                "location": j.get("location", ""),
                "salary": "",  # API may not include salary
                "url": j.get("url", ""),
                "description": j.get("description", "") or "",
                "tags": j.get("tags", []),
                "remote": j.get("remote", False),
                "created_at": j.get("created_at", ""),
                "visa_sponsorship": j.get("visa_sponsorship", False),
            })
        # Advance pagination
        links = data.get("links", {})
        url = links.get("next")
        pages_fetched += 1

    return jobs
