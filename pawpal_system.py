"""
PawPal+ System Design
Core classes for pet care scheduling assistant
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class Task:
    """A single pet care activity with priority, duration, and completion tracking."""
    title: str
    description: str = ""  # Detailed description of the task
    duration_minutes: int = 0
    priority: str = "medium"  # low, medium, high
    category: str = ""  # walk, feeding, grooming, meds, enrichment
    frequency: str = "one-time"  # daily, weekly, one-time, etc.
    is_recurring: bool = False
    completed: bool = False  # Completion status
    tags: List[str] = field(default_factory=list)
    task_id: str = field(default="")
    
    def __post_init__(self):
        """Generate task_id if not provided."""
        if not self.task_id:
            self.task_id = f"{self.title.lower().replace(' ', '_')}_{id(self)}"
    
    def get_priority_score(self) -> int:
        """Returns numeric value for priority (high=3, medium=2, low=1)."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map.get(self.priority.lower(), 0)
    
    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.completed = False
    
    def to_dict(self) -> Dict:
        """Serialize task info to dictionary."""
        return asdict(self)


@dataclass
class Pet:
    """A pet with health info and a list of care tasks."""
    name: str
    species: str  # dog, cat, other
    age: int
    health_conditions: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    pet_id: str = field(default="")
    
    def __post_init__(self):
        """Generate pet_id if not provided."""
        if not self.pet_id:
            self.pet_id = f"{self.name.lower()}_{id(self)}"
    
    def get_care_requirements(self) -> List[str]:
        """Returns list of mandatory care needs based on pet info."""
        requirements = []
        if self.species == "dog":
            requirements.extend(["daily walk", "feeding", "fresh water"])
        elif self.species == "cat":
            requirements.extend(["litter box cleaning", "feeding", "fresh water"])
        
        if self.health_conditions:
            requirements.append("health monitoring")
        
        return requirements
    
    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks for this pet."""
        return self.tasks
    
    def get_pending_tasks(self) -> List[Task]:
        """Retrieve incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]
    
    def to_dict(self) -> Dict:
        """Serialize pet info to dictionary."""
        data = {
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'health_conditions': self.health_conditions,
            'pet_id': self.pet_id,
            'tasks': [task.to_dict() for task in self.tasks]
        }
        return data


@dataclass
class Owner:
    """A pet owner managing multiple pets and their care schedules."""
    name: str
    availability_hours: Dict[str, int]  # day: minutes available
    pets: List[Pet] = field(default_factory=list)
    preferences: Dict = field(default_factory=dict)
    timezone: str = "UTC"
    owner_id: str = field(default="")
    
    def __post_init__(self):
        """Generate owner_id if not provided."""
        if not self.owner_id:
            self.owner_id = f"{self.name.lower()}_{id(self)}"
    
    def get_available_time(self) -> int:
        """Returns total minutes available today."""
        return sum(self.availability_hours.values())
    
    def can_complete_task(self, task: Task, current_time: int) -> bool:
        """Check if owner has time to complete a task at given time."""
        remaining_time = self.get_available_time() - current_time
        return remaining_time >= task.duration_minutes
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to owner's pet list."""
        self.pets.append(pet)
    
    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Retrieve a specific pet by ID."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_all_tasks())
        return all_tasks
    
    def get_all_pending_tasks(self) -> List[Task]:
        """Retrieve all incomplete tasks across all pets."""
        all_pending = []
        for pet in self.pets:
            all_pending.extend(pet.get_pending_tasks())
        return all_pending
    
    def to_dict(self) -> Dict:
        """Serialize owner info to dictionary."""
        data = {
            'name': self.name,
            'availability_hours': self.availability_hours,
            'timezone': self.timezone,
            'owner_id': self.owner_id,
            'preferences': self.preferences,
            'pets': [pet.to_dict() for pet in self.pets]
        }
        return data


@dataclass
class Scheduler:
    """Generates optimized daily schedules for all owner's pets."""
    owner: Owner
    schedule: Dict = field(default_factory=dict)
    scheduler_id: str = field(default="")
    
    def __post_init__(self):
        """Generate scheduler_id if not provided."""
        if not self.scheduler_id:
            self.scheduler_id = f"scheduler_{id(self)}"
    
    def get_tasks_for_pet(self, pet_id: str) -> List[Task]:
        """Retrieve all tasks for a specific pet."""
        pet = self.owner.get_pet(pet_id)
        if pet:
            return pet.get_all_tasks()
        return []
    
    def get_all_pending_tasks(self) -> List[Task]:
        """Retrieve all incomplete tasks across all pets."""
        return self.owner.get_all_pending_tasks()
    
    def generate_schedule(self) -> Dict:
        """Creates ordered schedule based on priority and time constraints across all pets."""
        all_tasks = self.get_all_pending_tasks()
        
        if not all_tasks:
            return {"pets": {}, "total_tasks": 0, "is_valid": True}
        
        # Sort tasks by priority score (descending) then by duration (ascending)
        sorted_tasks = sorted(
            all_tasks,
            key=lambda t: (-t.get_priority_score(), t.duration_minutes)
        )
        
        # Organize by pet
        schedule_by_pet = {}
        for pet in self.owner.pets:
            pet_tasks = [t for t in sorted_tasks if t in pet.tasks]
            if pet_tasks:
                schedule_by_pet[pet.pet_id] = {
                    "pet_name": pet.name,
                    "tasks": [task.to_dict() for task in pet_tasks],
                    "total_duration": sum(task.duration_minutes for task in pet_tasks)
                }
        
        self.schedule = {
            "pets": schedule_by_pet,
            "total_tasks": len(sorted_tasks),
            "total_duration": sum(task.duration_minutes for task in sorted_tasks),
            "is_valid": self.validate_schedule()
        }
        return self.schedule
    
    def get_schedule_explanation(self) -> str:
        """Returns reasoning for task organization."""
        if not self.schedule:
            return "No schedule generated yet."
        
        explanation = f"Schedule for {self.owner.name}:\n\n"
        
        for pet_id, pet_schedule in self.schedule["pets"].items():
            explanation += f"📍 {pet_schedule['pet_name']}:\n"
            for i, task_dict in enumerate(pet_schedule["tasks"], 1):
                explanation += f"  {i}. {task_dict['title']} ({task_dict['duration_minutes']} min) - Priority: {task_dict['priority']}\n"
            explanation += f"  Subtotal: {pet_schedule['total_duration']} minutes\n\n"
        
        explanation += f"Total tasks: {self.schedule['total_tasks']}\n"
        explanation += f"Total duration: {self.schedule['total_duration']} minutes\n"
        explanation += f"Fits available time: {'Yes' if self.schedule['is_valid'] else 'No'}\n"
        
        return explanation
    
    def validate_schedule(self) -> bool:
        """Check if schedule fits owner's availability."""
        total_duration = sum(task.duration_minutes for task in self.get_all_pending_tasks())
        available_time = self.owner.get_available_time()
        return total_duration <= available_time
    
    def to_dict(self) -> Dict:
        """Serialize full schedule to dictionary."""
        return {
            "owner": self.owner.to_dict(),
            "schedule": self.schedule,
            "scheduler_id": self.scheduler_id
        }


if __name__ == "__main__":
    # Example usage
    mochi = Pet(name="Mochi", species="dog", age=3, health_conditions=[])
    max_pet = Pet(name="Max", species="cat", age=5, health_conditions=["sensitive stomach"])
    
    jordan = Owner(name="Jordan", availability_hours={"morning": 60, "afternoon": 90, "evening": 45})
    jordan.add_pet(mochi)
    jordan.add_pet(max_pet)
    
    # Tasks for Mochi
    morning_walk = Task(title="Morning walk", description="20-minute walk in the park", duration_minutes=20, priority="high", category="walk", frequency="daily")
    evening_walk = Task(title="Evening walk", description="Evening stroll around the neighborhood", duration_minutes=20, priority="high", category="walk", frequency="daily")
    feeding_dog = Task(title="Feed Mochi", description="Prepare and serve dog food with fresh water", duration_minutes=10, priority="high", category="feeding", frequency="daily")
    playtime = Task(title="Playtime with Mochi", description="Interactive play with toys and fetch", duration_minutes=30, priority="medium", category="enrichment", frequency="daily")
    
    mochi.add_task(morning_walk)
    mochi.add_task(evening_walk)
    mochi.add_task(feeding_dog)
    mochi.add_task(playtime)
    
    # Tasks for Max
    litter_box = Task(title="Clean litter box", description="Scoop and clean Max's litter box daily", duration_minutes=10, priority="high", category="grooming", frequency="daily")
    feeding_cat = Task(title="Feed Max", description="Serve cat food with fresh water", duration_minutes=5, priority="high", category="feeding", frequency="daily")
    grooming = Task(title="Brush Max", description="Gentle brushing to reduce shedding", duration_minutes=15, priority="low", category="grooming", frequency="weekly")
    
    max_pet.add_task(litter_box)
    max_pet.add_task(feeding_cat)
    max_pet.add_task(grooming)
    
    scheduler = Scheduler(owner=jordan)
    scheduler.generate_schedule()
    print(scheduler.get_schedule_explanation())
