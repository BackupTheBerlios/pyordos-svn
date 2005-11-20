# -*- coding: UTF-8 -*-
import os, sys, time, cStringIO

WAITING = 0
RUNNING = 1
COMPLETION = 2
SUCCESS = 3
FAILURE = 4
ABORT = -1

strstatus = {WAITING: "WAITING",
             RUNNING: "RUNNING",
             COMPLETION: "COMPLETION",
             FAILURE: "FAILURE",
             ABORT: "ABORT"
            }

class Task:
    def __init__(self, command, parents, needs, status=WAITING):
        self.command = command
        self.parents = parents
        self.status = status
        self.message = ""
        self.returncode = ""
        if self.status != ABORT:
            self.todo = True
        else:
            self.todo = False
    
    def getReturnCode(self):
        return self.returncode
    
    def getCommand(self):
        return self.command
    
    def getParents(self):
        return self.parents.keys()
        
    def getConditions(self, parent):
        if parent in self.parents.keys():
            return(self.parents[parent])
        else:
            return None
        
    def getTodo(self):
        return self.todo

    def getStatus(self):
        return self.status

    def getStrStatus(self):
        return str(strstatus[self.status])

    def getAbort_reason(self):
        return self.abort_reason

    def validate(self, tasks):
        valid = False
        for parent in self.parents:
            for condition in self.getConditions(parent):
                if condition[0] == "eq":
                    valid = (tasks[parent].getReturnCode() == condition[1])
                elif condition[0] == "ne":
                    valid = (tasks[parent].getReturnCode() != condition[1])
                elif condition[0] == "lt":
                    valid = (tasks[parent].getReturnCode() <  condition[1])
                elif condition[0] == "gt":
                    valid = (tasks[parent].getReturnCode() >  condition[1])
                elif condition[0] == "le":
                    valid = (tasks[parent].getReturnCode() <= condition[1])
                elif condition[0] == "ge":
                    valid = (tasks[parent].getReturnCode() >= condition[1])
        return valid
        
    def run(self, tasks, name):
        if self.status != RUNNING and self.todo:
            self.status = RUNNING
        else:
            return
        for parent in self.parents:
            if tasks[parent].getTodo():
                self.status = WAITING
                return
            elif tasks[parent].getStatus() == FAILURE \
              or tasks[parent].getStatus() == ABORT \
              or not self.validate(tasks):
                self.status = ABORT
                self.todo = False
                if tasks[parent].getStatus() == FAILURE \
                or tasks[parent].getStatus() == ABORT:
                    self.abort_reason = "Parent error : "+parent
                else:
                    self.abort_reason = "Bad return code from parent"
                return
        if self.status == RUNNING:
            child = {}
            try:
                print "START", name, time.strftime("%c")
                (child["in"], child["out"], child["err"]) = os.popen3(self.command)
            except Exception, (errno, strerror):
                child["err"] = cStringIO.cStringIO("-"+str(errno)+" - "+strerror+"-")
                self.status = FAILURE
                self.todo = False
                return
            self.returncode = child["err"].read()
            self.status = COMPLETION
            self.todo = False
            print "END", name, time.strftime("%c")
