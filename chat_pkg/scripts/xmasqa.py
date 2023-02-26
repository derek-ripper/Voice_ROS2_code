#!/usr/bin/env python3
################################################################################
# Filename: xmasqa.py
# Author  : Derek Ripper
# Created : 18 Dec 2022
# Purpose : Define a class to define questions and answers for Xmas 2022 Robot
#           video.
#               
################################################################################
# Updates:
# ??/???/???? by ????? - info ......
################################################################################
cname = "xmasqa "

import random
# simple routine to use instead of print() -
# To get colour coded messages for ERROR,INFO,RESULT, etc
import  py_utils_pkg.text_colours     as TC
prt = TC.Tc()

class QandA():
    def __init__(self):
        #set up questions with key words to search on
        self.questions=[
            #what is your name",
            "your name",
            
            # what would you like for christmas
            "like for christmas",
            
            #where do you live
            "you live",
            
            #tell me a christmas joke
            "christmas joke",
            
            #who is your favourite employee at B R L
            "employee",
            ]
            
        self.answers=[
                ["my name is just robot as i'm still under constuction",
                 "I'm nameless but would like to be called Marvin or Kryten given the choice",
                 "still waiting for some one to notice me to give me a name",
                ],
            
                ["a large can of w d forty please",
                 "another robot to share my lack of life with would be good",
                 "a suprise please",
                ],
                 
                ["I live in this very lonely laboratory called B R L",
                 "I live at the B R L until I can escape!",
                 "I live in Bristol but would prefer anywhere else",
                ],
                
                ["What do you call a robot that lives at the north pole? A snow-bot",
                 "What is a robot's favourite food? Microchips",
                 "Why did the robot go to the shoe shop? To get rebooted",
                 "Why does santa have three gardens? So he can              Ho Ho Ho",
                 "what kind of motor bike does santa ride?  A Holly Davidson",
                ],
                
                ["Gordon as he is a great guy and always here",
                 "Tom will be OK when he finishes building me",
                ],
            ]   
                
        self.nq = len(self.questions)   
        self.na = len(self.answers)
        
    def printme(self):
        print("Phrases in questions arrary to be searched for to get a response")
        
        for row in range(self.nq):
            print("nq row is: "+str(row)+" "+self.questions[row])
        print("\n")
        
        print("Answers array")
        for row in range(self.na):
            print("Row in Answers array    is: "+str(row))
            npa = len(self.answers[row])
            print("Number of possible answers: "+str(npa))

            for col in range(0, npa):
                print(self.answers[row][col])
            print("\n")

    def process_answer(self,stt):
        stt = stt.lower()

        if stt == "bad_recognition":
            return "Just heard some noise so please repeat your question"
            
        else:
            #search for key words in stt argument
            irow = -1
            for keyphrase in self.questions:
                irow += 1
                index = stt.find(keyphrase)
                if index > -1:
                    found = True
                    break
                else:   
                    found = False 

            if found == True:        
                # Number of Possible Answsers in the list item
                npa = len(self.answers[irow]) -1
                rancol = random.randint(0, npa)
                text2speak = self.answers[irow][rancol]
            else:
                text2speak = "Sorry but I have not been programmed for your question please try again"
                
            return (text2speak)


#################################################################################################
###                                   MAIN   PRGRAM
#################################################################################################
#
# def main():


    # qanda = QandA()
    
    # qanda.printme()
    
    # texttospeak = qanda.process_answer("your name")
    # print("Text for robot to speak:\n",texttospeak)
 



# if __name__ == '__main__':
    # try:
        # main()
    # except KeyboardInterrupt:
        # prt.warning(cname+" Cancelelld by user !")
