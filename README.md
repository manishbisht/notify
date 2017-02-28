## Name
Contest Notify

## Tagline
Amazon Alexa Skill kit that will tell you the details about the programming contest from different websites

## Inspiration
I am a programmer that uses the different programming websites to improve my algorithmic knowledge. Everyday I have to check that is there any contest coming on website for today. Now to save my time on just checking these websites regularly I have given this task to Alexa. So doesn't it looks quite cool that now I can ask Alexa about the upcoming or current contests from different websites and she will tell you the details about the contests.

Also the [Amazon Alexa Skills Challenge on Devpost](https://alexa.devpost.com/) have **$43,620 in prizes** what more I need as an Inspiration :)

## What it does
This is a Amazon Alexa Skill Kit that will update you about the current and future programming contest available on different websites like codeforces, codechef and hackerrank. You can ask questions like When is the codefoces next contest, when is the next hackerrank contest or Is there any contest running on codechef. Right now this skill support only codeforces, codechef and hackerrank. I will update it for all major programming websites.

## How I built it
I have never build this type of application before so I have followed links from the resources tab and the [Amazon Alexa documentation](https://developer.amazon.com/alexa-skills-kit). I have used python 2.7 to build this skill and the backend is hosted on AWS Lamda. I have also used BeautifulSoup Python Library to dynamically get the required content from the contest pages.

## Challenges I ran into
I have faced many issues while building this entire project.
1. I have learnt how to use Amazon AWS to host the Amazon Skills Kit backend.
2. The datetime format is different on all the contest pages so I have to deal with datatime objects and then format it according to the need.
3. I have learnt about scrapping web pages as all the contest websites doesn't provides their API.
4. I have changed the maximum execution time to 10 seconds so that the content is retrived properly. But I have to improve it more so that it becomes more responsive.
5. I have to create the deployment package for this project as it uses BeautifulSoup that is not by default included in AWS Lamda.

While there are other issues also but with awesome Amazon Alexa and Amazon AWS documentation these problems can be easily solved bu anyone.
 
## Accomplishments that I'm proud of
Finally now Alexa can tell me the details about the current and upcoming contests. So no need to regularly check the websites. Ask Alexa :)
Below is the link to get the details about enabling the skill on your device.

## What I learned
1. How t use Amazon AWS Lamda.
2. How to do web scrapping using BeautifulSoup library in Python 2.7
3. Last but the major How to create Amazon Alexa Skills Kit.

## What's next for Contest Notify
I will try to improve it in my free time. I will add the support for more programming websites. Also I will add the feature to register for the contests.

I will also add function to get the Hackathon details also. and may be next time you will be using this skill to register for the upcoming devpost hackathon. :p

## Try It Out
https://www.amazon.com/Manish-Bisht-Contest-Notify/dp/B06W5B8BS9/

## About me
I have worked on creating the amazon alexa skills kit using python 2.7 and BeautifulSoup Python library to get the required content from the web pages. And then I have hosted the backend on Amazon AWS Lamda. It was my first time using BeautifulSoup and Amazon AWS, Sometimes I have faces some issues also but at the end I have learnt a lot of new things.
