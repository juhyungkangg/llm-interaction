from datetime import timedelta

from LLMInteraction.run.batch_runner import *
from SQLInteraction.SQLResult import *
from SQLInteraction.queries import *
from LLMInteraction.assets.prompts import *
from LLMInteraction.assets.json_schema import *
import schedule
from mainTasks.llm_layer import *
import time
from mainTasks.get_signals import *

load_dotenv()

def main():
    llm_filter()
    llm_sentiment_analysis()
    get_signals()
    print(f"Job completed at {datetime.now()}")

# Schedule the function to run at specific times
schedule.every().day.at("06:00").do(main)
schedule.every().day.at("07:00").do(main)
schedule.every().day.at("08:00").do(main)


if __name__ == '__main__':
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    main()