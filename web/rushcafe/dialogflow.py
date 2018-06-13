from dialogflow_lite.dialogflow import Dialogflow, DialogflowQueryException
from dialogflow_lite.status import HTTP_200_SUCCESS


class CafeDialogflow(Dialogflow):

    def text_request(self, text):
        responses = []
        result = self._query(text)
        try:
            if result['status']['code'] == HTTP_200_SUCCESS:
                for msg in result['result']['fulfillment']['messages']:
                    responses.append(msg['speech'])
        except KeyError:
            print('No response from the agent')
        except DialogflowQueryException:
            print('Failed to get response url: {} with status: {}'.format(
                self.query_url,
                result['status']['errorType']
            ))

        return responses[0]
