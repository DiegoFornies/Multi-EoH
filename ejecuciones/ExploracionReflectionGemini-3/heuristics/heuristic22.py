
def heuristic(input_data):
    """
    A heuristic to solve the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes jobs with fewer remaining operations and selects the fastest machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {}

    remaining_operations = {job: len(ops) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_jobs = [job for job, count in remaining_operations.items() if count > 0]
        if not eligible_jobs:
            break
        
        #Prioritize jobs with fewer remaining operations.
        job_priorities = {job: remaining_operations[job] for job in eligible_jobs}
        selected_job = min(job_priorities, key=job_priorities.get)

        if selected_job not in schedule:
            schedule[selected_job] = []

        operation_index = len(schedule[selected_job])
        machines, times = jobs_data[selected_job][operation_index]

        # Select machine that results in the earliest completion time
        best_machine = None
        min_end_time = float('inf')
        
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[selected_job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
        
        start_time = max(machine_available_times[best_machine], job_completion_times[selected_job])
        end_time = start_time + best_processing_time
        
        schedule[selected_job].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[selected_job] = end_time
        remaining_operations[selected_job] -= 1

    return schedule
