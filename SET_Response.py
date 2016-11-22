from HandleData import sFindDataID, HandleDateType
from sFindIDFun import sFindErrID
from shared_functions import *

def Set8601(offset,*data_in) :
    tmpAPDULen=0
    output(data_in[offset+tmpAPDULen]+' —— PIID')
    tmpAPDULen=tmpAPDULen+1
    
    sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
    tmpAPDULen=tmpAPDULen+4

    sFindErrID(data_in[offset+tmpAPDULen])
    tmpAPDULen=tmpAPDULen+1
    
    return tmpAPDULen    
    

def Set8602(offset,*data_in) :
    tmpAPDULen=0
    output(data_in[offset+tmpAPDULen]+' —— PIID')
    tmpAPDULen=tmpAPDULen+1
    SetListSum=int(data_in[offset+tmpAPDULen],16)
    output(data_in[offset+tmpAPDULen]+' —— SEQUENCE OF个数='+str(SetListSum))
    tmpAPDULen=tmpAPDULen+1
    for i in range(0,SetListSum) :         
        sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
        tmpAPDULen=tmpAPDULen+4
        
        sFindErrID(data_in[offset+tmpAPDULen])
        tmpAPDULen=tmpAPDULen+1    
    
    return tmpAPDULen    
    
    
def Set8603(offset,*data_in) :
    tmpAPDULen=0
    output(data_in[offset+tmpAPDULen]+' —— PIID')
    tmpAPDULen=tmpAPDULen+1
    SetListSum=int(data_in[offset+tmpAPDULen],16)
    output(data_in[offset+tmpAPDULen]+' —— SEQUENCE OF个数='+str(SetListSum))
    tmpAPDULen=tmpAPDULen+1
    for i in range(0,SetListSum) :         
        sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
        tmpAPDULen=tmpAPDULen+4
        
        sFindErrID(data_in[offset+tmpAPDULen])
        tmpAPDULen=tmpAPDULen+1    
        
        sFindDataID(data_in[offset+tmpAPDULen : offset+tmpAPDULen + 4])
        tmpAPDULen=tmpAPDULen+4        
                        
        DataResult=data_in[offset+tmpAPDULen]
        tmpAPDULen=tmpAPDULen+1
        if DataResult=='01' :                
            output(DataResult+' —— Data')            
                                                        
            tmpLenLen=HandleDateType(tmpAPDULen+offset,1,1,*data_in)
            tmpAPDULen=tmpAPDULen+tmpLenLen    
                    
        else :
            if DataResult=='00' :    
                output(DataResult+' —— DAR')
                sFindErrID(data_in[offset+tmpAPDULen])
                tmpAPDULen=tmpAPDULen+1    
            else :    
                output(DataResult+' —— 报文有误')

        
        

    return tmpAPDULen        
    
