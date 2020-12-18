#
# module run_freefem :
#
# (c) pascal.lafon@utt.fr 11/2020
#
#  run_freefem function launch FreeFemm with model_name and input_value
#  arguments.
#
#  model_name : string of model simulation filename e.g : "mymodel.edp"
#  input_value : np.array of 4 elements containing x1,x2,x3,x4 arguments for FreeFem
#
#  model_name and the code "getARGV.idp" must lie in the current directory of execution.
#  
#
# Version 1.0 - 2020/11/25
#
import numpy as np
import subprocess
def run_freefem(model_name,input_value):
    if not hasattr(run_freefem, "input_val"):
        # LastRes does not exist (first call of the function), then initialize LastRes
        # with an dictionnary identical to input_val but with np.inf for each numerical value
        run_freefem.input_val = dict.fromkeys(input_value.keys(),np.inf)
        run_freefem.output_val = []
        run_freefem.output_cmd = []
        
    # Get machine precision for testing difference
    # of the norm of two vectors.
    tolx = (np.finfo(float).eps)**0.5   
    diff = 0.0
    for key in input_value.keys():
        # Input value must be a float
        inpval = float(input_value[key])
        # Try to read the corresponding key in the attribut of run_freefem (the last correct one)
        # if no key -> reset LastRes
        try:
            savval = run_freefem.input_val[key]
        except:
            savval = np.inf
            run_freefem.input_val = dict.fromkeys(input_value.keys(),np.inf)
            
        diff = diff + (inpval - savval)**2
    # Euclidian norm of diff :
    diff = np.sqrt(diff)
    
    if diff > tolx:
    #if (np.linalg.norm(input_value - run_freefem.input_val)>tolx):
        # Command to launch FreeFem++ with options and filename of model.
        # -nw : no windows (no plot display)
        # -v 0 : verbose level = 0 -> don't display any detail on simulation
        cmd = "FreeFem++ -nw -v 0 " + model_name + " "
        # Bluid arguments for FreeFem with input value
        #cmd_values = " "
        # Names of arguments -> see "model_name.edp" in which theses names are defined.
        for key in input_value.keys():
            cmd = cmd + str(key) + " " + str(input_value[key]) + " "
        #name_values = ["-x1 ","-x2 ","-x3 ","-x4 "]
        #for i,val in enumerate(input_value):
        #    cmd_values = cmd_values + name_values[i] + str(val)  + " "
        # Final command
        #cmd = cmd + cmd_values
        # Launch FreeFem as a shell subprocess
        # output is an object containing result of the subprocess
        # output.stdout -> message on std output
        # output.returncode -> = 0 correct termination of the subprocess
        # outpt.stderr -> error message of the subprocess.
        output_value = []  
        output=subprocess.run(cmd,capture_output=True,shell=True)      
        # Initialize output_value as an empty list
        if output.returncode==0:
            # Extract numerical values from output.stdout -> " " is a separator
            # we use split() method of string object 'output.stdout' is a string object.
            # We try float() to convert in numerical value an catch error for non numerical value

            for t in output.stdout.decode().split():
                try:
                    output_value.append(float(t))
                except ValueError:
                    pass
            # Store input and output values in attribute of run_freefem function to be use
            # in further call of run_freefem with the same input value.
            run_freefem.input_val  = input_value                    
            run_freefem.output_val = output_value
            run_freefem.output_cmd = output
        #else:
            # returncode is not 0 -> error on simulation
            #output_value = run_freefem.output_val
            #output_value = []
            #output = run_freefem.output_cmd
            #run_freefem.input_val = np.full(input_value.shape,np.inf)
            #run_freefem.output_val = []
            #run_freefem.output_cmd = []
    else:
        # input value are identical to the last correct simulation store in run_freefem attributes
        # return the stored values.
        output_value = run_freefem.output_val
        output = []
 
    
    return (np.array(output_value),output)
            
                
                
    
    
    