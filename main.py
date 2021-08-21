# Some Assumptions about the programs:
# Here Instead of comma(',') we have used semicolon(';') as delimiter
#  The Section Label like section 1 and section 2 are to be specified in the question no part and all the other fields are to be list empty
# For the or we have to specify the indentation and in Question we can use ***OR OR OR*** to call the or fucntion to print or there for indentation number you can use the same number as Previous For Example 
# To Create or section in subsubpart the Question_no should be x.x.x.x
# To Create or section in subpart the Question_no should be x.x.x
# To Create or section in part the Question_no should be x.x
# TO Create or section in question section Question_no should be x
# Here the 'x' in the above Four lines are to be replaced by numbers
# to End the Document APPend '***END***' Without Quotation Marks in the Question_no section to tell the program that it is the end of the document
# To go into math prinitng use $...$ to print inline and $$...$$ to print on a separate line

import csv
import re
import sys
#from icecream import ic
from doc import *
filename=sys.argv[1]
outputfile=sys.argv[2]
titles=['Title','Course Code','Course Title','Date','Time','Maximum Marks']
testpaper_titles=['Question_no','Marks','Question']
testpaper_field={}
field_des={}
flag_title=False
flag_ins=False
flag_quest=False
Instructions=[]
document=doc(filename,outputfile)
section_exp=re.compile('section',re.IGNORECASE)
with open(filename,encoding='utf8') as paper:
    paper_reader=csv.reader(paper,delimiter=';')
    for row in paper_reader:
        matches=section_exp.findall(row[0])
        
        if row[2]=='***END***':
                       #Create and Print The document as the paper is ended
            document.CompileTex()
            
        for match in matches:
            if match:
                
                document.WriteSection(row[0])
                continue
        if row[0]=='' and row[0]==' ':
            continue
        
        if(flag_quest):    # to pass all the questions
            quest=row.copy()
            
            for title in testpaper_titles:
                for que in quest:
                    testpaper_field[title]=que
                    quest.remove(que)
                    break
            if(testpaper_field['Question']=='***OR OR OR***'):
                document.WriteOrSection(testpaper_field['Question_no'])
                continue    
            document.WriteQuestions(testpaper_field)    

        elif(flag_ins):       # to get all the insturctions
            instruction=row.copy()
            for ins in instruction:
                Instructions.append(ins)
                instruction.remove(ins)
            document.WriteInstruction(Instructions)
            flag_ins=False    
                

        elif(flag_title):         #get all the header information
            fields=row.copy()
                        
            for title in titles:    # Create a Dictionary for all The Header Values
                for field in fields:
                    field_des[title]=field
                    fields.remove(field)
                    break
            document.WriteHeader(field_des)    
            flag_title=False
        # TO Check if it is the tile header    
        if row[0] in titles:
            flag_title= True
        # To Check if it is the instructions header    
        elif (row[0]=='Instructions'):
            flag_ins=True

        elif (row[0]=='Question no.'):  # To Start the quesiton section
            flag_quest=True    
        #else:
         #   document.appendfunc(row[0])


# print("resultant List: " + str(field_des))
# print('\n\nResultant Instructions: ' + str(instructions))                    
                
                      
