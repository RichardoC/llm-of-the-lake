import app
# Requests is a great library for working with API's, and it's included
# in the badge libraries, so let's use it here!
#
# See https://requests.readthedocs.io/ for more information on how to use
# it properly!
import requests

from app_components import Menu, Notification, clear_background
from events.input import Buttons, BUTTON_TYPES
import sys


class LLMOfTheLakeApp(app.App):
    text: str
    wisdom: str
    connected: bool
    notification: Notification


    def __init__(self):
        # When we load, grab all the API data in JSON format
        # Requests will automatically convert this to a python dict
        # for us, it really is that good!
        # self.schedule = requests.get("https://emffilms.org/schedule.json").json()


        self.button_states = Buttons(self)
        self.text = ""
        self.connected = False
        self.notification = None
        self.try_connect()


            # sys.exit(1)

        # # Setup lists to hold our film titles and timings
        # main_menu_items = []
        # # self.timings = []
        # # Iterate over the films, adding the title to the menu
        # for line in self.wisdom.split("\n"):
        # # for film in self.schedule['films']:
        #     # text = f"{film['title']}"
        #     # time = f"{film['showing']['text']}"
        #     main_menu_items.append(line)
        #     # self.timings.append(time)
        # # Create the menu object
        # self.menu = Menu(
        #     self,
        #     main_menu_items,
        #     select_handler=self.select_handler,
        #     back_handler=self.back_handler,
        # )
        # self.notification = None

    # def select_handler(self, item, position):
    #     self.notification = Notification('Showing at ' + self.timings[position] + '!')

    def try_connect(self):
        # Add a try connecting screen
        self.connected = False
        self.text = "Connecting to\nwifi..."
        try:
            import wifi

            wifi.connect()
            self.text = "Connected to\nwifi. Press C button\nto get wisdom."
            self.connected = True
        except ImportError as e:
            self.connected = False
            self.text = "Wifi failure"
            raise e
    def back_handler(self):
        self.button_states.clear()
        self.minimise()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.getWisdom()
            self.button_states.clear()
        elif self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def getWisdom(self):

        try:
            headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0' }
            chatResponse = requests.post("http://bore.pub:27559/completion", headers=headers, json='{"stream":false,"n_predict":400,"temperature":0.7,"stop":[],"repeat_last_n":256,"repeat_penalty":1.18,"top_k":40,"top_p":0.95,"min_p":0.05,"tfs_z":1,"typical_p":1,"presence_penalty":0,"frequency_penalty":0,"mirostat":0,"mirostat_tau":5,"mirostat_eta":0.1,"grammar":"","n_probs":0,"min_keep":0,"image_data":[],"cache_prompt":true,"api_key":"","slot_id":0,"prompt":"You are the spirit of the Lake at the EMF hacker camp in England. I am a tinker and general hacker in the broadest sense of the word. What is your wisdom for me?\n Be extremely brief, only 10 words per line, as the response will be shown on a small screen. Just give me one or two sentences that spark inspiration.}')
            # chatResponse.raise_for_status()
            if chatResponse.status_code == 200:
                self.wisdom = chatResponse.json()["content"]
                chatResponse.close()
            else:
                chatResponse.close()
                self.text = "Failed to connect to server"
                raise Exception('Server returned non-200')
        except Exception as e:
            self.text = "exception:{e}"
            sys.print_exception(e)
            self.button_states.clear()
            self.minimise()
        self.text = self.wisdom

    def draw(self, ctx):
        # if self.wisdom:
        #     clear_background(ctx)
        #     # Display the menu on the device
        #     # as a scrollable list of film titles
        #     self.menu.draw(ctx)
        #     if self.notification:
        #         self.notification.draw(ctx)
        # else:
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(0, 1, 0).move_to(-95, 0).text(self.text)

__app_export__ = LLMOfTheLakeApp
