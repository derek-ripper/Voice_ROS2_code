#!/usr/bin/env python3
################################################################################
# Filename: xmasqa.py
# Author  : Derek Ripper
# Created : 18 Dec 2022
# Purpose : Define a class to define questins and answers for Xmas 2022 Robot
#           video.
#               
################################################################################
# Updates:
# ??/???/???? by ????? - info ......
################################################################################
cname = "xmasq&a "

import random

class QandA():
    def __init__(self):
        #set up questions with key words to search on
        self.questions=[
            #what is your name",
            "your name",
            
            # what would ypu like for christmas
            "like for christmas",
            
            #where do you live
            "you live",
            ]
            
        self.answers=[
                ["my name is just robot as i'm still under constuction"],
            
                ["a large can of w d forty please",
                 "another robot to share my lack of live with would be good",
                 "a suprise please"],
                 
                ["I live in this very lonely laboratory called B R L",
                 "I live at B R L",
                 "I live in Bristol but would prefer anywhere else"],
                ]   
                
        self.nq = len(self.questions)   
        self.na = len(self.answers)
        
        for row in range(self.nq):
            print("nq row is: "+str(row)+" "+self.questions[row]+"\n")
            
        for row in range(self.na):
            print("na row is: "+str(row)+"\n")
            npa = len(self.answers[row]) -1
            
            rancol = random.randint(0, npa)
            print("num of possible answers: "+str(npa))
            #for col in range(npa):
            print(self.answers[row][rancol])

    def process_answer(self,stt):
        #search for key words in stt argument
        print("stt: ",stt)
        for ans in self.questions:
            if stt.find(ans) > 1:
                print("FOUND")
                print("answers are: ",ans)
            else:
                print("NOT Found")    

        

#################################################################################################
###                                   MAIN   PRGRAM
#################################################################################################
#
def main():


    qanda = QandA()
    
    qanda.process_answer("what would ypu like for christmas")

 



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        prt.warning(cname+" Cancelelld by user !")
