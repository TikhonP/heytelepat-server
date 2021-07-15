
# Heytelepat

# Introduction
Interact with heytelepat-agent

# Overview
Medsenger agent is for connectiong to medsenger api and Speaker api is for connecting from speaker

# Authentication
api_key/token

# Error Codes
200 - ok

400 - bad request, see answer for detail

404 - page/object not found

500 - internal server error

# Rate limit
No yet

## Indices

* [MEDSENGER](#medsenger)

  * [MEDSENGER Add New Device](#1-medsenger-add-new-device)
  * [MEDSENGER Incoming message](#2-medsenger-incoming-message)
  * [MEDSENGER init](#3-medsenger-init)
  * [MEDSENGER order](#4-medsenger-order)
  * [MEDSENGER remove](#5-medsenger-remove)
  * [MEDSENGER status](#6-medsenger-status)

* [SPEAKER](#speaker)

  * [SPEAKER init](#1-speaker-init)
  * [SPEAKER messages](#2-speaker-messages)
  * [SPEAKER push value](#3-speaker-push-value)


--------


## MEDSENGER



### 1. MEDSENGER Add New Device


Handles connection of device and notifies speaker socket


***Endpoint:***

```bash
Method: POST
Type: FORMDATA
URL: http://127.0.0.1:8000/medsenger/newdevice
```



***Body:***

| Key | Value | Description |
| --- | ------|-------------|
| code | 864284 |  |
| contract_id | 3808 |  |



### 2. MEDSENGER Incoming message


Handles incoming message and notifies speaker socket


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/medsenger/message
```



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808,
    "message": {
        "id": 123,
        "text": "Тестqw ",
        "date": "2021-06-11 11:30:32",
        "sender": "asdf"
    }
}
```



***More example Requests/Responses:***


##### I. Example Request: MEDSENGER Incoming message



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808,
    "message": {
        "id": 123,
        "text": "Тестqw ",
        "date": "2021-06-11 11:30:32",
        "sender": "asdf"
    }
}
```



##### I. Example Response: MEDSENGER Incoming message
```js
ok
```


***Status Code:*** 200

<br>



### 3. MEDSENGER init


Connect consultation channel


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/medsenger/init
```



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808
}
```



***More example Requests/Responses:***


##### I. Example Request: MEDSENGER init



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808
}
```



##### I. Example Response: MEDSENGER init
```js
ok
```


***Status Code:*** 200

<br>



### 4. MEDSENGER order


Handles order medicines or forms and notifies speaker socket


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/medsenger/order
```



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808,
    "sender_id": 27,
    "order": "form",
    "params": {
        "id": 693,
        "contract_id": 3808,
        "patient_id": 3970,
        "title": "Глюкоза",
        "doctor_description": "Запрашивает у пациента уровень глюкозы в крови.",
        "patient_description": "Пожалуйста, измерьте уровень сахара в крови до еды с помощью глюкометра и укажите его в поле ниже.",
        "thanks_text": null,
        "fields": [
            {
                "category": "glukose",
                "description": "ммоль/л",
                "max": null,
                "min": null,
                "params": {
                    "max": 20,
                    "min": 1
                },
                "required": true,
                "text": "Глюкоза",
                "type": "float",
                "uid": "24c2258b-d338-4184-a114-5cae3721bb16"
            },
            {
                "category": "information",
                "params": [],
                "prefix": "Комментарий пациента - ",
                "text": "Комментарий",
                "type": "textarea",
                "uid": "93722301-d652-4903-8404-e56da4d31ad7"
            }
        ],
        "timetable": {
            "mode": "daily",
            "points": [
                {
                    "hour": 17,
                    "minute": 43
                }
            ]
        },
        "show_button": true,
        "button_title": "Записать глюкозу",
        "custom_title": null,
        "custom_text": null,
        "is_template": false,
        "template_id": 196,
        "algorithm_id": null,
        "warning_days": 0,
        "template_category": "Общее",
        "instant_report": false,
        "clinics": null,
        "sent": 5,
        "done": 0
    }
}
```



***More example Requests/Responses:***


##### I. Example Request: MEDSENGER order



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808,
    "sender_id": 27,
    "order": "form",
    "params": {
        "id": 693,
        "contract_id": 3808,
        "patient_id": 3970,
        "title": "Глюкоза",
        "doctor_description": "Запрашивает у пациента уровень глюкозы в крови.",
        "patient_description": "Пожалуйста, измерьте уровень сахара в крови до еды с помощью глюкометра и укажите его в поле ниже.",
        "thanks_text": null,
        "fields": [
            {
                "category": "glukose",
                "description": "ммоль/л",
                "max": null,
                "min": null,
                "params": {
                    "max": 20,
                    "min": 1
                },
                "required": true,
                "text": "Глюкоза",
                "type": "float",
                "uid": "24c2258b-d338-4184-a114-5cae3721bb16"
            },
            {
                "category": "information",
                "params": [],
                "prefix": "Комментарий пациента - ",
                "text": "Комментарий",
                "type": "textarea",
                "uid": "93722301-d652-4903-8404-e56da4d31ad7"
            }
        ],
        "timetable": {
            "mode": "daily",
            "points": [
                {
                    "hour": 17,
                    "minute": 43
                }
            ]
        },
        "show_button": true,
        "button_title": "Записать глюкозу",
        "custom_title": null,
        "custom_text": null,
        "is_template": false,
        "template_id": 196,
        "algorithm_id": null,
        "warning_days": 0,
        "template_category": "Общее",
        "instant_report": false,
        "clinics": null,
        "sent": 5,
        "done": 0
    }
}
```



##### I. Example Response: MEDSENGER order
```js
ok
```


***Status Code:*** 200

<br>



### 5. MEDSENGER remove


Delete consultation channel


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/medsenger/remove
```



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808
}
```



***More example Requests/Responses:***


##### I. Example Request: MEDSENGER remove



***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808
}
```



##### I. Example Response: MEDSENGER remove
```js
ok
```


***Status Code:*** 200

<br>



### 6. MEDSENGER status


Check status


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/medsenger/status
```



***Body:***

```js        
{
    "api_key": "{{api_key}}"
}
```



***More example Requests/Responses:***


##### I. Example Request: MEDSENGER status



***Body:***

```js        
{
    "api_key": "{{api_key}}"
}
```



##### I. Example Response: MEDSENGER status
```js
{
    "is_tracking_data": true,
    "supported_scenarios": [],
    "tracked_contracts": [
        3808
    ]
}
```


***Status Code:*** 200

<br>



## SPEAKER



### 1. SPEAKER init


Speaker initialization


***Endpoint:***

```bash
Method: POST
Type: 
URL: http://127.0.0.1:8000/speakerapi/init/
```



***More example Requests/Responses:***


##### I. Example Request: SPEAKER init



##### I. Example Response: SPEAKER init
```js
{
    "code": 155948,
    "token": "ze7a2O3JQDD6AbLk9zDDkw"
}
```


***Status Code:*** 200

<br>



### 2. SPEAKER messages


Get messages list


***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://127.0.0.1:8000/speakerapi/incomingmessage/
```



***Body:***

```js        
{
    "token": "{{token}}"
}
```



***More example Requests/Responses:***


##### I. Example Request: SPEAKER messages



***Body:***

```js        
{
    "token": "{{token}}"
}
```



##### I. Example Response: SPEAKER messages
```js
[
    {
        "text": "Тестqw",
        "id": 3,
        "date": "2021-06-11T11:30:32+03:00"
    }
]
```


***Status Code:*** 200

<br>



### 3. SPEAKER push value


Push value with given category is and value


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/speakerapi/pushvalue/
```



***Body:***

```js        
{
    "token": "{{token}}",
    "values": [
        {
            "category_name": "fds",
            "value": "sd"
        }
    ]
}
```



***More example Requests/Responses:***


##### I. Example Request: SPEAKER push value



***Body:***

```js        
{
    "token": "{{token}}",
    "values": [
        {
            "category_name": "fds",
            "value": "sd"
        }
    ]
}
```



##### I. Example Response: SPEAKER push value
```js
OK
```


***Status Code:*** 200

<br>



***Available Variables:***

| Key | Value | Type |
| --- | ------|-------------|
| domain | 127.0.0.1:8000 |  |
| api_key | $2y$10$EhnTCMUX3m1MdzJoPc5iQudhoLvZSyWPXV463/yH.EqC3qV9CSir2 |  |
| token | e7a2O3JQDD6AbLk9zDDkw |  |



---
[Back to top](#heytelepat)
> Made with &#9829; by [thedevsaddam](https://github.com/thedevsaddam) | Generated at: 2021-07-15 17:26:20 by [docgen](https://github.com/thedevsaddam/docgen)
