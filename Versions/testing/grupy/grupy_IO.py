import os
import json


def GetInput():
	dir = []
	sg = ""
	bz_path = []
	
	cwd = os.getcwd()
	
	for file in os.listdir( cwd ) :
	
		if file.lower() == "grupy.in":
			
			f = open(file, 'r')
			
			for line in f:
				
				if "dir" in line.lower():
				
					s = line.split()
					
					for i in xrange( len( s )):
					
						if i>0 and s[i] != "=":
							
							dir.append( s[i] )
				
				if "space_group" in line.lower():
				
					s = line.split()
					
					for i in xrange( len( s )):
					
						if i>0 and s[i] != "=":
						
							sg = s[i]	
		
				if "path" in line.lower():
				
					s = line.split()
					
					if (len(s)-1)%4 != 0:
						print "Error: check your BZ path and make sure all points are labelled"
						return 0
						
					n = ((len(s)-1)/4)
					
					
					for i in xrange( 0, n ):
						
						
						label = s[ 1+ i*4]
						one = float( s[2 + i*4] )
						two = float( s[3 + i*4] )
						three = float( s[4 + i*4] )
						
						c = [ label, one, two, three]
						
						bz_path.append(c)
				
		
				
								
			f.close()

	return dir, sg, bz_path


## WRITE THE OUT FILE IN JSON FORMAT
def WriteGrupyFile ( Gout, Gin ):
	
	if Gin:
		gfile = "%s.grupy.bands.out" %Gout.prefix
	else:
		gfile = "%s.grupy.out" %Gout.prefix
	
	if os.path.isfile("%s" %(gfile) ):
		os.remove("%s" %(gfile)) #overwrite previous files
		
	#with open("%s.grupy.out"%Gout.prefix, "w") as file:
	with open('%s'%gfile, 'w') as file:
		
		## Write the high symmetry labels first
		for i in xrange( len(Gout.q_labels) ):
			label_line = {'prefix': '%s'%Gout.prefix,\
						  'label': '%s'%Gout.q_labels[i][0],\
						  'label_q': Gout.q_labels[i][1] } 
			l = json.dumps(label_line)
			file.write(l)
			file.write("\n")
	
		## Now write the data

		if Gin:
			num = len(Gin.V)
		else:
			num = 1
		for X in range( num ):
		
			for j in xrange( len(Gout.gru_data[0])-1 ):  # q points
				
				if Gin:
					data_line = {'prefix': '%s'%Gout.prefix, \
								 'Calculation': '%s'%Gin.dir[X],\
								 'Volume':'%s'%Gin.V[X],  \
								 'q':'%s'%Gout.gru_data[X][j][0], 'Omega':[] }
				
					for i in xrange(1, len(Gout.gru_data[X][j]) ):
						data_line['Omega'].append('%s'%Gout.gru_data[X][j][i])
				
				
				else:	
					data_line = {'prefix': '%s'%Gout.prefix, \
								 'Volume': None, \
								'q':'%s'%Gout.gru_data[0][j], 'Gru':[] }
			
					for i in xrange(1, len(Gout.gru_data) ):  # modes
						data_line['Gru'].append('%s'%Gout.gru_data[i][j])

				l = json.dumps(data_line)
				file.write(l)
				file.write("\n")		
	

		file.close()
	
	return 0
