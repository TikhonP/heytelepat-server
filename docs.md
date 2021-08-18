# Heytelepat

# Introduction

Interact with heytelepat-agent

# Overview

Medsenger agent is for connection to medsenger api and Speaker api is for connecting from speaker

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

    * [SPEAKER commit medicine](#1-speaker-commit-medicine)
    * [SPEAKER firmware](#2-speaker-firmware)
    * [SPEAKER get list of all categories](#3-speaker-get-list-of-all-categories)
    * [SPEAKER measurement (get list/push/patch)](#4-speaker-measurement-(get-listpushpatch))
    * [SPEAKER medicines list](#5-speaker-medicines-list)
    * [SPEAKER messages](#6-speaker-messages)
    * [SPEAKER push value](#7-speaker-push-value)
    * [SPEAKER send message](#8-speaker-send-message)
    * [SPEAKER speaker (get/create/update/delete)](#9-speaker-speaker-(getcreateupdatedelete))

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

##### II. Example Request: MEDSENGER order

***Body:***

```js        
{
    "api_key": "{{api_key}}",
    "contract_id": 3808,
    "sender_id": 27,
    "order": "medicine",
    "params": {
        "id": 79,
        "contract_id": 3808,
        "patient_id": 3970,
        "title": "Бубарин",
        "rules": "По одной бубине",
        "timetable": {"mode": "daily", "points": [{"hour": 18, "minute": 25}]},
        "is_template": false,
        "template_id": null,
        "warning_days": 0,
        "sent": 7,
        "done": 0
    }
}

```

##### II. Example Response: MEDSENGER order

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

### 1. SPEAKER commit medicine

***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/medicine/commit/
```

***Body:***

```js        
{
    "token": "{{token}}",
    "medicine": "Бубарин"
}
```

***More example Requests/Responses:***

##### I. Example Request: SPEAKER commit medicine

***Body:***

```js        
{
    "token": "{{token}}",
    "medicine": "Бубарин"
}
```

##### I. Example Response: SPEAKER commit medicine

```js
[
    "ok"
]
```

***Status Code:*** 200

<br>

### 2. SPEAKER firmware

***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/speakerapi/firmware/
```

***Body:***

```js        
{
    "token": "{{token}}"
}
```

***More example Requests/Responses:***

##### I. Example Request: SPEAKER firmware

***Body:***

```js        
{
    "token": "{{token}}"
}
```

##### I. Example Response: SPEAKER firmware

```js
{
    "new_firmware": "0.0.2"
}
```

***Status Code:*** 200

<br>

##### II. Example Request: SPEAKER firmware

***Body:***

```js        
{
    "token": "{{token}}",
    "version": "0.0.2"
}
```

##### II. Example Response: SPEAKER firmware

```js
{
    "id": 1,
    "version": "0.0.2",
    "data": "/media/firmwares/speaker_firmware_0.0.2.zip",
    "is_active": true,
    "date": "2021-07-22T18:09:29.549618+03:00"
}
```

***Status Code:*** 200

<br>

### 3. SPEAKER get list of all categories

***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/measurement/categories/
```

***Body:***

```js        
{
    "token": "{{token}}",
    "names_only": false
}
```

***More example Requests/Responses:***

##### I. Example Request: SPEAKER get list of all categories names only

***Body:***

```js        
{
    "token": "{{token}}",
    "names_only": true
}
```

##### I. Example Response: SPEAKER get list of all categories names only

```js
[
    "medicines",
    "diastolic_pressure",
    "pulse",
    "weight",
    "systolic_pressure",
    "temperature",
    "glukose",
    "medicine",
    "information"
]
```

***Status Code:*** 200

<br>

##### II. Example Request: SPEAKER get list of all categories

***Body:***

```js        
{
    "token": "{{token}}",
    "names_only": false
}
```

##### II. Example Response: SPEAKER get list of all categories

```js
[
    {
        "id": 27,
        "name": "medicines",
        "description": "Назначенные лекарства",
        "unit": "",
        "type": "string",
        "default_representation": "values",
        "is_legacy": true,
        "subcategory": null
    },
    {
        "id": 3,
        "name": "diastolic_pressure",
        "description": "Диастолическое (нижнее) артериальное давление",
        "unit": "мм рт. ст.",
        "type": "integer",
        "default_representation": "scatter",
        "is_legacy": false,
        "subcategory": "Измерения"
    },
    {
        "id": 1,
        "name": "pulse",
        "description": "Пульс в покое",
        "unit": "удары в минуту",
        "type": "integer",
        "default_representation": "scatter",
        "is_legacy": false,
        "subcategory": "Измерения"
    },
    {
        "id": 4,
        "name": "weight",
        "description": "Вес",
        "unit": "кг",
        "type": "float",
        "default_representation": "values",
        "is_legacy": false,
        "subcategory": "Измерения"
    },
    {
        "id": 2,
        "name": "systolic_pressure",
        "description": "Систолическое (верхнее) артериальное давление в покое",
        "unit": "мм рт. ст.",
        "type": "integer",
        "default_representation": "scatter",
        "is_legacy": false,
        "subcategory": "Измерения"
    },
    {
        "id": 25,
        "name": "temperature",
        "description": "Температура",
        "unit": "град Цельсия",
        "type": "float",
        "default_representation": "values",
        "is_legacy": false,
        "subcategory": "Измерения"
    },
    {
        "id": 24,
        "name": "glukose",
        "description": "Глюкоза",
        "unit": "моль/литр",
        "type": "float",
        "default_representation": "values",
        "is_legacy": false,
        "subcategory": "Измерения"
    },
    {
        "id": 29,
        "name": "medicine",
        "description": "Принятое лекарство",
        "unit": "",
        "type": "string",
        "default_representation": "values",
        "is_legacy": false,
        "subcategory": "Общее"
    },
    {
        "id": 35,
        "name": "information",
        "description": "Общая информация",
        "unit": "",
        "type": "string",
        "default_representation": "values",
        "is_legacy": false,
        "subcategory": "Общее"
    }
]
```

***Status Code:*** 200

<br>

### 4. SPEAKER measurement (get list/push/patch)

Get list of all measurements and push status. If `request_type` set to `is_sent`, then model's `.is_sent` attribute will
be `True`. If `request_type` set to `is_done`, then model's `.is_done` attribute will be `True`. Returns model instance.

***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/measurement/
```

***Body:***

```js        
{
    "token": "{{token}}",
    "request_type": "get"
}
```

***More example Requests/Responses:***

##### I. Example Request: SPEAKER measurement (get list)

***Body:***

```js        
{
    "token": "{{token}}",
    "request_type": "get"
}
```

##### I. Example Response: SPEAKER measurement (get list)

```js
[
    {
        "id": 17,
        "contract": 3808,
        "fields": [
            {
                "id": 1,
                "uid": "24c2258b-d338-4184-a114-5cae3721bb16",
                "category": "glukose",
                "description": "ммоль/л",
                "max_value": null,
                "min_value": null,
                "text": "Глюкоза",
                "value_type": "float",
                "prefix": null
            },
            {
                "id": 6,
                "uid": "93722301-d652-4903-8404-e56da4d31ad7",
                "category": "information",
                "description": null,
                "max_value": null,
                "min_value": null,
                "text": "Комментарий",
                "value_type": "textarea",
                "prefix": "Комментарий пациента -"
            }
        ],
        "title": "Глюкоза",
        "doctor_description": "Запрашивает у пациента уровень глюкозы в крови.",
        "patient_description": "Пожалуйста, измерьте уровень сахара в крови до еды с помощью глюкометра и укажите его в поле ниже.",
        "thanks_text": null,
        "custom_text": null,
        "is_sent": false,
        "is_done": false
    }
]
```

***Status Code:*** 200

<br>

##### II. Example Request: SPEAKER measurement (patch)

***Body:***

```js        
{
    "token": "{{token}}",
    "request_type": "is_sent",
    "measurement_id": 17
}
```

##### II. Example Response: SPEAKER measurement (patch)

```js
{
    "id": 17,
    "contract": 3808,
    "fields": [
        {
            "id": 1,
            "uid": "24c2258b-d338-4184-a114-5cae3721bb16",
            "category": "glukose",
            "description": "ммоль/л",
            "max_value": null,
            "min_value": null,
            "text": "Глюкоза",
            "value_type": "float",
            "prefix": null
        },
        {
            "id": 6,
            "uid": "93722301-d652-4903-8404-e56da4d31ad7",
            "category": "information",
            "description": null,
            "max_value": null,
            "min_value": null,
            "text": "Комментарий",
            "value_type": "textarea",
            "prefix": "Комментарий пациента -"
        }
    ],
    "title": "Глюкоза",
    "doctor_description": "Запрашивает у пациента уровень глюкозы в крови.",
    "patient_description": "Пожалуйста, измерьте уровень сахара в крови до еды с помощью глюкометра и укажите его в поле ниже.",
    "thanks_text": null,
    "custom_text": null,
    "is_sent": true,
    "is_done": false
}
```

***Status Code:*** 200

<br>

### 5. SPEAKER medicines list

***Endpoint:***

```bash
Method: PATCH
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/medicine/
```

***Body:***

```js        
{
    "token": "{{token}}",
    "request_type": "is_done",
    "measurement_id": 3
}
```

***More example Requests/Responses:***

##### I. Example Request: SPEAKER medicines list

***Body:***

```js        
{
    "token": "{{token}}",
    "request_type": "init"
}
```

##### I. Example Response: SPEAKER medicines list

```js
[
    {
        "id": 3,
        "contract": 3808,
        "title": "Бубарин",
        "rules": "По одной бубине",
        "is_sent": false,
        "is_done": false
    }
]
```

***Status Code:*** 200

<br>

##### II. Example Request: SPEAKER medicine patch

***Body:***

```js        
{
    "token": "{{token}}",
    "request_type": "is_done",
    "measurement_id": 3
}
```

##### II. Example Response: SPEAKER medicine patch

```js
{
    "id": 3,
    "contract": 3808,
    "title": "Бубарин",
    "rules": "По одной бубине",
    "is_sent": false,
    "is_done": true
}
```

***Status Code:*** 200

<br>

### 6. SPEAKER messages

Get messages list

***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/message/
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
        "id": 5,
        "sender": "doctor",
        "text": "Лалаоаос",
        "date": "2021-07-21T17:47:40+03:00",
        "medsenger_id": 249532,
        "is_red": true,
        "is_notified": true,
        "contract": 3808
    }
]
```

***Status Code:*** 200

<br>

### 7. SPEAKER push value

***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/measurement/push/
```

***Body:***

```js        
{
    "token": "{{token}}",
    "values": [
        {
            "category_name": "glukose",
            "value": "4.3"
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
            "category_name": "glukose",
            "value": "4.3"
        }
    ]
}
```

##### I. Example Response: SPEAKER push value

```js
[
    "ok"
]
```

***Status Code:*** 200

<br>

### 8. SPEAKER send message

***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/message/send/
```

***Body:***

```js        
{
    "token": "{{token}}",
    "message": "sample message"
}
```

***More example Requests/Responses:***

##### I. Example Request: SPEAKER send message

***Body:***

```js        
{
    "token": "{{token}}",
    "message": "sample message"
}
```

##### I. Example Response: SPEAKER send message

```js
[
    "ok"
]
```

***Status Code:*** 200

<br>

### 9. SPEAKER speaker (get/create/update/delete)

***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://127.0.0.1:8000/speaker/api/v1/speaker/
```

***Body:***

```js        
{
    "version": "0.0.1"
}
```

***More example Requests/Responses:***

##### I. Example Request: SPEAKER speaker (create)

***Body:***

```js        
{
    "version": "0.0.1"
}
```

##### I. Example Response: SPEAKER speaker (create)

```js
{
    "id": 14,
    "code": "560632",
    "token": "yyLgKYXYr3otTa1J7DMNDA",
    "version": "0.0.1"
}
```

***Status Code:*** 201

<br>

##### II. Example Request: SPEAKER speaker (get)

***Body:***

```js        
{
    "token": "{{token}}"
}
```

##### II. Example Response: SPEAKER speaker (get)

```js
{
    "id": 14,
    "code": "560632",
    "token": "CqZbVsePBoVeemN0t3oiSQ",
    "version": "0.0.1"
}
```

***Status Code:*** 200

<br>

##### III. Example Request: SPEAKER speaker (update)

***Body:***

```js        
{
    "token": "{{token}}",
    "version": "0.0.2"
}
```

##### III. Example Response: SPEAKER speaker (update)

```js
{
    "id": 14,
    "code": "560632",
    "token": "CqZbVsePBoVeemN0t3oiSQ",
    "version": "0.0.2"
}
```

***Status Code:*** 200

<br>

##### IV. Example Request: SPEAKER speaker (delete)

***Body:***

```js        
{
    "token": "{{token}}"
}
```

***Status Code:*** 204

<br>



***Available Variables:***

| Key | Value | Type |
| --- | ------|-------------|
| domain | 127.0.0.1:8000 |  |
| api_key | $2y$10$EhnTCMUX3m1MdzJoPc5iQudhoLvZSyWPXV463/yH.EqC3qV9CSir2 |  |
| token | e7a2O3JQDD6AbLk9zDDkw |  |

---
[Back to top](#heytelepat)
> Made with &#9829; by [thedevsaddam](https://github.com/thedevsaddam) | Generated at: 2021-07-22 21:56:34 by [docgen](https://github.com/thedevsaddam/docgen)
