---
title: Start

toc_footers:
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

search: true
---

# Introduction

Welcome to Transactino! This application provides useful information about the bitcoin blockchain for an easy-to-use bitcoin subscription with bulletproof security via GPG.

Named for the Norse World-serpent that brings about Ragnarok, Jormungand is the first user client for the Transactino application. Although this client allows a user to take advantage of almost all features of the API, it is highly recommended to access the API through a custom interface for more serious use, as this allows a user to control finer-grained aspects of the API, such as complex error handling.

A more detailed guide to the API can be found here: [API]

## Latest release

[1.3.0](www.transactino.com/releases/jormungand_1.3.0.zip)

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

Any method that requires a challenge to be solved or a payment to be submitted can be run initially with no arguments. In fact, most commands will initially ignore all arguments until its criterion is met.

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

```bash
~$ python jormungand.py create account
```

> This returns:

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

The Account model holds information about the public key registered on the system.

The `account create` command takes the public key from the path provided in the `env.json` file. Once an account has been created, the IP address used to access the system will be locked to the public key. Any request from the IP address will be treated as though it comes from this account. For this reason, it is prudent to ensure you have complete control of the IP you are using. Sensitive changes to the account data on the system will require GPG challenges for security. You can create more IP addresses for this account once you have an active subscription.

`account verify` takes no arguments and requires a challenge to be solved. This first challenge proves that the account holder has control of a corresponding private key.

`account delete` requires a challenge to be solved and removes all data related to the account on the system.

`account lock` requires a challenge to be solved and prevents all access to the system by the account in question until another command is given to unlock.

## Challenge

A Challenge contains a plaintext piece of data that is delivered once it has been encrypted to the public key of the account. Once the account holder receives this information, it must be decrypted using their private key and re-encrypted to the public key of the system before being sent back to close the challenge. In this way, the holder of the public key proves their possession of the corresponding private key. This process is repeated with a new piece of plaintext every time the user wishes to modify data on the system.

For clarity, each challenge occurs in the following order:

1. The user submits a request that is restricted for security purposes.
2. A challenge object is created on the user account, with an `origin` relevant to the action.
3. The user makes a request for the data contained in the challenge, and receives a piece of ascii armor data, `A` encrypted to their public key.
4. The user decrypts `A` using their private key to yield `B`, proving that they possess it.
5. The user makes a request for the public key of the system.
6. The user encrypts `B` to the public key of the system, yielding `C`.
7. The user makes a request containing `C` to respond to the challenge.
8. The user re-attempts the action attempted in step 1.

### challenge get

`challenge get (closed) (save)` returns the set of challenges, either `closed` or not, on the user account. The `save` argument will write the encrypted content of the challenge to the directory specified in `env.json`. A directory will be created if it does not exist, named for the ID of the challenge, containing the file `message.asc`.

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

A subscription is a formal agreement between the user and the system for a set period of time, backed by a fixed bitcoin payment made to a given address. The address to be used for a payment is revealed when the payment is opened. For as long as a subscription is active, the user has access to all offerings available on the system.

Multiple subscriptions can be created with different start and end points, and it is theoretically possible for multiple subscriptions to be active simultaneously, although this comes with no additional benefits. The control of this is left to the user's discretion.

The subscription process happens in two stages. In the first stage, a subscription object is created, requiring a challenge. In the second stage, the subscription must be activated, requiring a payment. As a restriction on user actions, a payment behaves in a very similar manner to a challenge, expect for the fact that a user is dependent on the behaviour of the bitcoin blockchain for the payment to be closed.

### subscription get

`subscription get (inactive)` returns the set of subscriptions, either `inactive` or not, on the user account.

Parameter | Default | Description
--------- | ------- | -----------
`subscription_id` | `null` | Optional, specifies the subscription ID to get.

### subscription create

`subscription create` creates a subscription on the user account. This requires a challenge to be solved.

Parameter | Description
--------- | -----------
`duration_in_days` | The number of days for which the subscription should be active.
`activation_date` | The date on which the subscription should start. The Jormungand client forces the timezone of the date to be set to the timezone of the local user system, but the remote system will accept any valid datetime for this parameter.

It is important to note that the date value submitted to the system is left to the user's discretion. It is possible to enter a date before the current date, in which case the subscription will activate immediately upon closure of the payment, as though the activation date had been the moment of payment closure. It is also possible to set an activation date in the future, in which case the system will not activate the subscription until that date has passed, even if the payment has been closed. This can be used to chain subscriptions if needed.

The date parser on the system supports most common date formats, but it will normalise the date entered into a common format. Check this date using `get` to satisfy yourself that the activation date the system has interpreted is correct. If it is not, use `delete` to remove the subscription and create a new one. If the system is unable to parse the date you have entered, it will return an error.

### subscription activate

`subscription activate` marks a subscription for activation. If the activation date is in the future, the system will not activate the subscription until that time, but this command must be run to allow that to happen. This method requires a payment to be submitted. Each subscription has a unique `origin` property that can be viewed by using `get`. Only the payment with this `origin` can be closed to allow this specific subscription to be activated.

Parameter | Description
--------- | -----------
`subscription_id` | The ID of the subscription to be activated.

It is important to note that the process of activation is decoupled from user action via this method and relies only on the system's cycle of verification to determine the status of each subscription. The user must wait for the timing of this cycle to address the subscription in question. This can take up to two minutes. The status of the subscription can be checked using `get`.

### subscription delete

`subscription delete` deletes a subscription. This requires a challenge to be solved and is irreversible.

Parameter | Description
--------- | -----------
`subscription_id` | The ID of the subscription to be deleted.

This method is **irreversible** and **independent of the status of the subscription**. This means that a subscription that is active and paid-for can still be deleted. This is left to the user's discretion.

## IP



## Payment

A payment is needed to allow access to several offerings within this application. All payments are mediated by the bitcoin blockchain. A typical payment is made by creating a transaction with an output that specifies the correct address given and the correct unique amount. The unique amount acts as an identifier that allows an automatic system
to differentiate payments. Payment amounts will be given as an integer representing the number of Satoshi required.

Payments on an account cannot be interacted with or modified in any way, except in the case of deletion.

The lifetime of a typical payment follows this series of steps:

1. The user attempts an action that is restricted by a payment.
2. A payment is opened with an `origin` property that connects it to the action.
3. The user makes a request for the `Address` object referenced in the payment.
3. The user creates a transaction with the value of the address and the unique amount specified in the payment.
4. The user waits for the transaction to be mined.
5. Once the transaction is detected on the blockchain, the payment will be closed on the system.
6. The user re-attempts the action.

### payment get

`payment get (closed)` returns details of open payments, unless the `closed` argument is included. This can be used to find the `origin` and `unique_btc_amount` properties for a specific payment.

Parameter | Default | Description
--------- | ------- | -----------
`payment_id` | null | Optional, specifies the payment ID to get.

### payment delete

`payment delete` deletes a payment. This command should be used if you do not wish to continue with an open payment in order to enable a method. For example, if making a payment for `subscription activate`, the payment can be removed to reset the method.

Parameter | Description
--------- | -----------
`payment_id` | The ID of the payment to be deleted.

This is **irreversible** and is left to the user's discretion.

## Fee Report

A fee report contains regularly updated statistical details about the fee information contained in bitcoin blocks. For example, the average fee in Satoshi and the average fee weight in Satoshi per byte are provided. When creating a fee report, the user has the option to specify that this average should be calculated over a certain number of blocks, e.g. ten. Thus, the updated average fee would be that of all transactions in the latest ten blocks. This moving average is meant to give users planning to submit transactions an idea of what fee they should provide. These values are updated as soon as possible following the mining of a new block.

### fee_report get

`fee_report get (inactive)` returns details about fee reports on the account. The `inactive` flag will return inactive fee reports. Use the `activate` method to set the active status of a fee report to add or remove it from your focus.

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

The `activate` method controls the active status of the fee report.

Parameter | Description
--------- | -----------
`fee_report_id` | The ID of the fee report.
`is_active` | The active status of the fee report to set.

### fee_report delete

The `delete` method permanently deletes the fee report from the user account.

Parameter | Description
--------- | -----------
`fee_report_id` | The ID of the fee report to delete.

## Transaction Report

A transaction report monitors the blockchain for transaction outputs that match its requirements. A single address to watch must be specified, along with upper and lower bounds, or alternatively an exact value, for the integer output in Satoshi. A successful match will yield TransactionMatch objects.

### transaction_report get

`transaction_report get (inactive)` returns details about transaction reports on the account. The `inactive` flag will return inactive transaction reports. Use the `activate` method to set the active status of a transaction report to add or remove it.

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

The `activate` method controls the active status of the transaction report.

Parameter | Description
--------- | -----------
`transaction_report_id` | The ID of the transaction report.
`is_active` | The active status of the transaction report to set.

### transaction_report delete

The `delete` method permanently deletes the transaction report from the user account.

Parameter | Description
--------- | -----------
`transaction_report_id` | The ID of the transaction report to delete.

## Transaction Match

Transaction match objects represent successful matches of their corresponding transaction report objects. They can be filtered by a variety of useful parameters including their parent address and the hash of the block they occurred in.

### transaction_match get

The `get` method makes several filters available to find the correct results from transaction reports.

Parameter | Description
--------- | -----------
`transaction_report_id` | The ID of the parent transaction report.
`transaction_report_target_address` | The target address of the parent transaction report.
`transaction_report_is_active` | The active status of the parent transaction report.
`transaction_match_id` | The ID of the transaction match object.
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

## Walkthrough from anonymous user to active subscription
## Walkthrough from active subscriber to Fee Report with data returned
## Walkthrough from active subscriber to Transaction Report with data returned
