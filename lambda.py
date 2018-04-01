from __future__ import print_function
import random
import json

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# ---------------------------- Data for the skill ------------------------------

ques = ["What is the maximum number of overs a bowler can bowl in T-20 cricket?",
        "A new concept in T-20 cricket is that of the football style bowl-out. When is a bowl-out resorted to?",
        "Another new concept of T-20 cricket is the free-hit, wherein a batsman gets a change to have a free hit at the ball knowing that he cannot be given out. When does the free-hit come into play?",
        "The powerplay is the fielding restrictions in a one day match, when not more than 2 fielders are allowed outside the 30 yard circle. In a T-20 match, how many overs of powerplay is allowed?",
        "A bowler bowls a fast full toss (beamer) at the batsman which misses his head, this is immediately called as a no-ball by the umpire. The batsman gets a free hit the next delivery.",
        "How long is the duration of one innings of a T-20 match?",
        "In T-20 cricket, how many bouncers are allowed in any over?",
        "How many drink breaks are allowed in a T-20 innings?",
        "Why do batsmen in T-20 matches sit close to the boundary, instead of sitting in the dressing room?",
        "In T-20 cricket, a batsman is not allowed to bat after scoring a century. After scoring 100, the batsman has to retire."
        ]

opA = ["5",
       "When the match has to be called off",
       "When the bowler bowls a foot fault no ball",
       "6",
       "True",
       "90 minutes",
       "2",
       "1",
       "To sledge the fielding team",
       "True"
       ]

opB = ["2",
       "When the match is interrupted by rain",
       "When the bowler bowls a beamer",
       "5",
       "False",
       "60 minutes",
       "0",
       "If the umpire is thirsty, he can call for a drinks break",
       "To reach the field of play quickly",
       "False"
       ]

opC = ["6",
       "When the result of the match is a tie",
       "When the bowler bowls a wide",
       "4",
       "",
       "75 minutes",
       "3",
       "2",
       "To get a better view",
       ""
       ]

opD = ["4",
       "When there is time for only less than 5 overs to be bowled",
       "When the bowler sledges the batsman",
       "10",
       "",
       "20 minutes",
       "1",
       "0",
       "None of these",
       ""
       ]

ans = ["D",
       "C",
       "A",
       "A",
       "B",
       "C",
       "D",
       "D",
       "B",
       "B"
       ]

ansInfo = ["The T-20 rules provide for 5 bowlers who can bowl a maximum of 4 overs each. In the 50 overs version of the game, each bowler can bowl a maximum of 10 overs. Of course, there is no restriction on the number of bowlers that can be used, the only restriction is on the maximum number of overs. In test cricket there is no restriction on number of overs that can be bowled by a bowler.",
           "The bowl-out is a new football style concept. This is applicable whenever the match ends in a tie (scores level). In this case, five bowlers from each of side bowl in turns at the stumps; whoever hits the stumps (bowled) gets one point. The team getting the most points is declared the winner. The first bowl out in the history of T-20 cricket happened in the First T-20 World cup in South Africa in the match between India and Pakistan. India won the bowl out by a margin of 3-0. Bowl-out is not used in the 50 overs version of the game or in test cricket. If scores are level, the match will be called as a tie.",
           "Whenever a bowler bowls a no ball, a penalty of one run is awarded to the batting side and the batsman gets an extra delivery. However in T-20 cricket apart from this penalty, a free hit is given in the next delivery. So if a foot fault no-ball occurs, then the next ball is a free hit for the batsman, he can play any stroke and will not be given out (except run out). Though this rule is loaded in favour of the batsman, in the opinion of great bowlers like Ian Bishop, this rule has helped bowlers to be more disciplined and control the number of no-balls. After the success of this rule in T-20 cricket, it has been extended to the 50 overs version. However, there is no free hit in test cricket.",
           "Powerplay refers to the fielding restrictions in place during the start of the match. This is done to allow batsman to have a go at the bowlers and make the match more interesting. During the fielding restrictions, only 2 players are allowed outside the 30 yard circle and of the remaining players 2 (excluding the wicket keeper) have to be in a catching position. This opens up gaps in the field allowing the batsman to get quick runs. In T-20 matches, the powerplay is one for 6 overs. In 50 overs match, it is for 20 overs (10 fixed + 2 blocks of 5 overs used at the fielding side's discretion). There is no powerplay concept in test cricket.",
           "The free hit is allowed only for a foot fault no ball, i.e. if the bowler oversteps his mark while bowling. If the no ball results from bowling a beamer or more than the permitted number of bouncers or for violating fielding restrictions, then the no ball will result in a penalty run and one extra ball, but the free hit is not allowed. This rule is applicable for both T-20 and 50 overs matches. Free hit rule is not applicable for test cricket.",
           "The duration of each innings of a T-20 match is 1 hour 15 minutes, i.e, 75 minutes. One innings in a 50 over one day match has to be completed in three and a half hours. In test matches a minimum of ninety overs needs to be bowled in one day.",
           "In both T-20, a bowler can bowl only one bouncer per over. A bouncer is defined as a fast delivery that goes above shoulder height of the batsman. If the bowler bowls a second bouncer, it is called a no ball. In test cricket and ODIs, a bowler can bowl two bouncers per over.",
           "No drinks breaks are allowed in a T-20 innings. This is because the objective is to finish the match as quickly as possible, with minimum breaks. There will only one break allowed, which will be in between innings which would be generally between 15-20 minutes. In 50 overs cricket, there would be two drinks break per innings. In test cricket, there would be a drinks break after every hour of play.",
           "In test and 50 overs cricket, the two teams sit in the dressing room; but in T-20 cricket keeping in mind the time limitation, both teams sit in a baseball style dugout outside the boundary. In fact, on fall of a wicket the incoming batsman has to take guard within 1 minutes 30 seconds of the fall of wicket, failing which he will be declared timed out. In the 50 overs ODI and test cricket, a batsman can be timed out if he is not ready to take guard within 3 minutes of the fall of the previous wicket.",
           "There is no rule in either T-20, 50 overs or test cricket, that restricts the number of runs a batsman can score. Batsmen can bat as long as they wish or till they are out. However, a batsman can voluntarily retire if he is ill or for any other reason."
           ]

# --------------------------- Global variables ---------------------------------

totalQues = 10
quesInOneSession = 6
maxScore = quesInOneSession

score = 0
currQues = -1
askedQuesCount = 0
askedQues = []
session_attributes = {}
rulecount = 0

quesAnswered = True

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hi! This is a cricket quiz! For rules of the game, just say rules! " \
                    "Shall we find out how well you know cricket? Say start quiz to begin" 
                    
    reprompt_text = "Hey! I am waiting! " \
                    "Shall we get started? Say begin to get started!" 

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def result():
    
    init = "Yay! You completed the quiz! " + " You got " + str(score) + " out of " + str(quesInOneSession) + " correct. "
    if score == quesInOneSession:
        init = init + " Perfect score! You really know cricket! I am impressed! "
    elif score >= (quesInOneSession/1.5)+1:
        init = init + " Great score! Keep playing, keep getting better! "
    elif score >= (quesInOneSession/2.5)+1:
        init = init + " Good effort! You can do better, I believe in you! "
    else:
        init = init + " You can do better! Play again, get better!  "

    init = init + "  Wanna play again? Just say, Replay!"
    
    return (init)

def ret_question():

    q = ques[currQues] + " . "
    return (q)

def ret_options():

    o3 = ""
    o4 = ""
    
    o1 = "Option 1 . " + opA[currQues] + ". "
    o2 = "Option 2 . " + opB[currQues] + ". "

    if opC[currQues] != "":
        o3 = "Option 3 . " + opC[currQues] + ". "
        o4 = "Option 4 . " + opD[currQues] + ". "

    o = o1+o2+o3+o4
    return (o)
    

def quiz(intent, session):

    global askedQuesCount
    global currQues
    global askedQues
    global quesAnswered

    card_title = "Quiz"

    if askedQuesCount == 0:
        init = "Alright! Let us begin. "
    else:
        init = ""

    speech_output = ""
    reprompt_text = ""
    
    if askedQuesCount == quesInOneSession:
         
                speech_output = result()
                reprompt_text = " Hey! Let's play again! Say Replay to play again. Or Exit to stop playing "
                should_end_session = False

                return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
            
    if quesAnswered == False:
        card_title = "Alert!"

        speech_output = "Hey! Answer the last question I asked you."
        reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
             
    
    askedQuesCount = askedQuesCount+1   
    quesNo = askedQuesCount
    x =  random.randint(0,totalQues-1)
    while x in askedQues:
            x =  random.randint(0,totalQues-1)
        
    askedQues.append(x);
    currQues = x
    
    question = "Question " + str(quesNo) + ".  " + ret_question() 
    options = "Your options are. " + ret_options()
    
    session_attributes['question'] = ques[x]
    session_attributes['options']= options
    
    quesAnswered = False
    
    speech_output = init + question + options
    reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    #print(b['response']['outputSpeech']['text'])
    

def convert(val):

    if val == '1':
        val = "A"
    elif val == '2':
        val = "B"
    elif val == '3':
        val = "C"
    elif val == '4':
        val = "D"
    else:
        val = "E"

    return val    
    
def convertRev(val):

    if val == "A":
        val = "1"
    elif val == "B":
        val = "2"
    elif val == "C":
        val = "3"
    else:
        val = "4"

    return val    

def get_answer(intent, session):

    global score
    global quesAnswered

    card_title = "Answer"

    if quesAnswered == True:
        speech_output = "Hey! What you trying to pull buddy? You answered the question already."
        reprompt_text = "You can know more about this question's answer by saying, tell me more, or, you can move to the next question by saying, next question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

        
    correctAns = ans[currQues]

    if 'value' not in intent['slots']['option']:
        speech_output = "You need to select an option! Select an option."
        reprompt_text = "If you missed the options, say repeat options."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
    ans_input = intent['slots']['option']['value']
    ans_input = convert(ans_input)

    if ans_input == "E":
        speech_output = "You need to select a valid option! Select a valid option."
        reprompt_text = "If you missed the options, say repeat options."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

    if ans_input == correctAns:
        speak = "That is the correct answer!" + " Say next for the next question."
        score = score + 1
    else:
        speak = "That answer is incorrect. The correct answer is option " + convertRev(correctAns) + " . Say tell me more to know about the correct answer. " 

    session_attributes[score] = score
    
    quesAnswered = True
    speech_output = speak 
    reprompt_text = "You can know more about this question's answer by saying, tell me more. "
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    


def get_next_question(intent, session):

    if quesAnswered == False:
        card_title = "Alert!"

        speech_output = "Hey! You haven't answered the question yet. You can't move to the next question."
        reprompt_text = "Hey! I am waiting for your answer. If you missed the question, say repeat question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
    return quiz(intent,session)

def repeat_question(intent, session):

    card_title = "Question"

    if currQues == -1:
        speech_output = "The quiz has not started yet! Say begin to start the quiz"
        reprompt_text = "Say begin to start the quiz"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    
    if quesAnswered == True:
        speak = "Your question was. "
        re = "Say, next question, to move to the next question!"
    else:
        speak = "Your question is. "
        re = "Hey, there! I am waiting for your answer."

    speech_output = speak + ret_question() + " . Options.  " + ret_options()
    reprompt_text = re
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    

def repeat_options(intent, session):

    card_title = "Option"

    if currQues == -1:
        speech_output = "The quiz has not started yet! Say begin to start the quiz"
        reprompt_text = "Say begin to start the quiz"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    
    
    if quesAnswered == True:
        speak = "Your options were. "
        re = "Say, next question, to move to the next question!"
    else:
        speak = "Your options are. "
        re = "Hey, there! I am waiting for your answer."

    speech_output =  speak + ret_options()
    reprompt_text = re

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

    
def current_score(intent, session):

    card_title = "Score"

    sc = str(score)
    if askedQuesCount == quesInOneSession:
        speak = "You finished the quiz! You final score is "+ sc + ". Say, replay to play again."
        re = "Say replay to start the quiz again! Or say exit to exit the game"
    else:
        if quesAnswered == True:
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount) + " questions."
            re = "Move to the next question by saying, next question."
        else:
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount-1) + " questions."
            re = "I am waiting for the answer! Say, repeat question, if you want me to repeat the question."

    speech_output = speak
    reprompt_text = re
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

def tell_me_more(intent, session):

    card_title = "Tell Me More"

    if quesAnswered == False:
        speak = "You can't know about the answer yet! Answer the question first."
        re = "I am waiting for the answer! Say, repeat question, if you want me to repeat the question."
    else:
        speak = ansInfo[currQues] + " . Say begin to continue. "
        re = "Move to the next question by saying, next question."

    speech_output = speak
    reprompt_text = re
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))  


def replay_quiz(intent, session):
    
    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered
    
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    session_attributes = {}
    quesAnswered = True
    
    return quiz(intent, session)    


def no_response():

    card_title = "No!"
    
    speech_output = "I am sorry, I don't understand!"
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
        
def yes_response():

    card_title = "Yes!"
    
    speech_output = "Yes yes but I don't understand!"
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

    
def get_help_response():
    
    global rulecount
    
    card_title = "Help"
    
    rulecount = rulecount + 1
    if rulecount == 1:
        speech_output = "This is a cricket quiz and the rules are simple. " \
                        "Alexa will ask you a question. You choose your answer by saying Option 1 or Option 2 etc. "\
                        "Alex will tell you if you were correct. Move to the next question by saying Next! "
    else:
        speech_output = "Hi! Welcome to I Know Cricket! " \
                        "This is a cricket quiz and the rules are simple. " \
                        "After you start the quiz, you will be prompted with a question. "\
                        "Options for the same will be provided. You have to choose one option, by saying, Option 1, or, Option 2, or, Option 3, or, Option 4. " \
                        "After you answer the question, I will tell you, whether you were right, or not. Then say, next question, to move to the next question. "\
                        "You can get a question repeated, by saying, Repeat question. You can also get the options for a question, repeated, by saying, repeat options. "\
                        "You can also know more about the answer, of a question, by saying, tell me more. "\
                        "You will be asked 6 questions. You will get the final score after the game. To get your score between the game, you can ask, what is my score. "
        rulecount = 0                

    if askedQuesCount == 0:
        speech_output = speech_output + "That's all! We're all set to begin! Say begin to get started!"
    else:
        speech_output = speech_output + "Alright! Shall we continue? Say begin to continue!"
                    
    speech_output = speech_output + " For detailed rules, say rules again. "
    reprompt_text = "Hey there! What are you waiting for? " \
                    "Say begin!"
                    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():

    card_title = "Session Ended"
    speech_output = "I hope you had fun! " \
                    "Good day! Come back for more! Goodbye!"
    
    should_end_session = True
    
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))
		
		

# --------------- Events ------------------

def on_session_started(session_started_request, session):

    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered

    session_attributes = {}
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    quesAnswered = True

def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent)
    
    if intent_name == "QuizIntent":
        return quiz(intent, session)
    elif intent_name == "AnswerIntent":
        return get_answer(intent, session)
    elif intent_name == "NextQuestionIntent":
        return get_next_question(intent, session)
    elif intent_name == "RepeatQuestionIntent":
        return repeat_question(intent, session)
    elif intent_name == "RepeatOptionsIntent":
        return repeat_options(intent, session)
    elif intent_name == "ReplayIntent":
        return replay_quiz(intent, session)
    elif intent_name == "WhatsMyScoreIntent":
        return current_score(intent, session)
    elif intent_name == "TellMeMoreIntent":
        return tell_me_more(intent, session)
    elif intent_name == "NoIntent":
        return no_response(intent, session)
    elif intent_name == "YesIntent":
        return yes_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        
def on_session_ended(session_ended_request, session):
    session_attributes = {}

# --------------- Main handler ------------------

session_attributes = {}

def lambda_handler(event, context):
    
    if event['session']['new']:
	    on_session_started({'requestId': event['request']['requestId']},event['session'])
		
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

