# What did I learn making Metroscope?

My day job is writing requirements, which someone else then magically transforms into a website people can use to do things. There is a lot more than just writing code to make that magic happen, and I wanted to get a feel for the major tasks involved.

Why? Because seeing the world thru the eyes of the people who make that magic happen will make my requirements better.

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

As it is, to work on this project on a new machine, I can just:

1. Install Python

2. Install GitHub and log into repository

3. Pull repo down from Github

4. Run one command in terminal to set up virtual environment, install all dependencies with correct version

5. Run another command in terminal to run test suite to make sure everything works

6. Done, start coding!

A prime example of treating your future self as a colleague to onboard as easily as possible.

## Third Party Libraries & Frameworks

This project makes extensive use of third party libraries, and even in its short lifetime I have had to deal with upgrades, sunsets, security vulnerabilities, etc...

Even more fundamentally, this project relies on Flask as a web framework. Choosing to use it was an important decision, and fully vindicated.

A small glimpse into what architects do. :-)

## Managing a Code Base

While this was a single-coder project, I still learned some valuable lessons in managing a code base:

1. Choose and follow a code branching strategy

2. Use Issues to organize bugs and feature requests

3. Use Pull Requests to organize functional chunks of work

## Continuous Integration / Continuous Delivery

CI/CD has been the state of the art in managing the software development lifecycle for websites for years now, but I have never had the chance to work that way professionally. This project was the perfect chance to give it a go, since these days this can be done for free with a variety of tools/services.

The biggest pre-requisite to enabling this being an automated test suite, and TDD having forced me to create one, this was mostly a matter of signing up, linking sites/services, and configuring a few things.

The result was everything I could have hoped for!

Here is my favorite example:

1. Email from a Github bot, notifying me that:

    * a new security vulnerability has been found for one of my dependencies

    * a Pull Request was automatically created to fix the vulnerability

    * the code with the PR applied has already passed the automated test suite

    * a temporary website has been deployed with that code for me to check

2. After a quick review of the new code and the temporary site, I merged the Pull Request to main code branch with one click on GitHub, which triggered:

    * the test suite on main branch, which passed again

    * deployment of this latest release to the staging site

3. After a quick check of the staging site, I promoted staging to production with one click on GitHub, and:

    * Production updated, vulnerability fixed.

So yeah, now I get what all the CI/CD fuss is about. Total elapsed time, maybe twenty minutes and all it took was two clicks on GitHub and a bit of sanity testing on the temporary site.

## Conclusion

This is just the tip of the iceberg. I am still in no way a professional developer, but I have a renewed and much deeper appreciation for some of the work they do which is not actually writing code.

Now I can take all this with me the next time I write some requirements.

## Resources:

We get a free subscription to [O'Reilly ebooks](https://www.oreilly.com/) thru work, just use the SSO option to sign in. Some of these are excellent, fully able to walk you thru your newb-to-journeyman adventures. Some favorites of mine:

* [Test Driven Development with Python](https://www.goodreads.com/book/show/17912811-test-driven-web-development-with-python)

* [Flask Web Development: Developing Web Applications with Python](https://www.goodreads.com/book/show/18774655-flask-web-development)

* [Mastering Flask Web Development: Build enterprise-grade, scalable Python web applications](https://www.goodreads.com/book/show/42855654-mastering-flask-web-development)

There are some excellent YouTube channels covering the same territory, if books are not your favorite learning medium:

* Corey Schafer's [Python tutorials for beginners](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) are a great place to start with the language

* He does a great job [explaining what git is](https://www.youtube.com/playlist?list=PL-osiE80TeTuRUfjRe54Eea17-YfnOOAx), and why/how you use it

* His [Flask playlist](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) has you build a blog using Flask


[GitHub](https://github.com) is an excellent choice to host your code repository. They have excellent apps/tools, their free accounts are full featured, the community is friendly and very knowledgeable, and they integrate with everyone and their uncle. Hit me up at [/syvwlch](https://github.com/syvwlch) there!

[Travis CI](https://travis-ci.com/) is an excellent choice to automate your testing/integration. It plugs into Github to run your test suite on Pull Requests, branches, etc... and report the results back into your GitHub workflows.

[Heroku](https://www.heroku.com/) is an excellent choice for host your deployment pipeline. It also plays very nicely with Github, and for demos/POCs it is free. If you need a database for your site, they make it very easy.

[Python](https://www.python.org/) is a full-featured, modern, widely adopted programming language that is easy to learn and forces good habits. Give it a try if you don't already have a favorite language.

[Flask](https://palletsprojects.com/p/flask/) is a web framework in the Python language. It takes cares of all the low level stuff for you, but doesn't make assumptions about what your site/project is trying to do, so you only need use what you actually need. People have used to build websites, blogs, or web-APIs. It's great for learning how a website works, because you actually need to build all the plumbing, but it makes it very easy.

Lastly, feel free to reach out to me if you want a hand with any of this!
