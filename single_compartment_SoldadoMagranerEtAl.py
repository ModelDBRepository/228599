####################################################################################
# Ca3 pyramidal cell single compartment model of the study:
# "Conditioning by Subthreshold Synaptic Input Changes the Intrinsic Firing Pattern of CA3 Hippocampal Neurons"
# Saray Soldado-Magraner, Federico Brandalise, Suraj Honnuraiah, Michael Pfeiffer, Marie Moulinier, Urs Gerber, Rodney Douglas. JNeurophysiology, 2019. 
# Written by Adrian Gutierrez agutie@ini.uzh.ch and Saray Soldado-Magraner ssaray@ini.uzh.ch
#####################################################################################  


from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt


##Create soma
soma = h.Section(name='soma')

##Modify soma's properties
soma.L = 50.0      #Length of soma (um)
soma.diam = 50.0   #Diameter of soma (um)
h.celsius = 34
h.steps_per_ms= 40 #Default neuron integration
h.dt=0.025

##Insert passive biophysical mechanisms to soma
soma.insert('pas')
soma.Ra = 150.0            #Membrane axial resistance (Ohm/cm^2) 
soma.cm = 1.41             #Membrane capacitance 
soma.g_pas = 1.0/25370.0   #Leak maximal conductance 


##Insert active biophysical mechanisms to soma (inserting .mod files)

for channel in ['na3', 'kdr', 'kap', 'km', 'kd', 'kd_slow',
		'cacum', 'cal', 'can', 'cat', 'cagk']:
	soma.insert(channel)


###############################################
# Setup model conductances
################################################3

#Which pattern are we testing
pattern = 'iBurst'


soma.gbar_na3= 0.04  # Spiking conductances
soma.gkdrbar_kdr=0.01
soma.gkabar_kap=0.07

gCa= 0.001  # Firing pattern conductances
soma.gcatbar_cat=gCa
soma.gcanbar_can=gCa
soma.gcalbar_cal=gCa
soma.gbar_cagk=0.0001
soma.gbar_km=0.0006
soma.gkdbar_kd=0.00045
soma.gkdbar_kd_slow=0


#Reversal potentials and calcium
soma.depth_cacum = 50.0/2.0     #Set the point where calcium mechanisms act (Soma diameter/2)
soma.ek = -90.0             #Potassium reversal potential (mV)
soma.ena = 55.0             #Sodium reversal potential (mV)

###############################################
# Setup recording vectors
################################################

v_vec = h.Vector()   #Membrane potential vector
t_vec = h.Vector()   #Time stamp vector

v_vec.record(soma(0.5)._ref_v)  #Recording from the soma the desired quantities
t_vec.record(h._ref_t)

###############################################
# Current Clamp
################################################

st = h.IClamp(0.5)   #Choose where in the soma to point-stimulate 
	
st.dur = 1000    #Stimulus duration (ms) 
st.delay = 100    #Stimulus delay (ms)
st.amp = 1 #Stimulus amplitude (nA)
h.tstop = 1200  #stop the simulation (ms)


##########################################################################################################
# Run the simulation
##########################################################################################################

h.v_init = -65         #Set initializing simulation voltage (mV) at t0
h.finitialize(-65)     #Set initializing voltage for all mechanisms in the section
h.fcurrent()
if h.ismembrane('cal'):  #start the 'vClamp' by setting e_pas to match v_init (NEURON Book, ch8, p11) 
	soma.e_pas = soma.v + (soma.ina + soma.ik + soma.ica)/soma.g_pas
else:
	soma.e_pas = soma.v + (soma.ina + soma.ik)/soma.g_pas
	
h.run()	


###################################################
# PLOTTING
###################################################

plt.figure(figsize=(12,7))
plt.title(pattern + ' firing pattern (IClamp)', fontweight='bold')
plt.plot(t_vec, v_vec)
plt.ylabel('Membrane voltage (mV)',fontsize=16)
plt.xlabel('Time (ms)', fontsize=16)
plt.show()






