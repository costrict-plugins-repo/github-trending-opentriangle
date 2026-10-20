# OpenTriangle Plugin for Claude Code

Search for local businesses, check real-time availability, and book appointments on [OpenTriangle](https://opentriangle.ai) — directly from Claude Code.

## Installation

```bash
claude plugin add github:bearmountainlabs/opentriangle-plugin
```

Or install from a local directory:

```bash
claude --plugin-dir /path/to/opentriangle-plugin
```

## Setup

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Authentication (optional)

Searching and browsing businesses works without authentication. To **book appointments**, you need an API token:

1. Sign up at [opentriangle.ai](https://opentriangle.ai)
2. Go to **Profile > API Tokens**
3. Create a token with type **customer_bookings**
4. Set the environment variable:

```bash
export OPENTRIANGLE_API_TOKEN="apt_cus_your_token_here"
```

## Available Tools

| Tool | Description | Auth Required |
|------|-------------|:---:|
| `search_businesses` | Search by name, category, city, zip, or coordinates | No |
| `list_categories` | List all service categories | No |
| `get_business` | Get business details (address, hours, contact) | No |
| `get_providers` | List providers at a business | No |
| `get_available_slots` | Check available appointment times | No |
| `get_reviews` | Read customer reviews | No |
| `book_appointment` | Book an available time slot | Yes |
| `my_appointments` | View your appointments | Yes |
| `cancel_appointment` | Cancel an appointment | Yes |

## Usage

Use the `/opentriangle:book` skill for guided booking, or call tools directly:

```
Find hair salons in Austin, TX with available appointments this week
```

```
Show me dentists near zip code 90210 with good reviews
```

```
Book the 2pm slot with Dr. Smith tomorrow
```

## Links

- **Website**: [opentriangle.ai](https://opentriangle.ai)
- **App Store**: [Download for iOS](https://apps.apple.com/app/opentriangle/id6758877965)
- **Google Play**: [Download for Android](https://play.google.com/store/apps/details?id=ai.opentriangle.mobile)
- **Support**: [support@opentriangle.ai](mailto:support@opentriangle.ai)
