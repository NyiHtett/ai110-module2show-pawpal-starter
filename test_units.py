"""
Unit tests for PawPal+ System
Tests for Task, Pet, Owner, and Scheduler classes
"""

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Test cases for Task class"""
    
    def test_mark_completed_changes_status_to_true(self):
        """Test that calling mark_completed() changes completed status to True"""
        # Arrange
        task = Task(
            title="Morning walk",
            description="20-minute walk in the park",
            duration_minutes=20,
            priority="high",
            category="walk"
        )
        
        # Assert initial state
        assert task.completed == False, "Task should start as incomplete"
        
        # Act
        task.mark_completed()
        
        # Assert
        assert task.completed == True, "Task should be marked as completed"
    
    def test_mark_incomplete_changes_status_to_false(self):
        """Test that calling mark_incomplete() changes completed status to False"""
        # Arrange
        task = Task(
            title="Feeding",
            description="Feed the pet",
            duration_minutes=10,
            priority="high",
            category="feeding"
        )
        task.completed = True  # Start as completed
        
        # Act
        task.mark_incomplete()
        
        # Assert
        assert task.completed == False, "Task should be marked as incomplete"
    
    def test_get_priority_score_returns_correct_values(self):
        """Test that priority scores are correct"""
        # Arrange & Act & Assert
        high_task = Task(title="High priority", duration_minutes=10, priority="high", category="walk")
        medium_task = Task(title="Medium priority", duration_minutes=10, priority="medium", category="walk")
        low_task = Task(title="Low priority", duration_minutes=10, priority="low", category="walk")
        
        assert high_task.get_priority_score() == 3, "High priority should score 3"
        assert medium_task.get_priority_score() == 2, "Medium priority should score 2"
        assert low_task.get_priority_score() == 1, "Low priority should score 1"


class TestPet:
    """Test cases for Pet class"""
    
    def test_adding_task_increases_pet_task_count(self):
        """Test that adding a task to a pet increases the pet's task count"""
        # Arrange
        pet = Pet(name="Mochi", species="dog", age=3)
        initial_count = len(pet.get_all_tasks())
        
        # Act
        task1 = Task(title="Morning walk", duration_minutes=20, priority="high", category="walk")
        pet.add_task(task1)
        
        # Assert
        assert len(pet.get_all_tasks()) == initial_count + 1, "Task count should increase by 1"
        assert task1 in pet.get_all_tasks(), "Added task should be in pet's task list"
    
    def test_adding_multiple_tasks_increases_count_correctly(self):
        """Test that adding multiple tasks increases task count for each addition"""
        # Arrange
        pet = Pet(name="Max", species="cat", age=5)
        
        # Act
        task1 = Task(title="Feed", duration_minutes=5, priority="high", category="feeding")
        task2 = Task(title="Playtime", duration_minutes=20, priority="medium", category="enrichment")
        task3 = Task(title="Grooming", duration_minutes=15, priority="low", category="grooming")
        
        pet.add_task(task1)
        assert len(pet.get_all_tasks()) == 1, "After 1st task, count should be 1"
        
        pet.add_task(task2)
        assert len(pet.get_all_tasks()) == 2, "After 2nd task, count should be 2"
        
        pet.add_task(task3)
        assert len(pet.get_all_tasks()) == 3, "After 3rd task, count should be 3"
    
    def test_get_pending_tasks_only_returns_incomplete_tasks(self):
        """Test that get_pending_tasks() only returns incomplete tasks"""
        # Arrange
        pet = Pet(name="Buddy", species="dog", age=7)
        
        task1 = Task(title="Walk", duration_minutes=20, priority="high", category="walk")
        task2 = Task(title="Feeding", duration_minutes=10, priority="high", category="feeding")
        task3 = Task(title="Playtime", duration_minutes=30, priority="medium", category="enrichment")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Mark some tasks as completed
        task1.mark_completed()
        task3.mark_completed()
        
        # Act
        pending_tasks = pet.get_pending_tasks()
        
        # Assert
        assert len(pending_tasks) == 1, "Should have 1 pending task"
        assert task2 in pending_tasks, "task2 should be in pending tasks"
        assert task1 not in pending_tasks, "task1 should not be in pending tasks (completed)"
        assert task3 not in pending_tasks, "task3 should not be in pending tasks (completed)"


class TestOwner:
    """Test cases for Owner class"""
    
    def test_adding_pet_to_owner_increases_pet_count(self):
        """Test that adding a pet to an owner increases the pet count"""
        # Arrange
        owner = Owner(name="Jordan", availability_hours={"morning": 60, "afternoon": 90})
        initial_count = len(owner.pets)
        
        # Act
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        
        # Assert
        assert len(owner.pets) == initial_count + 1, "Pet count should increase by 1"
        assert pet in owner.pets, "Added pet should be in owner's pet list"
    
    def test_get_all_tasks_returns_tasks_from_all_pets(self):
        """Test that get_all_tasks() returns tasks from all owner's pets"""
        # Arrange
        owner = Owner(name="Alex", availability_hours={"morning": 60})
        
        pet1 = Pet(name="Buddy", species="dog", age=7)
        pet2 = Pet(name="Luna", species="cat", age=2)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        task1 = Task(title="Walk", duration_minutes=20, priority="high", category="walk")
        task2 = Task(title="Feed", duration_minutes=10, priority="high", category="feeding")
        task3 = Task(title="Playtime", duration_minutes=30, priority="medium", category="enrichment")
        
        pet1.add_task(task1)
        pet1.add_task(task2)
        pet2.add_task(task3)
        
        # Act
        all_tasks = owner.get_all_tasks()
        
        # Assert
        assert len(all_tasks) == 3, "Should return all 3 tasks from both pets"
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks
    
    def test_get_available_time_sums_all_availability_hours(self):
        """Test that get_available_time() correctly sums availability hours"""
        # Arrange
        owner = Owner(name="Jordan", availability_hours={"morning": 60, "afternoon": 90, "evening": 45})
        
        # Act
        total_time = owner.get_available_time()
        
        # Assert
        assert total_time == 195, "Total available time should be 60+90+45=195"


class TestScheduler:
    """Test cases for Scheduler class"""
    
    def test_generate_schedule_sorts_tasks_by_priority(self):
        """Test that generate_schedule sorts tasks correctly by priority"""
        # Arrange
        owner = Owner(name="Jordan", availability_hours={"morning": 120})
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        
        low_priority = Task(title="Training", duration_minutes=15, priority="low", category="enrichment")
        high_priority = Task(title="Walk", duration_minutes=20, priority="high", category="walk")
        medium_priority = Task(title="Playtime", duration_minutes=30, priority="medium", category="enrichment")
        
        pet.add_task(low_priority)
        pet.add_task(high_priority)
        pet.add_task(medium_priority)
        
        # Act
        scheduler = Scheduler(owner=owner)
        schedule = scheduler.generate_schedule()
        
        # Assert
        tasks = schedule["pets"][pet.pet_id]["tasks"]
        assert len(tasks) == 3, "Should have 3 tasks"
        assert tasks[0]["priority"] == "high", "First task should be high priority"
        assert tasks[1]["priority"] == "medium", "Second task should be medium priority"
        assert tasks[2]["priority"] == "low", "Third task should be low priority"
    
    def test_validate_schedule_returns_false_if_exceeds_available_time(self):
        """Test that validate_schedule returns False if total time exceeds available time"""
        # Arrange
        owner = Owner(name="Jordan", availability_hours={"morning": 30})  # Only 30 minutes available
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        
        task1 = Task(title="Walk", duration_minutes=20, priority="high", category="walk")
        task2 = Task(title="Playtime", duration_minutes=30, priority="high", category="enrichment")  # Total = 50 > 30
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner=owner)
        is_valid = scheduler.validate_schedule()
        
        # Assert
        assert is_valid == False, "Schedule should be invalid (50 min > 30 min available)"
    
    def test_validate_schedule_returns_true_if_within_available_time(self):
        """Test that validate_schedule returns True if total time fits available time"""
        # Arrange
        owner = Owner(name="Jordan", availability_hours={"morning": 60})  # 60 minutes available
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        
        task1 = Task(title="Walk", duration_minutes=20, priority="high", category="walk")
        task2 = Task(title="Feed", duration_minutes=10, priority="high", category="feeding")  # Total = 30 < 60
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner=owner)
        is_valid = scheduler.validate_schedule()
        
        # Assert
        assert is_valid == True, "Schedule should be valid (30 min <= 60 min available)"


# Run tests with: pytest test_units.py -v
# Or run specific test: pytest test_units.py::TestTask::test_mark_completed_changes_status_to_true -v
