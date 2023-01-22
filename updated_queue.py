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
        The function to compare two events based on their timestamp.

        Parameters
        ----------
        other
            The other event to compare to.
        
        Returns
        -------
        bool
            True if the timestamp of the current event is less than the timestamp
        '''
        return self.timestamp < other.timestamp

    def run(self, schedule):
        '''
        The function to run the event by calling the function with the arguments
        and keyword arguments.
        Parameters
        ----------
        schedule
            The schedule object that contains the event.
            
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
        The function to add an event to the schedule at a specific time.

        Parameters
        ----------
        timestamp : float
            The time at which the event should run.
        function : callable
            The function to call when running the event.
        args : tuple
            The positional arguments to pass to the function.
        kwargs : dict
            The keyword arguments to pass to the function.
        
        Returns
        -------
        None
        '''
        heapq.heappush(
            self.priority_queue,
            Event(timestamp, function, *args, **kwargs))
    
    def add_event_after(self, interval, function, *args, **kwargs):
        '''
        The function to add an event to the schedule after a specific interval.

        Parameters
        ----------
        interval : float
            The time after which the event should run.
        function : callable
            The function to call when running the event.
        args : tuple
            The positional arguments to pass to the function.
        kwargs : dict
            The keyword arguments to pass to the function.
        
        Returns
        -------
        None
        '''
        self.add_event_at(self.now + interval, function, *args, **kwargs)
    
    def next_event_time(self):
        '''
        The function to return the time at which the next event will run.

        Parameters
        ----------
        None

        Returns
        -------
        float
            The time at which the next event will run.
        '''
        return self.priority_queue[0].timestamp

    def run_next_event(self):
        '''
        The function to run the next event in the schedule.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        event = heapq.heappop(self.priority_queue)
        self.now = event.timestamp
        event.run(self)
        
    def __repr__(self):
        '''
        The function to return a string representation of the schedule.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string representation of the schedule.
        '''
        return (
            f'Schedule() at time {self.now}min ' +
            f'with {len(self.priority_queue)} events in the queue')
    
    def print_events(self):
        '''
        The function to print the schedule and the events in the queue.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        print(repr(self))
        for event in sorted(self.priority_queue):
            print(f'  ⏱ {event.timestamp}min: {event.function.__name__}')


#Add a MGC class to simulate
class Queue_MGC:
    '''
    The class stores the information of the queue.

    Attributes
    ----------
    service_distribution : scipy.stats.rv_continuous
        The distribution of the service time.
    manager : Manager
        The manager object that contains the queue.
    arrival_times : list
        The list of arrival times of the customers.
    departure_times : list
        The list of departure times of the customers.
    queue_length : int
        The number of customers in the queue.
    busy : bool
        The indication of whether the queue is busy.

    Methods
    -------
    _init_(self, service_distribution, manager)
        Initialize the queue.
    __lt__(self, other)
        The function to compare the queue length of two queues.
    add_customer(self, schedule)
        The function to add a customer to the queue.
    start_service(self, schedule)
        The function to start the service of the queue.
    end_service(self, schedule)
        The function to end the service of the queue.

    '''
    def _init_(self, service_distribution, manager):
        self.service_distribution = service_distribution
        self.manager = manager
        self.arrival_times = []
        self.departure_times = []
        self.queue_length = 0
        self.busy = False
    
    def __lt__(self, other):
        '''
        The function to compare the queue length of two queues.

        Parameters
        ----------
        other : Queue_MGC
            The other queue to compare with.

        Returns
        -------
        bool
            The indication of whether the queue length of the current queue is
        '''
        return self.queue_length < other.queue_length


    def add_customer(self, schedule):
        '''
        The function to add a customer to the queue.

        Parameters
        ----------
        schedule : Schedule
            The schedule object that contains the queue.

        Returns
        -------
        None
        '''
        #add customer to the queue
        self.queue_length += 1
        # heapq.heappush(self.arrival_times, schedule.now)
        self.arrival_times.append(schedule.now)
        #if the queue is not busy, start serving the customer
        if not self.busy:
        #     self.start_service(schedule)

        # else:
            # schedule.add_event_after(0, self.add_customer, customer)
            schedule.add_event_after(0, self.start_service)
        
    def start_service(self, schedule):
        '''
        The function to start serving a customer. It's accounts for the probability of the manager being called.
        
        Parameters
        ----------
        schedule : Schedule
            The schedule object that contains the queue.

        Returns
        -------
        None
        '''
        #start serving the customer
        self.queue_length -= 1
        self.busy = True
        service_time = self.service_distribution.rvs()
        # Probability of the manager being called
        schedule.add_event_after(service_time, self.end_service)
        if random.random() < 0.05:
            schedule.add_event_after(service_time, self.manager.add_customer)

    def end_service(self, schedule):
        '''
        The function to end serving a customer.

        Parameters
        ----------
        schedule : Schedule
            The schedule object that contains the queue.

        Returns
        -------
        None
        '''
        #end serving the customer
        self.busy = False
        self.departure_times.append(schedule.now)
        #if there are more customers in the queue, start serving the next customer
        if self.queue_length > 0:
            schedule.add_event_after(0, self.start_service)

class Manager(Queue_MGC):
    '''
    The class stores the information of the manager.

    Attributes
    ----------
    Queue_MGC : Queue_MGC
        The queue class that contains the manager.



    Methods
    -------
    _init_(self, service_distribution)
        Initialize the que that the manager will use

    start_service(self, schedule)
        The function to start serving a customer.
    .
    '''
    def __init__(self):
        super().__init__()

    def start_service(self, schedule):
        #start serving the customer
        self.queue_length -= 1
        self.busy = True
        service_time = self.service_distribution.rvs()
        schedule.add_event_after(service_time, self.end_service)

#add the manager to teh grocery store class
class GroceryStore_MGC:
    '''
    The class stores the information of the grocery store.

    Attributes
    ----------
    manager : Manager
        The manager object that contains the queue.
    queues : list
        The list of queues in the grocery store.
    arrival_distribution : scipy.stats.rv_continuous
        The distribution of the arrival time.

    '''
    def __init__(self, arrival_distribution, service_distribution, manager_distribution, queue_count):
        self.manager = Manager(manager_distribution)
        self.queues = [Queue_MGC(service_distribution, self.manager)] * queue_count
        self.arrival_distribution = arrival_distribution

    def add_customer(self, schedule):
        # Add this customer to the queue
        queue = min(self.queues)
        queue.add_customer(schedule)

        # Schedule when to add another customer
        schedule.add_event_after(
            self.arrival_distribution.rvs(),
            self.add_customer)

    def run(self, schedule):
        # Schedule when the first customer arrives
        schedule.add_event_after(
            self.arrival_distribution.rvs(),
            self.add_customer)
        

def run_simulation(arrival_distribution, service_distribution, manager_distribution, queue_count, run_until):
    schedule = Schedule()
    grocery_store = GroceryStore_MGC(arrival_distribution, service_distribution, manager_distribution, queue_count)
    grocery_store.run(schedule)
    while schedule.next_event_time() < run_until:
        schedule.run_next_event()
    return grocery_store
        

arrival_distribution = sts.expon(scale=1/2)
service_distribution = sts.expon(scale=1/3)
manager_distribution = sts.expon(scale=1/2)
queue_count = 3
run_until = 1000
run_simulation(arrival_distribution=arrival_distribution, service_distribution=service_distribution, manager_distribution=manager_distribution, queue_count=queue_count, run_until=run_until)
