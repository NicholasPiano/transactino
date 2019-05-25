---
title: Start

toc_footers:
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

search: true
---

# Introduction

Welcome to Transactino! This application provides useful information about the Bitcoin blockchain for an easy-to-use Bitcoin subscription with bulletproof security via GPG.

Named for the Norse World-serpent that brings about Ragnarok, Jormungand is the first user client for the Transactino application. Although this client allows a user to take advantage of almost all features of the API, it is highly recommended to access the API through a custom interface for more serious use, as this allows a user to control finer-grained aspects of the API, such as complex error handling.

A more detailed guide to the API can be found here: [API]

## Latest release

[1.4.0](www.transactino.com/releases/jormungand_1.4.0.zip)

# Setup

> Sample env.json

```json
{
  "url": "http://www.transactino.com/api/",
  "public_key": "/path/to/your_public_key.asc",
  "challenge_path": "/path/to/dump/challenge/messages"
}
```

1. Unpack the release into `PATH`
2. Create `PATH/env.json`
3. Install Python 3.7+
4. Create a virtualenv

`~$ python3.7 -m venv .`

5. Activate the virtualenv

`~$ source bin/activate`

6. Install dependencies

`~(jormungand)$ pip install -r requirements/common.txt`

7. Run the `Jormungand` script with desired arguments

`~(jormungand)$ python jormungand.py arg1 arg2 ...`

# Commands

> All available commands

```
schema
schema reduced

account create
account delete
account lock
account verify

challenge get (closed) (save)
challenge respond (read)
challenge delete

subscription get (inactive)
subscription create
subscription activate
subscription delete

ip get
ip create
ip delete

payment get (closed)
payment delete

fee_report get
fee_report create
fee_report activate
fee_report delete

transaction_report get
transaction_report create
transaction_report activate
transaction_report delete

transaction_match get
transaction_match dismiss

system get
address get
announcement get
```

When running commands, the order of the arguments does not matter, so `account verify === verify account`. Individual commands are discussed in detail below.

### Important note

Any method that requires a `Challenge` to be solved or a payment to be submitted can be run initially with no arguments. In fact, most commands will initially ignore all arguments until its challenge condition is met.

## Schema

```bash
~(jormungand)$ python jormungand.py schema reduced
```

> This returns:

```json
{
  "schema": {
    "readme": "Run this method to obtain the
    README for the system",
    "socket": "Run this method to obtain the
    information about the active socket if it exists.",
    "models": {
      "Account": {
        "methods": {
          "create": {
            "public_key": "A valid GPG public
            key in ASCII armor format with newlines
            replaced by their escaped equivalent (\\n)"
          }
        }
      },
      "System": {
        "methods": {
          "get": "The schema for the System get method.
          Returns details about the system including the
          public key and long key id."
        },
        "instances": "The schema for reporting details
        of instances of the System model. This schema
        takes no input and does not trigger any methods
        or any interaction with the API."
      }
    }
  }
}
```

The `schema` command returns the full description of the API. This is useful for checking function definitions and accepted data types for arguments. When new access is granted to different parts of the application when creating an account or subscribing, the changes to the schema will be visible with this command.

`schema reduced` removes all information regarding data types and supported errors, but retains some descriptions. This makes the overall structure easier to view at a glance.

## Account

The Account model holds information about the public key registered on the system.

The `account create` command takes the public key from the path provided in the `env.json` file. Once an account has been created, the IP address used to access the system will be locked to the public key. Any request from the IP address will be treated as though it comes from this account. For this reason, it is prudent to ensure you have complete control of the IP you are using. Sensitive changes to the account data on the system will require GPG challenges for security. You can create more IP addresses for this account once you have an active subscription.

`account verify` takes no arguments and requires a `Challenge` to be solved. This first challenge proves that the account holder has control of a corresponding private key.

`account delete` requires a `Challenge` to be solved and removes all data related to the account on the system.

`account lock` requires a `Challenge` to be solved and prevents all access to the system by the account in question until another command is given to unlock.

## Challenge

A `Challenge` contains a plaintext piece of data that is delivered once it has been encrypted to the public key of the account. Once the account holder receives this information, it must be decrypted using their private key and re-encrypted to the public key of the system before being sent back to close the challenge. In this way, the holder of the public key proves their possession of the corresponding private key. This process is repeated with a new piece of plaintext every time the user wishes to modify data on the system.

For clarity, each challenge occurs in the following order:

1. The user submits a request that is restricted for security purposes.
2. A `Challenge` object is created on the user account, with an `origin` relevant to the action.
3. The user makes a request for the data contained in the challenge, and receives a piece of ascii armor data, `A` encrypted to their public key.
4. The user decrypts `A` using their private key to yield `B`, proving that they possess it.
5. The user makes a request for the public key of the system.
6. The user encrypts `B` to the public key of the system, yielding `C`.
7. The user makes a request containing `C` to respond to the challenge.
8. The user re-attempts the action attempted in step 1.

### challenge get

`challenge get (closed) (save)` returns the set of `Challenge` objects, either `closed` or not, on the user account. The `save` argument will write the encrypted content of the challenge to the directory specified in `env.json`. A directory will be created if it does not exist, named for the ID of the challenge, containing the file `message.asc`.

It should be noted that `save` will cause all challenges returned by the request to be saved.

Parameter | Default | Description
--------- | ------- | -----------
`challenge_id` | `null` | Optional, specifies the challenge ID to get.

### challenge respond

`challenge respond (read)` allows the user to close a challenge using the challenge ID and the required data packet. With Jormungand, the result of the challenge can be written to a file named `encrypted.asc` in the challenge ID directory. This file will be sent to the system. The `read` argument must be included to control this.

Parameter | Description
--------- | -----------
`challenge_id` | The ID of the challenge to respond to.
`content` | The content of the challenge that has been re-encrypted to the public key of the system.

### Why are challenges needed?

A challenge harnesses the security of GPG to verify that a user holds the private key for the public key they have provided to the system. When changes are made to a user's data, challenges may be required in order to confirm the identity of the request origin and prevent intrusive attempts to modify data on the system.

The advantage of using this method is that the user's private key, used in step 4 above, can be kept completely offline to ensure security of the process. This is the same for the re-encryption process in step 6.

## Subscription

A `Subscription` is a formal agreement between the user and the system for a set period of time, backed by a fixed bitcoin payment made to a given address. The address to be used for a payment is revealed when the payment is opened. For as long as a subscription is active, the user has access to all offerings available on the system.

Multiple subscriptions can be created with different start and end points, and it is theoretically possible for multiple subscriptions to be active simultaneously, although this comes with no additional benefits. The control of this is left to the user's discretion.

The subscription process happens in two stages. In the first stage, a subscription object is created, requiring a `Challenge`. In the second stage, the subscription must be activated, requiring a payment. As a restriction on user actions, a payment behaves in a very similar manner to a challenge, expect for the fact that a user is dependent on the behaviour of the bitcoin blockchain for the payment to be closed.

### subscription get

`subscription get (inactive)` returns the set of `Subscription` objects, either `inactive` or not, on the user account.

Parameter | Default | Description
--------- | ------- | -----------
`subscription_id` | `null` | Optional, specifies the subscription ID to get.

### subscription create

`subscription create` creates a `Subscription` on the user account. This requires a `Challenge` to be solved.

Parameter | Description
--------- | -----------
`duration_in_days` | The number of days for which the subscription should be active.
`activation_date` | The date on which the subscription should start. The Jormungand client forces the timezone of the date to be set to the timezone of the local user system, but the remote system will accept any valid datetime for this parameter.

It is important to note that the date value submitted to the system is left to the user's discretion. It is possible to enter a date before the current date, in which case the subscription will activate immediately upon closure of the payment, as though the activation date had been the moment of payment closure. It is also possible to set an activation date in the future, in which case the system will not activate the subscription until that date has passed, even if the payment has been closed. This can be used to chain subscriptions if needed.

The date parser on the system supports most common date formats, but it will normalise the date entered into a common format. Check this date using `get` to satisfy yourself that the activation date the system has interpreted is correct. If it is not, use `delete` to remove the subscription and create a new one. If the system is unable to parse the date you have entered, it will return an error.

### subscription activate

`subscription activate` marks a `Subscription` for activation. If the activation date is in the future, the system will not activate the subscription until that time, but this command must be run to allow that to happen. This method requires a payment to be submitted. Each subscription has a unique `origin` property that can be viewed by using `get`. Only the payment with this `origin` can be closed to allow this specific subscription to be activated.

Parameter | Description
--------- | -----------
`subscription_id` | The ID of the subscription to be activated.

It is important to note that the process of activation is decoupled from user action via this method and relies only on the system's cycle of verification to determine the status of each subscription. The user must wait for the timing of this cycle to address the subscription in question. This can take up to two minutes. The status of the subscription can be checked using `get`.

### subscription delete

`subscription delete` deletes a `Subscription`. This requires a `Challenge` to be solved and is irreversible.

Parameter | Description
--------- | -----------
`subscription_id` | The ID of the subscription to be deleted.

This method is **irreversible** and **independent of the status of the subscription**. This means that a subscription that is active and paid-for can still be deleted. This is left to the user's discretion.

## IP

An `IP` object stores the IP address used by a user to access their account. An `IP` object is created when a user account is created, but more can be added at the user's discretion. A maximum of five `IP` objects may be on a user account before a payment is required for each subsequent `IP`.

### ip get

`ip get` returns the set of `IP` objects associated with the user account.

Parameter | Description
--------- | -----------
`ip_id` | The IP ID to return.

### ip create

`ip create` can be used to create an `IP` object. Only five can be created before a payment is required for each `IP`.

Parameter | Description
--------- | -----------
`value` | The IP address value.

### ip delete

`ip delete` deletes an `IP` from the user account. This is irreversible. A challenge must be solved to complete this method.

Parameter | Description
--------- | -----------
`ip_id` | The IP ID to delete.

## Payment

A `Payment` is needed to allow access to several offerings within this application. All payments are mediated by the bitcoin blockchain. A typical payment is made by creating a transaction with an output that specifies the correct address given and the correct unique amount. The unique amount acts as an identifier that allows an automatic system
to differentiate payments. Payment amounts will be given as an integer representing the number of Satoshi required.

`Payment` objects on an account cannot be interacted with or modified in any way, except in the case of deletion.

The lifetime of a typical payment follows this series of steps:

1. The user attempts an action that is restricted by a payment.
2. A `Payment` is opened with an `origin` property that connects it to the action.
3. The user makes a request for the `Address` object referenced in the `Payment`.
3. The user creates a transaction with the value of the address and the unique amount specified in the `Payment`.
4. The user waits for the transaction to be mined.
5. Once the transaction is detected on the blockchain, the `Payment` will be closed on the system.
6. The user re-attempts the action.

### payment get

`payment get (closed)` returns details of open `Payment` objects, unless the `closed` argument is included. This can be used to find the `origin` and `unique_btc_amount` properties for a specific `Payment`.

Parameter | Default | Description
--------- | ------- | -----------
`payment_id` | null | Optional, specifies the payment ID to get.

### payment delete

`payment delete` deletes a `Payment`. This command should be used if you do not wish to continue with an open payment in order to enable a method. For example, if making a payment for `subscription activate`, the payment can be removed to reset the method.

Parameter | Description
--------- | -----------
`payment_id` | The ID of the payment to be deleted.

This is **irreversible** and is left to the user's discretion.

## Fee Report

A `FeeReport` contains regularly updated statistical details about the fee information contained in bitcoin blocks. For example, the average fee in Satoshi and the average fee weight in Satoshi per byte are provided. When creating a fee report, the user has the option to specify that this average should be calculated over a certain number of blocks, e.g. ten. Thus, the updated average fee would be that of all transactions in the latest ten blocks. This moving average is meant to give users planning to submit transactions an idea of what fee they should provide. These values are updated as soon as possible following the mining of a new block.

### fee_report get

`fee_report get (inactive)` returns details about `FeeReport` objects on the account. The `inactive` flag will return inactive fee reports. Use the `activate` method to set the active status of a `FeeReport` to add or remove it from your focus.

Parameter | Description
--------- | -----------
`fee_report_id` | The ID of the fee report to be returned.
`is_active` | The active status of the fee reports to return.

### fee_report create

Fee reports can be created in an `inactive` state, but by default, Jormungand will submit an active status to the system.

Parameter | Description
--------- | -----------
`blocks_to_include` | The number of blocks to include in the updating fee report.
`is_active` | The initial active status of the fee report.

### fee_report activate

The `activate` method controls the active status of the `FeeReport`.

Parameter | Description
--------- | -----------
`fee_report_id` | The ID of the fee report.
`is_active` | The active status of the fee report to set.

### fee_report delete

The `delete` method permanently deletes the `FeeReport` from the user account.

Parameter | Description
--------- | -----------
`fee_report_id` | The ID of the fee report to delete.

## Transaction Report

A `TransactionReport` monitors the blockchain for transaction outputs that match its requirements. A single address to watch must be specified, along with upper and lower bounds, or alternatively an exact value, for the integer output in Satoshi. A successful match will yield TransactionMatch objects.

### transaction_report get

`transaction_report get (inactive)` returns details about `TransactionReport` objects on the account. The `inactive` flag will return inactive transaction reports. Use the `activate` method to set the active status of a transaction report to add or remove it.

Parameter | Description
--------- | -----------
`transaction_report_id` | The ID of the transaction report to be returned.
`is_active` | The active status of the transaction reports to return.

### transaction_report create

Fee reports can be created in an `inactive` state, but by default, Jormungand will submit an active status to the system.

Parameter | Description
--------- | -----------
`target_address` | The address to use for matching transactions.
`value_equal_to` | Any match must have exactly this integer Satoshi value.
`value_less_than` | Any match must have an integer Satoshi value less than this.
`value_greater_than` | Any match must have an integer Satoshi value greater than this.
`is_active` | The initial active status of the transaction report.

### transaction_report activate

The `activate` method controls the active status of the `TransactionReport`.

Parameter | Description
--------- | -----------
`transaction_report_id` | The ID of the transaction report.
`is_active` | The active status of the transaction report to set.

### transaction_report delete

The `delete` method permanently deletes the `TransactionReport` from the user account.

Parameter | Description
--------- | -----------
`transaction_report_id` | The ID of the transaction report to delete.

## Transaction Match

`TransactionMatch` objects represent successful matches of their corresponding `TransactionReport` objects. They can be filtered by a variety of useful parameters including their parent address and the hash of the block they occurred in.

### transaction_match get

The `get` method makes several filters available to find the correct results from transaction reports.

Parameter | Description
--------- | -----------
`transaction_report_id` | The ID of the parent `TransactionReport`.
`transaction_report_target_address` | The target address of the parent `TransactionReport`.
`transaction_report_is_active` | The active status of the parent `TransactionReport`.
`transaction_match_id` | The ID of the `TransactionMatch` object.
`is_new` | The new status of the transaction match.
`block_hash` | The block hash of the transaction match.

These filters can be combined in various ways to narrow the set of transaction matches returned.

### transaction_match dismiss

The `dismiss` method functions in exactly the same way as the `get` method, but it returns no results and all results matched by the parameters have their `is_new` status set to `False`. This allows filtering by this parameter for newer results.

## System

The `System` object represents the current identity of the system. Updates will be announced prior to any concrete change.

### system get

The `system get` method returns the details of the active `System` object, including the GPG public key used to verify and encrypt data.

## Address

The `Address` object stores information about a Bitcoin address used as part of a payment. This API remains mostly closed to the user, but addresses can be accessed by their ID in order to make a payment. In each `Payment` object, the `Address` object that the user should use is referenced as a relationship.

### address get

The `address get` method returns details about an `Address` object and requires an ID.

Parameter | Description
--------- | -----------
`address_id` | The ID of the `Address` object.

## Announcement

`Announcement` objects contain up-to-date communications between the maintainer of the system and the user. A message will be included with any query while the announcement is active.

### announcement get

The `announcement get` method will return all active `Announcement` objects on the system.

# Walkthroughs

The following walkthroughs are intended to give a new user a comprehensive introduction to the application by showing the commands that might be used as well as the data that could be returned by those commands. Some sample data has been modified to avoid specific references and thus may fail associated validation checks (IP addresses, GPG public keys).

Although the Jormungand client provides a simple way to execute commands, any commands run by Jormungand can also be run using cURL or a REST client such as Postman.

## Walkthrough from anonymous user to active subscription

When accessing the system for the first time, the user is **anonymous** as far as the system is concerned. The user obviously lacks a subscription or any other form of identification stored on the system. This walkthrough demonstrates the series of commands necessary to progress from this state to an active subscription on the system, allowing the user to access the full offering.

### 1. Schema

> (1) Result of `schema reduced`

```bash
~(jormungand)$ python jormungand.py schema reduced
```

```json
{
  "schema": {
    "readme": "Run this method to obtain the README for the system",
    "socket": "Run this method to obtain the information
    about the active socket if it exists.",
    "models": {
      "Account": {
        "methods": {
          "create": {
            "public_key": "A valid GPG public key in ASCII armor
            format with newlines replaced by their escaped equivalent (\\n)"
          }
        }
      },
      "System": {
        "methods": {
          "get": "The schema for the System get method.
          Returns details about the system including
          the public key and long key id."
        },
        "instances": "The schema for reporting details
        of instances of the System model. This schema
        takes no input and does not trigger any methods
        or any interaction with the API."
      }
    }
  }
}
```

When reaching any stable state, the user should check the commands available using the `schema` command. In this case, run `schema reduced` for an overview.

### 2. Create an account

> (2) Result of `account create` returns the system disclaimer:

```bash
~(jormungand)$ python jormungand.py account create
```

```
The IP used to create this account: xxx.xxx.xxx.xxx
The long key ID of your GPG public key: XXXXXXXXXXXXXXXX
Disclaimer: <DISCLAIMER OMITTED>
```

An account on the system is represented by a GPG public key. To use the `account create` command with Jormungand, the public key the user wishes to use must be placed in a directory accessible to the client and referenced in the `env.json` configuration file. Refer to the `account create` method documentation for more details.

After running each command, check the schema again by running `schema reduced` to see any changes.

### 3. Attempt to verify the account

> (3) Result of `account verify` returns a challenge ID:

```bash
~(jormungand)$ python jormungand.py account verify
```

```json
{
  "challenge_complete": false,
  "open_challenge_id": "1a159673c3a84e8a9299f1037726b871"
}
```

In order to progress further, an account must be verified. This is done by solving a single challenge. This method will fail when run for the first time, indicating the ID of the `Challenge` object that must be solved to continue.

### 4. Get `Challenge`

> (4) Result of `challenge get save`:

```bash
~(jormungand)$ python jormungand.py challenge get save
Enter the Challenge ID or leave blank for all: 1a159673c3a84e8a9299f1037726b871
```

```
Challenge ID:  1a159673c3a84e8a9299f1037726b871

<CHALLENGE PGP MESSAGE OMITTED>
```

Each method blocked by a `Challenge` object will include the `Challenge` ID. Enter this ID when prompted to fetch this specific challenge.

### 5. Decrypt challenge

> (5) Result of decryption:

```bash
~$ gpg --output decrypted.asc --decrypt message.asc
```

```
gpg: encrypted with 4096-bit RSA key, ID XXXXXXXXXXXXXXXX, created XXXX-XX-XX
      "xxxxxxxxxxx (xxxxxxxxxxxxx) <xxxxxxxxxxx@xxxx.xxx>"
```

This step must be done outside Jormungand. For security, it is recommended to perform this operation on an air-gapped computer. The GPG private key corresponding to the public key used to create the account is required.

A. Having used the `get challenge` command with the `save` argument, the challenge text can be found in the `challenge_path/{challenge_id}/message.asc` file, where `challenge_path` is that specified in the `env.json` configuration file.
B. Assuming your private key has been imported into GPG, run `~$ gpg --output decrypted.asc --decrypt message.asc` to decrypt the `message.asc` file and to place the output into the `decrypted.asc` file.
C. Preserve `decrypted.asc` for step 7. No data should leave the air-gapped environment until step 7 is complete.

### 6. Get `System`

> (6) Result of `system get`:

```bash
~(jormungand)$ python jormungand.py system get
```

```
System ID:  6503d4615774441085bff7fdc1b4dc4f

PUBLIC KEY:

<PUBLIC KEY OMITTED>

--------
GUARANTEE
<GUARANTEE OMITTED>

--------
GUARANTEE SIGNATURE
<GUARANTEE SIGNATURE OMITTED>

--------
DISCLAIMER
<DISCLAIMER OMITTED>

--------
DISCLAIMER SIGNATURE
<DISCLAIMER SIGNATURE OMITTED>

--------
```

The active `System` object contains the public key to which you should encrypt the content of any challenge. An `Announcement` object will become active if this `System` object becomes inactive or is replaced by another with a different public key, but until then, the public key only needs to be fetched once.

### 7. Re-encrypt challenge

This step should be done within the air-gapped environment to ensure security.

A. Import the system public key into GPG: `~$ gpg --import system_public_key.asc`. Remember to make a note of the LONG KEY ID for use in the `--encrypt` command.
B. Encrypt the challenge content in `decrypted.asc`: `~$ gpg --encrypt --output encrytped.asc --recipient $LONG_KEY_ID --armor decrypted.asc`. Substitute the LONG KEY ID for `$LONG_KEY_ID` and make a note of the output filename; in this case, `encrypted.asc`. This file can now leave the air-gapped environment.

### 8. Respond to challenge

> (8) Result of `challenge respond read`:

```bash
~(jormungand)$ python jormungand.py challenge respond read
Enter the Challenge ID to respond to: 1a159673c3a84e8a9299f1037726b871
```

```json
{
  "challenge_id": "1a159673c3a84e8a9299f1037726b871",
  "is_verified": true
}
```

If the output file from the previous step is named correctly (`encrypted.asc`), Jormungand is configured to read it from the `challenge_path/{challenge_id}` directory simply by using the `read` argument with the command `challenge respond`.

If you choose not to use the `read` argument, the `challenge respond` method will prompt you for the re-encrypted content of the challenge. In this case, newlines (`\n`) in the armor text must be replaced with escaped newlines (`\\n`).

### 9. Verify the account

> (9) Result of `account verify`:

```bash
~(jormungand)$ python jormungand.py account verify
```

```json
{
  "challenge_complete": true,
}
```

The solved `Challenge` will allow the `account verify` method to be run. This method takes no arguments and will complete directly.

### 10. Create a `Subscription`

> (10) Result of `subscription create` returns a challenge ID:

```bash
~(jormungand)$ python jormungand.py subscription create
INFO: Run this method leaving arguments blank to generate a Challenge for this method
Enter the activation date:
Enter the number of days the Subscription will be active:
```

```json
{
  "challenge_complete": false,
  "open_challenge_id": "a2f353e65cd74544b1a9c2bc61c55756"
}
```

Creating a `Subscription` will allow the user to access the full offering of the application. It requires a challenge to be solved, and the user should follow the same process outlined in steps 4-8.

Once a challenge has been solved, create a subscription using the `subscription create` method and specify the `duration_in_days` and `activation_date` parameters. Refer to the `subscription create` documentation for more information.

### 11. Attempt to activate the subscription

```bash
~(jormungand)$ python jormungand.py subscription get inactive
```

```json
{
  "415a57638ee54745bcf6f6498840ccbd": {
    "attributes": {
      "origin": "63bc4b94-5997-42c8-82e9-253374343fd0",
      "duration_in_days": 1,
      "activation_date": "2019-06-06 23:00:00+00:00",
      "is_valid_until": "__null",
      "has_been_activated": false,
      "is_active": false
    }
  }
}
```

```bash
~(jormungand)$ python jormungand.py subscription activate
Enter the Subscription ID to activate: 415a57638ee54745bcf6f6498840ccbd
```

```json
{
  "payment_complete": false,
  "open_payment_id": "4214fa1e2f1c4396bf4a716403172e90"
}
```

Running the `subscription activate` method requires a payment to be made. This is similar to the process of solving a challenge. The `Payment` ID will be specified in the response when the `subscription activate` method fails.

### 12. Get `Payment`

```bash
~(jormungand)$ python jormungand.py payment get
Enter the Payment ID or leave blank for all:
```

```json
{
  "4214fa1e2f1c4396bf4a716403172e90": {
    "attributes": {
      "origin": "63bc4b94-5997-42c8-82e9-253374343fd0",
      "is_open": true,
      "time_confirmed": "__null",
      "full_btc_amount": 48297,
      "block_hash": "",
      "txid": ""
    },
    "relationships": {
      "address": "Address.045fbda176534b678b3e6bd48f9592d9"
    }
  }
}
```

Each method blocked by a `Payment` object will include the `Payment` ID. Enter this ID when prompted to fetch this specific payment.

### 13. Get `Address`

```bash
~(jormungand)$ python jormungand.py address get
Enter an Address ID: 045fbda176534b678b3e6bd48f9592d9
```

```json
{
  "045fbda176534b678b3e6bd48f9592d9": {
    "attributes": {
      "value": "16FzUdcw2HVnwXhT73ZbRm57ZqELSTyz2v"
    }
  }
}
```

The `Payment` object includes a reference to the `Address` object that contains the value needed to make a payment. Enter the ID of the `Address` to fetch its data.

### 14. Make payment

Completing a payment requires the submission of a transaction to the Bitcoin blockchain. The transaction should be made taking account of the `address` value specified in the `Address` object and the integer Satoshi value specified in the `Payment` object. A successfully verified transaction will be matched based on these parameters, after which the `Payment` object will be closed by the system. Once the `Payment` has been closed, the action originally blocked by the payment can be completed.

### 15. Activate the subscription

Once the relevant `Payment` object has been closed, this method can be run successfully. Be careful to check the `origin` value of the `Payment` object matches that of the `Subscription` object. Only a `Subscription` with a closed `Payment` with a matching `origin` property can be activated.

### 16. Get subscription

Run the `subscription get` method to fetch details about the recently activated `Subscription`. Please allow up to two minutes for the system to verify the active status of the `Subscription`.

## Walkthrough from active subscriber to FeeReport with data returned

As an active subscriber, the full offering of the application will be available, so check the schema again using `schema reduced`. A fee report gathers data on the latest bitcoin transactions and summarises them in the form of average transaction fee and average transaction fee density, or fee per byte. This allows decisions about optimal fees to be made with a new transaction.

### 1. Create a `FeeReport`

> (1) Result to `fee_report create` returns a challenge ID:

```bash
~(jormungand)$ python jormungand.py fee_report create
INFO: Run this method leaving arguments blank to generate a Challenge for this method
Enter the number of blocks to include in the FeeReport:
```

```json
{
  "challenge_complete": false,
  "open_challenge_id": "914761d0597a44c7833da3b82b727bc1"
}
```

Once the challenge has been solved, run the method again to create the `FeeReport`.

### 2. Get the fee report until the first update has been made

> (2) Before populating

```bash
~(jormungand)$ python jormungand.py fee_report get
Enter the FeeReport ID or leave blank for all:
Enter the active status of the FeeReport (T/F):
```

```json
{
  "6a5cc43d81504d369e90b4e102ac66af": {
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

> (2) After populating

```json
{
  "6a5cc43d81504d369e90b4e102ac66af": {
    "attributes": {
      "is_active": true,
      "blocks_to_include": 1,
      "latest_block_hash": "0000000000000000000bd68725f1ec180cc40f6ab3292ae468af6fb0c02f5de4",
      "is_processing": false,
      "average_tx_fee": 3800.26508447305,
      "average_tx_fee_density": 10.0123897643769,
      "last_update_end_time": "2019-06-12 20:49:42.757694+00:00"
    }
  }
}
```

Running `fee_report get` shows the status of the `FeeReport`. When it is first created, it contains no data and must run calculations before it is first populated.

## Walkthrough from active subscriber to TransactionReport with data returned

A `TransactionReport` allows an address to be watched for transaction outputs that match certain details, such as a value range.

### 1. Create a `TransactionReport`

> (1) Result to `transaction_report create` returns a challenge ID:

```bash
~(jormungand)$ python jormungand.py transaction_report create
INFO: Run this method leaving arguments blank to generate a Challenge for this method
Enter the number of blocks to include in the TransactionReport:
```

```json
{
  "challenge_complete": false,
  "open_challenge_id": "01d4e60bf23048768e087c54a68a8b0d"
}
```

Once the challenge has been solved, run the method again to create the `TransactionReport`.

### 2. Get the transaction report
### 3. Get associated `TransactionMatch` objects
