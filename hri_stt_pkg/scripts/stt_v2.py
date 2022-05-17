#!/usr/bin/python3
###############################################################################
# Filename: stt_v2.py
# Created : 03 August 2021
# Author  : Derek Ripper
# Purpose : 1- capture audio from microphone. this is now it's ONLY function.
#           2- Process through one of the available speech engines to transcribe
#              to text.
# History:
# Original code was stt.py and written for ERL Lisbon competition in June 2017
# This is the same BUT 2 fuctions have been renoved:
#   1-To record voice on demand - ie not contunuous listening. Was neded for
#     FBM's (functional bench marks) in ERL competions.
#   2-To batch process a diectory of prerecorded .wav files and output results in EXCEL
#     format to compare to the actual answers (ERL Gold Standard file)
#     Output also in competition format for the ERL judge.

# Required support is:
#
#        sudo pip install SpeechRecognition   # for speech_recognition module
#        sudo apt-get install python-pyaudio  # for mcrophone operation
###############################################################################
# Updates:
# 22 Nov 2021 Derek - Code moved to ROS2 and Python3
#
###############################################################################
import sys, os

import rclpy

from rclpy.node     import Node
from std_msgs.msg   import String, Bool
#import pocketsphinx # In June 2017 gave up on this one!!

import speech_recognition as sr
# import python_support_library.text_colours     as TC      # print text in various colours/sstyles
import  py_utils_pkg.text_colours     as TC
# Only used by "google cloud platform" (GCP) speech recognition
# GCP needs an account with a "Payment Method!" currently there is not one.
#     The 2 sets ofcredentials in the code base are for Derek Ripper & Zeke Steer
import gcp_keywords_r     as gcpk # GCP preferred keyword/sphrases
import gcp_credentials_v2 as gcpc # GCP credentials to access GCP speech recognition

# simple routine to use instead of print() - to get colour coded messages for ERROR,INFO,RESULT, etc
prt = TC.Tc()

#code name - to be used in any warning/error msgs.
cname = " stt_v2: "
class SpeechRecognizer(Node):

    def __init__(self):
        super().__init__('SpeechRecognizer')
        prt.info(cname+" init section ===================")
        self.declare_parameter("SR_SPEECH_ENGINE",   'google')
        self.declare_parameter("SR_ENERGY_THRESHOLD", 1201)
        self.declare_parameter("SR_PAUSE_THRESHOLD",  1.00)

        self.publish_ = self.create_publisher(String, '/stt', 10)
        self.listen_toggle = self.create_subscription(String,'/stt_switch',self.stt_switch_callback,10)

        self.audio_sources = [ 'mic' ]
        self.speech_recognition_engines = [ 'google', 'ibm', 'sphinx', 'google_cloud', 'houndify', 'bing' ]

        self.sp_rec = sr.Recognizer()
        self.sp_rec.operation_timeout = 10
        self.speech_recognition_engine = self.get_parameter(
            'SR_SPEECH_ENGINE').get_parameter_value().string_value
        self.energy_threshold = self.get_parameter(
            'SR_ENERGY_THRESHOLD').get_parameter_value().integer_value
        self.pause_threshold = self.get_parameter(
            'SR_PAUSE_THRESHOLD').get_parameter_value().double_value
        self.dynamic_energy_threshold  = False # default is "True"

        self.set_speech_recognition_engine(self.speech_recognition_engine)


        prt.info(cname + "speech_recognition_engine: " + self.speech_recognition_engine)
        prt.info(cname + "Energy threshold         : " + str(self.energy_threshold))
        prt.info(cname + "Pause threshold          : " + str(self.pause_threshold))
        settings =  "SR/ET/PT: " + self.speech_recognition_engine + "/"+ \
               str(self.energy_threshold)+"/"+str(self.pause_threshold)

        prt.info(cname + "audio source is microphone")
        self.set_audio_source("mic")
    #    rate = self.create_rate(10)
        while rclpy.ok():
            self.jfdi()

    def jfdi(self):




            audio = self.get_audio_from_mic(self.energy_threshold, self.pause_threshold,
                    self.dynamic_energy_threshold)

            try:
                msg = String()
                msg.data  = self.recognize(audio)

                prt.info(cname + "SPEECH HEARD by ROBOT.")
                prt.result(cname + "" + msg.data + "\n")

            except Exception as exc:
                prt.error(cname + "Exception from speech_recogniser")
                prt.error(str(exc))

            if not msg.data is None:
            #    text = text.strip()
            #    my_node.publish_.publish(text.encode('utf-8'))
                self.publish_.publish(msg)


    def stt_switch_callback(self, msg):
        prt.debug(cname+"========== enter stt_switch_callback ##########################")

        switch = msg.data
        switch = switch.upper()
        prt.debug(cname+"arg = "+switch)
        if   switch == "LIVE":
            prt.info(cname + "========== is listening.  ############################")
            self.publish_ = self.create_publisher(String, '/stt', 10)

        elif switch == "KILL":
            try:
                prt.info(cname + "========== is NOT listening.###########################")
                del self.publish_
            except:
                prt.warning(cname + "========== NO publish object to delete!")
        else:
            prt.error(cname+'stt_switch_callback - Invalid arg: '+str(switch))

        return


    def set_audio_source(self, audio_source):
        self.audio_source = audio_source
        if self.audio_source == self.audio_sources[0]:
            self.init_mic()
        else:
            prt.error("Unsupported audio source: "+self.audio_source)
            quit()

    def set_speech_recognition_engine(self, speech_recognition_engine):
        if  speech_recognition_engine == self.speech_recognition_engines[0]: # google api
            self.init_google()
            self.speech_recognition_engine = speech_recognition_engine

        elif speech_recognition_engine == self.speech_recognition_engines[1]: #IBM
            #self.init_ibm()
            #self.speech_recognition_engine = speech_recognition_engine
            self.msg01(speech_recognition_engine)

        elif speech_recognition_engine == self.speech_recognition_engines[2]: #Sphinx
            #self.init_sphinx()
            #self.speech_recognition_engine = speech_recognition_engine
            self.msg01(speech_recognition_engine)

        elif speech_recognition_engine == self.speech_recognition_engines[3]: # google_cloud
            self.init_google_cloud()
            self.speech_recognition_engine = speech_recognition_engine

        elif speech_recognition_engine == self.speech_recognition_engines[4]: # houndify
            self.init_houndify()
            self.speech_recognition_engine = speech_recognition_engine

        elif speech_recognition_engine == self.speech_recognition_engines[5]: # bng
            self.init_azure()
            self.speech_recognition_engine = speech_recognition_engine

        else:
            prt.error("Unsupported Speech Engine: " + speech_recognition_engine+
            "\n\nUse CTRL-C to kill current ROS node")
            sys.exit()

    def msg01(self,se):
        prt.error("The " + se +
        " speech engne has not been implemented yet!"+
        "\n\nUse CTRL-C to kill current ROS node")
        sys.exit()

    def init_mic(self):
        self.m = sr.Microphone(device_index = None, sample_rate = 41000)

    def init_google(self):
        # may need to define google API credentials when I can work out how to
        # get them!
        pass
        return

    def init_ibm():
        #  these are out of date -initial 30 day intial period expired in 2017!!
        self.IBM_USERNAME = "c2db0a18-e3b6-4a21-9ecf-8afd2edeeb30"
        self.IBM_PASSWORD = "uAzeboVUvhuP"

    def init_sphinx(self):
        SPHINXPATH =   rclpy.get_param("SR_SPHINXPATH")
        # English-US model from 5prealpha
        ##ps_lm    = SPHINXPATH+"model2/en-us-phone.lm.bin"
        ##ps_dict  = SPHINXPATH+"model2/cmudict-en-us.dict"
        ##ps_hmm   = SPHINXPATH+"model2/en-us"

        ## English-US model
        ps_lm    = SPHINXPATH+"0885.lm"
        ps_dict  = SPHINXPATH+"0885.dic"
        ps_hmm   = SPHINXPATH+"model/en-us/en-us"

        ## English-Indian Model
        ##ps_lm   = SPHINXPATH+"model/en-us.lm.bin"
        ##ps_dict = SPHINXPATH+"model/en_in.dic"
        ##ps_hmm  = SPHINXPATH+"model/en_in.cd_cont_5000"

        config = pocketsphinx.Decoder.default_config()
        config.set_boolean("-remove_noise", False)
        config.set_string("-lm",  ps_lm)  # language_model_file
        config.set_string("-dict",ps_dict) # phoneme_dictionary_file
        config.set_string("-hmm",ps_hmm) #
        decoder = pocketsphinx.Decoder(config)
        return

    def init_google_cloud(self):
        self.gcp_kwords = None # gcpk.gcp_keywords_r()
        return

    def init_houndify(self):
        self.h_client_id  = 'jCqo3yZHc5RMHNghmlq5jA=='
        self.h_client_key = 'yEx021sLAzVVw2B3DU-B8tAOF9xm1I5xttnvfCG6mJpp5zGuP3THTEw2xMOZ4m1J939YMe5dFpJHns8IEJDJ6Q=='
        return

    def init_azure(self):
        self.azure_key  = '8280075ae6ed4f7ba1b6a18d248a8f2d'
        return

    def recognize_google(self, audio):
        # Google speech API key from Zeke Steer's account

        #22/06/2017 - Derek - API key failed, but probably
        #related to "Cloud" speech , and not the older API

        # for testing purposes,  using the default API key
        # to use another API key, use:
        # r.recognize_google(audio, key="API_KEY")`
        # instead of `r.recognize_google(audio)`

        return self.sp_rec.recognize_google(audio, language="en-GB")#,key='AIzaSyAFaKnn1cMIrjGYOOdocHMDnVjInbOF_yo')

    def recognize_ibm(self, audio):
        return self.sp_rec.recognize_ibm(audio, username=self.IBM_USERNAME,
        password=self.IBM_PASSWORD)

    def recognize_sphinx(self, audio):
        return self.sp_rec.recognize_sphinx(audio)

    def recognize_google_cloud(self, audio):
        prt.debug("ENV VALUE: "+os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        return self.sp_rec.recognize_google_cloud(
            audio,
            #credentials_json  = gcpc.gcp_credentials("Derek"),
            credentials_json  = None,
            language          ="en-GB",
            preferred_phrases = None) # self.gcp_kwords)

    def recognize_houndify(self, audio):
        return self.sp_rec.recognize_houndify(audio, client_id=self.h_client_id,
         client_key=self.h_client_key)

    def recognize_azure(self, audio):
        return self.sp_rec.recognize_azure(audio, key=self.azure_key,
        location='westeurope', language='en-GB' )


    def recognize(self, audio):
        text = None

        try:
            if self.speech_recognition_engine   == self.speech_recognition_engines[0]: #google
                text = self.recognize_google(audio)
            elif self.speech_recognition_engine == self.speech_recognition_engines[1]: #ibm
                text = self.recognize_ibm(audio)
            elif self.speech_recognition_engine == self.speech_recognition_engines[2]: #sphinx
                text = self.recognize_sphinx(audio)
            elif self.speech_recognition_engine == self.speech_recognition_engines[3]: #google_cloud
                text = self.recognize_google_cloud(audio)
            elif self.speech_recognition_engine == self.speech_recognition_engines[4]: #houndify
                text = self.recognize_houndify(audio)
                ## houndify is documented as rasing a "UknownValueError" when no speech
                ## can be detected ... but I found it just reurns a zero length string.
                ## Hence the work around below for consistancy.
                if(len(text)) == 0:
                   raise sr.UnknownValueError
            elif self.speech_recognition_engine == self.speech_recognition_engines[5]: #MS Azure
                text = self.recognize_azure(audio)


        except sr.UnknownValueError:
            prt.warning(cname + "speech recognition engine could not understand audio")
            text = 'BAD_RECOGNITION'
        except sr.RequestError as e:
            prt.error(cname + "could not request results from speech recognition engine: {0}".format(e))
        except TypeError:
            prt.warning(cname + "returned a None Type -- Cannot understand so continue...")
            text = 'BAD_RECOGNITION'
        except Exception as e:
            prt.error (cname + "exception e: ")
            prt.error(str(e))

        except:
            prt.error(cname + " - unknown error")

        if not text is None:
            pass
            # prt.result(cname + "You said: {}".format(text)+"\n")
        else:
            prt.error(cname + "No text returned by Recogniser!")
        return text

    def get_audio_from_mic(self, energy_threshold, pause_threshold, dynamic_energy_threshold):

        with self.m as source:
            #self.sp_tec.adjust_for_ambient_noise(source)
            self.sp_rec.dynamic_energy_threshold = dynamic_energy_threshold # default is "True"
            self.sp_rec.energy_threshold         = energy_threshold         # defaultis 300
            self.sp_rec.pause_threshold          = pause_threshold          # Default is 0.8 secs

            prt.input(cname + "ROBOT is Waiting for voice input .......")

            return self.sp_rec.listen(source)

    # def jfdi(self):
    #
    #
    #     speech_recognition_engine = my_node.get_parameter(
    #     'SR_SPEECH_ENGINE').get_parameter_value().string_value
    #     energy_threshold = my_node.get_parameter(
    #     'SR_ENERGY_THRESHOLD').get_parameter_value().integer_value
    #     pause_threshold = my_node.get_parameter(
    #     'SR_PAUSE_THRESHOLD').get_parameter_value().double_value
    #
    #     dynamic_energy_threshold  = False # default is "True"
    #
    #     my_node.set_speech_recognition_engine(speech_recognition_engine)
    #
    #     prt.info(cname + "speech_recognition_engine: " + speech_recognition_engine)
    #     prt.info(cname + "Energy threshold         : " + str(energy_threshold))
    #     prt.info(cname + "Pause threshold          : " + str(pause_threshold))
    #     settings = cname + "SR/ET/PT: " + speech_recognition_engine + "/"+ \
    #                str(energy_threshold)+"/"+str(pause_threshold)
    #
    #     prt.info(cname + "audio source is microphone")
    #     my_node.set_audio_source("mic")
    #     rate = my_node.create_rate(1)
    #
    #     # this class variable is updated by stt_switch
    #     prt.todo("Remove forced trigger for the RUN variable.")
    #     my_node.run = True
    #
    #     #while not my_node.is_shutdown():
    #     while True:
    #
    #         # This  Delay Loop is broken by TOPIC=/hearts/stt_toggle
    #         while my_node.run == False:
    #            rclpy.sleep = (0.1)
    #
    #         audio = my_node.get_audio_from_mic(energy_threshold, pause_threshold,
    #                 dynamic_energy_threshold)
    #
    #         try:
    #             time_begin = my_node.get_clock().now()
    #             prt.info(settings)
    #             msg = String()
    #
    #             msg.data  = my_node.recognize(audio)
    #
    #             time_end = my_node.get_clock().now()
    #             elapsed_time= time_end - time_begin
    #
    #             prt.info(cname + "Duration for Speech Recogniion process = " +
    #                               str(elapsed_time) )
    #             prt.info(cname + "SPEECH HEARD by ROBOT.")
    #             prt.result(cname + "" + msg.data + "\n")
    #
    #         except Exception as exc:
    #             prt.error(cname + "Exception from speech_recogniser")
    #             prt.error(str(exc))
    #
    #         if not msg.data is None:
    #         #    text = text.strip()
    #         #    my_node.publish_.publish(text.encode('utf-8'))
    #             my_node.publish_.publish(msg)


#####  END OF: class SpeechRecognizer():
########################################

#################################################################################################
###                                   MAIN   PRGRAM
#################################################################################################
#
def main(args=None):
    rclpy.init(args=args)
    prt.info(cname + "********************** XXX Starting  in main")

    my_node = SpeechRecognizer()
    rclpy.spin(my_node)


    # speech_recognition_engine = my_node.get_parameter(
    # 'SR_SPEECH_ENGINE').get_parameter_value().string_value
    # energy_threshold = my_node.get_parameter(
    # 'SR_ENERGY_THRESHOLD').get_parameter_value().integer_value
    # pause_threshold = my_node.get_parameter(
    # 'SR_PAUSE_THRESHOLD').get_parameter_value().double_value
    #
    # dynamic_energy_threshold  = False # default is "True"
    #
    # my_node.set_speech_recognition_engine(speech_recognition_engine)
    #
    # prt.info(cname + "speech_recognition_engine: " + speech_recognition_engine)
    # prt.info(cname + "Energy threshold         : " + str(energy_threshold))
    # prt.info(cname + "Pause threshold          : " + str(pause_threshold))
    # settings = cname + "SR/ET/PT: " + speech_recognition_engine + "/"+ \
    #            str(energy_threshold)+"/"+str(pause_threshold)
    #
    # prt.info(cname + "audio source is microphone")
    # my_node.set_audio_source("mic")
    # rate = my_node.create_rate(1)
    #
    # # this class variable is updated by stt_switch
    # prt.todo("Remove forced trigger for the RUN variable.")
    # my_node.run = True
    # firstpass = 1
    # #while not my_node.is_shutdown():
    # while True:
    #
    #     # This  Delay Loop is broken by TOPIC=/hearts/stt_toggle
    #     while my_node.run == False:
    #        rclpy.sleep = (0.1)
    #
    #     audio = my_node.get_audio_from_mic(energy_threshold, pause_threshold,
    #             dynamic_energy_threshold)
    #
    #     try:
    #         time_begin = my_node.get_clock().now()
    #         prt.info(settings)
    #         msg = String()
    #
    #         msg.data  = my_node.recognize(audio)
    #
    #         time_end = my_node.get_clock().now()
    #         elapsed_time= time_end - time_begin
    #
    #         prt.info(cname + "Duration for Speech Recogniion process = " +
    #                           str(elapsed_time) )
    #         prt.info(cname + "SPEECH HEARD by ROBOT.")
    #         prt.result(cname + "" + msg.data + "\n")
    #
    #     except Exception as exc:
    #         prt.error(cname + "Exception from speech_recogniser")
    #         prt.error(str(exc))
    #
    #     if not msg.data is None:
    #     #    text = text.strip()
    #     #    my_node.publish_.publish(text.encode('utf-8'))
    #         my_node.publish_.publish(msg)





    ### self.create_subscription.sleep()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        prt.warning(cname+" Cancelelld by user !")
