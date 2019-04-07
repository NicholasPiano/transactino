{% load static %}

# JORMUNGAND

Named for the Norse World-serpent that brings about Ragnarok, Jormungand is the first user client for the Transactino application. This document contains releases and documentation for its use.

## ACCESS DETAILS

```
URL: http://35.178.206.19/api/
```

## LATEST RELEASE

<a href="{% static 'jormungand_1.3.0.zip' %}">1.3.0</a>

## Usage
### Setup

1. Unzip the release into DIR
2. Create env.json in DIR with the following contents:

```json
{
  "url": "http://35.178.206.19/api/",
  "public_key": "/path/to/public_key.asc",
  "challenge_path": "/path/to/dump/challenge/messages"
}
```

3. Install Python3.5+
4. Create virtualenv `~$ python3.5 -m venv .`
5. Activate virtualenv `~$ source bin/activate`
6. Install dependencies with `pip` `~$ pip install -r requirements/common.txt`
6. Run script with arguments `~$ python jormungand.py arg1 arg2 ...`

### Commands

The order of the arguments does not matter: `account verify == verify account`

```
schema
schema reduced
account create
account verify
system get
challenge get
challenge get closed
challenge respond
payment get
payment get closed
subscription create
subscription get
subscription get inactive
fee_report create
fee_report get
```

### Example series of commands from creating an account to checking a fee report

1. Look at the schema to see available commands:

`~$ python jormungand.py schema reduced`

```json
{
  "schema": {
    "readme": "Run this method to obtain the README for the system",
    "socket": "Run this method to obtain the information about the active socket if it exists.",
    "models": {
      "Account": {
        "methods": {
          "create": {
            "public_key": "A valid GPG public key in ASCII armor format with newlines replaced by their escaped equivalent (\\n)"
          }
        }
      },
      "System": {
        "methods": {
          "get": "The schema for the System get method. Returns details about the system including the public key and long key id."
        },
        "instances": "The schema for reporting details of instances of the System model. This schema takes no input and does not trigger any methods or any interaction with the API."
      }
    }
  }
}
```

2. Create account (`env.json` points to valid gpg public key):

`~$ python jormungand.py create account`

```
    #### Disclaimer ####

    Your account has been created with the IP address xx.xxx.xxx.xx and long key
    id XXXXXXXX, but you should be aware of the following matters:

    1. Until you have an active subscription, your account will be bound to
       the current IP address. Any user with access to this IP address will
       be treated equally with respect to this account. For this reason, it
       is recommended to secure access to an IP address that is restricted
       to your use only.
    2. This interface is provided with a guarantee on behalf of the published
       public key. Please refer to this guarantee for more information, but
       understand that there is no recognised authority that is bound to
       enforce the terms offered therein. Please exercise caution and ensure
       that all material transferred to the system is secured cryptographically.
    3. Although the system guarantees the integrity of the information provided
       via this interface, it is prudent to regularly check the results against
       other external sources. The information is drawn from a single common
       source (The Blockchain), allowing the reported data to be easily
       corroborated.
```

3. Check the schema to see the changes:

`~$ python jormungand.py schema reduced`

```json
{
  "schema": {
    "readme": "Run this method to obtain the README for the system",
    "socket": "Run this method to obtain the information about the active socket if it exists.",
    "system": "This schema takes no input, but will display a message indicating that changes have been made to the system.",
    "announcements": "This schema takes no input, but will display a message when there are active announcements.",
    "models": {
      "Account": {
        "methods": {
          "verify": "The schema for the Account verify method. This method takes no arguments, but does require a challenge to be solved.",
          "delete": "The schema for the Account delete method. This method takes no arguments, but does require a challenge to be solved."
        }
      },
      "Announcement": {
        "methods": {
          "get": "The schema for the Announcement get method. Returns details about the active announcements."
        },
        "instances": "The schema for reporting details of instances of the Announcement model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Challenge": {
        "methods": {
          "respond": {
            "challenge_id": "The ID of the challenge in question",
            "content": "The decrypted text of the challenge, having been re-encrypted to the public key of the service and put into ascii armor format."
          },
          "get": {
            "challenge_id": "The challenge ID",
            "is_open": "Filter the list of challenges by their open states."
          }
        },
        "instances": "The schema for reporting details of instances of the Challenge model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "System": {
        "methods": {
          "get": "The schema for the System get method. Returns details about the system including the public key and long key id."
        },
        "instances": "The schema for reporting details of instances of the System model. This schema takes no input and does not trigger any methods or any interaction with the API."
      }
    }
  }
}
```

4. Verify account (initially with no completed challenge):

`~$ python jormungand.py verify account`

```json
{
  "open_challenge_id": "f5368309256f4394b44803539f309aa0",
  "challenge_complete": false
}
```

5. Look for challenge with corresponding ID:

`~$ python jormungand.py get challenge`

```
Challenge ID:  f5368309256f4394b44803539f309aa0

-----BEGIN PGP MESSAGE-----
Version: GnuPG v1

hQIMA7gX9tabJKqzAQ//UiAgM1jHpHFLkcHcQn4IcD4NJmxDGBJeIhdFi+vXyVW1
GG+DT6ZHs+fdi1AFl2liupcmKtGaBr+pxb+hmkCIIu6D1PXqhMUrtdN3MTltWdAa
qxaD/lXz6oLNdnFhLtq5iKw6VzOLAQOiBhx6bGAvSKu9Y3F/w4xQobY/YN5YsDxQ
CEedBpcCJX2DgEsAepkG3n/UYXjQ0nEOMGeAqdtu819LVcn9A6eBzAu12f3gaGHd
QMUzEYm/2zO0Y4pVHtm2TZtxezqCsaswfgCZ1IEQS064OgY0BOzNfHOCO07Y+Xyw
nNcSHr/CDvgJjtsawxYU0fIR1daou/xHtTq9RmlIVjt3zJyavX2PaEkwIDozPfyl
RFwrMqr/6udNRDil715zPHs6zLUeNvpZ3Hf/nS5oNCyeud2I0VNl55/7ANwfeNiy
wbZaTorkNNgK0BNAVwfhM/ZJKk768xUo7Nk/Me2l8NUFD+J4qsWDqnFPQgKgPsa8
4HT2OcZrIqlilRMwCSCqVC1os+eswDMOHKqijVo6f20GTsriAzMuR77NgqCznqQb
HE1IrfljZWMCqIF9xVbERl7M99DBQ8J8Per6cGL8HVYBTcYsdysterV0X/NOyX1I
W1pH5EOXiZ+RBANwTNfoLSaa61DmgPDdfWhdK4cJmoWngQ3GJz38z+pjqCG70b3S
wMEBxKSVBS0bwsY6ImQKc1JmA2mw1cMJdB91LJbaK5vZcF3sxixZKxp0G3QmSL83
iGm+0PGlKO5U2AzWM2JNcLT8767bAFVpqcO8kBk+9MCBXtSAQdvVNDQn6Znxnz05
crkMQ8e3xk5gZoAYbbSNp5TC0WR5fC1V6qTrWOaR4F+HV9M1rQooNrekABdOzMbw
S7GZII308YL2kMt+pZYPA9LqOF6brKqw0FtUP5iX8mtvGTMlIlT2W6h80bIKpt0A
b1up/aHPM6nJA3ibfHHTCqdtzi4yzkg8bDvEmq6xHPfFo5l7gNqyM/f8dOxde8bn
MhHkZADZuupWS+TvAOGXKoOLa8lhj14S73ifdSwpcLOj/gneXeLhE2flnVV+QqGG
mK/gkDcaGaQ2pvrtx+rPbeOsDo8M3c+FsFRlFcxCW/bVsXuuElsWE+owHTxytbL3
tcLzE0isT71eCpBpVhqOlC668eKnedPqfr4M3JMAUH3L6nb1zn9j9cVHQWlHn/ZB
+3VS
=FFmP
-----END PGP MESSAGE-----
```

6. Copy this into a file and decrypt (assuming private key has been added to GPG):

`~$ gpg --output decrypted.asc --decrypt file/with/challenge/message.asc`

7. Alternatively, run the `challenge get` command with `save` to save the contents of the challenge message to the directory specified in `env.json`:

`~$ python jormungand.py get challenge save`

8. Fetch the public key of the system (using the `system get` command) for the purposes of re-encrypting the decrypted challenge message:

`~$ python jormungand.py system get`

```
System ID:  a53be67160cd43b9b9bd39ff8aba5187

-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFyUlYcBCADn2eSAR8mJlIGkxIS780Qki/vaUAk7hFxdaNNDVVvWxMZh2o7j
XAfGDxRayWXOR+oJE/Ro9YEyHWGHpN9sYx+V7z1WHAG++qWSfW1ORb3stmVFAfMJ
vF5sDtNO7PeUdLTtDg4l7zwXfnjXG1+ROInsAgxKz8seqWkg8LvQweC8+UU94eiP
581O8Yo1A+xTiXpHf431SxRR6hqfEWVm0BhePSrHSD8dFTqFqI1K5QATU5w1xPU7
IVs/ycmBbeJELOu1MdRAO5IKJ/drnH0RB89PpM4ufugJKT9p+tRyNBm13ajQlNW+
021OAbB6UH/I/ZRHl9Stt6AT+h9NOu+bRohNABEBAAG0BnN5c3RlbYkBVAQTAQgA
PhYhBKkIh90bYRz18wzDJYYwvsF9/1r9BQJclJWHAhsDBQkDwmcABQsJCAcCBhUK
CQgLAgQWAgMBAh4BAheAAAoJEIYwvsF9/1r9WE4IAM1VYYFzjnY6M4pL7S66RGIj
TzJj5w+GcE78h90Hkr+7KYnGfgG1nj+CKF885KZZcabKBoLCOUxmmgcw9Gvf/mYP
qe4/Duh77CBRxHjHx0kb2XryNhm3u6PwjaFbDXKsjb0Em7VZ4hXRu5OaTvjMpu7r
ygDxFvT0Ks+VBPMzicVKXfysA1fNaM5cskM/wFB1ODbAsdwOxGFa1WsJByEoWHOb
Sc94NimiEiktXIJkr7Tz954HKRpA2Bs6haZfdg6T3NTEVeiNd1UUZAv97FOvZhmq
ZeqLq7t0eSTzl0znp1TJ3YvomQF4OfDczONBQtlYnN/zXDMv/MqirTTGvdA/TLu5
AQ0EXJSVhwEIALkNUhTcaBrdAoA2brJdIdf9xwRIXys5hvSaFj9tB4pvfrEw093z
9rZTjvm3drhvBQknMuXCBOYCWdGpcMDwIJ9hOs3vOJx2NgHG7W3gUbhF69ZfKUeN
osEaaap+zAaJxHOJpTj4kZrnQvW0T/OCwR67JrHbc2vLXhXZeJowPW4BndZJipwe
ab9c1KT5vL1pZjFkqYMgWoJMRzN+JreGvagW81pGZpahF0rc/6k/t3VnmZFmSlVr
sKwCsXjRBaXGgIq/U7ziZBqpE2Ap29lfaKSk48ocDZuTU0Xixkr+5aHX11Z68Xez
XIhvFjC7bUD0HnO9NlX/LeSR2C03OZdqV+UAEQEAAYkBPAQYAQgAJhYhBKkIh90b
YRz18wzDJYYwvsF9/1r9BQJclJWHAhsMBQkDwmcAAAoJEIYwvsF9/1r9mQ4H/iB6
7p8xGtnKyUQnBbwCKaMyr4MoE9oOVaj8rijQ2svRQflqP081EcE7p6o7sBf3dWwl
AGsYyg5zVdFxotMvUzpdK2swuHkC2+kV6M66KIgwbrSNOv5Z9HYatyR+C3cgVYeP
tuIJw3aT7W31pdBDNUNVmTjiae5mVnlG/ie932mgR2wpE59wXJmTPcVy3zqMWldG
0klMsNS5G+l0ATK/M8Z/vbMi/CO6R/7nqYd9IeH2ijOCRKhANB+W/d2P0yO2LsP9
nC3PIMuVGc2ongSNF5mOVJfQ1UpyZe0SG4UOcs9t3G695cPxWOQKFQ9cjI0B7tIm
sdhlBYG0oGQQV5IxfsY=
=yuG5
-----END PGP PUBLIC KEY BLOCK-----
```

9. Save the public key and import it into GPG:

`~$ gpg --import saved/public/key.asc`

Remember to make a note of the LONG KEY ID for use in the `--encrypt` command.

10. Re-encrypt the contents of the decrypted message using the LONG KEY ID:

`~$ gpg --encrypt --output encrypted.asc --recipient $LONG_KEY_ID --armor decrypted.asc`

11. If the resulting file is named correctly (`encrypted.asc`), it can be placed into the challenge directory where the original encrypted message was placed after running `challenge get save`. Make sure to place it in the correct challenge directory. If this is done, run the `challenge respond read` command. The `read` option will attempt to read the re-encrypted challenge from the corresponding challenge directory.

`~$ python jormungand.py respond challenge read`

```
Please enter a challenge ID: f5368309256f4394b44803539f309aa0
```

```json
{
  "challenge_complete": true,
  "challenge_id": "f5368309256f4394b44803539f309aa0"
}
```

12. If you choose not to do this, you must copy the text for the armor formatted re-encrypted challenge and paste it into the terminal as the answer to the second prompt. To do this, newlines in the text must be replaced by escaped newlines (`\n`):

`~$ python jormungand.py respond challenge`

```
Please enter a challenge ID: f5368309256f4394b44803539f309aa0
Please enter the decrypted string that has been re-encrypted to the public key of the System model. It should be in ASCII armor format with any newlines replaced with their escaped equivalents (\n). This is for the purposes of pasting the text into the command line:

-----BEGIN PGP MESSAGE-----\n\nhQEMA2wTbiAzUAymAQf/b9PtAFcoTeq3n4o1iiYlpRoTHskp4ZhVhfqmc60rVdJM\nNldYPyXOzD3EUB1XvK86eGOzjEeo8ewSoAgKLA3StDtxm3mEfBcxuHiPSpYBTTkv\nEo5zMDJxUmRqmj7MDlOiG3JWEKAY+s1l937nsAsQPwHCwU77Mibm0nEpESurHai7\nWrjvg80eiJNfEmrlTzeRKJeVkhu0xPmrnPLt3jn33PBPQF+oIsU0yC3/uf195EQM\n7oNzJU9X1Od6S29eRMyRFzWf7T41Eo6Eo0Gayi5hk4UYBxdfn2uWJaaVaewfNVVU\n94twHJM/2ZZqfzVcQB/MEckXw35CJOtz8pb/NnIc59LAuQG3teyBf1GCLb5CgS5C\nWOIl/sfVhoR1Gjj7vj3ecUpFpD9h76Z6d0wyq/ImAQsH4kfffQlQz1GGVLWmT8DO\nnw6Mvb6eBE5WYJqdyNnD07npx28qSMjssQLYJF7InhOfzXbezEE3TBPmQJnDeyVV\n2y0xCu5paMZ4w3qb2+nyUYc7obWpIL4NzxKb8YnMF+AmMStD//ieVsHaOTVKdQRb\nMOCnF1gmXe27sKr7LoW3MsrzxcD2TjQCOULbbtm91Sp+nlTblB1jPTEGgJHX++Mz\n8IWX4y3PSF968lJFj/ympTBRrZvwKJWeR6HbylZStbyP0xgYCOAKSivnukLM/DzG\n2DDI7YcbhOoM7JRWE1lbwUGY030WZhRFfJg4XzAnOX+jCAsUe39ltt5g2hRPR8de\nsq85n2VZaDCKB6Mas8KDSGjPZVW5ji4ELVCK79fsdUjMji9ER69ksoS9GZoUBqQ6\nVLXhp6ECZ2OlAOb0l0nls3tw58SbstXPOnF0\n=MeAf\n-----END PGP MESSAGE-----

```
```json
{
  "challenge_complete": true,
  "challenge_id": "f5368309256f4394b44803539f309aa0"
}
```

13. Run `verify account` again now that the challenge has been solved:

`~$ python jormungand.py verify account`

```json
{
  "challenge_complete": true
}
```

14. Check schema again to see changes:

`~$ python jormungand.py reduced schema`

```json
{
  "schema": {
    "readme": "Run this method to obtain the README for the system",
    "socket": "Run this method to obtain the information about the active socket if it exists.",
    "system": "This schema takes no input, but will display a message indicating that changes have been made to the system.",
    "announcements": "This schema takes no input, but will display a message when there are active announcements.",
    "models": {
      "Account": {
        "methods": {
          "verify": "The schema for the Account verify method. This method takes no arguments, but does require a challenge to be solved.",
          "delete": "The schema for the Account delete method. This method takes no arguments, but does require a challenge to be solved."
        }
      },
      "Announcement": {
        "methods": {
          "get": "The schema for the Announcement get method. Returns details about the active announcements."
        },
        "instances": "The schema for reporting details of instances of the Announcement model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Challenge": {
        "methods": {
          "respond": {
            "challenge_id": "The ID of the challenge in question",
            "content": "The decrypted text of the challenge, having been re-encrypted to the public key of the service and put into ascii armor format."
          },
          "get": {
            "challenge_id": "The challenge ID",
            "is_open": "Filter the list of challenges by their open states."
          }
        },
        "instances": "The schema for reporting details of instances of the Challenge model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "System": {
        "methods": {
          "get": "The schema for the System get method. Returns details about the system including the public key and long key id."
        },
        "instances": "The schema for reporting details of instances of the System model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Subscription": {
        "methods": {
          "create": {
            "duration_in_days": "The duration, measured in periods of 24 hours from the date of activation.",
            "activation_date": "The activation date. This can be given as any valid date string. Once this date is passed, a process will run that verifies and activates the subscription. From this point, a request made from any IP address associated with the account will be responded to accordingly."
          },
          "activate": {
            "subscription_id": "The ID of the Subscription"
          },
          "get": {
            "subscription_id": "The subscription ID",
            "is_active": "The subscription active status. If omitted, all subscriptions are returned."
          }
        },
        "instances": "The schema for reporting details of instances of the Subscription model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Payment": {
        "methods": {
          "get": {
            "payment_id": "The payment ID",
            "is_open": "The payment open status"
          }
        },
        "instances": "The schema for reporting details of instances of the Payment model. This schema takes no input and does not trigger any methods or any interaction with the API."
      }
    }
  }
}
```

15. Create subscription:

`~$ python jormungand.py create subscription`

Run initially without arguments until a challenge has been solved.

```json
{
  "challenge_complete": false,
  "open_challenge_id": "dea4dc47bad74a85aeda4fca47cdf3ab"
}
```

16. Repeat the challenge response process in steps 5-12, then run the command again:

`~$ python jormungand.py create subscription`

```
Enter the number of days the subscription will be active: 10
Enter the activation date: 2/12/2018
```
```json
{
  "challenge_complete": true
}
{
  "051daa7553134f2db5aa1f8178d6e2af": {
    "attributes": {
      "activation_date": "2018-02-12 00:00:00+00:00",
      "origin": "dd495ee2-581c-4382-b7d5-8dc33a48aced",
      "is_payment_confirmed": false,
      "is_valid_until": "None",
      "has_been_activated": false,
      "duration_in_days": 10,
      "is_active": false
    }
  }
}
```

17. Activate the subscription

`~$ python jormungand.py activate subscription`

```
Enter a subscription ID: 051daa7553134f2db5aa1f8178d6e2af
```
```json
{
  "open_payment_id": "f741940a260d4241832fb080727a4f8c",
  "payment_complete": false
}
```

A payment functions like a challenge, but there is no respond function.

18. View the payment to get the relevant details

`~$ python jormungand.py get payment`

```json
{
  "f741940a260d4241832fb080727a4f8c": {
    "attributes": {
      "address": "Address.6932c72d9d15494288b2969324e22bdf",
      "origin": "dd495ee2-581c-4382-b7d5-8dc33a48aced",
      "full_btc_amount": 406734
    }
  }
}
```

The amount shown is a combination of a base amount, in this case `400000` satoshi, and `6734` satoshi, the randomly generated amount meant to identify the payment.

Create a transaction with this amount to the address found in the next step. Once the transaction has been added to a block, the payment will be closed, and any action blocked by the payment can be run successfully.

19. Find the address needed to make the payment by running the `address get` method.

`~$ python jormungand.py get address`

```
Enter an address ID: 88148b738d8f40c7a7752eec0792598d
```
```json
{
  "88148b738d8f40c7a7752eec0792598d": {
    "attributes": {
      "value": "16FzUdcw2HVnwXhT73ZbRm57ZqELSTyz2v"
    }
  }
}
```

20. The payment can also be checked by running the get subscription command with inactive:

`~$ python jormungand.py get subscription inactive`

```json
{
  "051daa7553134f2db5aa1f8178d6e2af": {
    "attributes": {
      "activation_date": "2018-02-12 00:00:00+00:00",
      "is_active": false,
      "duration_in_days": 10,
      "is_payment_confirmed": true,
      "has_been_activated": false,
      "origin": "dd495ee2-581c-4382-b7d5-8dc33a48aced",
      "is_valid_until": "None"
    }
  }
}
```

`is_payment_confirmed` will read `true` when the payment has gone through.

21. Once the payment has been closed, activate the subscription.

`~$ python jormungand.py activate subscription`

```json
{
  "payment_complete": true
}
```

22. Check the subscription again:

`~$ python jormungand.py get subscription`

```json
{
  "051daa7553134f2db5aa1f8178d6e2af": {
    "attributes": {
      "activation_date": "2018-12-02 20:59:59.559503+00:00",
      "is_active": false,
      "duration_in_days": 10,
      "is_payment_confirmed": true,
      "has_been_activated": true,
      "origin": "dd495ee2-581c-4382-b7d5-8dc33a48aced",
      "is_valid_until": "2018-12-12 20:59:59.559503+00:00"
    }
  }
}
```

Note that `has_been_activated` is set to `true`. After a short duration, the system will update the active status of the subscription and it will possible to create a Fee report.

23. Check the available schema again:

`~$ python jormungand.py reduced schema`

```json
{
  "schema": {
    "readme": "Run this method to obtain the README for the system",
    "socket": "Run this method to obtain the information about the active socket if it exists.",
    "system": "This schema takes no input, but will display a message indicating that changes have been made to the system.",
    "announcements": "This schema takes no input, but will display a message when there are active announcements.",
    "models": {
      "Account": {
        "methods": {
          "lock": {
            "lock": "Value specifying the desired lock state of the account"
          }
        }
      },
      "Address": {
        "methods": {
          "get": {
            "address_id": "The address ID"
          }
        },
        "instances": "The schema for reporting details of instances of the Address model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Announcement": {
        "methods": {
          "get": "The schema for the Announcement get method. Returns details about the active announcements."
        },
        "instances": "The schema for reporting details of instances of the Announcement model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "System": {
        "methods": {
          "get": "The schema for the System get method. Returns details about the system including the public key and long key id."
        },
        "instances": "The schema for reporting details of instances of the System model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Challenge": {
        "methods": {
          "respond": {
            "challenge_id": "The ID of the challenge in question",
            "content": "The decrypted text of the challenge, having been re-encrypted to the public key of the service and put into ascii armor format."
          },
          "get": {
            "challenge_id": "The challenge ID",
            "is_open": "Filter the list of challenges by their open states."
          },
          "delete": {
            "challenge_id": "The challenge ID to delete"
          }
        },
        "instances": "The schema for reporting details of instances of the Challenge model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "IP": {
        "methods": {
          "create": {
            "value": "Must be a valid IPv4 address."
          },
          "delete": {
            "ip_id": "The IP address ID"
          },
          "get": {
            "ip_id": "The IP address ID"
          }
        },
        "instances": "The schema for reporting details of instances of the IP model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Payment": {
        "methods": {
          "get": {
            "payment_id": "The payment ID",
            "is_open": "The payment open status"
          }
        },
        "instances": "The schema for reporting details of instances of the Payment model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "Subscription": {
        "methods": {
          "create": {
            "duration_in_days": "The duration, measured in periods of 24 hours from the date of activation.",
            "activation_date": "The activation date. This can be given as any valid date string. Once this date is passed, a process will run that verifies and activates the subscription. From this point, a request made from any IP address associated with the account will be responded to accordingly."
          },
          "activate": {
            "subscription_id": "The ID of the Subscription"
          },
          "get": {
            "subscription_id": "The subscription ID",
            "is_active": "The subscription active status. If omitted, all subscriptions are returned."
          }
        },
        "instances": "The schema for reporting details of instances of the Subscription model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "FeeReport": {
        "methods": {
          "create": {
            "blocks_to_include": "The number of blocks over which to calculate the average. Defaults to 1 if omitted.",
            "is_active": "Whether or not the report should be initially active. Defaults to true if omitted."
          },
          "delete": {
            "fee_report_id": "The ID of the FeeReport object to delete."
          },
          "get": {
            "fee_report_id": "The ID of the FeeReport in question.",
            "is_active": "The active status of the FeeReport."
          },
          "activate": {
            "fee_report_id": "The ID of the FeeReport is question.",
            "is_active": "A boolean value that designates whether the report should be active."
          }
        },
        "instances": "The schema for reporting details of instances of the FeeReport model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "TransactionReport": {
        "methods": {
          "create": {
            "is_active": "Whether or not the report should be initially active.",
            "target_address": "The address to watch",
            "value_equal_to": "A match will be recorded if the integer Satoshi amount of an output to the target address is equal to this value. WARNING: cannot be used in conjunction with the value_less_than or value_greater_than properties.",
            "value_less_than": "A match will be recorded if the integer Satoshi amount of an output to the target address is less than this value, depending on the value of the value_greater_than property. WARNING: cannot be used in conjunction with the value_equal_to property.",
            "value_greater_than": "A match will be recorded if the integer Satoshi amount of an output to the target address is greater than this value, depending on the value of the value_less_than property. WARNING: cannot be used in conjunction with the value_equal_to property."
          },
          "delete": {
            "transaction_report_id": "The ID of the TransactionReport object to delete."
          },
          "get": {
            "transaction_report_id": "The ID of the TransactionReport in question.",
            "is_active": "The active status of the TransactionReport."
          },
          "activate": {
            "transaction_report_id": "The ID of the TransactionReport is question.",
            "is_active": "A boolean value that designates whether the report should be active. Defaults to true if omitted."
          }
        },
        "instances": "The schema for reporting details of instances of the TransactionReport model. This schema takes no input and does not trigger any methods or any interaction with the API."
      },
      "TransactionMatch": {
        "methods": {
          "get": {
            "transaction_report_id": "Filter by the ID of the parent TransactionReport.",
            "transaction_report_target_address": "Filter by the target address of the parent TransactionReport.",
            "transaction_report_is_active": "Filter by the active status of the parent TransactionReport.",
            "transaction_match_id": "The ID of the TransactionMatch in question. This value will override any filters applied.",
            "is_new": "Filter by the new status of the TransactionMatch.",
            "block_hash": "Filter by the block hash of the TransactionMatch."
          },
          "dismiss": {
            "transaction_report_id": "Filter by the ID of the parent TransactionReport.",
            "transaction_report_target_address": "Filter by the target address of the parent TransactionReport.",
            "transaction_report_is_active": "Filter by the active status of the parent TransactionReport.",
            "transaction_match_id": "The ID of the TransactionMatch in question. This value will override any filters applied.",
            "block_hash": "Filter by the block hash of the TransactionMatch."
          }
        },
        "instances": "The schema for reporting details of instances of the TransactionMatch model. This schema takes no input and does not trigger any methods or any interaction with the API."
      }
    }
  }
}
```

Fee report methods are now available.

24. Create a Fee report

`~$ python jormungand.py create fee_report`

Run initially without arguments until a challenge has been solved.

```json
{
  "challenge_complete": false,
  "open_challenge_id": "20e2f57049ad439787d061a76ac3499a"
}
```

Complete the challenge as before in steps 5-12. Finally:

`~$ python jormungand.py create fee_report`

```
Enter the number of blocks to include in the report: 1
```
```json
{
  "challenge_complete": true,
}
```

16. The fee report will begin processing immediately. Run the get method to check it's status.

`~$ python jormungand.py get fee_report`

```json
Enter fee report ID or leave blank for all:
{
  "086e57572dcd4eb6bcd6d55871764c8e": {
    "attributes": {
      "is_active": true,
      "blocks_to_include": 1,
      "latest_block_hash": "",
      "is_processing": true,
      "average_tx_fee": 0.0,
      "average_tx_fee_density": 0.0,
      "last_update_end_time": "__null"
    }
  }
}
```

Finally, the result should be similar to:

```json
Enter fee report ID or leave blank for all:
{
  "086e57572dcd4eb6bcd6d55871764c8e": {
    "attributes": {
      "is_active": true,
      "blocks_to_include": 1,
      "latest_block_hash": "00000000000000000027859408d4f0a27ceb982f13c8dc7e2b8516301ad055f8",
      "is_processing": false,
      "average_tx_fee": 14407.0524934383,
      "average_tx_fee_density": 32.1095516538207,
      "last_update_end_time": "2019-04-07 17:52:45.073935+00:00"
    }
  }
}
```
