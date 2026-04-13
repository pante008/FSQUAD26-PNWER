"""
Realistic Synthetic Visitor Data Generator
Generates data matching actual PNWER FIFA 2026 parameters:
- 750,000 visitors (100K sample for scaling)
- ~1 week average stay
- $870 average spend per visitor
- North America focused (60-70% Canada/USA)
"""

from __future__ import annotations

import csv
import json
import random
import time
from datetime import datetime, timedelta
from pathlib import Path


class RealisticVisitorDataGenerator:
    """
    Generates synthetic visitor data matching real PNWER parameters
    """

    def __init__(self, num_records: int = 100_000, output_dir: str = "data/raw"):
        self.num_records = num_records
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        random.seed(42)

        # PNWER REALISTIC DISTRIBUTIONS

        # Country distribution (60-70% North America)
        self.origin_countries = {
            # North America (65%)
            "Canada": 0.30,
            "USA": 0.35,
            # Latin America (20%)
            "Mexico": 0.08,
            "Brazil": 0.05,
            "Argentina": 0.04,
            "Colombia": 0.03,
            # Europe (10%)
            "England": 0.03,
            "Germany": 0.02,
            "France": 0.02,
            "Spain": 0.02,
            "Netherlands": 0.01,
            # Asia/Other (5%)
            "Japan": 0.02,
            "Australia": 0.01,
            "South Korea": 0.01,
            "China": 0.01,
        }

        self.activities = [
            "watch_matches",
            "shopping",
            "dining",
            "sightseeing",
            "nightlife",
            "hiking",
        ]

        self.booking_sources = ["online_booking", "travel_agent", "tour_operator", "direct"]
        self.accommodation_types = [
            "hotel",
            "airbnb",
            "hostel",
            "resort",
            "staying_with_friends",
        ]
        self.ticket_types = ["group_stage", "knockout", "vip_hospitality", "package_tour"]

        print(f"🚀 Realistic Visitor Data Generator")
        print(f"   Records to generate: {num_records:,}")
        print(f"   Output directory: {output_dir}")
        print(f"   Target avg spend: $870/visitor")
        print(f"   Target avg stay: 7 days")

    def weighted_choice(
        self, options: list[str], weights: list[float]
    ) -> str:
        """Weighted random selection"""
        total = sum(weights)
        r = random.uniform(0, total)
        cumsum = 0
        for option, weight in zip(options, weights):
            cumsum += weight
            if r <= cumsum:
                return option
        return options[-1]

    def gaussian_random(
        self, mean: float, std_dev: float, min_val: float, max_val: float
    ) -> float:
        """Normal distribution with bounds"""
        value = random.gauss(mean, std_dev)
        return max(min_val, min(max_val, value))

    def fake_name(self) -> tuple[str, str]:
        """Generate random first and last name"""
        first_names = [
            "Juan",
            "Maria",
            "Carlos",
            "Ana",
            "Luis",
            "Sofia",
            "Miguel",
            "Elena",
            "Diego",
            "Rosa",
            "Jorge",
            "Angela",
            "Francisco",
            "Monica",
            "Antonio",
            "John",
            "Mary",
            "James",
            "Patricia",
            "Michael",
            "Jennifer",
        ]
        last_names = [
            "Garcia",
            "Rodriguez",
            "Martinez",
            "Lopez",
            "Hernandez",
            "Gonzalez",
            "Perez",
            "Sanchez",
            "Torres",
            "Flores",
            "Rivera",
            "Diaz",
            "Cruz",
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
        ]
        return random.choice(first_names), random.choice(last_names)

    def fake_email(self) -> str:
        """Generate random email"""
        providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(5, 12)))
        return f"{username}@{random.choice(providers)}"

    def fake_phone(self) -> str:
        """Generate random phone"""
        return f"+{random.randint(1, 999)} {random.randint(100, 999)} {random.randint(1000000, 9999999)}"

    def generate_visitor(self, visitor_id: str) -> dict:
        """Generate single realistic visitor record"""

        # Origin country (North America focused: 65%)
        countries = list(self.origin_countries.keys())
        probabilities = list(self.origin_countries.values())
        origin = self.weighted_choice(countries, probabilities)

        # Age (normal distribution, 18-75)
        age = int(self.gaussian_random(38, 16, 18, 75))

        # Group size (weighted toward 2-3 people)
        group_sizes = [1, 2, 3, 4, 5, 6]
        group_probabilities = [0.15, 0.35, 0.25, 0.15, 0.07, 0.03]
        group_size = self.weighted_choice(group_sizes, group_probabilities)

        # ===== KEY CHANGE: STAY DURATION (Match PNWER ~1 week) =====
        # 70% stay 7 days, 20% stay 5-6 days, 10% stay 1-4 days
        stay_dice = random.random()
        if stay_dice < 0.70:
            days_staying = 7  # Full week (most common)
        elif stay_dice < 0.90:
            days_staying = random.randint(5, 6)  # Long weekend
        else:
            days_staying = random.randint(1, 4)  # Short trip

        # ===== KEY CHANGE: SPENDING (Match PNWER $870/visitor) =====
        # Daily spending distribution for realistic total
        # Average should be ~$124/day ($870 / 7 days)

        # Spending tier affects daily rate
        spending_tier_rand = random.random()
        if spending_tier_rand < 0.20:  # Budget (20%)
            daily_base = random.uniform(50, 100)  # $50-100/day
        elif spending_tier_rand < 0.55:  # Standard (35%)
            daily_base = random.uniform(100, 160)  # $100-160/day
        elif spending_tier_rand < 0.85:  # Premium (30%)
            daily_base = random.uniform(160, 250)  # $160-250/day
        else:  # VIP (15%)
            daily_base = random.uniform(250, 400)  # $250-400/day

        # Add some randomness and cap
        daily_spending = round(daily_base + random.gauss(0, 20), 2)
        daily_spending = max(50, min(400, daily_spending))

        # Primary activity
        primary_activity = random.choice(self.activities)

        # Is returning visitor (realistic ~15%)
        is_returning = random.random() < 0.15

        # Arrival date (June 1 - July 15, 2026)
        start_date = datetime(2026, 6, 1)
        days_offset = random.randint(0, 44)
        minutes_offset = random.randint(0, 1440)
        arrival_date = start_date + timedelta(days=days_offset, minutes=minutes_offset)

        # Departure = arrival + stay days
        departure_date = arrival_date + timedelta(days=days_staying)

        # Email and phone
        email = self.fake_email()
        phone = self.fake_phone()

        # Booking source
        booking_sources = ["online_booking", "travel_agent", "tour_operator", "direct"]
        booking_source_probs = [0.5, 0.2, 0.2, 0.1]
        booking_source = self.weighted_choice(booking_sources, booking_source_probs)

        # Accommodation
        accommodation_probs = [0.40, 0.30, 0.15, 0.10, 0.05]
        accommodation_type = self.weighted_choice(self.accommodation_types, accommodation_probs)

        # Ticket type
        ticket_probs = [0.50, 0.30, 0.10, 0.10]
        ticket_type = self.weighted_choice(self.ticket_types, ticket_probs)

        # Names
        first_name, last_name = self.fake_name()

        # Derived fields
        total_spending = round(daily_spending * days_staying, 2)
        group_total_spending = round(total_spending * group_size, 2)

        return {
            "visitor_id": visitor_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "age": age,
            "gender": random.choice(["Female", "Male", "Non-binary", "Prefer not to say"]),
            "country": origin,
            "origin_region": {
                "Canada": "North America",
                "USA": "North America",
                "Mexico": "North America",
                "Brazil": "South America",
                "Argentina": "South America",
                "Colombia": "South America",
                "England": "Europe",
                "Germany": "Europe",
                "France": "Europe",
                "Spain": "Europe",
                "Netherlands": "Europe",
                "Japan": "Asia",
                "Australia": "Oceania",
                "South Korea": "Asia",
                "China": "Asia",
            }.get(origin, "Other"),
            "group_size": group_size,
            "daily_spending": daily_spending,
            "days_staying": days_staying,
            "primary_activity": primary_activity,
            "is_returning_visitor": is_returning,
            "arrival_date": arrival_date.isoformat(),
            "departure_date": departure_date.isoformat(),
            "booking_source": booking_source,
            "accommodation_type": accommodation_type,
            "ticket_type": ticket_type,
            "total_spending": total_spending,
            "group_total_spending": group_total_spending,
            "created_at": datetime.now().isoformat(),
        }

    def generate_all_visitors(self) -> list[dict]:
        """Generate all visitor records"""
        print(f"\n📊 Generating {self.num_records:,} realistic visitor records...\n")

        start_time = time.time()
        visitors = []

        for i in range(self.num_records):
            visitor_id = f"V{i:07d}"
            visitor = self.generate_visitor(visitor_id)
            visitors.append(visitor)

            if (i + 1) % 10000 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                print(f"✓ Generated {i + 1:,} records ({rate:.0f} records/sec)")

        elapsed = time.time() - start_time
        print(f"\n✓ Generated {len(visitors):,} records in {elapsed:.2f} seconds")

        return visitors

    def save_to_csv(self, visitors: list[dict], filename: str = "visitors_2026.csv") -> Path:
        """Save visitors to CSV"""
        filepath = self.output_dir / filename

        print(f"\n💾 Saving to CSV: {filepath}")

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=visitors[0].keys())
            writer.writeheader()
            writer.writerows(visitors)

        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"   File size: {file_size_mb:.2f} MB")
        print(f"   Records: {len(visitors):,}")

        return filepath

    def save_to_json(self, visitors: list[dict], filename: str = "visitors_2026.json") -> Path:
        """Save visitors to JSON"""
        filepath = self.output_dir / filename

        print(f"\n💾 Saving to JSON: {filepath}")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(visitors, f, indent=2)

        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"   File size: {file_size_mb:.2f} MB")

        return filepath

    def print_summary(self, visitors: list[dict]) -> None:
        """Print data summary statistics"""
        if not visitors:
            return

        print("\n" + "=" * 80)
        print("📊 REALISTIC SYNTHETIC DATA SUMMARY")
        print("=" * 80)

        # Country distribution
        origin_counts = {}
        for v in visitors:
            origin = v["country"]
            origin_counts[origin] = origin_counts.get(origin, 0) + 1

        print("\n🌍 TOP 10 ORIGIN COUNTRIES:")
        for country, count in sorted(origin_counts.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]:
            pct = 100 * count / len(visitors)
            print(f"   {country:20s}: {count:6,} ({pct:5.1f}%)")

        # Verify North America percentage
        na_count = origin_counts.get("Canada", 0) + origin_counts.get("USA", 0)
        na_pct = 100 * na_count / len(visitors)
        print(
            f"\n   🇨🇦🇺🇸 North America Total: {na_count:,} ({na_pct:.1f}%) [Target: 65%]"
        )

        # Age statistics
        ages = [v["age"] for v in visitors]
        print(f"\n👥 AGE STATISTICS:")
        print(f"   Min: {min(ages)}, Max: {max(ages)}, Avg: {sum(ages)/len(ages):.1f}")

        # STAY DURATION (NEW KEY METRIC)
        stays = [v["days_staying"] for v in visitors]
        print(f"\n📅 STAY DURATION STATISTICS:")
        print(f"   Min: {min(stays)} days")
        print(f"   Max: {max(stays)} days")
        print(f"   Avg: {sum(stays)/len(stays):.1f} days [Target: 7 days]")

        # Count stay distributions
        stay_1_4 = sum(1 for s in stays if s <= 4)
        stay_5_6 = sum(1 for s in stays if 5 <= s <= 6)
        stay_7 = sum(1 for s in stays if s == 7)
        print(f"   1-4 days: {stay_1_4:,} ({100*stay_1_4/len(visitors):.1f}%) [Target: 10%]")
        print(f"   5-6 days: {stay_5_6:,} ({100*stay_5_6/len(visitors):.1f}%) [Target: 20%]")
        print(f"   7 days:   {stay_7:,} ({100*stay_7/len(visitors):.1f}%) [Target: 70%]")

        # SPENDING STATISTICS (NEW KEY METRIC)
        spendings = [v["total_spending"] for v in visitors]
        print(f"\n💰 TOTAL SPENDING STATISTICS:")
        print(f"   Min: ${min(spendings):.2f}")
        print(f"   Max: ${max(spendings):.2f}")
        avg_spend = sum(spendings) / len(spendings)
        print(f"   Avg: ${avg_spend:.2f} [Target: $870]")

        # Daily spending
        daily_spendings = [v["daily_spending"] for v in visitors]
        daily_avg = sum(daily_spendings) / len(daily_spendings)
        print(f"   Daily Avg: ${daily_avg:.2f} [Target: $124/day]")

        # Group sizes
        group_sizes = {}
        for v in visitors:
            size = v["group_size"]
            group_sizes[size] = group_sizes.get(size, 0) + 1

        print(f"\n👨‍👩‍👧 GROUP SIZE DISTRIBUTION:")
        for size in sorted(group_sizes.keys()):
            count = group_sizes[size]
            pct = 100 * count / len(visitors)
            print(f"   {size} people: {count:6,} ({pct:5.1f}%)")

        # Total spending across all visitors
        total_spend = sum(spendings)
        print(f"\n💵 TOTAL PROJECT SPENDING:")
        print(f"   Total: ${total_spend:,.2f}")
        print(f"   Avg/visitor: ${avg_spend:.2f}")

        # Comparison to real PNWER
        if len(visitors) == 100_000:
            projected_750k = (total_spend / 100_000) * 750_000
            print(f"\n📈 PROJECTED FOR 750K VISITORS:")
            print(f"   Projected total spending: ${projected_750k:,.0f}")
            print(f"   Real PNWER target: $652,600,000")
            variance = ((projected_750k / 652_600_000) - 1) * 100
            print(f"   Variance: {variance:+.1f}%")

        # Returning visitors
        returning = sum(1 for v in visitors if v["is_returning_visitor"])
        print(f"\n🔄 RETURNING VISITORS:")
        print(f"   {returning:,} ({100*returning/len(visitors):.1f}%) [Target: ~15%]")

        print("\n" + "=" * 80)

    def run(self) -> list[dict]:
        """Execute full pipeline"""
        print("\n" + "=" * 80)
        print("🚀 REALISTIC SYNTHETIC DATA GENERATION (PNWER-ALIGNED)")
        print("=" * 80)

        # Generate
        visitors = self.generate_all_visitors()

        # Summary
        self.print_summary(visitors)

        # Save
        self.save_to_csv(visitors)
        self.save_to_json(visitors)

        print("\n" + "=" * 80)
        print("✅ REALISTIC DATA GENERATION COMPLETE!")
        print("=" * 80)
        print("\nGenerated Files:")
        print(f"   ✓ data/raw/visitors_2026.csv")
        print(f"   ✓ data/raw/visitors_2026.json")
        print("\nNext Steps:")
        print("   1. Upload CSV to Snowflake")
        print("   2. Run: dbt run")
        print("   3. Verify projections match PNWER ($652.6M)")

        return visitors


def main() -> list[dict]:
    """Main execution"""
    generator = RealisticVisitorDataGenerator(
        num_records=100_000, output_dir="data/raw"
    )
    visitors = generator.run()
    return visitors


if __name__ == "__main__":
    visitors = main()