# SoloConnect
[![Build Status](https://app.travis-ci.com/gcivil-nyu-org/Wednesday-Fall2023-Team-5.svg?branch=develop)](https://app.travis-ci.com/gcivil-nyu-org/Wednesday-Fall2023-Team-5)

Team Members: 
Mike Zacharchenko 
Kumud Ravisankaran
Rishabh Verma
Rishie Nandhan Babu 


master: [![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/Wednesday-Fall2023-Team-5/badge.svg?branch=master)](https://coveralls.io/github/gcivil-nyu-org/Wednesday-Fall2023-Team-5?branch=master)
develop: [![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/Wednesday-Fall2023-Team-5/badge.svg?branch=develop)](https://coveralls.io/github/gcivil-nyu-org/Wednesday-Fall2023-Team-5?branch=develop)

SoloConnect is a full stack web application that aims to connect solo travelers with one another while they're abroad to facilitate face-to-face interaction and create more meaningful memories/experiences. Our goal is to improve safety during solo travel by helping users dynamically create travel groups and make unfamiliar environments not feel quite so foreign. 

SoloConnect is hosted using AWS Elastic Beanstalk and uses a Django/Channels/PostgreSQL stack on the backend and HTML/Bootstrap5/JavaScript on the front-end. These technologies were a great fit for many of the business problems we aimed to solve, and we've found this stack to be great to work with and an excellent educational experience.

Key Features:
- Creating a full user profile complete with bio, 5 profile images, age, education information, and set of interests
- Creating and updating trips to a set of the most popular tourist destinations in the 10 most popular countries for tourism in the United States
- Sending and receiving match requests between users visiting the same destination on overlapping dates
- Filtering the trip-level match pool based on a set of hard filters (age, spoken language) and using a KNN classifier to order the match pool by similarity score based on a set of soft filters (travel interests, smoking/drinking preference, education level, etc.)
- WebSocket-enabled real time chat between matched users with dynamic thread creation on match and dynamic deletion on unmatch

For a more detailed description of our features, UML diagrams, and overall project proposition, please see our wiki.

Our team would also like to shout out and thank Emma Dawson for her ongoing help with graphic design and user interface planning. Emma is a very talented graphic designer and digital marketer, and she can be reached for project work at edawson7@fordham.edu
