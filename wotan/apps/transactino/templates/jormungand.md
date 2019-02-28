{% load static %}

# JORMUNGAND

Named for the Norse World-serpent that brings about Ragnarok, Jormungand is the first user client for the Transactino application. This document contains releases and documentation for its use.

## ACCESS DETAILS

```
URL: http://35.178.206.19/api/
```

## Releases

<a href="{% static 'jormungand_1.0.0.zip' %}">1.0.0</a>
<a href="{% static 'jormungand_1.2.0.zip' %}">1.2.0</a>

## Usage
### Setup

1. Unzip the release into DIR
2. Create env.json in DIR with the following contents:

```json
{
  "url": "http://35.178.206.19/api/",
  "public_key": "/path/to/public_key.asc"
}
```

3. Install Python3.5+
4. Create virtualenv `~$ python3.5 -m venv .`
5. Activate virtualenv `~$ source bin/activate`
6. Run script with arguments `~$ python jormungand.py arg1 arg2`

### Commands

The order of the arguments does not matter `account verify == verify account`

```
schema
schema reduced
account create
account verify
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
    "models": {
      "Account": {
        "methods": {
          "create": {
            "public_key": "Tests for a valid public key"
          }
        }
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

3. Verify account (no challenge):

`~$ python jormungand.py verify account`

```json
{
  "open_challenge_id": "f5368309256f4394b44803539f309aa0",
  "verification_complete": false
}
```

4. Look for challenge with corresponding ID:

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

Copy this into a file and decrypt (assuming private key has been added to GPG):

`~$ gpg --decrypt file_with_challenge > output`

The string needed to respond to the challenge can be found in `output`:

```
9DA54E27F0AC496A7F6853B11B2D2FEB5D51767F3DA7C8B482EDFABE5D20D99A88A494BACEC00FBDD92F6DD994AC9923ED50F5DC2BCF94774A83AA5625A3ED9D9AC47B8F8F991A874D97C01F1E98196C1342049EAE865120F328E9603EA0E6EE289061D6D96FBC85CC6C32CE7A9C57BEA31C122BB8E2ED80BED41D55146395159FD31CB2418E0597B46FC62A25FF2041C4DF623B9ADA5123B82C7BCF7F85DDE2E1FC9BB298D824025C7BE69E3A3FF6EF484C5153B94E0E9AA3341489841E41AA5A0A8C2CC115E00432E18AD9DF13857A500A2FA6441DE0EC0678FC6BDE7EF1D7432461625068402BBE164A7BFFCF810BA5726CFB861B6D88450966149FB13E48
```

5. Respond to the challenge:

`~$ python jormungand.py respond challenge`

```
Please enter a challenge ID: f5368309256f4394b44803539f309aa0
Please enter the decrypted string: 9DA54E27F0AC496A7F6853B11B2D2FEB5D51767F3DA7C8B482EDFABE5D20D99A88A494BACEC00FBDD92F6DD994AC9923ED50F5DC2BCF94774A83AA5625A3ED9D9AC47B8F8F991A874D97C01F1E98196C1342049EAE865120F328E9603EA0E6EE289061D6D96FBC85CC6C32CE7A9C57BEA31C122BB8E2ED80BED41D55146395159FD31CB2418E0597B46FC62A25FF2041C4DF623B9ADA5123B82C7BCF7F85DDE2E1FC9BB298D824025C7BE69E3A3FF6EF484C5153B94E0E9AA3341489841E41AA5A0A8C2CC115E00432E18AD9DF13857A500A2FA6441DE0EC0678FC6BDE7EF1D7432461625068402BBE164A7BFFCF810BA5726CFB861B6D88450966149FB13E48
```
```json
{
  "is_verified": true,
  "challenge_id": "f5368309256f4394b44803539f309aa0"
}
```

6. Run `verify account` again now that the challenge has been solved:

`~$ python jormungand.py verify account`

```json
{
  "verification_complete": true
}
```

7. Check schema again to see changes:

`~$ python jormungand.py reduced schema`

```json
{
  "schema": {
    "models": {
      "Payment": {
        "methods": {
          "get": {
            "is_open": null,
            "id": null
          }
        },
        "instances": null
      },
      "Subscription": {
        "methods": {
          "activate": {
            "subscription_id": null
          },
          "get": {
            "id": null,
            "is_active": null
          },
          "create": {
            "activation_date": null,
            "duration_in_days": null
          }
        },
        "instances": null
      },
      "Challenge": {
        "methods": {
          "respond": {
            "armor": null,
            "challenge_id": null,
            "plaintext": null
          },
          "get": {
            "is_open": null
          }
        },
        "instances": null
      },
      "Account": {
        "methods": {
          "delete": null,
          "verify": null
        }
      }
    }
  }
}
```

8. Create subscription:

`~$ python jormungand.py create subscription`

Run initially without arguments until a challenge has been solved.

```json
{
  "create_complete": false,
  "open_challenge_id": "dea4dc47bad74a85aeda4fca47cdf3ab"
}
```

9. Repeat steps 4 and 5, then run the command again:

`~$ python jormungand.py create subscription`

```
Enter the number of days the subscription will be active: 10
Enter the activation date: 2/12/2018
```
```json
{
  "create_complete": true
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

10. Activate the subscription

`~$ python jormungand.py activate subscription`

```
Enter a subscription ID: 051daa7553134f2db5aa1f8178d6e2af
```
```json
{
  "open_payment_id": "f741940a260d4241832fb080727a4f8c",
  "activation_complete": false
}
```

A payment functions like a challenge, but there is no respond function.

11. View the payment to get the relevant details

`~$ python jormungand.py get payment`

```json
{
  "f741940a260d4241832fb080727a4f8c": {
    "attributes": {
      "address": "example_address",
      "origin": "dd495ee2-581c-4382-b7d5-8dc33a48aced",
      "full_btc_amount": 406734
    }
  }
}
```

The amount shown is a combination of a base amount, in this case `40000` satoshi, and `6734` satoshi, the randomly generated amount meant to identify the payment.

Create a transaction with this amount to the address specified at the top of this document. Once the transaction has been added to a block, the payment will be closed, and any action blocked by the payment can be run successfully.

12. The payment can also be checked by running the get subscription command with inactive:

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

13. Once the payment has been closed, activate the subscription.

`~$ python jormungand.py activate subscription`

```json
{
  "activation_complete": true
}
```

14. Check the subscription again:

`~$ python jormungand.py get subscription`

```json
{
  "051daa7553134f2db5aa1f8178d6e2af": {
    "attributes": {
      "activation_date": "2018-12-02 20:59:59.559503+00:00",
      "is_active": true,
      "duration_in_days": 10,
      "is_payment_confirmed": true,
      "has_been_activated": true,
      "origin": "dd495ee2-581c-4382-b7d5-8dc33a48aced",
      "is_valid_until": "2018-12-12 20:59:59.559503+00:00"
    }
  }
}
```

Note that `is_active` is set to `true`. It will now possible to create a Fee report.

15. Check the available schema again:

`~$ python jormungand.py reduced schema`

```json
{
  "schema": {
    "models": {
      "Account": {
        "methods": {
          "lock": null
        }
      },
      "Subscription": {
        "instances": null,
        "methods": {
          "get": {
            "is_active": null,
            "id": null
          },
          "activate": {
            "subscription_id": null
          },
          "create": {
            "activation_date": null,
            "duration_in_days": null
          }
        }
      },
      "FeeReport": {
        "instances": null,
        "methods": {
          "get": {
            "is_active": null,
            "id": null
          },
          "activate": {
            "fee_report_id": null,
            "is_active": null
          },
          "create": {
            "blocks_to_include": null,
            "is_active": null
          },
          "delete": null
        }
      },
      "Challenge": {
        "instances": null,
        "methods": {
          "respond": {
            "armor": null,
            "challenge_id": null,
            "plaintext": null
          },
          "get": {
            "is_open": null
          }
        }
      },
      "IP": {
        "instances": null,
        "methods": {
          "get": null,
          "create": {
            "value": null
          },
          "delete": null
        }
      },
      "Payment": {
        "instances": null,
        "methods": {
          "get": {
            "is_open": null,
            "id": null
          }
        }
      }
    }
  }
}
```

Fee report methods are now available.

16. Create a Fee report

`~$ python jormungand.py create fee_report`

Run initially without arguments until a challenge has been solved.

```json
{
  "create_complete": false,
  "open_challenge_id": "20e2f57049ad439787d061a76ac3499a"
}
```

Complete the challenge following steps 4 and 5. Finally:

```
Enter the number of blocks to include in the report: 1
```
```json
{
  "create_complete": true,
}
```

16. The fee report will begin processing immediately. Run the get method to check it's status.

`~$ python jormungand.py get fee_report`

```json
Enter fee report ID or leave blank for all:
{
  "45977183ea644ad4969d50e24c4400d1": {
    "attributes": {
      "is_active": true,
      "date_created": "2018-12-02 21:09:54.379962+00:00",
      "last_update_end_time": "None",
      "average_tx_fee_density": 0.0,
      "latest_block_hash": "0000000000000000001aa23222738c5213183ed0f6ae44dae3fbcb821ec817ab",
      "blocks_to_include": 1,
      "average_tx_fee": 0.0
    }
  }
}
```

Finally, the result should be similar to:

```json
Enter fee report ID or leave blank for all:
{
  "45977183ea644ad4969d50e24c4400d1": {
    "attributes": {
      "is_active": true,
      "date_created": "2018-12-02 21:09:54.379962+00:00",
      "last_update_end_time": "2018-12-02 21:16:16.901939+00:00",
      "average_tx_fee_density": 216.140251362626,
      "latest_block_hash": "00000000000000000024f408b05838d9f5f3cbb0da9b7fe776d99a79558613bd",
      "blocks_to_include": 1,
      "average_tx_fee": 92225.4427454978
    }
  }
}
```
