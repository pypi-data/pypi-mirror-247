from .format_handlers.json_response_parser import JsonResponseParser
from .format_handlers.csv_response_parser import CsvResponseParser

class WebfleetConnectResponse():
  def __init__(self, response, url, is_json):
    self._response = response
    self._url = url
    self._parser = self._build_parser(is_json)

  def status_code(self):
    return self._response.status_code
  
  def to_hash(self):
    return self._parser.to_hash(self._response)
  
  def url(self):
    return self._url
  
  def __str__(self):
    return self._response.text

  def _build_parser(self, is_json):
    if is_json:
      return JsonResponseParser()
    return CsvResponseParser()
