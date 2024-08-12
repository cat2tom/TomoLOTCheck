


import pyperclip as clip

from datetime import datetime

import sys

import os




sys.path.append("C:\\AitangResearch\\") # add the root directory to python path.


from TomoLOTCheck.pdfLib.report import *  # import the class from report lib.

from TomoLOTCheck.configureFile.configFile import pdf_dir




class ClipBoard(object):
    
    '''
    Responsiblity: read the content from clipboard and process the data to provide the core 
    functions needed by the program.
    
    '''
    
    
    def getOpentimeCount(self):
      
        '''
          Fucntion: To get the contents from clipboard.
          Input: no
        
          output:  tuple=(opentiem, count)  
        
        '''
  
    
        # get all contents in string format
        
        from_clip=clip.paste()
        
        # use newline character to get each leaf opentime-count pair in string format
        
        tmp1=from_clip.split('\n')
        
        tmp2_open_time=[] # to hold the open time
        
        tmp2_leaf_count=[] # to hold count.
        
        tmp1=tmp1[1:]
        
        for each in tmp1:
            
            tmp3=each.split(',') # split open time from count.
            
            
            
            # get the count to get rid of zero element.      
                  
            if len(tmp3)==2: # get the element if it is not a pair of number.
                
                                   
                                        
                    open_time=float(tmp3[0])
                    
                    leaf_count=float(tmp3[1])
                    
                    tmp2_open_time.extend([open_time])
                    
                    tmp2_leaf_count.extend([leaf_count])
                    
                  
        return (tuple(tmp2_open_time),tuple(tmp2_leaf_count)) 
        
    
    def isFraction(self):
        
        '''
        Responsibility: to judge if the content in clipboard is fraction or optimisation file using 15 ms threshold.
        
        Input: none
        
        Output: 'F'-fraction
                'O'-Optimisation.
        
        '''
        
        # get the open time
        
        (open_time, count)=self.getOpentimeCount()
        
        tmp1_time=[each for each in open_time if each<15] # get element less than 15ms. 
        
        tmp2_count=list(count[:len(tmp1_time)]) # get the count element
        
               
        # get the the first element
        
        file_type=''
        
        if all(tmp2_count): # if true is F and false is O
                                             
                file_type='O'  # it is an optimisation.
        else:
                
                file_type='F'  # it is an fraction.
                
    
        return file_type
        
           
    def get100msLeaves(self):
        
        '''
         
        Responsibility: to get the average leaf number whose open time less than 100ms.
        Input: none
        
        output: average numbe of leaves whose open time less than 100ms for optimisaton and fractionation.
        
        
        '''
    
        
        # get file time
        
        file_type=self.isFraction()
        
        # get the open time and count.
        
        (open_time,count)=self.getOpentimeCount()
        
        open_time=list(open_time)
        
        count=list(count)
       
        if file_type=='F':
           
           # get open time less than 100ms
           
            tmp1=[each for each in open_time if each <100 ]
            
           # get leaf count
           
            tmp2=count[:len(tmp1)]
            
           # the leaf count
           
            mean_leaf_count=float(sum(tmp2))/float(len(tmp2))
            
        if file_type=='O':
               
            #  get rid of open times less than 15ms   
            
            tmp5=zip(open_time, count) # zip time-count together.
            
            tmp6=[each for each in tmp5 if each[0]>15] # to get all element whose open time is greater than 15ms.
            
           
           
            # get the counts less than 100ms
            
            tmp9=[each for each in tmp6 if each[0]<100]
            
                    
            # to get unzipped time-count between 15 and 100 ms.
            
            (unzipped_time, unzipped_count)=zip(*tmp9)
            
                 
                        
            mean_leaf_count=float(sum(unzipped_count))/float(len(unzipped_count))
            
            
                                        
        
        return mean_leaf_count
            
          
    def writeToTxtFile(self,MRN='',patient_name=''):
        '''
        Write to txt file. 
        Input: MRN or patient name.
        output: the file name is named after MRN if given or patient name if given or both if both are given. Otherwise,
        the file_name is named using date time up to second.
              
        '''
        # get open-count pair
        
        (time,count)=self.getOpentimeCount()
        
        # ziped them together
        
        tmp1=zip(time, count)
        
        # changed into string separated by ','
        
        tmp2=[str(x)+','+str(y) for (x,y) in tmp1]
        
        
        
        # get file type and datetime
        
        file_type=self.isFraction() # get file type to be as the part of the file.
        
        current_date=datetime.now()
        
        current_date_time=current_date.strftime('%Y-%m-%d-%H-%M-%S')
        
        
         
        
        file_name=current_date_time+'.txt'
        
        # add the file_type
        
        if file_type=='O':
            
            file_name='Optimisation_'+file_name
            
        if file_type=='F':
            
            file_name='Fraction_'+file_name
            
        
        # get the file name
        
        if  MRN and (not patient_name):
            
            file_name=MRN+'_'+file_name
            
            
        if  (not MRN) and patient_name:
            
            file_name=patient_name+'_'+file_name
            
        if MRN and patient_name:
            
            file_name=MRN+'_'+patient_name+'_'+file_name
            
        
        # determine file name
        
        f=open(file_name,'w')
        
        for each in tmp2:
            
            f.write(each+'\n')
        
        f.close
        
        return file_name
    
    def writeToPDFFile(self,pdfDir='',MRN='',patient_name=''):
       
        '''
      To write the results and recommendation to one page pdf report using report library.
      Input: lot_time-the averaged of leaf count whose open time is less than 15ms. 
             MRN, patient_name-patient info.
             
      output:              
        
       '''
        # # establish the file name using MRN or patient_name, or date-time and file type as did for txt file.
        
        # get file type and datetime
               
        file_type=self.isFraction() # get file type to be as the part of the file.
                 
        current_date=datetime.now()
                 
        current_date_time=current_date.strftime('%Y-%m-%d-%H-%M-%S') # for file name.
        
        current_date_time2=current_date.strftime('%Y.%m.%d.%H.%M.%S') # for report.
                 
                         
        file_name=current_date_time+'.pdf'
                 
        # add the file_type
                 
        if file_type=='O':
                     
            file_name='Optimisation_'+file_name
                     
        if file_type=='F':
                     
            file_name='Fraction_'+file_name
                     
                 
        # get the file name
                 
        if  MRN and (not patient_name):
                     
           file_name=MRN+'_'+file_name
                     
                     
        if  (not MRN) and patient_name:
                     
            file_name=patient_name+'_'+file_name
                     
        if MRN and patient_name:
                     
            file_name=MRN+'_'+patient_name+'_'+file_name
            
        if pdf_dir:
            
            file_name=os.path.join(pdf_dir,file_name)
            
                     
        # get leaf count 
        
        leaf_count=self.get100msLeaves()
        
             
        # # establish the pdf file obj and write the content to the file.
        
        LOT_report_obj=Report(file_name)
        
        # add patient data
        
        patient_section=ReportSection("  ")
        
        patient_info=''' <para fontsize=20> <u>  <b> Patient Information: <para> <b> <u> \n'''
        
        patient_name=''' <para fontsize=15>    <b> Patient Name:  ''' +  patient_name+ '''<para> <b>  \n ''' 
        
        patient_MRN=''' <para fontsize=15>  <b> Patient MRN:  ''' + MRN + '''<para> <b>  \n '''
        
        date_time=''' <para fontsize=15>  <b> Date/time:  ''' + current_date_time2+ '''<para> <b>  \n '''
        
        
        patient_section.add_text(patient_info)
        
        patient_section.add_text(patient_name)
        
        patient_section.add_text(patient_MRN)
        
        patient_section.add_text(date_time)
        
        
       # mean leaf count.
       
        #leaf_count_section=ReportSection("Mean leaf count for current : ")
        
        if  leaf_count>1.7:
           
                leaf_count2=str(leaf_count)
             
                leaf_count2= ''' <para fontsize=20>  <font color="green"> '''+leaf_count2+'''  <para> <font>\n'''
             
        
        if  leaf_count<=1.7:
                      
                leaf_count2=str(leaf_count)
                        
                leaf_count2= ''' <para fontsize=20 > <font color="red">'''+leaf_count2+''' <para> <font> \n'''         
        
          
        
        plan_info=''' <para fontsize=20> <u>  <b> Tomo Plan information: <para> <b> <u> \n'''
        
        mean_leaf_count=''' <para fontsize=15> <b>   Mean Leaf Count:'''+leaf_count2+ '''<para>  <b> \n '''
        
        plan_type2=''
        
        if file_type=='F':
        
            plan_type2=''' <para fontsize=15> <b> File Type: '''+''' Fracton'''+ '''<para>  <b> \n '''
          
        if file_type=='O':
            
            plan_type2=''' <para fontsize=15> <b>   File Type: '''+''' Fracton'''+ '''<para>  <b> \n '''
        
        
        patient_section.add_text(plan_info)
        
        patient_section.add_text(mean_leaf_count)
        patient_section.add_text(plan_type2)


        #leaf_count_section.add_text(mean_leaf_count)
        
        #patient_section.add_text(mean_leaf_count)
         
        # recommendation section.
        
        
        recommendation1=''' <para fontsize=20> <u>  <b> Recommendation: <para> <b> <u> \n'''
        
        #recommendation_section=ReportSection("Recommendation")
        
        recommendation2=''
        
        if leaf_count<=1.7:
            
            recommendation2=''' <para fontsize=15>  <font color="red">  <b> it is recommended to adjust the pitch to reduce the average number of leaf count less than 1.7% for open time less than 100ms. </font>  <para> <b>  \n'''
        
        if leaf_count>1.7:
            
            recommendation2=''' <para fontsize=15>  <font color="green" > <b>  This Tomo plan satifies the requirements that the mean leaf accout is less than 1.7 for open time less 100ms. </font> <para> <b>  \n'''
        
        
        patient_section.add_text(recommendation1)
        patient_section.add_text(recommendation2)
        
        
        #patient_section.add_text(recommendation2)
        
        #recommendation_section.add_text(recommendation2)        

        # add all sections to the pdf files
        
        LOT_report_obj.sections.append(patient_section)
        
        #LOT_report_obj.sections.append(leaf_count_section)
        
        #LOT_report_obj.sections.append(recommendation_section)
        
        LOT_report_obj.write()
        
        return file_name  
        
        
  
   
if  __name__=='__main__':
    
    # #object
    
    clip_obj=ClipBoard()
    
    
    # #test get Opentiem and count.
    
    (open2,count)=clip_obj.getOpentimeCount()
    
    #print open
    #print count
    
    # #test isFraction
    
    file_type=clip_obj.isFraction()
    
    #print file_type
    
    # #test 100ms leaf
    
    mean_leaf_count=clip_obj.get100msLeaves()
    
    #print mean_leaf_count
    
    # # test writetotxt function
    
    #clip_obj.writeToTxtFile('tom,cat')
    
    # test pdf file
    
    clip_obj.writeToPDFFile()
    
    
    
    
    
    
   
    
    
    
    