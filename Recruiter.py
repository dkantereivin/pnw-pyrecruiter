import json
import sqlite3
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any

import requests


class Recruiter:
    def __init__(self, settings=None, settings_path="settings.json"):
        """ Loads recruiter settings and connects to the sqlite3 database specified in the settings.
        :param settings=None A dictionary containing all settings to be used by the recruiter.
        :param settings_path="settings.json" The filepath to locate settings, if settings param is not provided.
        """
        if settings:  # a settings object has been provided
            self.settings: Dict[str, Any] = settings
        else:
            with open(settings_path) as settings:  # load and encode settings to object
                self.settings = json.load(settings)
        try:
            self.db: Any = sqlite3.connect(self.settings['sec']['db_path'])
            time_test: str = self.db.execute("SELECT datetime('now');").fetchone()[0]
            print("Successful connection to the database at {}.".format(time_test))
        except:
            raise Exception("Unable to connect to the SQLLite Database.")

    def run_recruitment_round(self) -> None:
        """ Run a single recruitment round, fetches all nations from the Nations API endpoints, iterates them,
        and sends a message if the nation meets the self.should_contact(nation) conditions.
        :return: None
        """
        current_time: datetime = datetime.today()
        print("Recruitment Round Starting @ {}".format(current_time))

        # Fetch and filter nations to those which should be contacted
        all_nations: List[Dict[str, Any]] = self.get_nations()
        print("<-- Nations API (Fetched Nations from PnW)")
        target_nations: iter = filter(self.should_contact, all_nations)

        conn: requests.Session = self.login()
        failed: int = 0  # number of failed requests

        for nation in target_nations:
            try:
                time.sleep(self.settings['READ_ONLY']['delay'])
                self.send_message(nation, conn)
            except Exception:
                failed += 1
                print(Exception)
            self.db.execute("INSERT OR REPLACE INTO nations_contacted(nation_id, time_sent) " +
                            "VALUES (?, datetime('now'));",
                            (int(nation['nationid']),))
            self.db.commit()
            print(f"--> Message Sent to {nation['leader']} (id: {nation['nationid']} @ {datetime.today()}")
        print(f"---- ROUND COMPLETE [Errors: {failed}] ----")

    def login(self) -> requests.Session:
        """ Authenticates with login details specified in settings.json and returns a logged in requests session.
        :return: The logged in session -- to be used for all outgoing traffic (POST requests to send messages).
        """
        payload = {
            'email': self.settings['sec']['user'],
            'password': self.settings['sec']['pass'],
            'loginform': "Login"
        }
        conn = requests.Session()
        conn.post(self.settings['READ_ONLY']['login'], payload)
        print("--> LOGIN and Start Nation Sweep @ {}".format(datetime.today()))
        return conn

    def send_message(self, nation: dict, conn: any) -> None:
        payload = {
            'newconversation': 'true',
            'receiver': nation['leader'],
            'carboncopy': "",
            'subject': self.replace_str_parameters(self.settings['msg']['subject'], nation),
            'body': self.replace_str_parameters(self.settings['msg']['content'], nation),
            'sndmsg': 'Send Message'
        }
        conn.post(self.settings['READ_ONLY']['msg'], payload)

    def should_contact(self, nation: dict) -> bool:
        """ Checks the specified nation for whether it should be contacted, based on:
            - alliance
            - city count
            - inactive time
            - manual exclusions
            - previously contacted nations from the database
        :param nation: The nation for which to check if it should be contacted.
        :return:
        """
        if str(nation['alliance']) not in self.settings['info']['target_alliance']:  # ["None"] for no alliance
            return False
        if int(nation['cities']) < self.settings['info']['min_cities']:  # too few cities
            return False
        if int(nation['minutessinceactive']) > self.settings['info']['max_inactive']:  # too inactive
            return False
        if int(nation['nationid']) in self.settings['info']['exclude']:  # in exclude list
            return False

        qry = self.db.execute("SELECT time_sent FROM nations_contacted WHERE nation_id = ?;",
                              (int(nation['nationid']),)).fetchone()
        if not qry:
            return True
        qry = qry[0]
        qry_time = datetime.strptime(qry, "%Y-%m-%d %H:%M:%S")
        if qry_time > datetime.today() - timedelta(days=self.settings['info']['contact_again']):
            return False

        return True

    def get_nations(self) -> List[Dict[str, Any]]:
        """ Fetches all nations from the nations API and returns them as a list of parsed JSON dictionaries.
        :return:
        """
        endpoint: str = self.settings['READ_ONLY']['nations'] + self.settings['sec']['api_key']
        data: dict = requests.get(endpoint).json()
        return data['nations']

    @staticmethod
    def replace_str_parameters(text: str, nation: dict) -> str:
        """ Replaces all ${property} in the input string with it's value based on current nation.
        Does not replace mathematical expression string parameters. See Recruiter.replace_math_expressions()
        Variable params holds all possible parameters. Replaced via iteration through params.
        :param text The text to have its parameters replaced.
        :param nation Holds a dict with all properties of current nation which will be used for replacement.
        :return: formatted string.
        """
        params = {
            'nation': nation['nation'],
            'leader': nation['leader'],
            'id': nation['nationid'],
            'score': nation['score'],
            'cities': nation['score'],
            'infra': nation['infrastructure'],
            'color': nation['color']
        }
        for param in params:
            text = text.replace("${" + param + "}", str(params[param]))
        return text


if __name__ == '__main__':
    recruiter = Recruiter()
    while True:
        recruiter.run_recruitment_round()
        time.sleep(recruiter.settings['info']['frequency'])
