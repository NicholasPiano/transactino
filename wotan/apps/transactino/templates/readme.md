# README

The API is accessed by connecting a websocket to `/api/` or via GET request to the same endpoint. GET requests obviously will not be able to receive live updates.

## Request format

All data must be sent to the server as valid JSON. The JSON is structured as a recursive schema, where the basic type consists of a key and a value, like so:

```json
{
  "key": "value"
}
```

The value can be any valid JSON value, such as another structure, or an array. The service will provide a list of types that map to JSON types, e.g. UUID type will map to JSON string.

Each schema unit can report its verbose form when its value is set to `null`:

```json
{
  "key": null
}
```

For the above structure, an example of the verbose reported string might be the following:

```json
{
  "key": {
    "_description": "The key schema!",
    "_types": {
      "001": {
        "name": "__string",
        "_description": "A string of characters"
      }
    },
    "_errors": {
      "001": {
        "name": "incorrect_payload_type",
        "_description": "Type of payload must be one of the specified server types"
      }
    }
  }
}
```

If an incorrect type is sent for example:

```json
{
  "key": 0
}
```

The response would be:

```json
{
  "key": {
    "_errors": {
      "001": {
        "name": "incorrect_payload_type",
        "_description": "Type of payload [0] must be one of [__string]"
      }
    }
  }
}
```

## Recursion

The format of the data is recursive, meaning that when a structure or an array is a value of another key, the same rules apply to each level. For example, the following schema:

```json
{
  "key": {
    "key2": "value2"
  }
}
```

would have the verbose form:

```json
{
  "key": {
    "_description": "The key schema!",
    "_types": {
      "005": {
        "name": "__structure",
        "_description": "A JSON object"
      }
    },
    "_errors": {
      "001": {
        "name": "incorrect_payload_type",
        "_description": "Type of payload must be one of the specified server types"
      }
    },
    "_children": {
      "key2": {
        "_description": "The key 2 schema!",
        "_types": {
          "001": {
            "name": "__string",
            "_description": "A string of characters"
          }
        },
        "_errors": {
          "001": {
            "name": "incorrect_payload_type",
            "_description": "Type of payload must be one of the specified server types"
          }
        }
      }
    }
  }
}
```

In large schemas, the types and errors will be reported in verbose form only at the top level, where they are aggregated from the whole, and displayed in a reduced form where they apply.

```json
{
  "key": {
    "_description": "The key schema!",
    "_types": {
      "001": {
        "name": "__string",
        "_description": "A string of characters"
      },
      "005": {
        "name": "__structure",
        "_description": "A JSON object"
      }
    },
    "_errors": {
      "001": {
        "name": "incorrect_payload_type",
        "_description": "Type of payload must be one of the specified server types"
      }
    },
    "_children": {
      "key2": {
        "_description": "The key 2 schema!",
        "_types": ["002"],
        "_errors": ["001"]
      }
    }
  }
}
```

## Templates

An array or indexed schema (a JSON structure whose keys are of a consistent type, such as the UUID of a database object) will include a template schema that each member beneath it must match. For example, the following payload:

```json
{
  "key": [
    {
      "key2": "value2",
    },
    {
      "key2": "value2",
    }
  ]
}
```

Might be matched against the schema:

```json
{
  "key": {
    "_description": "The key schema!",
    "_types": {
      "004": {
        "name": "__array",
        "_description": "A JSON array"
      },
    },
    "_errors": {
      "001": {
        "name": "incorrect_payload_type",
        "_description": "Type of payload must be one of the specified server types"
      }
    },
    "_template": {
      "_description": "The key template schema",
      "_types": ["002"],
      "_errors": ["001"],
      "_children": {
        "key2": {
          "_description": "The key 2 schema!",
          "_types": ["002"],
          "_errors": ["001"]
        }
      }
    }
  }
}
```

## Client schemas

The structure returned from an interaction may be different from the structure sent. This is reported initially as the `client` schema. It shows what the result will be so it can be handled at the appropriate time. Consider the following interaction:

```json
{
  "methods": {
    "activate": "<ID>"
  }
}
```

From the server:

```json
{
  "methods": {
    "activate": {
      "has_been_activated": true
    }
  }
}
```

The initial reported schema for this interaction would be:

```json
{
  "methods": {
    "activate": {
      "_description": "",
      "_types": {

      },
      "_errors": {

      },
      "_client": {
        "_description": "",
        "_types": ["002"],
        "_errors": ["001"],
        "_children": {
          "has_been_activated": {
            "_description": "",
            "_types": ["002"],
            "_errors": ["001"]
          }
        }
      }
    }
  }
}
```

## Using the API

Now that these concepts have been explained, the use of the API should be self-explanatory. Detailed descriptions of each schema, type, and error are given in place, both in human-readable and machine-readable format. Some examples of API use are given below.

### Using the Smart Websocket Client

For normal use, a small application can be written, but a simple websocket client can provide the functionality needed to interact with the API. Try downloading the Smart Websocket Client Chrome extension [here](https://chrome.google.com/webstore/detail/smart-websocket-client/omalebghpgejjiaoknljcfmglgbpocdp).

Simply enter the url `ws://ec2-35-178-85-150.eu-west-2.compute.amazonaws.com:8000/api/` into the connection box.

If the schema returned is very large, it is recommended to copy the text into a text editor that supports code folding and fold portions of the schema for easier understanding.

To send payloads, simply paste the JSON text into the send box and press the send button. The response and any live updates should be visible below.

### Structure of the application

The purpose of the application is to control access to data derived from the blockchain in the form of reports. For example, a Fee Report tracks the average transaction fee and fee density (satoshis per byte) of transactions across a range of blocks specified by the user. These values can be updated when new blocks become available.

There are four states a user can be in with respect to the system:
1. Anonymous: the public key of the user is unknown to the system
2. Unsubscribed: the public key is known, but no active subscription exists for the user
3. Subscribed: there is an active subscription
4. Locked: either manually locked by the user, or locked by an admin due to violation of the user agreement

Each state opens new capabilities to the user. Make a point of sending `null` to the schema to get a description of what is available in the new schema.

### Going from anonymous to unsubscribed

#### 1. Create an account with a public key

The value of `public_key` should be a valid GPG public key in armor format with the newlines replaced by `\n` characters.

```json
{
  "schema": {
    "models": {
      "Account": {
        "methods": {
          "create": {
            "public_key": "<YOUR PUBLIC KEY>"
          }
        }
      }
    }
  }
}
```

Response:

```json
{
  "schema": {
    "models": {
      "Account": {
        "methods": {
          "create": {
            "disclaimer": "<DISCLAIMER>"
          }
        }
      }
    }
  }
}
```

The account is now unsubscribed. This account is bound to the IP address that was originally used to connect, so it is advisable to maintain access to that public IP address.

### Going from unsubscribed to an active subscription

#### 1. Verify the account by responding to a challenge

a. Verify the account (methods are called with an empty object if they take no arguments):

```json
{
  "schema": {
    "models": {
      "Account": {
        "methods": {
          "verify": {}
        }
      }
    }
  }
}
```

b. Response (blocked by challenge):

```json
{
  "schema": {
    "models": {
      "Account": {
        "methods": {
          "verify": {
            "verification_complete": false,
            "open_challenge_id": "<CHALLENGE ID>"
          }
        }
      },
      "Challenge": {
        "instances": {
          "<CHALLENGE ID>": {
            "encrypted_content": "<CHALLENGE ENCRYPTED CONTENT>"
          }
        }
      }
    }
  }
}
```

c. Respond to challenge

First, decrypt the armor string using GPG:

`~$ gpg --decrypt path/to/armor/file`

```json
{
  "schema": {
    "models": {
      "Challenge": {
        "methods": {
          "respond": {
            "challenge_id": "<CHALLENGE ID>",
            "plaintext": "<CHALLENGE DECRYPTED CONTENT>"
          }
        }
      }
    }
  }
}
```

d. Response to successful challenge

```json
{
  "schema": {
    "models": {
      "Challenge": {
        "methods": {
          "respond": {
            "challenge_id": "<CHALLENGE ID>",
            "is_verified": true
          }
        }
      }
    }
  }
}
```

e. Call verify method again

```json
{
  "schema": {
    "models": {
      "Account": {
        "methods": {
          "verify": {}
        }
      }
    }
  }
}
```

f. Response with accepted challenge

```json
{
  "schema": {
    "models": {
      "Account": {
        "methods": {
          "verify": {
            "verification_complete": true
          }
        }
      }
    }
  }
}
```

#### 2. Create a subscription

a. Create subscription and respond to challenge in the same way as before. This challenge process will be repeated for every interaction that requires a challenge.

```json
{
  "schema": {
    "models": {
      "Subscription": {
        "methods": {
          "create": {
            "activation_date": "<DATE TO ACTIVATE SUBSCRIPTION>",
            "duration_in_days": "<NUMBER OF DAYS ACTIVE>"
          }
        }
      }
    }
  }
}
```

b. Response after completing challenge

```json
{
  "schema": {
    "models": {
      "Subscription": {
        "methods": {
          "create": {
            "create_complete": true,
          }
        }
      }
    }
  }
}
```

The account is now subscribed, and has the ability to create fee reports and additional IP addresses.

### Create a fee report

A fee report calculates the average transaction fee and fee density over the number of blocks specified since the latest block. This is a rolling average, and updates with each new block added to the chain. Updates are sent live through the websocket connection last opened by the user. Only active reports are updated.

```json
{
  "schema": {
    "models": {
      "FeeReport": {
        "methods": {
          "create": {
            "blocks_to_include": "<NUMBER OF BLOCKS SINCE LATEST>",
            "is_active": "<WHETHER THE REPORT IS INITIALLY ACTIVE>"
          }
        }
      }
    }
  }
}
```

All interactions that involve creating or modifying objects will require a challenge to be solved before the action can be completed.

### Getting objects

At any time, a set of objects can be returned from the system by invoking the `get` method of the object in question. The example below lists fee reports and their parameters

```json
{
  "schema": {
    "models": {
      "FeeReport": {
        "methods": {
          "get": {}
        }
      }
    }
  }
}
```

Response:

```json
{
  "schema": {
    "models": {
      "FeeReport": {
        "instances": {
          "b6200149ffd24fa4865771a3c345015e": {
            "attributes": {
              "average_tx_fee_density": "16.5727891553804",
              "date_created": "2018-10-29 20:14:16.402048+00:00",
              "last_update_time": "2018-10-30 16:07:52.559328+00:00",
              "blocks_to_include": 10,
              "average_tx_fee": "8998.49411689765",
              "is_active": true,
              "latest_block_hash": "0000000000000000001068e998410fbd03680f346698413002e5b5d8fad11c84"
            }
          },
          "80230677f4624ba199c3140dd6fae483": {
            "attributes": {
              "average_tx_fee_density": "16.7322089022333",
              "date_created": "2018-10-30 06:59:13.434444+00:00",
              "last_update_time": "2018-10-30 16:07:52.405589+00:00",
              "blocks_to_include": 8,
              "average_tx_fee": "9348.40518275327",
              "is_active": true,
              "latest_block_hash": "0000000000000000001068e998410fbd03680f346698413002e5b5d8fad11c84"
            }
          },
          "8cd55dc6add949e4b5c29fb22c685fe8": {
            "attributes": {
              "average_tx_fee_density": "10.1728671898941",
              "date_created": "2018-10-28 19:49:56.498778+00:00",
              "last_update_time": "2018-10-31 07:24:52.612021+00:00",
              "blocks_to_include": 1,
              "average_tx_fee": "4405.4",
              "is_active": true,
              "latest_block_hash": "0000000000000000001068e998410fbd03680f346698413002e5b5d8fad11c84"
            }
          }
        },
        "methods": {
          "get": {
            "is_active": null,
            "id": null
          }
        }
      }
    }
  }
}
```

Note, in the `methods.get` section of the schema, the parameters used to filter the reports are both null. A single ID or the `is_active` flag can be used to filter the reports. Check the `get` schema of the object with `null` to see what filtering parameters are available.

This same method will be used to report each individual active report live through the websocket if the connection is open.
