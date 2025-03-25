
def heuristic(input_data):
    """A heuristic for FJSSP using shortest processing time and earliest start."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs based on the sum of their shortest processing times
    job_priorities = {}
    for job, operations in jobs.items():
        shortest_times_sum = sum(min(times) for machines, times in operations)
        job_priorities[job] = shortest_times_sum
    sorted_jobs = sorted(job_priorities.items(), key=lambda item: item[1])

    for job_num, _ in sorted_jobs:
        schedule[job_num] = []
        for op_idx, (machines, times) in enumerate(jobs[job_num]):
            op_num = op_idx + 1
            
            # Find the best machine based on earliest available time and shortest processing time
            best_machine, best_time = None, float('inf')
            for i, machine in enumerate(machines):
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job_num])
                
                if start_time + times[i] < best_time:
                    best_machine = machine
                    best_time = start_time + times[i]
                    processing_time = times[i]

            start_time = max(machine_available_time[best_machine], job_completion_time[job_num])
            end_time = start_time + processing_time
            
            schedule[job_num].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_num] = end_time

    return schedule
