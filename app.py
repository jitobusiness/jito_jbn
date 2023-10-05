from flask import Flask,request,make_response,jsonify
import requests
import json
import re
import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')


r = requests.get("https://jitojbnapp.com/WebServices/WS.php?type=all_india_jbn_chapter_list")
data = json.loads(r.text)['DATA'][0]['chapter_list']
city = []
for i in range(len(data)):
    city.append(data[i]['chapter_name'].lower().strip())

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
        user_id = json.loads(r.text)['DATA'][0]['user_id']
    except:
        user_name = ''
        user_id = ''
    return response,user_name,user_id

def get_chapter_id_from_name(chapter_name):
    r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=jito_chapter_filter')
    chapters_list = json.loads(r.text)
    for i in chapters_list['DATA'][0]['jito_chapter']:
        if i['name']==chapter_name:
            return i['id']
        
def send_aisensy_template_message(sender_mobile,sender_name,reciever_mobile,receiver_name,amount):
    url = "https://backend.aisensy.com/campaign/t1/api"

    headers = {
                "Content-Type": "application/json"}

    data = {
      "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0MGYwNzEzOGNhMDUwNGE2ZTlmYzE1ZCIsIm5hbWUiOiJKQk4iLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjQwZjA3MTM4Y2EwNTA0YTZlOWZjMTU4IiwiYWN0aXZlUGxhbiI6IkJBU0lDX01PTlRITFkiLCJpYXQiOjE2Nzg3MDY0NTF9.qOV1YJOKZPe_spIblfzTeC1m9Rt0i8c5_fGxWuPyU30",
      "campaignName": "Thank You Slip",
      "destination": """+91"""+reciever_mobile,
      "userName": "Customer",
      "templateParams": [
        str(receiver_name),
        str(amount),
        str(sender_name),
      ]
    }

    resp = requests.post(url, headers=headers, json=data)
    
    return resp.text

def send_thank_you_slip(sender_mobile,sender_name,sender_user_id,reciever_mobile,receiver_name,amount):
    
    date = datetime.datetime.now(tz).date().strftime("%d-%m-%Y")
    r = requests.get("https://jitojbnapp.com/WebServices/WS.php?type=thank_you_note_bot&sender_user_id="+str(sender_user_id)+"&reference_contact="+str(reciever_mobile)+"&business_amount="+str(amount)+"&work_date="+str(date))
    response = json.loads(r.text)['DATA'][0]['msg']
    
    if response == "THANK YOU NOTE RECORD SUCCESSFULLY":
        aisensy_response = send_aisensy_template_message(sender_mobile,sender_name,reciever_mobile,receiver_name,amount)
        return aisensy_response
    
    else:
        return 'System error'
        
        
    
        
def results():
    req = request.get_json(force=True)
    #print(req)
    
    intent_name = req['queryResult']['intent']['displayName']
    whatsapp_mobile_number = req['originalDetectIntentRequest']['payload']['AiSensyMobileNumber'][3:]
    #whatsapp_mobile_number = "9600012183"
    whatsapp_customer_name = req['originalDetectIntentRequest']['payload']['AiSensyName']
        
    if intent_name=="Default Welcome Intent":
        response,user_name,user_id = check_registered_user(whatsapp_mobile_number)
        if response == 'User is registered in our database':
            text = "Welcome to JBN, the Automated Business Connector for economic empowerment. Please choose from the following options or simply type your inquiry:\n1. Your Ask\n2. Thank You Slip\n3. About JBN\n4. Setu Settings\n5. Help"
            return return_text_and_suggestion_chip(text,['Main Menu'])
        else:
            return {
                  "followupEventInput": {
                    "name": "Not_JITO_Member",
                    "languageCode": "en-US"
                  }
                }
        
    if intent_name=="Search Vendors" or intent_name == "Incorrect City Entered":

        keyword = req['queryResult']['parameters']['keyword']
        chapter_name = req['queryResult']['parameters']['chapter_name']
        
        if chapter_name.lower().strip() not in city:
            return {
                  "followupEventInput": {
                    "name": "incorrect_city_entered",
                    "languageCode": "en-US"
                  }
                }
        
        
        chapter_id = get_chapter_id_from_name(chapter_name)
        
        r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=member_list_bot&filter_keyword='+keyword+'&filter_jito_chapter='+str(chapter_id))
        response = json.loads(r.text)
        if response['DATA'][0]['msg']=='Members List':
            answer = 'Here are the details you searched for:\n\n'
            for member_details in response['DATA'][0]['member']:
                answer = answer+"*Name:* "+member_details['full_name']+"\n*Mobile:* "+str(member_details['mobile'])+"\n*Company:* "+member_details['company_name']+'\n*Address:* '+member_details['company_address']+'\n\n'


            return return_text_and_suggestion_chip(answer,['Search Vendors','Main Menu'])
        
        else:
            text = "Sorry, but we couldn't find any results that match your search. Please verify your keyword and try again."
            return return_text_and_suggestion_chip(text,['Search Vendors','Main Menu'])
        
    if intent_name=="Direct Search Query":
        response,user_name,user_id = check_registered_user(whatsapp_mobile_number)
        if response == 'User is registered in our database':


            keyword = req['queryResult']['parameters']['keyword']
            chapter_name = req['queryResult']['parameters']['chapter_name']
            if chapter_name.lower().strip() not in city:
                return {
                      "followupEventInput": {
                        "name": "incorrect_city_entered",
                        "languageCode": "en-US"
                      }
                    }
            
            if len(chapter_name)>1:
                chapter_id = get_chapter_id_from_name(chapter_name)
                r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=member_list_bot&filter_keyword='+keyword+'&filter_jito_chapter='+str(chapter_id))
                response = json.loads(r.text)
                if response['DATA'][0]['msg']=='Members List':
                    answer = 'Here are the details you searched for:\n\n'
                    for member_details in response['DATA'][0]['member']:
                        answer = answer+"*Name:* "+member_details['full_name']+"\n*Mobile:* "+str(member_details['mobile'])+"\n*Company:* "+member_details['company_name']+'\n*Address:* '+member_details['company_address']+'\n\n'

                    return return_text_and_suggestion_chip(answer,['Search Vendors','Main Menu'])

                else:
                    text = "Sorry, but we couldn't find any results that match your search. Please verify your keyword and try again."
                    return return_text_and_suggestion_chip(text,['Search Vendors','Main Menu'])

            else:
                r = requests.get('https://jitojbnapp.com/WebServices/WS.php?type=member_list&filter_keyword='+keyword)
                response = json.loads(r.text)
                if response['DATA'][0]['msg']=='Members List':
                    answer = 'Here are the details you searched for:\n\n'
                    for member_details in response['DATA'][0]['member']:
                        answer = answer+"*Name:* "+member_details['full_name']+"\n*Mobile:* "+str(member_details['mobile'])+"\n*Company:* "+member_details['company_name']+'\n*Address:* '+member_details['company_address']+'\n\n'

                    return return_text_and_suggestion_chip(answer,['Search Vendors','Main Menu'])

                else:
                    text = "Sorry, but we couldn't find any results that match your search. Please verify your keyword and try again."
                    return return_text_and_suggestion_chip(text,['Search Vendors','Main Menu'])

        else:
            return {
                  "followupEventInput": {
                    "name": "Not_JITO_Member",
                    "languageCode": "en-US"
                  }
                }
        
    if intent_name == "Thank you Slip":
        
        response,sender_user_name,sender_user_id = check_registered_user(whatsapp_mobile_number)
        if response == 'User is registered in our database':
            
            sender_mobile = whatsapp_mobile_number

            reciever_mobile = req['queryResult']['parameters']['send_to'][-10:]

            reciever_response,reciever_user_name,reciever_user_id = check_registered_user(reciever_mobile)

            amount = req['queryResult']['parameters']['transaction_amount']

            response = send_thank_you_slip(sender_mobile,sender_user_name,sender_user_id,reciever_mobile,reciever_user_name,amount)

            if response == "Success.":
                text = "Thank you for generating the Thank you slip. Hope to see you back with JITO soon!"
                return return_text_and_suggestion_chip(text,['Main Menu'])
            else:
                text = "We apologize for the inconvenience. It appears that there was a timeout due to an error on our end. Please retry your request. If the issue persists, please contact our support team for further assistance.\nThank you for your understanding."
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