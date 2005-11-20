# -*- coding: UTF-8 -*-
import os, os.path, thread
import xml.dom.minidom as minidom

import task

def load_tasks():
    tasks = {}
    for task_file in ["tasks/"+tmp for tmp in os.listdir("tasks") if tmp[-3:] == "xml"]:
        dom = minidom.parse(task_file)
        curr_task = dom.firstChild
        id = curr_task.getAttribute("id")
        tasks[id] = {}
        tasks[id]["name"] = curr_task.getElementsByTagName("name")[0].childNodes[0].nodeValue
        tasks[id]["command"] = curr_task.getElementsByTagName("command")[0].childNodes[0].nodeValue
        tasks[id]["needs"] = {}
        for need in [tmp for tmp in curr_task.getElementsByTagName("needs")[0].childNodes if tmp.nodeType == 1]:
            tasks[id]["needs"][need.nodeName] = {}
            for key, val in need.attributes.items():
                tasks[id]["needs"][need.nodeName][key] = val
        tasks[id]["dependencies"] = {}
        for dependency in curr_task.getElementsByTagName("dependency"):
            tasks[id]["dependencies"][dependency.getAttribute("id")] = []
            for condition in dependency.getElementsByTagName("returncondition"):
                tasks[id]["dependencies"][dependency.getAttribute("id")].append((condition.getAttribute("compare"), condition.getAttribute("value")))
    return(tasks)

def create_jobs(tasks):
    jobs = {}
    for id, params in tasks.items():
        jobs[id] = task.Task(params["command"], params["dependencies"], params["needs"])
    return(jobs)

def launch(jobs):
    lst_jobs = jobs.keys()
    lst_jobs.sort()
    while True:
        for curr_job in lst_jobs:
            thread.start_new_thread(jobs[curr_job].run, (jobs, curr_job))
        finished = True
        for curr_job in lst_jobs:
            if jobs[curr_job].getTodo():
                finished = False
                break
        if finished:
            for curr_job in lst_jobs:
                if jobs[curr_job].getStrStatus() == "ABORT":
                    print curr_job, jobs[curr_job].getAbort_reason()
            break

if __name__ == "__main__":
    launch( create_jobs( load_tasks() ) )

