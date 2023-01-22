#Import all the libraries

import numpy as np
import heapq
import matplotlib.pyplot as plt
import scipy.stats as sts
import random




#Code modified from session 2.1 (M/G/1 queue), modified to include manager and more than one queue

class Event:
    '''
    Store the properties of one event in the Schedule class defined below. Each
    event has a time at which it needs to run, a function to call when running
    the event, along with the arguments and keyword arguments to pass to that
    function.
    
    Attributes
    ----------
    timestamp : float
        The time at which the event should run.
    function : callable
        The function to call when running the event.
    args : tuple
        The positional arguments to pass to the function.
    kwargs : dict
        The keyword arguments to pass to the function.

    Methods
    -------
    __lt__(self, other)
        Compare two events based on their timestamp.
    run(self, schedule)
        Run the event by calling the function with the arguments and keyword


    '''
    def __init__(self, timestamp, function, *args, **kwargs):
        self.timestamp = timestamp
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __lt__(self, other):
        '''
        your docstring
        Parameters
        ----------
        other
            <include your description here>
        
        Returns
        -------
        bool
            <include your description here>
        '''
        return self.timestamp < other.timestamp

    def run(self, schedule):
        '''
        your docstring
        Parameters
        ----------
        schedule
            <include your description here>
        '''
        self.function(schedule, *self.args, **self.kwargs)


class Schedule:
    '''
    Implement an event schedule using a priority queue. You can add events and
    run the next event.
    
    The `now` attribute contains the time at which the last event was run.
    
    Attributes
    ----------
    now : float
        The time at which the last event was run.
    priority_queue : list
        The priority queue of events.

    Methods
    -------
    add_event_at(self, timestamp, function, *args, **kwargs)
        Add an event to the schedule at a specific time.
    add_event_after(self, interval, function, *args, **kwargs)
        Add an event to the schedule after a specific interval.
    next_event_time(self)
        Return the time at which the next event will run.
    run_next_event(self)
        Run the next event in the schedule.
    __repr__(self)
        Return a string representation of the schedule.
    print_events(self)
        Print the schedule and the events in the queue.


    '''
    
    def __init__(self):
        self.now = 0  
        self.priority_queue = []  
    
    def add_event_at(self, timestamp, function, *args, **kwargs):
        '''
        your docstring
        Parameters
        ----------
        <include your list and description here>
        
        Returns
        -------
        <include your list and description here>
        '''
        heapq.heappush(
            self.priority_queue,
            Event(timestamp, function, *args, **kwargs))
    
    def add_event_after(self, interval, function, *args, **kwargs):
        '''
        your docstring
        Parameters
        ----------
        <include your list and description here>
        
        Returns
        -------
        <include your list and description here>
        '''
        self.add_event_at(self.now + interval, function, *args, **kwargs)
    
    def next_event_time(self):
        return self.priority_queue[0].timestamp

    def run_next_event(self):
        '''
        your docstring
        Parameters
        ----------
        <include your list and description here>
        
        Returns
        -------
        <include your list and description here>
        '''
        event = heapq.heappop(self.priority_queue)
        self.now = event.timestamp
        event.run(self)
        
    def __repr__(self):
        return (
            f'Schedule() at time {self.now}min ' +
            f'with {len(self.priority_queue)} events in the queue')
    
    def print_events(self):
        print(repr(self))
        for event in sorted(self.priority_queue):
            print(f'  ⏱ {event.timestamp}min: {event.function.__name__}')


#Add a MGC class to simulate


class Costumer:
    def __init__(self, arrival_time, departure_time):
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.wait_time = departure_time - arrival_time


class Queue_MGC:
    def _init_(self, service_distribution, id):
        self.service_distribution = service_distribution
        self.queue_id = id
        self.customers = []
        self.arrival_times = []
        self.departure_times = []
        self.que_lenght = 0
        self.busy = False
        self.customers = []


    def add_customer(self, schedule, customer):
        #add customer to the queue
        self.customers.append(customer)
        heapq.heappush(self.arrival_times, schedule.now)
        self.que_lenght += 1
        #if the queue is not busy, start serving the customer
        if not self.busy:
            self.start_service(schedule)

        else:
            schedule.add_event_after(0, self.add_customer, customer)
        
    def start_service(self, schedule):
        #start serving the customer
        self.que_lenght -= 1
        self.busy = True
        service_time = self.service_distribution.rvs()
        schedule.add_event_after(service_time, self.end_service)

    def end_service(self, schedule):



   
#add the manager to teh grocery store class
class GroceryStore_MGC:
    pass
        

