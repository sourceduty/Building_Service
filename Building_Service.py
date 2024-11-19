# Building Service Program
# Copyright (C) 2024, Sourceduty - All Rights Reserved.
# Customizable tool for managing building services, system services, and maintenance plans.

import json
import datetime
import schedule
import time

class BuildingServiceProgram:
    def __init__(self):
        self.buildings = {}
        self.maintenance_schedule = {}
    
    def add_building(self, building_id, name, location, systems):
        self.buildings[building_id] = {
            "name": name,
            "location": location,
            "systems": systems,
            "service_history": {}
        }
    
    def log_service(self, building_id, system, service_date, notes):
        if building_id in self.buildings:
            if system not in self.buildings[building_id]["service_history"]:
                self.buildings[building_id]["service_history"][system] = []
            self.buildings[building_id]["service_history"][system].append({
                "date": service_date,
                "notes": notes
            })
    
    def schedule_maintenance(self, building_id, system, task, frequency):
        if building_id in self.buildings:
            if building_id not in self.maintenance_schedule:
                self.maintenance_schedule[building_id] = []
            self.maintenance_schedule[building_id].append({
                "system": system,
                "task": task,
                "frequency": frequency
            })
            schedule.every(frequency).days.do(self.execute_task, building_id, system, task)
    
    def execute_task(self, building_id, system, task):
        print(f"Executing task '{task}' for system '{system}' in building '{self.buildings[building_id]['name']}'")
    
    def display_schedule(self):
        for building_id, tasks in self.maintenance_schedule.items():
            print(f"Maintenance Schedule for {self.buildings[building_id]['name']}:")
            for task in tasks:
                print(f"  System: {task['system']}, Task: {task['task']}, Frequency: {task['frequency']} days")
    
    def save_data(self, filename="building_data.json"):
        with open(filename, 'w') as f:
            json.dump({"buildings": self.buildings, "maintenance_schedule": self.maintenance_schedule}, f)
    
    def load_data(self, filename="building_data.json"):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.buildings = data["buildings"]
            self.maintenance_schedule = data["maintenance_schedule"]

# Example usage:
program = BuildingServiceProgram()
program.add_building(1, "Office Tower", "Downtown", ["HVAC", "Plumbing", "Electrical"])
program.log_service(1, "HVAC", "2024-11-18", "Routine filter replacement")
program.schedule_maintenance(1, "HVAC", "Filter Check", 30)
program.display_schedule()
program.save_data()

while True:
    schedule.run_pending()
    time.sleep(1)
