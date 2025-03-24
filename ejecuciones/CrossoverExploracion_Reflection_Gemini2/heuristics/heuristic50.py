
def heuristic(input_data):
    """Schedules jobs minimizing makespan, considering machine availability and shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data.keys()}

    remaining_operations = {j: len(jobs_data[j]) for j in jobs_data.keys()}

    def find_next_eligible_operations():
        eligible_operations = []
        for job in jobs_data.keys():
            if remaining_operations[job] > 0:
                eligible_operations.append(job)
        return eligible_operations
    
    while sum(remaining_operations.values()) > 0:
        eligible_jobs = find_next_eligible_operations()

        best_job = None
        best_machine = None
        earliest_start_time = float('inf')
        shortest_processing_time = float('inf')
        
        for job in eligible_jobs:
            op_idx = len(schedule.get(job,[]))
            machines, times = jobs_data[job][op_idx]
            
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if start_time < earliest_start_time or (start_time == earliest_start_time and processing_time < shortest_processing_time):
                    best_job = job
                    best_machine = machine
                    earliest_start_time = start_time
                    shortest_processing_time = processing_time
                    best_processing_time = processing_time

        if best_job is not None:
            op_idx = len(schedule.get(best_job, [])) + 1
            start_time = earliest_start_time
            end_time = start_time + best_processing_time

            if best_job not in schedule:
                schedule[best_job] = []

            schedule[best_job].append({
                'Operation': op_idx,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[best_job] = end_time
            remaining_operations[best_job] -= 1
        else:
            break

    return schedule
