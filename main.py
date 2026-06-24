"""
Test script for PawPal+ System
Creates multiple owners, pets, and tasks to demonstrate the scheduling system
"""

from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    print("=" * 80)
    print("🐾 PAWPAL+ SYSTEM TEST - Multiple Owners and Pets")
    print("=" * 80)
    
    # ============================================================================
    # OWNER 1: JORDAN
    # ============================================================================
    print("\n" + "=" * 80)
    print("OWNER 1: JORDAN")
    print("=" * 80)
    
    jordan = Owner(
        name="Jordan",
        availability_hours={"morning": 60, "afternoon": 90, "evening": 45}
    )
    print(f"\n✓ Created Owner: {jordan.name}")
    print(f"  Available time today: {jordan.get_available_time()} minutes")
    print(f"  Availability: {jordan.availability_hours}")
    
    # Jordan's Pets
    mochi = Pet(name="Mochi", species="dog", age=3, health_conditions=[])
    max_pet = Pet(name="Max", species="cat", age=5, health_conditions=["sensitive stomach"])
    
    jordan.add_pet(mochi)
    jordan.add_pet(max_pet)
    
    print(f"\n✓ Added pets to Jordan:")
    print(f"  - {mochi.name} (Dog, {mochi.age} years old)")
    print(f"  - {max_pet.name} (Cat, {max_pet.age} years old, {max_pet.health_conditions})")
    
    # Tasks for Mochi
    print(f"\n📋 Creating tasks for {mochi.name}:")
    mochi_tasks = [
        Task(title="Morning walk", description="20-minute walk in the park", duration_minutes=20, priority="high", category="walk", frequency="daily"),
        Task(title="Feed Mochi", description="Prepare and serve dog food with fresh water", duration_minutes=10, priority="high", category="feeding", frequency="daily"),
        Task(title="Evening walk", description="Evening stroll around the neighborhood", duration_minutes=20, priority="high", category="walk", frequency="daily"),
        Task(title="Playtime with Mochi", description="Interactive play with toys and fetch", duration_minutes=30, priority="medium", category="enrichment", frequency="daily"),
        Task(title="Training session", description="Teach new tricks or reinforce commands", duration_minutes=15, priority="low", category="enrichment", frequency="daily"),
    ]
    
    for task in mochi_tasks:
        mochi.add_task(task)
        print(f"  ✓ {task.title} ({task.duration_minutes} min, {task.priority} priority)")
    
    # Tasks for Max
    print(f"\n📋 Creating tasks for {max_pet.name}:")
    max_tasks = [
        Task(title="Clean litter box", description="Scoop and clean Max's litter box daily", duration_minutes=10, priority="high", category="grooming", frequency="daily"),
        Task(title="Feed Max", description="Serve cat food with fresh water (sensitive stomach diet)", duration_minutes=5, priority="high", category="feeding", frequency="daily"),
        Task(title="Brush Max", description="Gentle brushing to reduce shedding", duration_minutes=15, priority="low", category="grooming", frequency="weekly"),
        Task(title="Play with Max", description="Interactive play with feather toys", duration_minutes=20, priority="medium", category="enrichment", frequency="daily"),
    ]
    
    for task in max_tasks:
        max_pet.add_task(task)
        print(f"  ✓ {task.title} ({task.duration_minutes} min, {task.priority} priority)")
    
    # Generate schedule for Jordan
    print(f"\n{'─' * 80}")
    print("📅 GENERATING SCHEDULE FOR JORDAN")
    print(f"{'─' * 80}")
    
    scheduler_jordan = Scheduler(owner=jordan)
    scheduler_jordan.generate_schedule()
    
    print("\n" + scheduler_jordan.get_schedule_explanation())
    
    # ============================================================================
    # OWNER 2: ALEX
    # ============================================================================
    print("\n" + "=" * 80)
    print("OWNER 2: ALEX")
    print("=" * 80)
    
    alex = Owner(
        name="Alex",
        availability_hours={"morning": 45, "afternoon": 60, "evening": 90}
    )
    print(f"\n✓ Created Owner: {alex.name}")
    print(f"  Available time today: {alex.get_available_time()} minutes")
    print(f"  Availability: {alex.availability_hours}")
    
    # Alex's Pets
    buddy = Pet(name="Buddy", species="dog", age=7, health_conditions=["arthritis"])
    luna = Pet(name="Luna", species="cat", age=2, health_conditions=[])
    
    alex.add_pet(buddy)
    alex.add_pet(luna)
    
    print(f"\n✓ Added pets to Alex:")
    print(f"  - {buddy.name} (Dog, {buddy.age} years old, {buddy.health_conditions})")
    print(f"  - {luna.name} (Cat, {luna.age} years old)")
    
    # Tasks for Buddy
    print(f"\n📋 Creating tasks for {buddy.name}:")
    buddy_tasks = [
        Task(title="Gentle morning walk", description="Slow-paced walk considering arthritis", duration_minutes=25, priority="high", category="walk", frequency="daily"),
        Task(title="Feed Buddy", description="Senior dog food with supplements", duration_minutes=10, priority="high", category="feeding", frequency="daily"),
        Task(title="Medication", description="Give arthritis medication with food", duration_minutes=5, priority="high", category="meds", frequency="daily"),
        Task(title="Afternoon nap spot", description="Ensure comfortable resting area is available", duration_minutes=10, priority="medium", category="enrichment", frequency="daily"),
        Task(title="Grooming", description="Brush and check for skin issues", duration_minutes=20, priority="low", category="grooming", frequency="weekly"),
    ]
    
    for task in buddy_tasks:
        buddy.add_task(task)
        print(f"  ✓ {task.title} ({task.duration_minutes} min, {task.priority} priority)")
    
    # Tasks for Luna
    print(f"\n📋 Creating tasks for {luna.name}:")
    luna_tasks = [
        Task(title="Feed Luna", description="Premium cat food with fresh water", duration_minutes=5, priority="high", category="feeding", frequency="daily"),
        Task(title="Litter box check", description="Check and clean litter box", duration_minutes=5, priority="high", category="grooming", frequency="daily"),
        Task(title="Playtime", description="Active play with laser pointer and wand toys", duration_minutes=30, priority="high", category="enrichment", frequency="daily"),
        Task(title="Window perch time", description="Ensure access to favorite window", duration_minutes=15, priority="low", category="enrichment", frequency="daily"),
    ]
    
    for task in luna_tasks:
        luna.add_task(task)
        print(f"  ✓ {task.title} ({task.duration_minutes} min, {task.priority} priority)")
    
    # Generate schedule for Alex
    print(f"\n{'─' * 80}")
    print("📅 GENERATING SCHEDULE FOR ALEX")
    print(f"{'─' * 80}")
    
    scheduler_alex = Scheduler(owner=alex)
    scheduler_alex.generate_schedule()
    
    print("\n" + scheduler_alex.get_schedule_explanation())
    
    # ============================================================================
    # COMPARISON & SUMMARY
    # ============================================================================
    print("\n" + "=" * 80)
    print("📊 SYSTEM SUMMARY")
    print("=" * 80)
    
    print(f"\nOwner 1: {jordan.name}")
    print(f"  Pets: {len(jordan.pets)}")
    print(f"  Total tasks: {len(jordan.get_all_tasks())}")
    print(f"  Pending tasks: {len(jordan.get_all_pending_tasks())}")
    print(f"  Total scheduled time: {scheduler_jordan.schedule['total_duration']} minutes / {jordan.get_available_time()} available")
    print(f"  Schedule valid: {'✅ YES' if scheduler_jordan.schedule['is_valid'] else '❌ NO'}")
    
    print(f"\nOwner 2: {alex.name}")
    print(f"  Pets: {len(alex.pets)}")
    print(f"  Total tasks: {len(alex.get_all_tasks())}")
    print(f"  Pending tasks: {len(alex.get_all_pending_tasks())}")
    print(f"  Total scheduled time: {scheduler_alex.schedule['total_duration']} minutes / {alex.get_available_time()} available")
    print(f"  Schedule valid: {'✅ YES' if scheduler_alex.schedule['is_valid'] else '❌ NO'}")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
