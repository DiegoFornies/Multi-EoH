
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with shortest processing time
    on available machines and balances machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    
    #operations_queue is a list of tuples, each tuple represents a waiting job. Each of these tuples contains the job index and the operation list
    operations_queue = []
    for job_index in jobs:
      operations_queue.append((job_index,0))
    #ready_operations is a dictionary, where key is a tuple (job index, operation index) and value is the operation object
    ready_operations = {}
    for job_index in jobs:
      ready_operations[(job_index,0)] = jobs[job_index][0]

    solution = {} # dict of solutions

    scheduled_operations = 0
    total_operations = sum([len(operations) for operations in jobs.values()])

    while scheduled_operations < total_operations:
      #Find best ready operation
      best_operation = None
      best_machine = None
      min_end_time = float('inf')
      job_index = None
      operation_index = None
      for (j, op_idx) in ready_operations:
          machines, times = ready_operations[(j,op_idx)]
          for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine],job_completion_time[j])
            end_time = start_time + processing_time
            if end_time < min_end_time:
              min_end_time = end_time
              best_operation = ready_operations[(j,op_idx)]
              best_machine = machine
              job_index = j
              operation_index = op_idx

      # schedule
      if job_index not in solution:
        solution[job_index] = []

      start_time = max(machine_available_time[best_machine],job_completion_time[job_index])
      processing_time = best_operation[0][best_operation[0].index(best_machine)]

      solution[job_index].append({
                  'Operation': operation_index+1,
                  'Assigned Machine': best_machine,
                  'Start Time': start_time,
                  'End Time': start_time + processing_time,
                  'Processing Time': processing_time
              })

      machine_available_time[best_machine] = start_time + processing_time
      job_completion_time[job_index] = start_time + processing_time

      #Remove scheduled operation from ready_operations
      del ready_operations[(job_index,operation_index)]
      scheduled_operations += 1

      #Add new ready operation
      next_operation_index = operation_index + 1
      if next_operation_index < len(jobs[job_index]):
        ready_operations[(job_index,next_operation_index)] = jobs[job_index][next_operation_index]


    return solution
