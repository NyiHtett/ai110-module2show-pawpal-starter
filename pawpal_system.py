"""
PawPal+ System Design
Core classes for pet care scheduling assistant
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class Pet:
    """Represents a pet with care requirements and health information."""
    name: str
    species: str  # dog, cat, other
    age: int
    health_conditions: List[str] = field(default_factory=list)
    
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
    
    def to_dict(self) -> Dict:
        """Serialize pet info to dictionary."""
        return asdict(self)


@dataclass
class Task:
    """Represents a pet care task with priority and duration."""
    title: str
    duration_minutes: int
    priority: str  # low, medium, high
    category: str  # walk, feeding, grooming, meds, enrichment
    is_recurring: bool = False
    tags: List[str] = field(default_factory=list)
    
    def get_priority_score(self) -> int:
        """Returns numeric value for priority (high=3, medium=2, low=1)."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map.get(self.priority.lower(), 0)
    
    def to_dict(self) -> Dict:
        """Serialize task info to dictionary."""
        return asdict(self)


@dataclass
class Owner:
    """Represents a pet owner with availability and preferences."""
    name: str
    availability_hours: Dict[str, int]  # day: minutes available
    preferences: Dict = field(default_factory=dict)
    timezone: str = "UTC"
    
    def get_available_time(self) -> int:
        """Returns total minutes available today."""
        return sum(self.availability_hours.values())
    
    def can_complete_task(self, task: Task, current_time: int) -> bool:
        """Check if owner has time to complete a task at given time."""
        remaining_time = self.get_available_time() - current_time
        return remaining_time >= task.duration_minutes
    
    def to_dict(self) -> Dict:
        """Serialize owner info to dictionary."""
        return asdict(self)


@dataclass
class Scheduler:
    """Orchestrates the pet care scheduling logic."""
    pet: Pet
    owner: Owner
    tasks: List[Task] = field(default_factory=list)
    schedule: Dict = field(default_factory=dict)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the task list."""
        self.tasks.append(task)
    
    def generate_schedule(self) -> Dict:
        """Creates ordered schedule based on priority and time constraints."""
        if not self.tasks:
            return {}
        
        # Sort tasks by priority score (descending) then by duration (ascending)
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (-t.get_priority_score(), t.duration_minutes)
        )
        
        self.schedule = {
            "tasks": [task.to_dict() for task in sorted_tasks],
            "total_duration": sum(task.duration_minutes for task in sorted_tasks),
            "is_valid": self.validate_schedule()
        }
        return self.schedule
    
    def get_schedule_explanation(self) -> str:
        """Returns reasoning for task order."""
        if not self.schedule:
            return "No schedule generated yet."
        
        explanation = f"Schedule for {self.pet.name} ({self.owner.name}):\n"
        for i, task_dict in enumerate(self.schedule["tasks"], 1):
            task = Task(**task_dict)
            explanation += f"{i}. {task.title} ({task.duration_minutes} min) - Priority: {task.priority}\n"
        
        explanation += f"\nTotal duration: {self.schedule['total_duration']} minutes\n"
        explanation += f"Fits schedule: {'Yes' if self.schedule['is_valid'] else 'No'}\n"
        
        return explanation
    
    def validate_schedule(self) -> bool:
        """Check if schedule fits owner's availability."""
        total_duration = sum(task.duration_minutes for task in self.tasks)
        available_time = self.owner.get_available_time()
        return total_duration <= available_time
    
    def to_dict(self) -> Dict:
        """Serialize full schedule to dictionary."""
        return {
            "pet": self.pet.to_dict(),
            "owner": self.owner.to_dict(),
            "tasks": [task.to_dict() for task in self.tasks],
            "schedule": self.schedule
        }


if __name__ == "__main__":
    # Example usage
    mochi = Pet(name="Mochi", species="dog", age=3, health_conditions=[])
    jordan = Owner(name="Jordan", availability_hours={"morning": 60, "afternoon": 90, "evening": 45})
    
    morning_walk = Task(title="Morning walk", duration_minutes=20, priority="high", category="walk")
    feeding = Task(title="Feeding", duration_minutes=10, priority="high", category="feeding")
    playtime = Task(title="Playtime", duration_minutes=30, priority="medium", category="enrichment")
    
    scheduler = Scheduler(pet=mochi, owner=jordan)
    scheduler.add_task(morning_walk)
    scheduler.add_task(feeding)
    scheduler.add_task(playtime)
    
    scheduler.generate_schedule()
    print(scheduler.get_schedule_explanation())
