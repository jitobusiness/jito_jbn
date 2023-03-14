from flask import Flask,request,make_response,jsonify
import requests
import json
import re


app = Flask(__name__)

@app.route('/')
def index():
    return 'JITO WhatsApp Bot!'

def return_text_and_suggestion_chip_with_context(text,suggestions,context_session,context_parameter_name,context_value):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}


def return_list(title,subtitle,options,descriptions,button_text,postback_text):
    options_list = []
    for option,description,postback in zip(options,descriptions,postback_text):
        options_list.append(
    {
                      "cells": [
                        {},
                        {
                          "text": option
                        },
                        {
                          "text": description
                        },
                        {
                            "text":postback
                        }
                        
                      ]
                    })
    return {"fulfillmentMessages": [
              {
                "platform": "ACTIONS_ON_GOOGLE",
                "simpleResponses": {
                  "simpleResponses": [
                    {
                      "textToSpeech": ""
                    }
                  ]
                }
              },
              {
                "platform": "ACTIONS_ON_GOOGLE",
                "tableCard": {
                  "title": title,
                  "subtitle": subtitle,
                  "columnProperties": [
                    {
                      "header": "Section Title",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Option Title",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Option Description",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Postback text",
                      "horizontalAlignment": "LEADING"
                    }
                  ],
                  "rows": options_list,
                  "buttons": [
                    {
                      "title": button_text,
                      "openUriAction": {}
                    }
                  ]
                }
              },
              {
                "text": {
                  "text": [
                    ""
                  ]
                }
              }
            ]}

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


def return_text_and_suggestion_chip_with_context(text,suggestions,context_session,context_parameter_name,context_value):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}

def return_text_with_context(text,context_session,context_parameter_name,context_value):

    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}
    

def return_file_with_buttons(subtitle,text,url,suggestions):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "basicCard": {
          "subtitle": subtitle,
          "formattedText": text,
          "image": {
            "imageUri": url,
            "accessibilityText": "Please try again later"
          }
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      }
    ]}


def return_text_and_suggestion_chip(text,suggestions):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ]}


def return_only_text(text):
    return {'fulfillmentMessages':[{"text":{"text":[text]}}]}

def check_registered_user(mobile_number):
    r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=check_user&mobile='+mobile_number)
    response = json.loads(r.text)['DATA'][0]['msg']
    try:
        user_name = json.loads(r.text)['DATA'][0]['name']
    except:
        user_name = ''
    return response,user_name

def get_chapter_id_from_name(chapter_name):
    r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=jito_chapter_filter')
    chapters_list = json.loads(r.text)
    for i in chapters_list['DATA'][0]['jito_chapter']:
        if i['name']==chapter_name:
            return i['id']

def search_keyword_with_chapter(keyword,chapter):
    r = requests.get()
    
        
def results():
    req = request.get_json(force=True)
    
    
    intent_name = req['queryResult']['intent']['displayName']
    whatsapp_mobile_number = req['originalDetectIntentRequest']['payload']['AiSensyMobileNumber'][3:]
    #whatsapp_mobile_number = "9600012183"
    whatsapp_customer_name = req['originalDetectIntentRequest']['payload']['AiSensyName']
        
    if intent_name=="Default Welcome Intent":
        response,user_name = check_registered_user(whatsapp_mobile_number)
        if response == 'User is registered in our database':
            text = "Hi *"+str(user_name)+"!*\n\nWelcome to JITO Chatbot. Please select one of the below buttons to continue."
            return return_text_and_suggestion_chip(text,['Search Vendors','Send Thank You Slip'])       
        else:
            return {
                  "followupEventInput": {
                    "name": "Not_JITO_Member",
                    "languageCode": "en-US"
                  }
                }
        
    if intent_name=="Search Vendors":
        
        keyword = req['queryResult']['parameters']['keyword']
        chapter_name = req['queryResult']['parameters']['chapter_name']
        
        chapter_id = get_chapter_id_from_name(chapter_name)
        
        r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=member_list&filter_keyword='+keyword+'&filter_chapter_id='+str(chapter_id))
        response = json.loads(r.text)
        if response['DATA'][0]['msg']=='Members List':
            answer = 'Here are the details you searched for:\n\n'
            for member_details in response['DATA'][0]['member']:
                answer = answer+"*Name:* "+member_details['full_name']+"\n*Mobile:* "+str(member_details['mobile'])+"\n*Company:* "+member_details['company_name']+'\n*Address:* '+member_details['company_address']+'\n\n'


            return return_text_and_suggestion_chip(text,['Main Menu'])
        
        else:
            text = "Sorry! We don't have any vendors under this category right now.\n\nYou can try searching something else."
            return return_text_and_suggestion_chip(text,['Main Menu'])
        
    if intent_name=="Direct Search Query":
        response,user_name = check_registered_user(whatsapp_mobile_number)
        if response == 'User is registered in our database':


            keyword = req['queryResult']['parameters']['keyword']
            chapter_name = req['queryResult']['parameters']['chapter_name']
            if len(chapter_name)>1:
                chapter_id = get_chapter_id_from_name(chapter_name)
                r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=member_list&filter_keyword='+keyword+'&filter_chapter_id='+str(chapter_id))
                response = json.loads(r.text)
                if response['DATA'][0]['msg']=='Members List':
                    answer = 'Here are the details you searched for:\n\n'
                    for member_details in response['DATA'][0]['member']:
                        answer = answer+"*Name:* "+member_details['full_name']+"\n*Mobile:* "+str(member_details['mobile'])+"\n*Company:* "+member_details['company_name']+'\n*Address:* '+member_details['company_address']+'\n\n'

                    return return_text_and_suggestion_chip(text,['Main Menu'])

                else:
                    text = "Sorry! We don't have any vendors under this category right now.\n\nYou can try searching something else."
                    return return_text_and_suggestion_chip(text,['Main Menu'])

            else:
                r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=member_list&filter_keyword='+keyword)
                response = json.loads(r.text)
                if response['DATA'][0]['msg']=='Members List':
                    answer = 'Here are the details you searched for:\n\n'
                    for member_details in response['DATA'][0]['member']:
                        answer = answer+"*Name:* "+member_details['full_name']+"\n*Mobile:* "+str(member_details['mobile'])+"\n*Company:* "+member_details['company_name']+'\n*Address:* '+member_details['company_address']+'\n\n'

                    return return_text_and_suggestion_chip(answer,['Main Menu'])

                else:
                    text = "Sorry! We don't have any vendors under this category right now.\n\nYou can try searching something else."
                    return return_text_and_suggestion_chip(text,['Main Menu'])

        else:
            return {
                  "followupEventInput": {
                    "name": "Not_JITO_Member",
                    "languageCode": "en-US"
                  }
                }
        
        
        
            
        
@app.route('/api/', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))



if __name__ == '__main__':
    app.run()
    #app.run(host="0.0.0.0",port = 8000)