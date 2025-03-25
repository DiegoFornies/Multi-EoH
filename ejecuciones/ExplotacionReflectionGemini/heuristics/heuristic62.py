
def heuristic(input_data):
    """Schedules jobs minimizing idle time and using SPT for tie-breaking."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {j: len(jobs[j]) for j in jobs}

    scheduled_operations = {j: 0 for j in jobs}

    while any(remaining_operations.values()):
        eligible_jobs = [j for j in jobs if remaining_operations[j] > 0]
        if not eligible_jobs:
            break

        best_job = None
        best_machine = None
        earliest_start_time = float('inf')
        shortest_processing_time = float('inf')

        for job_id in eligible_jobs:
            op_idx = scheduled_operations[job_id]
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                #Primary criterion: Earliest start time.
                #Secondary criterion: shortest process time.
                if start_time < earliest_start_time or \
                   (start_time == earliest_start_time and processing_time < shortest_processing_time):

                    earliest_start_time = start_time
                    shortest_processing_time = processing_time
                    best_job = job_id
                    best_machine = machine

        op_idx = scheduled_operations[best_job]
        machines, times = jobs[best_job][op_idx]
        machine_index = machines.index(best_machine) #Find the best machine index
        processing_time = times[machine_index] #Get correcponding processing time for the machine.

        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])
        end_time = start_time + processing_time

        if best_job not in schedule:
            schedule[best_job] = []

        schedule[best_job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        remaining_operations[best_job] -= 1
        scheduled_operations[best_job] += 1

    return schedule
