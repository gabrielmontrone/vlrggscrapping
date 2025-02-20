from fastapi import APIRouter, Query, Request # type: ignore
from slowapi import Limiter # type: ignore
from slowapi.util import get_remote_address # type: ignore

from api.scrape import Vlr

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
vlr = Vlr()


@router.get("/news")
@limiter.limit("250/minute")
async def VLR_news(request: Request):
    return vlr.vlr_news()


@router.get("/stats")
@limiter.limit("250/minute")
async def VLR_stats(
    request: Request,
    region: str = Query(..., description="Region shortname"),
    timespan: str = Query(..., description="Timespan (30, 60, 90, or all)"),
):
    """
    Get VLR stats with query parameters.

    region shortnames:\n
        "na": "north-america",\n
        "eu": "europe",\n
        "ap": "asia-pacific",\n
        "sa": "latin-america",\n
        "jp": "japan",\n
        "oce": "oceania",\n
        "mn": "mena"\n
    """
    return vlr.vlr_stats(region, timespan)


@router.get("/rankings")
@limiter.limit("250/minute")
async def VLR_ranks(
    request: Request, region: str = Query(..., description="Region shortname")
):
    """
    Get VLR rankings for a specific region.

    region shortnames:\n
        "na": "north-america",\n
        "eu": "europe",\n
        "ap": "asia-pacific",\n
        "la": "latin-america",\n
        "la-s": "la-s",\n
        "la-n": "la-n",\n
        "oce": "oceania",\n
        "kr": "korea",\n
        "mn": "mena",\n
        "gc": "game-changers",\n
        "br": "Brazil",\n
        "cn": "china",\n
        "jp": "japan",\n
        "col": "collegiate",\n
    """
    return vlr.vlr_rankings(region)


@router.get("/match")
@limiter.limit("250/minute")
async def VLR_match(request: Request, q: str):
    """
    query parameters:\n
        "upcoming": upcoming matches,\n
        "live_score": live match scores,\n
        "results": match results,\n
    """
    if q == "upcoming":
        return vlr.vlr_upcoming_matches()
    elif q == "live_score":
        return vlr.vlr_live_score()
    elif q == "results":
        return vlr.vlr_match_results()
    else:
        return {"error": "Invalid query parameter"}

@router.get("/events")
@limiter.limit("250/minute")
async def VLR_events(request: Request):
    return vlr.vlr_events()

@router.get("/matchdetails")
@limiter.limit("250/minute")
async def VLR_check_match_urls(request: Request):
    return vlr.vlr_check_match_urls()

@router.get("/tournament-overview")
@limiter.limit("250/minute")
async def VLR_tournament_overview(request: Request):
    return vlr.vlr_tournament_overview()

@router.get("/players-details")
@limiter.limit("250/minute")
async def VLR_players_details(request: Request, profile_url: str = None):
    if profile_url is None:
        return {"error": "profile_url is required"}
    if not profile_url.startswith("http"):
        return {"error": "Invalid profile_url. It must start with 'http'."}
    return vlr.vlr_players_details(profile_url)


@router.get("/health")
def health():
    return vlr.check_health()
