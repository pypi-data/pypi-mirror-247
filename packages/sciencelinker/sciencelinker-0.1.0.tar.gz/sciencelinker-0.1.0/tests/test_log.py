from sciencelinker import processing_log as log

# Trivial example that documents how to solve a*(b+c) with 3*(2+4)

a=3
b=2
c=4

# Outer processing step
in1 = log.DataItem(name='a', value=a, description='Factor to multiply the parentheses with')
in2 = log.DataItem(name='b', value=b, description='First summand from parentheses')
in3 = log.DataItem(name='c', value=c, description='Second summand from parentheses')
log.start_procedure(name='Solve a*(b+c)', l_inputs=[in1,in2,in3],method_url='https://...', log_name='Math problem')

# Add a note what is about to happen
log.add_note('First we solve b+c then we multiply it with a', log_name='Math problem')

# First inner processing step
log.start_procedure(name='Solve b+c', l_inputs=[in2, in3], method_url='https://en.wikipedia.org/wiki/Addition', log_name='Math problem')
d = b+c
out1 = log.DataItem(name='d', value=d, description='Result of the addition')
log.end_procedure(l_outputs=[out1], log_name='Math problem')

# Add notes to explain what happens
log.add_note(f"The result of the addition was d={d}.", log_name='Math problem')
log.add_note('Now the multiplication', log_name='Math problem')

# Second inner processing step
log.start_procedure(name='Solve a*d', l_inputs=[in1, out1], method_url='https://en.wikipedia.org/wiki/Multiplication', log_name='Math problem')
e = a*d
out2 = log.DataItem(name='e', value=e, description='Result of the Multiplication')
log.end_procedure(l_outputs=[out2], log_name='Math problem')

# Add a note explaining that we are finished
log.add_note(f"The result of the multiplication was e={e}.", log_name='Math problem')

out3 = out2.clone(description='Result of the math problem')
log.end_procedure(l_outputs=[out3], log_name='Math problem')

s = log.write_log(output_format='html', log_name='Math problem')
print(s)

