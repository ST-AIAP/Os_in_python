import click
import datetime as dt
import pickle
from typing import Optional, List
from difflib import SequenceMatcher as SM
from dataclasses import dataclass

@dataclass
class Task:
	name: str = ""
	deadline: Optional[dt.date] = None
	done: bool = False
	

def _get_task_list() -> List[Task]:
    try:
        return pickle.load(open("reminder.p","rb"))
    except Exception:
        return []
        

def _save_task_list(task_list: List[Task]) -> None:
    pickle.dump(task_list,open("reminder.p","wb"))
    

def _overdue(deadline:Optional[dt.date]) -> bool:
    if deadline is None:
        return False
        
    if deadline < dt.date.today():
        return True
        
def _to_date(deadline:str) -> dt.date:
    try:
        return dt.date.fromisoformat(deadline)
    except ValueError:
        raise ValueError(f"{deadline} is not in YYYY-MM-DD format.") from None
        

def _find_task(target:str,task_list: List[Task]) -> Optional[Task]:
    for task in task_list:
        if target.lower() == task.name.lower():
            return task
            
            
def _find_match(target:str):
    potential_match = []
    
    for task in task_list:
        score = SM(None,target,task.name).ratio()
        if score >= 0.9:
            potential_match.append((score,task.name))
            
        if potential_match:
            potential_match = sorted(potential_match,key = lambda x:x[0],reverse = True)
            click.echo(f"Cannot find {target}, here are the close matches:")
            for num, match in enumerate(potential_match):
                click.echo(f"{num+1}.{match[1]}")
                

@click.group()
def app():
    pass
    

@click.command()
@click.option("--deadline",default = None, help ="Enter date in YYYY-MM-DD format.")
@click.argument('task')

def add(task:str,deadline:str):
    """Add a task in reminders"""
    task_list+_get_task_list()
    target = _find_task(task,task_list)
    if target is not None:
        click.echo(f"'{task}' already in the list.")
        return
    if deadline is None:
        task_list.append(Task(task))
    else:
        task_list.append(Task(task,_to_date(deadline)))
    _save_task_list(task_list)


@click.command()
def list():
    """list all the task in reminder"""
    task_list = _get_task_list()