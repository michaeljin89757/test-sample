#!/usr/bin/env python3
"""Sample log analysis script for a test repository.

Reads a list of (ip, request, status_code) tuples, then prints a report with:
  1. The top requesting IP addresses (by number of requests).
  2. Statistics (counts) for every HTTP status code seen in the data.

This is intentionally a simple, self-contained example so it can be committed
to a demo repo and run without any external dependencies or input files.
"""

# Sample access-log style data: (ip, request_path, status_code)
LOG_ENTRIES = [
    ("192.168.1.10", "/home", 200),
    ("192.168.1.10", "/about", 200),
    ("192.168.1.10", "/contact", 404),
    ("10.0.0.5", "/home", 200),
    ("10.0.0.5", "/login", 200),
    ("10.0.0.5", "/admin", 403),
    ("10.0.0.5", "/dashboard", 500),
    ("172.16.0.9", "/home", 200),
    ("172.16.0.9", "/home", 200),
    ("172.16.0.9", "/api/users", 200),
    ("172.16.0.9", "/api/users", 503),
    ("192.168.1.20", "/home", 200),
    ("192.168.1.20", "/missing", 404),
]


def build_ip_counts(entries):
    """Return a dict mapping each IP to how many requests it made."""
    counts = {}
    for ip, _request, _status in entries:
        counts[ip] = counts.get(ip, 0) + 1
    return counts


def build_status_counts(entries):
    """Return a dict mapping each status code to how many times it appeared."""
    counts = {}
    for _ip, _request, status in entries:
        counts[status] = counts.get(status, 0) + 1
    return counts


def top_requesting_ips(ip_counts, limit=3):
    """Return the IPs with the most requests.

    BUG: the sort key uses `x[1]` which is correct for value, but we sort
    ascending instead of descending. As a result this returns the LEAST
    active IPs, not the top ones. Should be `reverse=True`.
    """
    # TODO: fix this — currently reports the wrong IPs on purpose for the demo.
    ranked = sorted(ip_counts.items(), key=lambda x: x[1])  # BUG: missing reverse=True
    return ranked[:limit]


def print_report(entries):
    ip_counts = build_ip_counts(entries)
    status_counts = build_status_counts(entries)

    print("=" * 48)
    print("TOP REQUESTING IP ADDRESSES")
    print("=" * 48)
    for ip, count in top_requesting_ips(ip_counts, limit=3):
        print(f"  {ip:<15} {count} request(s)")

    print()
    print("=" * 48)
    print("STATUS CODE STATISTICS")
    print("=" * 48)
    for status in sorted(status_counts):
        print(f"  {status}: {status_counts[status]} response(s)")

    print()
    print(f"Total entries analyzed: {len(entries)}")


if __name__ == "__main__":
    print_report(LOG_ENTRIES)
