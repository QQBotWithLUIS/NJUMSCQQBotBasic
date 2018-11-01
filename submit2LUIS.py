import json
import os.path
from pprint import pprint

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient

from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "36fb4cae87a246169da2edf98e082113"

CWD = os.path.dirname(__file__)

def runtime(subscription_key):
    """Resolve.

    This will execute LUIS prediction
    """
    client = LUISRuntimeClient(
        'https://westus.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key),
    )

    try:
        # 在这里调用函数，获取对方
        query ="活动部是干什么的？"

        print("Executing query: {}".format(query))
        result = client.prediction.resolve(
            "204f9894-2f57-4c7d-889f-31f2df44f0f3",  # LUIS Application ID
            query
        )

        print("\nDetected intent: {} (score: {:d}%)".format(
            result.top_scoring_intent.intent,
            int(result.top_scoring_intent.score*100)
        ))
        print("Detected entities:")
        for entity in result.entities:
            print("\t-> Entity '{}' (type: {}, score:{:d}%)".format(
                entity.entity,
                entity.type,
                int(entity.additional_properties['score']*100)
            ))
        print("\nComplete result object as dictionnary")
        pprint(result.as_dict())

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

    runtime(SUBSCRIPTION_KEY_ENV_NAME)

