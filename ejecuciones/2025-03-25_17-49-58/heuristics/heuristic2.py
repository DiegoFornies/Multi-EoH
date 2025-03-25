
def heuristic(input_data):
    """
    A heuristic for FJSSP scheduling. Assigns operations to machines
    based on Earliest Finish Time (EFT) using a greedy approach.
    Prioritizes jobs with fewer remaining operations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {job: 0 for job in jobs_data}
    remaining_operations = {job: len(ops) for job, ops in jobs_data.items()}

    scheduled_operations = [] # Keep track of scheduled operations

    while any(remaining_operations.values()):
        eligible_jobs = [job for job, count in remaining_operations.items() if count > 0]

        #Prioritize jobs with fewer remaining operations
        job_priorities = {job: remaining_operations[job] for job in eligible_jobs}
        sorted_jobs = sorted(eligible_jobs, key=lambda job: job_priorities[job])

        best_job, best_op, best_machine, best_start_time, best_end_time, best_processing_time = None, None, None, float('inf'), float('inf'), None

        for job in sorted_jobs:
            op_idx = len(jobs_data[job]) - remaining_operations[job]
            machines, times = jobs_data[job][op_idx]

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_last_end_time[job])
                end_time = start_time + processing_time

                if end_time < best_end_time:
                    best_job = job
                    best_op = op_idx + 1
                    best_machine = machine
                    best_start_time = start_time
                    best_end_time = end_time
                    best_processing_time = processing_time

        if best_job is not None:
            if best_job not in schedule:
                schedule[best_job] = []

            schedule[best_job].append({
                'Operation': best_op,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_end_time
            job_last_end_time[best_job] = best_end_time
            remaining_operations[best_job] -= 1
            scheduled_operations.append((best_job, best_op)) # Mark scheduled

    return schedule
