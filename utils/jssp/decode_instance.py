def decode_instance(instance):
    lines = instance.strip().split('\n')
    
    first_line = lines[0].strip().split()
    num_jobs = int(first_line[0])
    num_machines = int(first_line[1])
    
    jobs = {}
    line_index = 1
    
    for job_id in range(1, num_jobs + 1):
        job_info = lines[line_index].strip().split()
        num_operations = int(job_info[0])
        operations = []
        
        index = 1
        for _ in range(num_operations):
            num_machines_for_op = int(job_info[index])
            index += 1
            machines_list = []
            times_list = []
            
            for _ in range(num_machines_for_op):
                machine_id = int(job_info[index])
                processing_time = int(job_info[index + 1])
                machines_list.append(machine_id)
                times_list.append(processing_time)
                index += 2
            
            operations.append((machines_list, times_list))
        
        jobs[job_id] = operations
        line_index += 1
    return {'n_jobs': num_jobs, 'n_machines': num_machines, 'jobs': jobs}