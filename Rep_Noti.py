from HandleData import sFindDataID, HandleDateType
from sFindIDFun import sFindErrID
from shared_functions import *

def Rep8801(offset,*data_in) :
	tmpAPDULen=0
	output(data_in[offset+tmpAPDULen]+' —— PIID')
	tmpAPDULen=tmpAPDULen+1
	
	
	RepSum=int(data_in[offset+tmpAPDULen],16)
	output(data_in[offset+tmpAPDULen]+' —— SEQUENCE OF个数='+str(RepSum))
	tmpAPDULen=tmpAPDULen+1
	for i in range(0,RepSum) : 			
	
		sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
		tmpAPDULen=tmpAPDULen+4	
	
		DataResult=data_in[offset+tmpAPDULen]
		tmpAPDULen=tmpAPDULen+1
		if DataResult=='01' :				
			output(DataResult+' —— Data')		
															
			tmpLenLen=HandleDateType(tmpAPDULen+offset,1,1,*data_in)
			tmpAPDULen=tmpAPDULen+tmpLenLen							
					
		else :

			sFindErrID(DataResult)
		
	
	
	
	return tmpAPDULen
	
	
	
def Rep8802(offset,*data_in) :
	tmpAPDULen=0
	output(data_in[offset+tmpAPDULen]+' —— PIID')
	tmpAPDULen=tmpAPDULen+1
	
	RepSum=int(data_in[offset+tmpAPDULen],16)
	output(data_in[offset+tmpAPDULen]+' —— SEQUENCE OF个数='+str(RepSum))
	tmpAPDULen=tmpAPDULen+1
	for ii in range(0,RepSum) : 				
	
		sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
		tmpAPDULen=tmpAPDULen+4				
		
		ListSum=int(data_in[offset+tmpAPDULen],16)
		output(data_in[offset+tmpAPDULen]+' —— RCSD，SEQUENCE OF个数='+str(ListSum))		
		tmpAPDULen=tmpAPDULen+1
		
		for i in range(0,ListSum) : 	
			DataResult=data_in[offset+tmpAPDULen]
			tmpAPDULen=tmpAPDULen+1
			if DataResult=='00' :				
				output(DataResult+' —— 第'+str(i+1)+'列OAD')
				sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
				tmpAPDULen=tmpAPDULen+4					
			else :
				if DataResult=='01' :				
					output(DataResult+' —— 第'+str(i+1)+'列ROAD')
					
					sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
					tmpAPDULen=tmpAPDULen+4						
					
					ListSum1=int(data_in[offset+tmpAPDULen],16)
					output(data_in[offset+tmpAPDULen]+' —— ROAD，SEQUENCE OF个数='+str(ListSum1))	
					tmpAPDULen=tmpAPDULen+1
					for k in range(0,ListSum1) : 
						sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
						tmpAPDULen=tmpAPDULen+4
				else :	
					output(data_in[offset+tmpAPDULen]+' —— RCSD列标识有误')		
					
		DataResult=data_in[offset+tmpAPDULen]
		tmpAPDULen=tmpAPDULen+1		

		if DataResult=='01' :				
			output(DataResult+' —— 记录数据')	
			ListSum2=int(data_in[offset+tmpAPDULen],16)
			output(data_in[offset+tmpAPDULen]+' —— M条记录，M='+str(ListSum2))	
			tmpAPDULen=tmpAPDULen+1


			tmpLenLen=HandleDateType(tmpAPDULen+offset,ListSum2,ListSum,*data_in)
			tmpAPDULen=tmpAPDULen+tmpLenLen
		else :
			if DataResult=='00' :	
				output(DataResult+' —— DAR')
				sFindErrID(data_in[offset+tmpAPDULen])
				tmpAPDULen=tmpAPDULen+1	
			else :	
				output(DataResult+' —— 报文有误')


	return tmpAPDULen