from icecream import ic
import re
import subprocess

class format:
    def __init__(self) -> None:
        pass
    def base(self,string):
        return f"\\begin{{{string}}} \n !data \n \end{{{string}}}\n"
    def baseline(self,string):
        return f"\\{string} !data \n"  
    def singlebaseline(self,string):
        return f"\\{string}{{ !data }}\n"
    def baseopt(self,string):          
        return f"\\begin[!option]{{{string}}} \n !data \n \end{{{string}}}\n"
    def baselineopt(self,string):
        return f"\\{string}[!option] !data\n"
    def singlebaselineopt(self,string):
        return f"\\{string}[!option]{{ !data }}\n"

    def CreateDocument(self):
        temp=self.base('document')
        temp=temp.replace('!data','!documentdata')
        return temp
    
    def CreateQuestionsSection(self):
        temp=self.base('questions')
        temp=temp.replace('!data','!questsecdata')
        return temp

    def CreatePartsSection(self):
        temp=self.base('parts')
        temp=temp.replace('!data','!partsecdata')
        return temp

    def CreateSubPartsSection(self):
        temp=self.base('subparts')
        temp=temp.replace('!data','!subpartsecdata')
        return temp

    def CreateSubSubPartsSection(self):
        temp=self.base('subsubparts')
        temp=temp.replace('!data','!subsubpartsecdata')
        return temp 

    def Center(self,Data):
        temp=self.base('center')
        temp=temp.replace('!data',Data)
        return temp

    def CreateItemList(self):
        temp=self.base('itemize')
        temp=temp.replace('!data','!itemdata')
        return temp

    def CreateQuestion(self,Data,Marks=None):
        if Marks is None:
            temp=self.baseline('question')
            temp=temp.replace('!data',Data)
            return temp
        else:
            temp=self.baselineopt('question')
            temp=temp.replace('!option',Marks)
            temp=temp.replace('!data',Data)
            return temp    

    def CreatePartQuestion(self,Data,Marks=None):
        if Marks is None:
            temp=self.baseline('part')
            temp=temp.replace('!data',Data)
            return temp
        else:
            temp=self.baselineopt('part')
            temp=temp.replace('!option',Marks)
            temp=temp.replace('!data',Data)
            return temp    
    

    def CreateSubPartQuestion(self,Data,Marks=None):   
        if Marks is None:
            temp=self.baseline('subpart')
            temp=temp.replace('!data',Data)
            return temp
        else:
            temp=self.baselineopt('subpart')
            temp=temp.replace('!option',Marks)
            temp=temp.replace('!data',Data)
            return temp    
             

    def CreateSubSubPartQuestion(self,Data,Marks=None):
        if Marks is None:
            temp=self.baseline('subsubpart')
            temp=temp.replace('!data',Data) 
            return temp
        else:
            temp=self.baselineopt('subsubpart')
            temp=temp.replace('!option',Marks)
            temp=temp.replace('!data',Data)
            return temp   

    def CreateItem(self,Data):
        temp=self.baseline('item')
        temp=temp.replace('!data',Data)
        return temp

    def InsertImage(self,ImageName,options:str=None,position:str='H',caption:str=None):
        temp_image=f'\\begin{{figure}}[{position}] \n \\centering !figuredata \n \\end{{figure}}'
        if caption:
            temp_caption=self.singlebaseline('caption')
            temp_caption=temp_caption.replace('!data',caption)
            temp_image=temp_image.replace('!figuredata','!figuredata \n'+temp_caption)
        if options is None:
            temp=self.singlebaselineopt('includegraphics')
            temp=temp.replace('!option','width=0.3\\textwidth')
            temp=temp.replace('!data',ImageName)
            temp_image=temp_image.replace('!figuredata',temp)
            return temp_image
        else:
            temp=self.singlebaselineopt('includegraphics')
            temp=temp.replace('!option',options)
            temp=temp.replace('!data',ImageName)
            temp_image=temp_image.replace('!figuredata',temp)
            return temp_image    
    
    def Bold(self,Data):
        temp=self.singlebaseline('textbf')
        temp=temp.replace('!data',Data)
        return temp

    def Large(self,Data):
        temp=self.base('Large')
        temp=temp.replace('!data',Data)
        return temp

    def Underline(self,Data):
        temp=self.singlebaseline('underline')
        temp=temp.replace('!data',Data)
        return temp        

    def Center(self,Data):
        temp=self.base('center')
        temp=temp.replace('!data',Data)
        return temp

    def SubScript(self,base,subscript):
        temp=f'\\displaystyle'
        subscrip=f'$ {{{base}}}_{{{subscript}}} $'
        temp=temp+' '+subscrip
        return temp

    def SuperScript(self,base,superscript):
        temp=f'\\displaystyle'
        supscrip=f'$ {{{base}}}^{{{superscript}}} $'
        temp=temp+' '+supscrip
        return temp  

    
    def Options(self,Data:list,Horizontal=True,Vertical=False,optionview='bigcirc',Shapes=False):
        fin_string=f'\\checkboxchar{{$\\{optionview}$}}\n'
        if Shapes:
            
            if Vertical:
                temp=self.base('checkboxes')
                temp=temp.replace('!data','!choices')
            elif Horizontal:
                temp=self.base('oneparcheckboxes')
                temp=temp.replace('!data','!choices')    
        else:                
            
            if Vertical:
                temp=self.base('choices')
                temp=temp.replace('!data','!choices')
            elif Horizontal:
                temp=self.base('oneparchoices')
                temp=temp.replace('!data','!choices')    
        choices=' '
        for choice in Data:
            temp_choice=self.baseline('choice')
            temp_choice=temp_choice.replace('!data', choice)
            if choices==' ':
                choices=temp_choice+'\n !choicedata'
            else:
                choices=choices.replace('!choicedata',temp_choice+'\n !choicedata')
        choices=choices.replace('!choicedata',' ')
        temp=temp.replace('!choices',choices)
        if not Shapes:
            return temp
        else:    
            fin_string=fin_string+'\n'+temp
            return fin_string        


    def Integral(self,expr,LowerLimit=None,UpperLimit=None,wrt='dx'):
        empty=''
        return f'\\displaystyle'+' '+f' \\int_{{{LowerLimit if LowerLimit is not None else empty }}}^{{{UpperLimit if UpperLimit is not None else empty}}}  {expr} \\, {wrt}'

    def ContourIntegral(self,expr,path=None,wrt='dx'):
        empty=''
        return f'\\displaystyle'+' '+f' \\oint_{empty if path is None else path}  {expr}  \\, {wrt}'

    def Sum(self,expr:str,LowerLimit=None,UpperLimit=None):
        empty=''
        return f'\\displaystyle'+' '+f' \\sum_{{{empty if LowerLimit is None else LowerLimit}}}^{{{empty if UpperLimit is None else UpperLimit}}} {expr}'

    def Limit(self,expr,From=None,To=None):
        empty=''
        return f'\\displaystyle'+' '+f' \\lim_{{{empty if From is None else From}\\to{{{empty if To is None else To}}}}}  {expr}'

    def Frac(self,upper=None,lower=None):
        empty=''
        return f'\\displaystyle'+' '+f' \\frac{{{empty if upper is None else upper}}}{{{empty if lower is None else lower}}}'

    def SolArea(self,option='Line',height=1,unit:str='in'):
        if option=='Line':
            temp=self.singlebaseline('fillwithlines')
            temp=temp.replace('!data',str(height)+unit)
        elif option=="Box":
            temp=self.singlebaseline('makeemptybox')
            temp=temp.replace('!data',str(height)+unit)
                
        elif option=='Dotted':
            temp=self.singlebaseline('fillwithdottedlines')
            temp=temp.replace('!data',str(height)+unit)
        elif option=='Grid':
            temp=self.singlebaseline('fillwithgrid')
            temp=temp.replace('!data',str(height)+unit)        
        elif option=='Mcq':
            temp=self.baseline('answerline')
            temp=temp.replace('!data',' ')   
        return temp

    def NewPage(self):
        temp=self.baseline('newpage')
        temp=temp.replace('!data',' ')
        return temp
    def NewLine(self):
        return f'\\\\'
    def AnsSpace(self,ans:str=None,size:float=None,unit:str='in'):
        if ans is not None:
            if size is None:
                return f'\\fillin[{ans}]'
            else:
                return f'\\fillin[{ans}][{str(size)+unit}]'
        else:
            if size is None:
                return  f'\\fillin'
            else:
                return f'\\fillin[][{str(size)+unit}]' 

    def GradTable(self,row=1,part:str='questions',questionssub:str=None,pagesub:str=None,pointssub:str=None,scoresub:str=None,totalsub:str=None):
        fintemp=''
        if questionssub is not None:
            temp=self.singlebaseline('hqword')
            temp=temp.replace('!data',questionssub)
            fintemp+=temp+'\n'
        if pagesub is not None:
            temp=self.singlebaseline('hpgword')
            temp=temp.replace('!data',pagesub)
            fintemp+=temp+'\n'    
        if pointssub is not None:
            temp=self.singlebaseline('hpword')
            temp=temp.replace('!data',pointssub)
            fintemp+=temp+'\n'    
        if scoresub is not None:
            temp=self.singlebaseline('hsword')
            temp=temp.replace('!data',scoresub)
            fintemp+=temp+'\n'    
        if totalsub is not None:
            temp=self.singlebaseline('htword')
            temp=temp.replace('!data',totalsub)
            fintemp+=temp+'\n'    
        temp_grade_table=f'\\multirowgradetable{{{row}}}[{part}]'  
        fintemp=fintemp+temp_grade_table 
        fintemp=self.Center(fintemp)
        return fintemp

    def CombGradTable(self,row=1,part:str='questions',questionssub:str=None,pagesub:str=None,pointssub:str=None,scoresub:str=None,totalsub:str=None):
        fintemp=''
        if questionssub is not None:
            temp=self.singlebaseline('hqword')
            temp=temp.replace('!data',questionssub)
            fintemp+=temp+'\n'
        if pagesub is not None:
            temp=self.singlebaseline('hpgword')
            temp=temp.replace('!data',pagesub)
            fintemp+=temp+'\n'    
        if pointssub is not None:
            temp=self.singlebaseline('hpword')
            temp=temp.replace('!data',pointssub)
            fintemp+=temp+'\n'    
        if scoresub is not None:
            temp=self.singlebaseline('hsword')
            temp=temp.replace('!data',scoresub)
            fintemp+=temp+'\n'    
        if totalsub is not None:
            temp=self.singlebaseline('htword')
            temp=temp.replace('!data',totalsub)
            fintemp+=temp+'\n'
        temp_grade_table=f'\\multirowcombinedgradetable{{{row}}}[{part}]'
        fintemp+=temp_grade_table   
        fintemp=self.Center(fintemp)
        return fintemp

    def ColGradTable(self,col=1,part:str='questions',questionssub:str=None,pagesub:str=None,pointssub:str=None,scoresub:str=None,totalsub:str=None):
        fintemp=''
        if questionssub is not None:
            temp=self.singlebaseline('vqword')
            temp=temp.replace('!data',questionssub)
            fintemp+=temp+'\n'
        if pagesub is not None:
            temp=self.singlebaseline('vpgword')
            temp=temp.replace('!data',pagesub)
            fintemp+=temp+'\n'    
        if pointssub is not None:
            temp=self.singlebaseline('vpword')
            temp=temp.replace('!data',pointssub)
            fintemp+=temp+'\n'    
        if scoresub is not None:
            temp=self.singlebaseline('vsword')
            temp=temp.replace('!data',scoresub)
            fintemp+=temp+'\n'    
        if totalsub is not None:
            temp=self.singlebaseline('vtword')
            temp=temp.replace('!data',totalsub)
            fintemp+=temp+'\n'  
        temp_grade_table=f'\\multicolumngradetable{{{col}}}[{part}]'   
        fintemp+=temp_grade_table
        fintemp=self.Center(fintemp)
        return fintemp

    def CombColGradTable(self,col=1,part:str='questions',questionssub:str=None,pagesub:str=None,pointssub:str=None,scoresub:str=None,totalsub:str=None):
        fintemp=''
        if questionssub is not None:
            temp=self.singlebaseline('vqword')
            temp=temp.replace('!data',questionssub)
            fintemp+=temp+'\n'
        if pagesub is not None:
            temp=self.singlebaseline('vpgword')
            temp=temp.replace('!data',pagesub)
            fintemp+=temp+'\n'    
        if pointssub is not None:
            temp=self.singlebaseline('vpword')
            temp=temp.replace('!data',pointssub)
            fintemp+=temp+'\n'    
        if scoresub is not None:
            temp=self.singlebaseline('vsword')
            temp=temp.replace('!data',scoresub)
            fintemp+=temp+'\n'    
        if totalsub is not None:
            temp=self.singlebaseline('vtword')
            temp=temp.replace('!data',totalsub)
            fintemp+=temp+'\n'
        temp_grade_table=f'\\multicolumncombinedgradetable{{{col}}}[{part}]'   
        fintemp+=temp_grade_table
        fintemp=self.Center(fintemp)
        return fintemp
          
    def Or(self):
        temp_or=self.Bold(' OR OR OR ')
        return '\n '+temp_or+'\n'

    
        
        

class doc(format):
    prequisetes=r'''\documentclass[a4paper,20pt,addpoints ]{exam}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{times}
\usepackage{graphicx}
\usepackage{float}
\usepackage{amsfonts,amssymb,amsmath}
\pointsinrightmargin
\bracketedpoints
\pagestyle{headandfoot}
\firstpageheadrule
\footrule
\setlength{\headheight}{60pt}
\extrafootheight{.7in}
'''
    Header=f'''\\lhead[\\bfseries Course Code : !coursecode \\\\ Date : !date]{{}}
\\chead[\\bfseries !collegetitle  \\vspace{{0.5cm}} \\\\ Course Title : !coursetitle \\\\
Time : !time]{{}}
\\rhead[\\bfseries Maximum Marks: !maxmarks]{{}}
\\lfoot[]{{}}
\\cfoot[]{{\\iflastpage{{\\begin{{Large}}
\\textbf{{***End of Exam***}}\\end{{Large}}}}
}}
\\rfoot[\\textbf{{Page no. \\thepage \\, of \\, \\numpages}}]{{\\textbf{{Page no. \\thepage \\, of \\numpages}}}}
'''
    paper=''' '''
    Instructions=''' '''
    questions=''' '''
    currentquestion=0
    currentpartquestion=0
    currentsubpartquestion=0
    currentsubsubpartquestion=0
    createdquestion=False
    createdpartquestion=False
    createdsubpartquestion=False
    createdsubsubpartquestion=False
    filename: str
    outputfilename: str

    def __init__(self,filen,output)->None:
        self.paper=self.prequisetes+self.Header
        self.filename=filen
        self.outputfilename=output
        print(self.filename)
        super().__init__()
    
    def Counter(self,section:str,num=None):
        if num is None:
            if section=='subsubpartno':
                num=self.currentsubsubpartquestion-1;
            elif  section=='subpartno':
                num=self.currentsubpartquestion-1;
            elif section=='partno':
                num=self.currentpartquestion-1;
            elif section=='question':
                num=self.currentquestion-1;                
        return f'\\setcounter{{{section}}}{{{num}}}';

    def WriteHeader(self,fields):
        self.paper=self.paper.replace('!coursecode',fields['Course Code'])
        self.paper=self.paper.replace('!date',fields['Date'])
        self.paper=self.paper.replace('!coursetitle',fields['Course Title'])
        self.paper=self.paper.replace('!time',fields['Time'])
        if not fields['Maximum Marks'] or fields['Maximum Marks']=='NULL':
            self.paper=self.paper.replace('!maxmarks','\\numpoints')
        else:    
            self.paper=self.paper.replace('!maxmarks',fields['Maximum Marks'])
        self.paper=self.paper.replace('!collegetitle',fields['Title'])
        self.paper=self.paper+self.base('document')
        #print('paper: \n'+self.paper)

    def WriteInstruction(self,instruction):
        self.Instructions=self.Bold('Instructions :')
        self.Instructions=self.Large(self.Instructions)
        self.Instructions+='\n'+self.CreateItemList()
        temp_append=''' '''
        for ins in instruction:
            if ins=='' or ins==' ':
                continue
            temp_ins=self.CreateItem(ins)
            temp_append+=temp_ins+'\n'
        self.Instructions=self.Instructions.replace('!itemdata',temp_append)    
        
        self.paper=self.paper.replace('!data',self.Instructions+'\n !data')
        #ic(self.paper)

    def WriteQuestions(self,quest):
        if not(self.createdquestion):
            temp=self.CreateQuestionsSection()
            self.questions=temp
            self.createdquestion=True
        print(quest['Question'])    
        if  quest['Question'] !='NULL':    
            quest['Question']=self.ExecuteFunction(quest['Question'])
        print(quest['Question'])    
        quest_no=quest['Question_no']
        quest_no=quest_no.split('.')
        
        try:
            for no in range(len(quest_no)):
                quest_no[no]=int(quest_no[no])
        except Exception:
            pass
            
        if(len(quest_no)==1):
            self.WriteQuestionsSection(quest,quest_no)

        elif (len(quest_no)==2):
            self.WritePartsSection(quest,quest_no)

        elif(len(quest_no)==3):
            self.WriteSubPartsSection(quest,quest_no)

        elif(len(quest_no)==4):
            self.WriteSubSubPartsSection(quest,quest_no)    
        else:
            self.WriteQuestionsSection(quest)
    def WriteQuestionsSection(self,quest,quest_no=[]):
            #Create a Question Section in Questions Attribute of the Class for the FIrst Time is it is Empty and Set Created Question =True
        if self.questions==' ':
            self.questions=self.CreateQuestionsSection()
            self.questions+='\n'
            self.createdquestion=True    

        if (self.createdpartquestion):
            self.EndPartQuestionSectionAppend()
            
        if (self.createdsubpartquestion):
            self.EndSubPartQuestionSectionAppend()
            
        if (self.createdsubsubpartquestion):
            self.EndSubSubPartQuestionSectionAppend()     
                       
        # Now It's The start of the new question so part,subpart and subsubpart current value is set to Zero
        self.currentpartquestion=0;self.currentsubpartquestion=0;self.currentsubsubpartquestion=0;
            # See if the Current Question Term Has Marks 
            
        if quest['Marks'] !='NULL' and quest['Question'] !='NULL':
            temp_question=self.CreateQuestion(quest['Question'],quest['Marks'])
            self.questions=self.questions.replace('!questsecdata',temp_question+'\n !questsecdata \n')
            if quest_no==[]:
                self.currentquestion=int(quest_no[0])

        elif quest['Marks'] !='NULL' and quest['Question'] == 'NULL':    
            temp_question=self.CreateQuestion('  ',quest['Marks'])
            self.questions=self.questions.replace('!questsecdata',temp_question+'\n !questsecdata \n')
            if quest_no==[]:
                self.currentquestion=int(quest_no[0])

        elif quest['Marks'] =='NULL' and quest['Question'] != 'NULL':
            temp_question=self.CreateQuestion(quest['Question'])
            self.questions=self.questions.replace('!questsecdata',temp_question+'\n !questsecdata \n')
            if quest_no==[]:
                self.currentquestion=int(quest_no[0])   

        elif quest['Marks'] =='NULL' and quest['Question'] =='NULL':
            temp_question=self.CreateQuestion('  ')
            self.questions=self.questions.replace('!questsecdata',temp_question+'\n !questsecdata \n')
            if quest_no==[]:
                self.currentquestion=int(quest_no[0]) 
        return


    def WritePartsSection(self,quest,quest_no):
        if self.createdpartquestion==False:
                temp_partquest=self.CreatePartsSection()
                self.questions=self.questions.replace('!questsecdata',temp_partquest+'\n !questsecdata \n')
                self.createdpartquestion=True

        if(self.createdsubpartquestion):
            self.EndSubPartQuestionSectionAppend()

        if(self.createdsubsubpartquestion):
            self.EndSubSubPartQuestionSectionAppend()

        self.currentsubpartquestion=0;self.currentsubsubpartquestion=0;
        if quest['Marks'] !='NULL' and quest['Question'] !='NULL':
            temp_partquestion=self.CreatePartQuestion(quest['Question'],quest['Marks'])
            self.questions=self.questions.replace('!partsecdata',temp_partquestion+'\n !partsecdata \n')
            self.currentpartquestion=int(quest_no[1])
            
        elif quest['Marks'] !='NULL' and quest['Question'] == 'NULL':
            temp_partquestion=self.CreatePartQuestion('  ',quest['Marks'])
            self.questions=self.questions.replace('!partsecdata',temp_partquestion+'\n !partsecdata \n')
            self.currentpartquestion=int(quest_no[1])
            
        elif quest['Marks'] =='NULL' and quest['Question'] != 'NULL':
            temp_partquestion=self.CreatePartQuestion(quest['Question'])
            self.questions=self.questions.replace('!partsecdata',temp_partquestion+'\n !partsecdata \n')
            self.currentpartquestion=int(quest_no[1])
            
        elif quest['Marks'] =='NULL' and quest['Question'] =='NULL':
            temp_partquestion=self.CreatePartQuestion('  ')
            self.questions=self.questions.replace('!partsecdata',temp_partquestion+'\n !partsecdata \n')
            self.currentpartquestion=int(quest_no[1])     
        return


    def WriteSubPartsSection(self,quest,quest_no):
        if self.createdsubpartquestion==False:
            temp_subpartquest=self.CreateSubPartsSection()
            self.questions=self.questions.replace('!partsecdata',temp_subpartquest+'\n !partsecdata \n')
            self.createdsubpartquestion=True
        
        if(self.createdsubsubpartquestion):
            self.EndSubSubPartQuestionSectionAppend()

        self.currentsubsubpartquestion=0;
        if quest['Marks'] !='NULL' and quest['Question'] !='NULL':
            temp_subpartquestion=self.CreateSubPartQuestion(quest['Question'],quest['Marks'])
            self.questions=self.questions.replace('!subpartsecdata',temp_subpartquestion+'\n !subpartsecdata \n')
            self.currentsubpartquestion=int(quest_no[2])
            

        elif quest['Marks'] !='NULL' and quest['Question'] == 'NULL':
            temp_subpartquestion=self.CreateSubPartQuestion('  ',quest['Marks'])
            self.questions=self.questions.replace('!subpartsecdata',temp_subpartquestion+'\n !subpartsecdata \n')
            self.currentsubpartquestion=int(quest_no[2])
            
        elif quest['Marks'] =='NULL' and quest['Question'] != 'NULL':
            temp_subpartquestion=self.CreateSubPartQuestion(quest['Question'])
            self.questions=self.questions.replace('!subpartsecdata',temp_subpartquestion+'\n !subpartsecdata \n')
            self.currentsubpartquestion=int(quest_no[2])

        elif quest['Marks'] =='NULL' and quest['Question'] =='NULL':
            temp_subpartquestion=self.CreateSubPartQuestion('  ')
            self.questions=self.questions.replace('!subpartsecdata',temp_subpartquestion+'\n !subpartsecdata \n')
            self.currentsubpartquestion=int(quest_no[2])
        return


    def WriteSubSubPartsSection(self,quest,quest_no):    
        if self.createdsubsubpartquestion==False:
            temp_subsubpartquest=self.CreateSubSubPartsSection()
            self.questions=self.questions.replace('!subpartsecdata',temp_subsubpartquest+'\n !subpartsecdata \n')
            self.createdsubsubpartquestion=True

        if quest['Marks'] !='NULL' and quest['Question'] !='NULL':
            temp_subsubpartquestion=self.CreateSubSubPartQuestion(quest['Question'],quest['Marks'])
            self.questions=self.questions.replace('!subsubpartsecdata',temp_subsubpartquestion+'\n !subsubpartsecdata \n')
            self.currentsubsubpartquestion=int(quest_no[3])
            

        elif quest['Marks'] !='NULL' and quest['Question'] == 'NULL':
            temp_subsubpartquestion=self.CreateSubSubPartQuestion('  ',quest['Marks'])
            self.questions=self.questions.replace('!subsubpartsecdata',temp_subsubpartquestion+'\n !subsubpartsecdata \n')
            self.currentsubsubpartquestion=int(quest_no[3])

        elif quest['Marks'] =='NULL' and quest['Question'] != 'NULL':
            temp_subsubpartquestion=self.CreateSubSubPartQuestion(quest['Question'])
            self.questions=self.questions.replace('!subsubpartsecdata',temp_subsubpartquestion+'\n !subsubpartsecdata \n')
            self.currentsubsubpartquestion=int(quest_no[3])

        elif quest['Marks'] =='NULL' and quest['Question'] =='NULL':
            temp_subsubpartquestion=self.CreateSubSubPartQuestion('  ')
            self.questions=self.questions.replace('!subsubpartsecdata',temp_subsubpartquestion+'\n !subsubpartsecdata \n')
            self.currentsubsubpartquestion=int(quest_no[3]) 
        return             

    def EndQuestionSectionAppend(self):
        self.questions=self.questions.replace('!questsecdata',' ')
        self.createdquestion=False
        return

    def EndPartQuestionSectionAppend(self):
        self.questions=self.questions.replace('!partsecdata',' ')
        self.createdpartquestion=False
        return

    def EndSubPartQuestionSectionAppend(self):
        self.questions=self.questions.replace('!subpartsecdata','  ')
        self.createdsubpartquestion=False
        return

    def EndSubSubPartQuestionSectionAppend(self):
        self.questions=self.questions.replace('!subsubpartsecdata',' ')
        self.createdsubsubpartquestion=False
        return

    def WriteSection(self,sectitle):
        temp_section=self.Center(self.Bold(self.Underline(sectitle)))
        
        if(self.createdsubsubpartquestion):
            self.questions=self.questions.replace('!subsubpartsecdata','   ')
            self.createdsubsubpartquestion=False
        if(self.createdsubpartquestion):
            self.questions=self.questions.replace('!subpartsecdata',' ')
            self.createdsubpartquestion=False
        if(self.createdpartquestion):
            self.questions=self.questions.replace('!partsecdata','  ')
            self.createdpartquestion=False
        if(self.createdquestion):
            self.questions=self.questions.replace('!questsecdata',' ')
            self.paper=self.paper.replace('!data',self.questions+'\n !data')
            self.createdquestion=False
            self.questions=' '
        else:
            self.paper=self.paper.replace('!data',temp_section+'\n !data')    

        # if self.questions==' ':
        #     self.questions=self.CreateQuestionsSection()
        #     self.questions=self.questions.replace('!questsecdata',temp_section+'\n  !questsecdata \n')
        #     self.createdquestion=True
        # else:    
        #     self.questions=self.questions.replace('!questsecdata',temp_section+'\n  !questsecdata \n')
        return
        
    def WriteOrSection(self,quest):
        
        quest=quest.split('.')
        temp_or=self.Bold(' OR OR OR ')   
        if(len(quest)==4):
            temp_counter=self.Counter('subsubpartno')
            self.questions=self.questions.replace('!subsubpartsecdata',temp_or+'\n  !subsubpartsecdata  \n')
            self.questions=self.questions.replace('!subsubpartsecdata',temp_counter+'\n  !subsubpartsecdata  \n')
        elif(len(quest)==3):
            temp_counter=self.Counter('subpartno')
            self.EndSubSubPartQuestionSectionAppend()
            self.questions=self.questions.replace('!subpartsecdata',temp_or+'\n  !subpartsecdata  \n')
            self.questions=self.questions.replace('!subpartsecdata',temp_counter+'\n  !subpartsecdata  \n')
        elif(len(quest)==2):
            temp_counter=self.Counter('partno')
            self.EndSubSubPartQuestionSectionAppend()
            self.EndSubPartQuestionSectionAppend()
            self.questions=self.questions.replace('!partsecdata',temp_or+'\n !partsecdata \n')
            self.questions=self.questions.replace('!partsecdata',temp_counter+'\n !partsecdata \n')
        elif(len(quest)==1):
            temp_counter=self.Counter('question')
            self.EndSubSubPartQuestionSectionAppend()
            self.EndSubPartQuestionSectionAppend()
            self.EndPartQuestionSectionAppend()
            self.questions=self.questions.replace('!questsecdata',temp_or+'\n  !questsecdata  \n')
            self.questions=self.questions.replace('!questsecdata',temp_counter+'\n  !questsecdata  \n')
            
        return    
    
    def ExecuteFunction(self,question):
        question=question.split('//')
        loc={}
        #exp=re.compile('[a-zA-Z]+\([^\)]*\)(\.[^\)]*\))?')
        for no in range(len(question)):
            # if exp.findall(question[no]):
            #     temp=exec("self."+question[no])
            #     question[no]=temp
            try:
                question[no].strip()
                function_string="questionreplace=self."+question[no]
                
               # ic(function_string)
                #exec(function_string,{'self':self,'Bold':self.Bold,'Underline':self.Underline},loc)
                exec(function_string,{'self':self,
                'Bold':self.Bold,
                'Underline':self.Underline,
                'Large':self.Large,
                'Center':self.Center,
                'SuperScript':self.SuperScript,
                'SubScript':self.SubScript,
                'Integral':self.Integral,
                'InsertImage':self.InsertImage,
                'Sum':self.Sum,
                'Limit':self.Limit,
                'Frac':self.Frac,
                'ContourIntegral':self.ContourIntegral,
                'WriteOrSection':self.WriteOrSection,
                'Or':self.Or,
                'Options':self.Options,
                'SolArea': self.SolArea,
                'NewPage':self.NewPage,
                'NewLine':self.NewLine,
                'AnsSpace':self.AnsSpace,
                'CombGradTable':self.CombGradTable,
                'GradTable':self.GradTable,
                'ColGradTable':self.ColGradTable,
                'CombColGradTable':self.CombColGradTable,
                'Counter':self.Counter,
                },loc)
               # ic(loc['questionreplace'])
                question[no]=loc['questionreplace']
            except:    
                continue
        #ic(question)
        questionstring=' '.join(question)
      #  ic(questionstring)
        return questionstring    
                  
    def appendfunc(self,string):
        string=self.ExecuteFunction(string)
        if self.createdsubsubpartquestion:
            self.EndSubSubPartQuestionSectionAppend()
            
        if self.createdsubpartquestion:
            self.EndSubPartQuestionSectionAppend()
            
        if self.createdpartquestion:
            self.EndPartQuestionSectionAppend()
                    
        if self.createdquestion:
            self.EndQuestionSectionAppend()
        self.paper=self.paper.replace('!data',string+'\n !data \n')        

    def CompileTex(self):
        if(self.createdsubsubpartquestion):
            self.EndSubSubPartQuestionSectionAppend()
        if(self.createdsubpartquestion):
            self.EndSubPartQuestionSectionAppend()
        if(self.createdpartquestion):
            self.EndPartQuestionSectionAppend()
        if(self.createdquestion):
            self.EndQuestionSectionAppend()
        self.paper=self.paper.replace('!data',self.questions)
        print(self.paper)
        texname=self.filename.split('.')
        texname=texname[0]
        print(texname)
        with open(texname+'.tex','w',encoding='utf-8') as output:
            output.writelines(' ')
            output.writelines(self.paper)
        command=['pdflatex ',texname+'.tex','-job-name='+self.outputfilename]
        #delcommand1=['del ',self.outputfilename+'.log']
        #delcommand2=['del ',self.outputfilename+'.aux']
        subprocess.run(command,check=True)
        subprocess.run(command,check=True)
        
        return
                


# test=doc('test','test')
# string=test.WriteQuestions({'Question_no':'1.1','Marks':'20','Question':'This is the test to see if the //Or()// //Bold("test")//works or not//Options(["one","Two","Three","Four","Five"])'}) 
# string=test.Center('Test')
#print(string)

        

        

        







