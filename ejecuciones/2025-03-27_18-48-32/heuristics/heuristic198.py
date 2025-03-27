
def heuristic(input_data):
    """Hybrid: SPT within EDD, balances machine load dynamically."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_due_dates = {}  # Earliest Due Date (EDD) calculation
    for job in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation in jobs_data[job]:
            total_processing_time += min(operation[1])
        job_due_dates[job] = total_processing_time * 2 #simple EDD
    
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        eligible_operations.sort(key=lambda x: job_due_dates[x[0]]) #EDD

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            shortest_time = float('inf')
            shortest_machine = None
            for m_idx, m in enumerate(machines):
                if times[m_idx] < shortest_time:
                    shortest_time = times[m_idx]
                    shortest_machine = m
            
            start_time = max(machine_available_times[shortest_machine], sum([op['Processing Time'] for op in scheduled_operations[job]]))
            if start_time < earliest_start:
                earliest_start = start_time
                best_op = op_num
                best_machine = shortest_machine
                best_time = shortest_time
                best_job = job

        start_time = max(machine_available_times[best_machine], sum([op['Processing Time'] for op in scheduled_operations[best_job]]))
        end_time = start_time + best_time
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = end_time

        eligible_operations.remove((best_job, best_op))
        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
