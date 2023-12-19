


'''
	python3 status.py "ports/find_multiple/status_1.py"
'''

import rovers.ports.find_multiple as find_multiple_ports
import rovers.ports.available as available_port
	
def check_1 ():
	ports = find_multiple_ports.beautifully (
		limits = [ 10000, 60000 ],
		amount = 10
	)
	
	assert (len (ports) == 10), len (ports)
	
	for port in ports:
		assert (available_port.check (port) == True)

	
	
checks = {
	"1": check_1 
}