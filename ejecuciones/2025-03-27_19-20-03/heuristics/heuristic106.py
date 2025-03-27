
def heuristic(input_data):
    """Minimize makespan using a global optimization with simulated annealing."""
    import random
    import copy

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    def calculate_makespan(schedule_):
        """Calculates the makespan of a schedule."""
        machine_end_times = {m: 0 for m in range(n_machines)}
        for job in schedule_:
            for op in schedule_[job]:
                machine_end_times[op['Assigned Machine']] = max(
                    machine_end_times[op['Assigned Machine']], op['End Time'])
        return max(machine_end_times.values())

    def initial_solution():
        """Generates an initial feasible schedule."""
        schedule_ = {}
        machine_time = {m: 0 for m in range(n_machines)}
        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
        job_ops = {job: 0 for job in jobs}

        for job in jobs:
            schedule_[job] = []

        job_queue = list(jobs.keys())

        while job_queue:
            job = job_queue.pop(0)
            op_idx = job_ops[job]
            machines, times = jobs[job][op_idx]
            best_machine = None
            min_end_time = float('inf')

            for m, t in zip(machines, times):
                start_time = max(machine_time[m], job_completion_time[job])
                end_time = start_time + t
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = m
                    best_time = t

            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + best_time

            schedule_[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time
            job_ops[job] += 1
            if job_ops[job] < len(jobs[job]):
                job_queue.append(job)

        return schedule_

    def neighbor(schedule_):
        """Generates a neighboring schedule by swapping operations."""
        new_schedule = copy.deepcopy(schedule_)
        job1 = random.choice(list(jobs.keys()))
        job2 = random.choice(list(jobs.keys()))

        if len(new_schedule[job1]) > 1:
             op_index1 = random.randint(0, len(new_schedule[job1]) - 1)
        else:
            op_index1 = 0

        if len(new_schedule[job2]) > 1:
            op_index2 = random.randint(0, len(new_schedule[job2]) - 1)
        else:
             op_index2 = 0

        op1 = new_schedule[job1][op_index1]
        op2 = new_schedule[job2][op_index2]

        #Swap Machines
        temp_machine = op1['Assigned Machine']
        op1['Assigned Machine'] = op2['Assigned Machine']
        op2['Assigned Machine'] = temp_machine

        new_schedule[job1][op_index1] = op1
        new_schedule[job2][op_index2] = op2

        #Adjust timing
        machine_time = {m: 0 for m in range(n_machines)}
        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

        #Rebuild the schedule
        for job in jobs:
            for op_idx, op in enumerate(new_schedule[job]):
                 machines, times = jobs[job][op_idx]
                 assigned_machine = op['Assigned Machine']

                 processing_time = None
                 try:
                   processing_time = times[machines.index(assigned_machine)]
                 except ValueError:
                     processing_time = min(times) #If a machine change makes operation unfeasible, take minimum feasible time
                     machines_avail = jobs[job][op_idx][0]
                     assigned_machine = machines_avail[0] #If a machine change makes operation unfeasible, take 1st feasible machine
                     op['Assigned Machine'] = assigned_machine
                     processing_time = times[0] #Take the first machine time

                 start_time = max(machine_time[assigned_machine], job_completion_time[job])
                 end_time = start_time + processing_time

                 op['Start Time'] = start_time
                 op['End Time'] = end_time
                 op['Processing Time'] = processing_time

                 machine_time[assigned_machine] = end_time
                 job_completion_time[job] = end_time

                 new_schedule[job][op_idx] = op

        return new_schedule

    def acceptance_probability(old_cost, new_cost, temperature):
        """Calculates the acceptance probability."""
        if new_cost < old_cost:
            return 1.0
        else:
            return pow(2.71828, (old_cost - new_cost) / temperature)

    # Simulated Annealing parameters
    temperature = 1000.0
    cooling_rate = 0.003
    iterations = 500

    # Initial solution
    current_schedule = initial_solution()
    best_schedule = copy.deepcopy(current_schedule)
    best_makespan = calculate_makespan(best_schedule)

    # Simulated Annealing loop
    for i in range(iterations):
        new_schedule = neighbor(current_schedule)
        current_makespan = calculate_makespan(current_schedule)
        new_makespan = calculate_makespan(new_schedule)

        # Acceptance criterion
        if acceptance_probability(current_makespan, new_makespan, temperature) > random.random():
            current_schedule = new_schedule

        # Update best solution
        if new_makespan < best_makespan:
            best_schedule = copy.deepcopy(new_schedule)
            best_makespan = new_makespan

        # Cool down the temperature
        temperature *= (1 - cooling_rate)

    return best_schedule
