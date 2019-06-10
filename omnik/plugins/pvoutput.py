import json
from datetime import datetime

import urllib.parse
import requests
from omnik.plugins import Plugin

class pvoutput(Plugin):

  def get_weather(self):
    try:
      if 'weather' not in self.cache:
        url = "https://{endpoint}/data/2.5/weather?lon={lon}&lat={lat}&units={units}&APPID={api_key}".format(
          endpoint = self.config.get('openweathermap', 'endpoint'),
          lat      = self.config.get('openweathermap', 'lat'),
          lon      = self.config.get('openweathermap', 'lon'),
          units    = self.config.get('openweathermap', 'units', fallback='metric'),
          api_key  = self.config.get('openweathermap', 'api_key'),
        )

        res = requests.get(url)

        self.logger.debug('OK') if res.status_code == 200 else self.logger.debug('NOK: {}'.format(res.status_code))

        res.raise_for_status()

        self.cache['weather'] = res.json()
      else:
        self.logger.info('[HIT] Got cached weather data')

      return self.cache['weather']

    except requests.exceptions.HTTPError as e:
      self.logger.error('Unable to get data. [{0}]: {1}'.format(type(e).__name__, str(e)))
      raise e

  def process(self, **args):
    """
    Send data to pvoutput
    """
    now = datetime.utcnow()

    msg = args['msg']

    self.logger.info(json.dumps(msg, indent=2))

    if not self.config.has_option('pvoutput', 'sys_id') or not self.config.has_option('pvoutput', 'api_key'):
      self.logger.warn('[{}] No api_key and/or sys_id found in configuration'.format(__name__))
      return

    headers = {
      "X-Pvoutput-Apikey": self.config.get('pvoutput', 'api_key'),
      "X-Pvoutput-SystemId": self.config.get('pvoutput', 'sys_id'),
      "Content-type": "application/x-www-form-urlencoded",
      "Accept": "text/plain"
    }

    # See: https://pvoutput.org/help.html
    data = {
        'd': now.strftime('%Y%m%d'),
        't': now.strftime('%H:%M'),
        'v1': str(float(msg['i_eday']) * 1000),
        'v2': str(msg['i_pow_n'])
    }

    if self.config.getboolean('pvoutput', 'use_temperature', fallback=False):
      weather = self.get_weather()

      data['v5'] = str(weather['main']['temp'])

    encoded = urllib.parse.urlencode(data)

    self.logger.info(json.dumps(data, indent=2))

    # result = requests.post("http://pvoutput.org/service/r2/addstatus.jsp", data=encoded, headers=headers)
    # self.logger.info(result)



    

    