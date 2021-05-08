# DeepESG Data Processing Technical Challenge

## Introduction

Coding of DeepESG data processing test.

Basically, a dictionary was created with all the accounts and to perform the accounting of general_ledger, added the account value to all the higher accounts by a set of strings.
Example: account AA.BB.CC.DD had an associated value of 100.00. This value is added to the existing values of AA.BB.CC.DD, AA.BB.CC, AA.BB and AA.

## About DB

The database chosen for demonstration purposes was Sqlite. To change the DB, just change the connection in the dbConnect method.

## Time for development

The duration of the development was 4 hours and 20 minutes.

In the first 2 hours and 20 minutes, some recursion attempts were made to generate the dictionaries, partly but not entirely successful. From that moment on, a new strategy was devised, abandoning recursion and choosing to work with the key string.

It became easier to understand and maintain.
