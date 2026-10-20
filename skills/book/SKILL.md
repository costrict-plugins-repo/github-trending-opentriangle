---
name: book
description: Search for businesses and book appointments on OpenTriangle
---

# OpenTriangle Booking

Use the OpenTriangle MCP tools to help the user find and book appointments with local service businesses.

## Workflow

1. **Understand the request** - Ask the user what service they need (e.g., haircut, dental cleaning, massage) and their location (city, zip code, or coordinates).

2. **Search for businesses** - Use `search_businesses` with the service category and location. Show the user a summary of matching businesses with their ratings and available slot counts.

3. **Get details** - When the user picks a business, use `get_business` to show full details and `get_providers` to list available providers.

4. **Check availability** - Use `get_available_slots` to show available times. Present them in a clear format grouped by date.

5. **Book** - When the user confirms a slot, use `book_appointment` with the slot ID. If authentication is required, guide them to generate an API token in the OpenTriangle app (Profile > API Tokens > Create with type "customer_bookings") and set the `OPENTRIANGLE_API_TOKEN` environment variable.

6. **Manage** - Use `my_appointments` to show upcoming appointments and `cancel_appointment` if needed.

## Tips

- Always confirm with the user before booking (show business name, provider, date/time, duration).
- If no businesses are found, try broadening the search (remove category filter, increase radius).
- Use `list_categories` if the user isn't sure what category to search for.
- Use `get_reviews` to help the user decide between businesses.
