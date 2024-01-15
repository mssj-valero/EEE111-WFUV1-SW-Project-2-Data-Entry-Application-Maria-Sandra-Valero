from ToDoEntry import ToDoEntry
import json
import csv

class ToDoDb:
    def __init__(self, init=False, dbName='ToDoDb.csv'):       
        self.dbName = dbName
        self.entries = []                                                                                    
        if init is False:                                                                                                
            self.entries = [ToDoEntry('monday', 'take car to garage', 'Not Started'),
                            ToDoEntry('tuesday', 'product reveal', 'In Progress'),
                            ToDoEntry('friday', 'board meeting', 'Not Started'),
                            ToDoEntry('friday', 'SEO deep dive', 'Done'),
                            ToDoEntry('wednesday', 'campaign brainstorm', 'Not Started'),
                            ToDoEntry('thursday', 'video chat with consultant', 'In Progress'),
                            ToDoEntry('weekend', 'quarter review', 'Done'),
                            ToDoEntry('weekend', 'spring schedule', 'Not Started'),
                            ToDoEntry('tuesday', 'send release email', 'Done'),
                            ToDoEntry('tuesday', 'check sale goes live', 'Not Started'),
                            ToDoEntry('wednesday', 'duvet day', 'Done'),
                            ToDoEntry('weekend', 'Frasier marathon', 'Done'),
                            ToDoEntry('thursday', 'get traffic figures', 'Done')
                            ]

    def fetch_task(self):
        tupleList = []                                                                                          
        for entry in self.entries:                                                                              
            tupleList.append([entry.day, entry.task, entry.status])                      
        return tupleList    

    def insert_task(self, day, task, status):
        newEntry = ToDoEntry(day=day.lower(), task=task, status=status)
        self.entries.append(newEntry)                                                     

    def delete_task(self, task, day):
        entries_to_remove = []
        for entry in self.entries:
            if entry.task == task and entry.day == day:
                entries_to_remove.append(entry)

        new_entries = []
        for entry in self.entries:
            if entry not in entries_to_remove:
                new_entries.append(entry)

        self.entries = new_entries
        return len(entries_to_remove) > 0


    def update_task(self, current_day, current_task, new_day, new_task, new_status):
        for entry in self.entries:
            if entry.day == current_day and entry.task == current_task:
                if self.task_exists(new_day, new_task):
                    return False
                else:
                    entry.day = new_day
                    entry.task = new_task
                    entry.status = new_status 
                    return entry 
        return None

    def export_csv(self):
        with open(self.dbName, 'w') as file:
            for entry in self.entries:
                file.write(f"{entry.day.capitalize()},{entry.task},{entry.status}\n")
    
    def export_json(self):
        json_data = []

        for entry in self.entries:
            entry_dict = {'day': entry.day.capitalize(),
                'task': entry.task,
                'status': entry.status}
            json_data.append(entry_dict)

        with open(self.dbName.replace('.csv', '.json'), 'w') as json_file:
            json.dump(json_data, json_file, indent=2)

    def import_csv(self, csv_filename):
        try:
            with open(csv_filename, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) == 3:
                        day, task, status = row
                        new_entry = ToDoEntry(day.lower(), task, status)
                        self.entries.append(new_entry)
                    else:
                        return False
        except FileNotFoundError:
            return False
        except Exception as e:
            return False

    def task_exists(self, task, day):
        for entry in self.entries:                                                                            
            if entry.task==task and entry.day==day:                                                               
                return True
        return False                                                         
