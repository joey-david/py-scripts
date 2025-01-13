from backend import chat_shrinker, local_analysis
from backend.llm import llm_analysis

def detectFileType(data):
    '''Detects '''
    # check that all of the files are of the same type
    filetype = ""
    if filetype is in []:
        general = "log"
    elif filetype is in []:
        genral = "img" 
    elif filetype is in []:
        general = "voice"
    else:
        raise("Invalid file type")
    return general, filetype


def processLog(input_file, start_date, end_date, start_time, end_time):
    compressed_string, msgCount, n_users, user_list, nickname_list = chat_shrinker.shrink_chat(
        input_file, start_date, end_date, start_time, end_time)
    json, response = llm_analysis.promptToJSON(prompt=compressed_string, users=user_list, nicknames=nickname_list)
    return json, response
