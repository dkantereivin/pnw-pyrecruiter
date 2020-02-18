import json
import time
from collections import OrderedDict
from typing import List, Dict, Any

import ezgui as eg

from pnw import Recruiter

# STATIC
categories: Dict[str, str] = {
    'Secure Details': 'sec',
    'Preferences': 'info',
    'Messages': 'msg',
    'Save Changes': None,
    'Reset Changes': None,
    'Exit': None
}

sec_names: Any = OrderedDict()
sec_names['DB Path'] = 'db_path'
sec_names['API Key'] = 'api_key'
sec_names['Username'] = 'user'
sec_names['Password'] = 'pass'

pref_names: Any = OrderedDict()
pref_names['Alliance Name: str'] = 'alliance'
pref_names['Target Alliance str[]'] = 'target_alliance'
pref_names['Max Inactive Time int'] = 'max_inactive'
pref_names['Min Cities int'] = 'min_cities'
pref_names['Exclude int[]'] = 'exclude'
pref_names['Contact Again After int'] = 'contact_again'


def run_main():
    bot = Recruiter()
    while True:
        bot.run_recruitment_round()
        time.sleep(bot.settings['info']['frequency'])


opt: bool = eg.ynbox("Should I open the graphical settings manager?", "PnW Recruiter - Canter Py3.6", ("Yes", "No"))
if opt:
    eg.msgbox('On the screen that follows, please select your settings file.',
              'Graphical Settings Manager - PnW PyRecruiter')
    with open(eg.fileopenbox(), 'r') as file:
        settings = json.load(file)

    while True:

        category: str = eg.buttonbox('Select a settings category, or save changes.',
                                     image='PnW.gif', choices=list(categories.keys()))
        if category == 'Secure Details':
            fields: List[str] = eg.multpasswordbox('Enter new secure information to store.',
                                                   category, list(sec_names.keys()))

            idx: int = 0
            for setting in sec_names.keys():
                if fields[idx] != '':
                    settings[categories[category]][sec_names[setting]] = fields[idx]
                idx += 1

        elif category == 'Preferences':

            fields: List[str] = eg.multpasswordbox('Enter preferences. For str[], int[], use comma-separated values.',
                                                   category, list(pref_names.keys()))
            idx: int = -1
            for key in pref_names.keys():
                idx += 1
                if len(fields[idx]) < 1:
                    continue
                val: Any
                if '[]' in key:
                    val = fields[idx].split(',')
                    if 'int' in key:
                        for i in range(len(val)):
                            val[i] = int(val[i])
                elif 'int' in key:
                    val = int(fields[idx])
                else:
                    val = fields[idx]
                settings[categories[category]][pref_names[key]] = val

        elif category == 'Messages':
            subj = eg.enterbox('Enter a subject line.', category)
            if len(subj) > 0:
                settings[categories[category]]['subject'] = subj

            msg = eg.enterbox('Enter the message content in plaintext', category)
            if len(msg) > 0:
                settings[categories[category]]['content'] = msg

        elif category == 'Save Changes':
            out = json.dumps(settings)
            with open(eg.fileopenbox(), 'w') as file:
                file.write(out)
            eg.msgbox('Successfully saved changes.')

        elif category == 'Reset Changes':
            with open(eg.fileopenbox(), 'w') as file:
                settings = json.load(file)
            eg.msgbox('Successfully reloaded the settings file.')

        elif category == 'Exit':
            break
        print(settings)

else:
    run_main()
