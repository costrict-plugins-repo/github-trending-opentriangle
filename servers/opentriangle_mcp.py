"""OpenTriangle MCP Server — search businesses, check availability, and book appointments."""

import os
import json
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

API_URL = os.environ.get("OPENTRIANGLE_API_URL", "https://api.opentriangle.ai")
API_TOKEN = os.environ.get("OPENTRIANGLE_API_TOKEN", "")

mcp = FastMCP("opentriangle")


def _headers(auth: bool = False) -> dict:
    """Build request headers, optionally with auth token."""
    headers = {"Content-Type": "application/json"}
    if auth and API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    return headers


async def _get(path: str, params: Optional[dict] = None, auth: bool = False) -> dict | list:
    """Make a GET request to the OpenTriangle API."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{API_URL}{path}", params=params, headers=_headers(auth))
        resp.raise_for_status()
        return resp.json()


async def _post(path: str, data: Optional[dict] = None, auth: bool = True) -> dict:
    """Make a POST request to the OpenTriangle API."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{API_URL}{path}", json=data, headers=_headers(auth))
        resp.raise_for_status()
        return resp.json()


# --- Public tools (no auth required) ---


@mcp.tool()
async def search_businesses(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_miles: Optional[float] = 25,
    limit: Optional[int] = 20,
) -> str:
    """Search for businesses on OpenTriangle by name, category, city, zip code, or coordinates.

    Returns businesses with ratings, available slot counts, and distance from search location.
    """
    params = {}
    if search:
        params["search"] = search
    if category_id:
        params["category_id"] = category_id
    if city:
        params["city"] = city
    if state:
        params["state"] = state
    if zip_code:
        params["zip_code"] = zip_code
    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude
    if radius_miles:
        params["radius_miles"] = radius_miles
    if limit:
        params["limit"] = limit

    results = await _get("/api/businesses/", params=params)
    if not results:
        return "No businesses found matching your search."
    return json.dumps(results, indent=2)


@mcp.tool()
async def list_categories(search: Optional[str] = None) -> str:
    """List all service categories available on OpenTriangle (e.g., Hair Salons, Dentists, Spas)."""
    params = {}
    if search:
        params["search"] = search
    results = await _get("/api/categories/", params=params)
    return json.dumps(results, indent=2)


@mcp.tool()
async def get_business(business_id: int) -> str:
    """Get full details for a specific business including description, address, hours, and contact info."""
    result = await _get(f"/api/businesses/{business_id}")
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_providers(business_id: int) -> str:
    """List all service providers (stylists, doctors, technicians, etc.) at a business."""
    results = await _get(f"/api/providers/business/{business_id}")
    return json.dumps(results, indent=2)


@mcp.tool()
async def get_available_slots(
    business_id: int,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> str:
    """Get available appointment time slots for a business.

    Args:
        business_id: The business ID to check availability for.
        from_date: Filter slots from this date (ISO 8601 format, e.g. 2026-03-10T00:00:00).
        to_date: Filter slots until this date (ISO 8601 format).
    """
    params = {"status": "AVAILABLE"}
    if from_date:
        params["from_date"] = from_date
    if to_date:
        params["to_date"] = to_date

    results = await _get(f"/api/slots/business/{business_id}", params=params)
    if not results:
        return "No available slots found for this business."
    return json.dumps(results, indent=2)


@mcp.tool()
async def get_reviews(business_id: int) -> str:
    """Get customer reviews for a business."""
    results = await _get(f"/api/reviews/business/{business_id}")
    if not results:
        return "No reviews yet for this business."
    return json.dumps(results, indent=2)


# --- Authenticated tools (require API token) ---


@mcp.tool()
async def book_appointment(slot_id: int, party_size: int = 1) -> str:
    """Book an available time slot on OpenTriangle.

    Requires an API token (set OPENTRIANGLE_API_TOKEN env var).
    Generate a token in the OpenTriangle app: Profile > API Tokens > Create (type: customer_bookings).

    Args:
        slot_id: The ID of the available time slot to book.
        party_size: Number of people for the appointment (default 1).
    """
    if not API_TOKEN:
        return "Error: OPENTRIANGLE_API_TOKEN environment variable is not set. Generate a token in the OpenTriangle app: Profile > API Tokens > Create (type: customer_bookings)."

    try:
        result = await _post("/api/appointments/", data={"slot_id": slot_id, "party_size": party_size})
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return f"Error: Slot is not available. {e.response.text}"
        elif e.response.status_code == 401:
            return "Error: Invalid or expired API token. Generate a new one in the OpenTriangle app."
        raise


@mcp.tool()
async def my_appointments(
    status: Optional[str] = None,
    upcoming_only: bool = True,
) -> str:
    """Get your appointments on OpenTriangle.

    Requires an API token (set OPENTRIANGLE_API_TOKEN env var).

    Args:
        status: Filter by status (PENDING, CONFIRMED, CANCELLED, COMPLETED, NO_SHOW).
        upcoming_only: Only show upcoming appointments (default true).
    """
    if not API_TOKEN:
        return "Error: OPENTRIANGLE_API_TOKEN environment variable is not set."

    params = {"upcoming_only": str(upcoming_only).lower()}
    if status:
        params["status"] = status

    results = await _get("/api/appointments/my", params=params, auth=True)
    if not results:
        return "No appointments found."
    return json.dumps(results, indent=2)


@mcp.tool()
async def cancel_appointment(appointment_id: int) -> str:
    """Cancel an existing appointment on OpenTriangle.

    Requires an API token. Customers can cancel up to the appointment start time.

    Args:
        appointment_id: The ID of the appointment to cancel.
    """
    if not API_TOKEN:
        return "Error: OPENTRIANGLE_API_TOKEN environment variable is not set."

    try:
        result = await _post(f"/api/appointments/{appointment_id}/cancel")
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return f"Error: Cannot cancel this appointment. {e.response.text}"
        elif e.response.status_code == 404:
            return "Error: Appointment not found."
        raise


if __name__ == "__main__":
    mcp.run()
