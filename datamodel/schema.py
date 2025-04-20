schema = {
    "$schema": "http://iglucentral.com/schemas/com.snowplowanalytics.self-desc/schema/jsonschema/1-0-0#",
    "description": "Schema for a local or remote push notification",
    "self": {
        "vendor": "com.apple",
        "name": "notification_event",
        "format": "jsonschema",
        "version": "1-0-1"
    },
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "maxLength": 100
        },
        "categoryIdentifier": {
            "type": "string",
            "maxLength": 100
        },
        "threadIdentifier": {
            "type": "string",
            "maxLength": 100
        },
        "trigger": {
            "type": "string",
            "enum": ["PUSH", "LOCATION", "CALENDAR", "TIME_INTERVAL"]
        },
        "deliveryDate": {
            "type": "string",
            "maxLength": 100
        },
        "notification": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "maxLength": 300
                },
                "subtitle": {
                    "type": "string",
                    "maxLength": 300
                },
                "body": {
                    "type": "string",
                    "maxLength": 1000
                },
                "badge": {
                    "type": "integer"
                },
                "sound": {
                    "type": "string",
                    "maxLength": 300
                },
                "launchImageName": {
                    "type": "string",
                    "maxLength": 300
                },
                "attachments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "identifier": {
                                "type": "string",
                                "maxLength": 100
                            },
                            "url": {
                                "type": "string",
                                "maxLength": 750
                            },
                            "type": {
                                "type": "string",
                                "maxLength": 100
                            }
                        },
                        "required": ["identifier", "url", "type"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["title", "body"],
            "additionalProperties": False
        }
    },
    "required": ["action", "categoryIdentifier", "threadIdentifier", "trigger", "deliveryDate", "notification"],
    "additionalProperties": False
}
