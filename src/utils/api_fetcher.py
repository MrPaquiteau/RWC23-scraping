import os
import re
import time
from datetime import datetime

import requests
from tqdm import tqdm

from src.utils.models import Team, Player, Match
from src.utils.images_builder import (
    build_flag_url,
    build_shape_url,
    build_logo_url,
    is_url_valid,
    build_phto_url,
)


class RugbyDataFetcher:
    """
    A class to fetch data from the Rugby World Cup 'API'.

    Robustness notes:
    - PulseLive migrated event ids from numeric (``1893``) to UUIDs, which
      caused months of ``400 InvalidParameter: 'eventUuid'`` failures. The
      UUID is now resolved dynamically (with a hardcoded fallback) instead
      of being frozen in every URL.
    - All HTTP goes through :meth:`_get` (browser-like headers, timeout,
      exponential-backoff retry on 429/5xx/network errors, useful error
      body in logs).
    - All JSON parsing is defensive (``.get`` + per-item try/except) so one
      malformed team/player/match no longer kills the whole monthly job.
    """

    BASE_URL = "https://api.wr-rims-prod.pulselive.com/rugby/v3/"

    # Numeric id 1893 no longer accepted by the API (400: 'eventUuid' has an
    # invalid value). Resolved via GET /rugby/v3/event:
    # id 1893 = Rugby World Cup 2023 = altId below.
    EVENT_ID = "1893"
    EVENT_UUID_FALLBACK = "f14aca9d-f746-431d-8e5e-9db6c311ec69"
    # Backwards-compat alias (old code used RugbyDataFetcher.EVENT_UUID).
    EVENT_UUID = EVENT_UUID_FALLBACK

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Origin": "https://www.rugbyworldcup.com",
        "Referer": "https://www.rugbyworldcup.com/",
    }

    RETRYABLE_STATUS = {429, 500, 502, 503, 504}
    TIMEOUT = 20
    MAX_RETRIES = 4

    _event_uuid_cache = None

    # ------------------------------------------------------------------
    # Event UUID resolution
    # ------------------------------------------------------------------
    @classmethod
    def resolve_event_uuid(cls):
        """Return the event UUID, discovering it via the API if needed."""
        if cls._event_uuid_cache:
            return cls._event_uuid_cache

        # Manual override for CI/debug without code change.
        env_uuid = os.getenv("RWC_EVENT_UUID")
        if env_uuid:
            cls._event_uuid_cache = env_uuid
            return env_uuid

        discovered = cls._discover_event_uuid()
        cls._event_uuid_cache = discovered or cls.EVENT_UUID_FALLBACK
        return cls._event_uuid_cache

    @classmethod
    def _discover_event_uuid(cls):
        """Look up altId for numeric EVENT_ID via GET /event (paginated)."""
        try:
            page = 0
            while page < 30:  # 30 * 100 > 2369 entries, safe upper bound
                resp = requests.get(
                    f"{cls.BASE_URL}event",
                    params={"pageSize": 100, "page": page},
                    headers=cls.HEADERS,
                    timeout=cls.TIMEOUT,
                )
                resp.raise_for_status()
                content = resp.json().get("content", [])
                if not content:
                    break
                for entry in content:
                    if str(entry.get("id")) == str(cls.EVENT_ID) and entry.get("altId"):
                        return entry["altId"]
                page += 1
        except Exception as e:
            print(f"Could not auto-discover event UUID, using fallback: {e}")
        return None

    # ------------------------------------------------------------------
    # HTTP helper
    # ------------------------------------------------------------------
    @classmethod
    def _get(cls, url, params=None, max_retries=None):
        """GET with timeout, headers, retry + useful error body on failure."""
        max_retries = max_retries if max_retries is not None else cls.MAX_RETRIES
        last_exc = None
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(
                    url, params=params, headers=cls.HEADERS, timeout=cls.TIMEOUT
                )
                if response.status_code in cls.RETRYABLE_STATUS and attempt < max_retries:
                    print(
                        f"Retryable {response.status_code} ({attempt}/{max_retries}): {url}"
                    )
                    time.sleep(2 ** (attempt - 1))
                    continue
                try:
                    response.raise_for_status()
                except requests.HTTPError:
                    body = (response.text or "")[:500]
                    print(f"API request failed: {response.status_code} {url} -> {body}")
                    # If the hardcoded UUID ever rots again, re-discover once.
                    if response.status_code == 400 and "eventUuid" in body:
                        cls._event_uuid_cache = None
                    raise
                return response
            except (requests.Timeout, requests.ConnectionError) as e:
                last_exc = e
                print(f"Network error ({attempt}/{max_retries}) {url}: {e}")
                if attempt < max_retries:
                    time.sleep(2 ** (attempt - 1))
            except requests.HTTPError:
                raise
        if last_exc:
            raise last_exc
        raise requests.HTTPError(f"GET failed after {max_retries} retries: {url}")

    # ------------------------------------------------------------------
    # Stats normalization (single place, .get-based, never KeyErrors)
    # ------------------------------------------------------------------
    @staticmethod
    def _num(value, default=0):
        try:
            if value is None:
                return default
            return value
        except Exception:
            return default

    @classmethod
    def build_player_stats(cls, stats):
        """Normalize raw stats payload into the 12-field dict used by the site."""
        if not isinstance(stats, dict):
            stats = {}
        ext = stats.get("extendedStats") or {}
        base = stats.get("stats") or {}

        tackles = cls._num(ext.get("Tackles"), 0)
        try:
            tackles_int = int(float(tackles))
        except (TypeError, ValueError):
            tackles_int = 0
        success = ext.get("TackleSuccess")
        try:
            success_pct = float(success) * 100 if success is not None else 0
        except (TypeError, ValueError):
            success_pct = 0

        return {
            "Kick from hand": cls._num(ext.get("KicksFromHand"), 0),
            "Runs": cls._num(ext.get("Runs"), 0),
            "Passes": cls._num(ext.get("Passes"), 0),
            "Offload": cls._num(ext.get("Offload"), 0),
            "Tackles": f"{tackles_int} ({success_pct:.0f}%)",
            "Carries": cls._num(ext.get("Carries"), 0),
            "Metres made": cls._num(ext.get("Metres"), 0),
            "Defenders beaten": cls._num(ext.get("DefendersBeaten"), 0),
            "Clean breaks": cls._num(ext.get("CleanBreaks"), 0),
            "Handling error": cls._num(ext.get("HandlingError"), 0),
            "Red cards": cls._num(base.get("RedCards"), 0),
            "Yellow cards": cls._num(base.get("YellowCards"), 0),
        }

    # ------------------------------------------------------------------
    # Fetchers
    # ------------------------------------------------------------------
    @classmethod
    def fetch_teams(cls):
        """
        Fetches the list of teams participating in the 2023 World Cup.

        Returns:
            list: A list of Team objects.
        """
        event_uuid = cls.resolve_event_uuid()
        url = f"{cls.BASE_URL}event/{event_uuid}/teams"
        response = cls._get(url)

        teams = (response.json() or {}).get("teams", [])
        for team_data in tqdm(teams, desc="Fetching teams"):
            try:
                name = team_data.get("name")
                abbr = team_data.get("abbreviation")
                if not name or not abbr:
                    print(f"Skipping malformed team entry: {team_data}")
                    continue
                logo = build_logo_url(name)
                flag = build_flag_url(abbr)
                shape = build_shape_url(name)
                logo_light = logo[0] if is_url_valid(logo[0]) else logo[1]
                logo_dark = logo[1] if is_url_valid(logo[1]) else logo[0]

                Team(
                    id=team_data.get("id"),
                    country=name,
                    code=abbr,
                    images={'flag': flag,
                            'shape': shape,
                            'logo': {'light': logo_light,
                                     'dark': logo_dark}
                    }
                )
            except Exception as e:
                print(f"Skipping team after error {team_data.get('name')}: {e}")
        return Team.get_teams()

    @classmethod
    def fetch_team_squad(cls, team):
        """
        Fetches the list of players for a team.

        Args:
            team: The Team object (uses ``team.id``).

        Returns:
            list: A list of Player objects (possibly empty, never None).
        """
        team_id = getattr(team, "id", None)
        if team_id is None:
            print("fetch_team_squad: team has no id, skipping")
            return []
        event_uuid = cls.resolve_event_uuid()
        url = f"{cls.BASE_URL}event/{event_uuid}/squad/{team_id}"
        try:
            response = cls._get(url)
        except requests.HTTPError as e:
            print(f"Error fetching squad for team {team_id}: {e}")
            return []
        players = []
        for player_data in (response.json() or {}).get("players", []):
            try:
                p = player_data.get("player", {}) if isinstance(player_data, dict) else {}
                pid = p.get("id")
                if pid is None:
                    continue
                name = (p.get("name") or {}).get("display", "Unknown")
                age = (p.get("age") or {}).get("years")
                players.append(
                    Player(
                        id=pid,
                        name=name,
                        age=age,
                        height=p.get("height"),
                        weight=p.get("weight"),
                        hometown=p.get("pob"),
                        photo=build_phto_url(pid),
                    )
                )
            except Exception as e:
                print(f"Skipping malformed player entry: {e}")
        return players

    @classmethod
    def fetch_player_stats(cls, player_id):
        """
        Fetches statistics for a player.

        Args:
            player_id: The ID of the player.

        Returns:
            dict: Raw payload; ``{}``-shaped ``{"extendedStats": {}, "stats": {}}``
            on 404 so callers can still render default stats.
        """
        event_uuid = cls.resolve_event_uuid()
        url = f"{cls.BASE_URL}stats/player/{player_id}/EVENT?event={event_uuid}"
        try:
            response = cls._get(url)
        except requests.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            print(f"Error fetching stats for player {player_id}: {e}")
            if status == 404:
                return {"extendedStats": {}, "stats": {}}
            raise
        data = response.json()
        return data if isinstance(data, dict) else {}

    @classmethod
    def fetch_matches(cls):
        """
        Fetches the list of matches of the 2023 World Cup.

        Returns:
            list: A list of Match objects.
        """
        event_uuid = cls.resolve_event_uuid()
        url = f"{cls.BASE_URL}event/{event_uuid}/schedule?language=en"
        response = cls._get(url)

        for match_data in tqdm((response.json() or {}).get("matches", []), desc="Fetching matches"):
            try:
                label = (match_data.get("time") or {}).get("label", "")
                try:
                    numeric_date = datetime.strptime(label, '%Y-%m-%d')
                    date = numeric_date.strftime("%d %B %Y")
                except (ValueError, TypeError):
                    date = label or "Unknown date"
                venue = match_data.get("venue") or {}
                location = f'{venue.get("name", "?")}, {venue.get("city", "?")}'
                teams = match_data.get("teams") or []
                if len(teams) < 2:
                    print(f"Skipping match {match_data.get('matchId')}: not enough teams")
                    continue
                home_team = teams[0].get("name", "?")
                away_team = teams[1].get("name", "?")
                scores = match_data.get("scores") or [None, None]
                home_score = scores[0] if len(scores) > 0 else None
                away_score = scores[1] if len(scores) > 1 else None
                stage = re.sub(r'\d', '', match_data.get("eventPhase", "")).strip().title()

                Match(
                    id=match_data.get("matchId"),
                    date=date,
                    stage=stage,
                    home={'team': home_team, 'score': home_score},
                    away={'team': away_team, 'score': away_score},
                    location=location
                )
            except Exception as e:
                print(f"Skipping malformed match {match_data.get('matchId')}: {e}")
        return Match.get_matches()
