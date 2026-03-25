#!/usr/bin/env python3
"""
Roblox Accounts Monitoring - Real Data Assembler

Assembles the dashboard dataset from verified marketplace data only.
No synthetic/random data is used. All data comes from real_data_collector.py.
"""

import json
from datetime import datetime
from real_data_collector import (
    VERIFIED_LISTINGS, MARKETPLACE_PROFILES, SOURCE_URLS,
    PRICE_BENCHMARKS, get_source_stats, get_quality_tier_stats,
    SCRAPE_DATE,
)


def build_source_breakdown():
    """Build source breakdown from verified marketplace profiles and listings."""
    data = []
    for source_name, profile in MARKETPLACE_PROFILES.items():
        listings = [l for l in VERIFIED_LISTINGS if l["source"] == source_name]
        prices = [l["price_usd"] for l in listings]
        data.append({
            "source_name": source_name,
            "source_type": "marketplace",
            "source_url": profile["url"],
            "estimated_total_listings": profile["estimated_roblox_listings"],
            "estimated_total_sold": profile.get("estimated_total_sold", 0),
            "verified_sample_count": len(listings),
            "price_range_min": profile["price_range_usd"][0],
            "price_range_max": profile["price_range_usd"][1],
            "avg_price_usd": round(sum(prices) / len(prices), 2) if prices else profile["avg_price_usd"],
            "account_guarantee_days": profile["account_guarantee_days"],
            "delivery": profile["delivery"],
            "verified_sellers": profile["verified_sellers"],
            "categories": profile["categories"],
            "last_scraped": SCRAPE_DATE,
        })
    return data


def build_listings_by_category():
    """Group verified listings by category with stats."""
    categories = {}
    for listing in VERIFIED_LISTINGS:
        cat = listing["category"]
        if cat not in categories:
            categories[cat] = {"listings": [], "prices": [], "sources": set()}
        categories[cat]["listings"].append(listing)
        categories[cat]["prices"].append(listing["price_usd"])
        categories[cat]["sources"].add(listing["source"])

    result = []
    for cat, data in sorted(categories.items()):
        prices = data["prices"]
        result.append({
            "category": cat,
            "listing_count": len(data["listings"]),
            "sources": sorted(list(data["sources"])),
            "min_price_usd": min(prices),
            "max_price_usd": max(prices),
            "avg_price_usd": round(sum(prices) / len(prices), 2),
        })
    return result


def build_quality_tier_breakdown():
    """Build quality tier breakdown from real listings."""
    tier_stats = get_quality_tier_stats()
    result = []
    total = len(VERIFIED_LISTINGS)
    for tier, stats in tier_stats.items():
        result.append({
            "quality_tier": tier,
            "listing_count": stats["count"],
            "pct_of_total": round(stats["count"] / total, 3),
            "min_price_usd": stats["min_price"],
            "max_price_usd": stats["max_price"],
            "avg_price_usd": stats["avg_price"],
        })
    return result


def build_price_comparison():
    """Build cross-source price comparison for common categories."""
    cat_source_prices = {}
    for listing in VERIFIED_LISTINGS:
        key = listing["category"]
        source = listing["source"]
        if key not in cat_source_prices:
            cat_source_prices[key] = {}
        if source not in cat_source_prices[key]:
            cat_source_prices[key][source] = []
        cat_source_prices[key][source].append(listing["price_usd"])

    result = []
    for cat, sources in cat_source_prices.items():
        if len(sources) >= 2:
            comparison = {"category": cat, "sources": {}}
            for source, prices in sources.items():
                comparison["sources"][source] = {
                    "count": len(prices),
                    "avg_price": round(sum(prices) / len(prices), 2),
                    "min_price": min(prices),
                    "max_price": max(prices),
                }
            result.append(comparison)
    return result


def generate_all_data():
    """Generate complete dataset from real data only."""
    dataset = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "scrape_date": SCRAPE_DATE,
            "data_source": "Real marketplace data scraped from U7Buy, Eldorado.gg, and eBay",
            "total_verified_listings": len(VERIFIED_LISTINGS),
            "sources_tracked": len(MARKETPLACE_PROFILES),
            "synthetic_data": False,
            "version": "2.0.0",
        },
        "marketplace_profiles": MARKETPLACE_PROFILES,
        "source_urls": SOURCE_URLS,
        "source_breakdown": build_source_breakdown(),
        "verified_listings": VERIFIED_LISTINGS,
        "categories": build_listings_by_category(),
        "quality_distribution": build_quality_tier_breakdown(),
        "price_comparison": build_price_comparison(),
        "price_benchmarks": PRICE_BENCHMARKS,
        "source_stats": get_source_stats(),
    }
    return dataset


if __name__ == "__main__":
    data = generate_all_data()
    with open("dashboard_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"=== Real Data Dashboard ===")
    print(f"Total verified listings: {data['metadata']['total_verified_listings']}")
    print(f"Sources tracked: {data['metadata']['sources_tracked']}")
    print(f"Categories found: {len(data['categories'])}")
    print(f"Quality tiers: {len(data['quality_distribution'])}")
    print(f"Price comparisons: {len(data['price_comparison'])}")
    print(f"\nSource breakdown:")
    for s in data['source_breakdown']:
        print(f"  {s['source_name']}: ~{s['estimated_total_listings']} listings, "
              f"avg ${s['avg_price_usd']}, {s['verified_sample_count']} verified samples")
    print(f"\nData saved to dashboard_data.json")
