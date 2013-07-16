#Furuikeya Protocol

##About
Furuikeya is a small python program whose goal is to generate haikus from twitter API 1.1.

##The Haiku
What is a [Haiku](http://en.wikipedia.org/wiki/Haiku)?

A haiku is a Japanese short poem and consist of three structural criteria:

###Verses
Three verses : a short one of five syllables, a long one of seven syllables and finally another short one of five syllables.
The final structure of the poem is therefore 5/7/5.

###Kireji
A kireji, or cutting word, whose aim is to divide the poem into two parts. A haiku is therefore often considered as a 12/5 or 5/12 syllables composition.

###Kigo
Finally, a kigo, or season word, whose aim is to symbolize the season defining the ambiance of the poem.

One fact, which is seldom known by occidental people, is that haijins (haiku poets) using a particular kigo
consciouly or unconsciously in the haiku, tie their poem to every other haikus ever written and containing the same kigo.

This enable haijins to build beautiful litterary networks and canvases from this implied intertextuality.

For instance, in this famous haiku by Matsuo Bashô and from which I entitled the program :

```
Furuike ya kawazu tobikomu mizu no oto.

The Ancient Pond -
A Frog jumps in
Water's Sound.

(古池 蛙飛び込む 水の音), Matsuo Bashô
```
the kigo is kawazu, an ancient word meaning 'frog' and symbolizing spring.

##Concept
Hence, the main idea behind furuikeya is to consider Twitter's hashtags as an equivalent concept to the kigo.
Indeed, using a hashtag in a tweet will indicate which themes you are supposed to evoke within it and does
link it to every other tweet using the same one.

Let's use it to generate haikus then.

##Protocol
How does furuikeya work technically?

First of all, the program must be fed with a kigo. "Moon", for instance.

Hence, the program will ask Twitter API for tweets concerning the kigo hashtag.

Then, a blank haiku is created and a kireji is randomly selected from a list of common used kireji
in english haikus such as '-', ';', ',' and other several punctuations. Its positions, i.e. between first and
second verse of between second and third verse, is also choosen randomly.

The program has now to parse the tweets to find potential verses for the haiku. The tweets are filtered and cleaned
following some procedures that you may find at the beginning of the file 'model/protocol.py'.

The tweets are then cut into sentences parts. Syllables are counted and every piece that has +- 1 syllables from 5 or 7 is kept to
become a verse.

Once the haiku is finished, it is outputted by the program.

##Philosophy
The claim of the furuikeya program is not to convey that litterature can be procedurally generated. On the contrary, the aim of
furuikeya is just to communicate a reflexion about poetry and litterature as a whole.

This being said, one has to know that the furuikeya program is able to produce a grammatically correct haiku
every 20 tries and gives a aesthetically correct one every 50. The intervention of a human is still needed to
determine which ones are good and which ones are not. This is therefore a reflexion about choice and serendipity in
litterature rather than the annihilation of artistic creativity.

##The Saijiki
A saijiki, in Japanese, is an index of the most common kigos used in haikus.

In furuikeya, a file ('config/saijiki.txt') symbolizes your personal saijiki in which you can write
a kigo per line. This file can be used afterwards by the program to batch generate haikus.

##Installation
To install furuikeya, simply clone it into the desired directory and the download its dependencies.
(Be advised that you should use a virtualenv and install the dependencies within it.)

```sh
git clone https://github.com/Yomguithereal/furuikeya.git
cd furuikeya
pip install -r requirements
```

Hence, you should edit the settings.example.yml file to fill in your twitter authentification. Rename the file to
settings.yml afterwards.

```yaml
twitter:
    consumer_key: 'YOUR_CONSUMER_KEY'
    consumer_secret: 'YOUR_CONSUMER_SECRET'
    oauth_token: 'YOUR_OAUTH_TOKEN'
    oauth_secret: 'YOUR_OAUTH_SECRET'
```

##Usage

```sh
# Generating one haiku with a random kigo from the saijiki
python furuikeya.py

# Generating <N> haikus with a random kigo from the saijiki
python furuikeya.py -n/--number <N>

# Generating one haiku with selected <K> kigo
python furuikeya.py -k/--kigo <K>

# Generating <N> haikus with selected <K> kigo
python furuikeya.py -n/--number <N> -k/--kigo

# Generating one haiku per kigo in saijiki
python furuikeya.py -s/--saijiki

# Generating <N> haikus per kigo in saijiki
python furuikeya.py -s/--saijiki -n/--number <N>
```

##Dependencies
	
	python 2.7
	sylli
	numpy
	pyyaml
	nltk
	twitter
	colifrapy

Furuikeya uses [Sylli](http://sylli.sourceforge.net/install.html) library to count syllables.