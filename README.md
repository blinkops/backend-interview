# Blink-backend-interview
Take home exercise for a BE position
## Problem Definition

A busy hospital has a list of patients waiting to see a doctor. The waitlist is created sequentially (e.g. patients are added in a fifo order) from the time the patient calls.  Once there is an availability, the front desk calls each patient to offer the appointment in the order they were added to the waitlist. The staff member from the front desk has noticed that she wastes a lot of time trying to find a patient from the waitlist since they&#39;re often not available, don&#39;t pick up the phone, etc.  She would like to generate a better list that will increase her chances of finding a patient in the first few calls.

## Interview Task

Given patient demographics and behavioral data (see sample-data/patients.json), create an algorithm that will process a set of historical patient data and compute a score for each patient that (1 as the lowest, 10 as the highest) that represents the chance of a patient accepting the offer off the waitlist. Take in consideration that patients who have little behavior data should be randomly added to the top list as to give them a chance to be selected. Expose an api that takes a facility's location as input and returns an ordered list of 10 patients who will most likely accept the appointment offer.

## Weighting Categories

Demographic

- age  (weighted 10%) (the older the patient->the higher priority it gets)
- distance to practice (weighted 10%) (closer patients->have higher priority)

Behavior

- number of accepted offers (weighted 30%) (high number of accepted offers->higher priority)
- number of cancelled offers (weighted 30%) (less cancellations->higher priority)
- reply time (how long it took for patients to reply) (weighted 20%) (quicker reply time->higher priority)

## Patient Model

- ID
- Age (in years)
- location
  - Lat
  - long
- acceptedOffers (integer)
- canceledOffers (integer)
- averageReplyTime (integer, in seconds)

## Deliverables

The code should be written in Python or Golang and the api should be called using a REST call like this: /patients?location=<location>
It should contain documentation and unit tests that show your understanding of the problem. Once you&#39;re finished, submit a PR to this repo and add havivrosh as the reviewer.
