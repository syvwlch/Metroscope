# What did I learn making Metroscope?

My day job is writing requirements, which someone else then magically transforms into a website people can use to do things. There is a lot more than just writing code to make that magic happen, and I wanted to get a feel for the major tasks involved.

Why?

Because seeing the world thru the eyes of the people who make that magic happen will make my requirements better.

## Domain Matter

This project makes heavy use of NLP (Natural Language Processing) to automate some analysis tasks for poetry: scansion, rhyme schemes. I learned a lot about NLP which may come in handy if I ever work on chat bots, sentiment analysis, etc...

## Writing Code

I've been writing code as a hobby for 35 years... and yet every time I sit down to work on a new project I learn something new about the advantages and disadvantages of different data types, languages, etc...

Since this project uses NLP, I had to resort to new-to-me data types to efficiently store and manipulate raw text as well as the various results of NLP analyses.

I am a firm believer that we write better requirements if we understand how the data is structured and stored.

## Using Databases

Speaking of data structures, this is my first project with a database. It is used to store users, user roles, poems, poets, meters, etc...

I had no idea how much extra work goes into maintaining a database, in particular when you need to change its structure while preserving the data it already contains... or into setting up DBs for dev, QA, staging, and production environments, all of which have different needs and constraints!

## Test Driven Development

This is by far the biggest project I've done, and I am convinced I would have failed without TDD (Test Driven Development).

In TDD, you write the test before you write the functionality. I think of it as writing complete, detailed requirements and test cases which are then automatically enforced.

This gives you, amongst other things:

1. Fully documented requirements, right in your code!

2. Fully commented code

3. Automatic, exhaustive regression testing

4. Granular, reusable code which is easy to refactor

## Refactoring & Tech Debt

I got in the habit of explicitly refactoring code during this project, thanks to TDD.

Once code 'works' you can usually make it cleaner, more efficient, easier to read/maintain/re-use... and the benefits materialized so often it became automatic.

Having the automated tests just made it painless and fearless, and of course the cleaner the code, the easier it is to refactor, so it just felt wrong not to refactor as I went.

Not refactoring would have built up tech debt that would eventually have destroyed my ability to keep moving forward.

## Maintaining a Dev environment

I had to switch machines mid-project, and if I had not followed best practices for setting up and maintaining that dev environment, that would have been a painful roadblock.

As it is, I can work on this project on any machine after:

1. Install Python

2. Install GitHub and log into repository

3. Pull repo down from Github

4. Run one command in terminal to set up virtual environment, install all dependencies with correct version

5. Run another command in terminal to run test suite to make sure everything Frameworks

Done! A prime example of treating your future self as a colleague to onboard as easily as possible.

## Third Party Libraries & Frameworks

This project makes extensive use of third party libraries, and even in its short lifetime I have had to deal with upgrades, sunsets, security vulnerabilities, etc...

Even more fundamentally, this project relies on Flask as a web framework. Choosing to use it was an important decision, and fully vindicated.

A small glimpse into what architects do. :-)

## Managing a Code Base

While this was a single-coder project, I still learned some valuable lessons in managing a code base:

1. Choose and follow a code branching strategy

2. Use Pull Requests to organize functional chunks of work

3. Use Issues to organize bugs and feature requests

## Continuous Integration / Continuous Delivery

CI/CD has been the state of the art in managing the software development lifecycle for websites for years now, but I have never had the chance to work that way professionally. This project was the perfect chance to give it a go, since these days this can be done for free with a variety of tools/services.

The biggest pre-requisite to enabling this being an automated test suite, and TDD having forced me to create one, this was mostly a matter of signing up, linking sites/services, and configuring a few things.

The result was everything I could have hoped for!

Here is my favorite example:

1. Email from a Github bot notifying me that a new security vulnerability has been found for one of my dependencies, with a link to a Pull Request automatically created and which fixes the vulnerability

2. Code with Pull Request applied has already passed the automated test suite

3. Having passed the test suite, a temporary website has been stood up with that
code running on it

4. After a quick UAT on that temporary site, I merged the Pull Request to main code branch with one click

5. Test suite runs on main branch, and passes again

6. Staging site automatically updated to this latest release of main branch

7. After UAT on staging site, I promoted staging to production with one click.

8. Production updated, vulnerability fixed.

So yeah, now I get what all the CI/CD fuss is about!
