## Creator: aart17
#### Programming language: Python 3.9
#### Library: telebot
#### Time of creation: 11/15/2023
________

This project consists of two telegram bots linked by a database

The first bot, aka the main bot, offers the user the choice to watch a meme, a joke, or give a feedback
connection if a person chooses to watch a meme, the bot responds with a message in which you have to select the type of content,
by selecting the type the bot takes the last 10 records from the database and shows them to the user

The second bot is created only for the administration of the first one, with its help you can
1 add new entries
2 Add new admins
3 Consider feedback
4 Mass notify the main bot users

Also attached to the project is a database with ready-made memes and anecdotes on which performance tests were conducted

Here's a diagram of how it works
![Diagram]([https://coggle.it/diagram/ZVdHJK_HfWTHvWPU/t/%D0%B1%D0%BE%D1%82-%D1%81%D0%BE-%D1%81%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D1%8B%D0%BC%D0%B8-%D0%BC%D0%B5%D0%BC%D0%B0%D0%BC%D0%B8-%D0%B2-%D1%82%D0%B3/5a335211177b882eb7452d061c5d383949b3a7a8de1a423ecfbc55feb85ece98](https://coggle-downloads-production.s3.eu-west-1.amazonaws.com/06a2ef230b6f7f246e632def8b9705832ce6e48b5ae7e4b6995107360abae2b2/_____.pdf?AWSAccessKeyId=ASIA4YTCGXFHOLCY35WJ&Expires=1710716241&Signature=qKCUh%2F0spE4ZrOWNxYKD8vXzDKU%3D&X-Amzn-Trace-Id=Root%3D1-65f720f0-ba6ba4b4e974040760bd817f%3BParent%3D2835370414296138%3BSampled%3D0%3BLineage%3D51963df5%3A0&x-amz-security-token=IQoJb3JpZ2luX2VjELn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCWV1LXdlc3QtMSJIMEYCIQDK0%2Bzzl7zJi2srNnwk4bYyys3E2JXXMI1mAGerf9Es1QIhAMy5B6ebEbbkU1EUcRHGbnSLMsIVF23WJZtKOwRWbbhJKosDCML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMODc3NDUzMDMxNzU4IgzJSE1YWZghyyF64Qsq3wItbC2wKegoT98Vk%2F8eGvEFs9Ve0djOefUX3dosshYWCsltSBdTReThgPwzK0CMjx%2BKF2U51s%2FMXcQeiP4V4WTxEAFF4soeOQgo4dgPiawwb%2BB61CIu6%2FLc9kw%2Fhi%2BSZtGv14kRrUY8klKVqsgEHlqKGcFY1MzAV%2FYtEHQujujKV8e92V7Q0szjiBcCfuTmXGm958skinRrZ5K4vV8iwB4TsSmQ9fto%2B0jE6FtAho1BuqFHglawOIUHm6ifh8AGkK6pbLARrqI09SsiSrbR%2FIt8iT7LYejJ%2BjppPzzzGl%2BNrUOwJvwoPmA6q8nKwCNBxNIB3Bagf9gWYvpMeAMjmgrlV6P1meTIBVWKrikaYcZhGJFdXuHNd7ev4aPJ2i7qC%2BCnqEHWcSzaBDYIvV80rfvm56z7A%2FR7SQl8JAOnHrYmBxsMHgINLjXUW6lhkoiXpisx83IX5PURS9uF0SWOMGgwqrXcrwY6nQEBkLHNeGOhpNoD31jPw8t1D6sueS6NjOhXZn%2FYJ281tv3D4Y6qejPCPzXgd3gkkHra4nw77fwxpHkJIh%2FriRiEjnLnZl5smC0d2nRZellAmpX68MiOVRe48lxhub03ZlfgyM%2FX%2FmsOUcmYRl%2FJWmujqlRV1dh9UgSGD3wh8yiVw7eqU5yh91jG%2BAdlN5PqPw%2Bi7mSlCeSmgD5apPUX)https://coggle-downloads-production.s3.eu-west-1.amazonaws.com/06a2ef230b6f7f246e632def8b9705832ce6e48b5ae7e4b6995107360abae2b2/_____.pdf?AWSAccessKeyId=ASIA4YTCGXFHOLCY35WJ&Expires=1710716241&Signature=qKCUh%2F0spE4ZrOWNxYKD8vXzDKU%3D&X-Amzn-Trace-Id=Root%3D1-65f720f0-ba6ba4b4e974040760bd817f%3BParent%3D2835370414296138%3BSampled%3D0%3BLineage%3D51963df5%3A0&x-amz-security-token=IQoJb3JpZ2luX2VjELn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCWV1LXdlc3QtMSJIMEYCIQDK0%2Bzzl7zJi2srNnwk4bYyys3E2JXXMI1mAGerf9Es1QIhAMy5B6ebEbbkU1EUcRHGbnSLMsIVF23WJZtKOwRWbbhJKosDCML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMODc3NDUzMDMxNzU4IgzJSE1YWZghyyF64Qsq3wItbC2wKegoT98Vk%2F8eGvEFs9Ve0djOefUX3dosshYWCsltSBdTReThgPwzK0CMjx%2BKF2U51s%2FMXcQeiP4V4WTxEAFF4soeOQgo4dgPiawwb%2BB61CIu6%2FLc9kw%2Fhi%2BSZtGv14kRrUY8klKVqsgEHlqKGcFY1MzAV%2FYtEHQujujKV8e92V7Q0szjiBcCfuTmXGm958skinRrZ5K4vV8iwB4TsSmQ9fto%2B0jE6FtAho1BuqFHglawOIUHm6ifh8AGkK6pbLARrqI09SsiSrbR%2FIt8iT7LYejJ%2BjppPzzzGl%2BNrUOwJvwoPmA6q8nKwCNBxNIB3Bagf9gWYvpMeAMjmgrlV6P1meTIBVWKrikaYcZhGJFdXuHNd7ev4aPJ2i7qC%2BCnqEHWcSzaBDYIvV80rfvm56z7A%2FR7SQl8JAOnHrYmBxsMHgINLjXUW6lhkoiXpisx83IX5PURS9uF0SWOMGgwqrXcrwY6nQEBkLHNeGOhpNoD31jPw8t1D6sueS6NjOhXZn%2FYJ281tv3D4Y6qejPCPzXgd3gkkHra4nw77fwxpHkJIh%2FriRiEjnLnZl5smC0d2nRZellAmpX68MiOVRe48lxhub03ZlfgyM%2FX%2FmsOUcmYRl%2FJWmujqlRV1dh9UgSGD3wh8yiVw7eqU5yh91jG%2BAdlN5PqPw%2Bi7mSlCeSmgD5apPUX)
