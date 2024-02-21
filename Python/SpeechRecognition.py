{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "I am ready for your command\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n",
      "Your last command couldn't be heard\n",
      "Ready...\n"
     ]
    }
   ],
   "source": [
    "\n",
    "from gtts import gTTS\n",
    "import speech_recognition as sr\n",
    "import os\n",
    "import re\n",
    "import webbrowser\n",
    "import smtplib\n",
    "import requests\n",
    "#from weather import Weather\n",
    "\n",
    "def talkToMe(audio):\n",
    "    \"speaks audio passed as argument\"\n",
    "\n",
    "    print(audio)\n",
    "    for line in audio.splitlines():\n",
    "        os.system(\"say \" + audio)\n",
    "\n",
    "    #  use the system's inbuilt say command instead of mpg123\n",
    "    #  text_to_speech = gTTS(text=audio, lang='en')\n",
    "    #  text_to_speech.save('audio.mp3')\n",
    "    #  os.system('mpg123 audio.mp3')\n",
    "\n",
    "\n",
    "def myCommand():\n",
    "    \"listens for commands\"\n",
    "\n",
    "    r = sr.Recognizer()\n",
    "\n",
    "    with sr.Microphone() as source:\n",
    "        print('Ready...')\n",
    "        r.pause_threshold = 1\n",
    "        r.adjust_for_ambient_noise(source, duration=1)\n",
    "        audio = r.listen(source)\n",
    "\n",
    "    try:\n",
    "        command = r.recognize_google(audio).lower()\n",
    "        print('You said: ' + command + '\\n')\n",
    "\n",
    "    #loop back to continue to listen for commands if unrecognizable speech is received\n",
    "    except sr.UnknownValueError:\n",
    "        print('Your last command couldn\\'t be heard')\n",
    "        command = myCommand();\n",
    "\n",
    "    return command\n",
    "\n",
    "\n",
    "def assistant(command):\n",
    "    \"if statements for executing commands\"\n",
    "\n",
    "    if 'open reddit' in command:\n",
    "        reg_ex = re.search('open reddit (.*)', command)\n",
    "        url = 'https://www.reddit.com/'\n",
    "        if reg_ex:\n",
    "            subreddit = reg_ex.group(1)\n",
    "            url = url + 'r/' + subreddit\n",
    "        webbrowser.open(url)\n",
    "        print('Done!')\n",
    "\n",
    "    elif 'open website' in command:\n",
    "        reg_ex = re.search('open website (.+)', command)\n",
    "        if reg_ex:\n",
    "            domain = reg_ex.group(1)\n",
    "            url = 'https://www.' + domain\n",
    "            webbrowser.open(url)\n",
    "            print('Done!')\n",
    "        else:\n",
    "            pass\n",
    "\n",
    "    elif 'what\\'s up' in command:\n",
    "        talkToMe('Just doing my thing')\n",
    "    elif 'joke' in command:\n",
    "        res = requests.get(\n",
    "                'https://icanhazdadjoke.com/',\n",
    "                headers={\"Accept\":\"application/json\"}\n",
    "                )\n",
    "        if res.status_code == requests.codes.ok:\n",
    "            talkToMe(str(res.json()['joke']))\n",
    "        else:\n",
    "            talkToMe('oops!I ran out of jokes')\n",
    "\n",
    "    elif 'current weather in' in command:\n",
    "        reg_ex = re.search('current weather in (.*)', command)\n",
    "        if reg_ex:\n",
    "            city = reg_ex.group(1)\n",
    "            weather = Weather()\n",
    "            location = weather.lookup_by_location(city)\n",
    "            condition = location.condition()\n",
    "            talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))\n",
    "\n",
    "    elif 'weather forecast in' in command:\n",
    "        reg_ex = re.search('weather forecast in (.*)', command)\n",
    "        if reg_ex:\n",
    "            city = reg_ex.group(1)\n",
    "            weather = Weather()\n",
    "            location = weather.lookup_by_location(city)\n",
    "            forecasts = location.forecast()\n",
    "            for i in range(0,3):\n",
    "                talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'\n",
    "                         'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))\n",
    "\n",
    "\n",
    "    elif 'email' in command:\n",
    "        talkToMe('Who is the recipient?')\n",
    "        recipient = myCommand()\n",
    "\n",
    "        if 'John' in recipient:\n",
    "            talkToMe('What should I say?')\n",
    "            content = myCommand()\n",
    "\n",
    "            #init gmail SMTP\n",
    "            mail = smtplib.SMTP('smtp.gmail.com', 587)\n",
    "\n",
    "            #identify to server\n",
    "            mail.ehlo()\n",
    "\n",
    "            #encrypt session\n",
    "            mail.starttls()\n",
    "\n",
    "            #login\n",
    "            mail.login('username', 'password')\n",
    "\n",
    "            #send message\n",
    "            mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)\n",
    "\n",
    "            #end mail connection\n",
    "            mail.close()\n",
    "\n",
    "            talkToMe('Email sent.')\n",
    "\n",
    "        else:\n",
    "            talkToMe('I don\\'t know what you mean!')\n",
    "\n",
    "\n",
    "talkToMe('I am ready for your command')\n",
    "\n",
    "#loop to continue executing multiple commands\n",
    "while True:\n",
    "    assistant(myCommand())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": ""
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
