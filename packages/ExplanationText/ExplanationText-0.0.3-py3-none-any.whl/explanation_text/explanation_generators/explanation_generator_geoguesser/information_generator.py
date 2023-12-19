from explanation_text.explanation_generators.api_utils import query_text_generation
from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.knowledge_base_controller import \
    (get_prefiltered_information, get_full_information_of_country)
from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.landmark_detection import \
    detect_landmark

knowledge_base_path = ("explanation_generators/explanation_generator_geoguesser/knowledge_base"
                       "/countries/")
endpoint = "https://api-inference.huggingface.co/models/"

landmark_classes = ["building", "monastery", "palace", "residence", "religious residence", "apiary", "boathouse",
                    "place of worship", "church", "mosque", "theater", "cinema", "library", "planetarium", "restaurant",
                    "prison", "institution"]


def generate_part_information(use_landmark_detection, location, part, api_token, google_vision_api_key):
    information = ""
    part_label = str(part.get("part_label")).replace('_', ' ')
    if use_landmark_detection and part_label.lower() in landmark_classes:
        information += detect_landmark(part_label, part.get("img"), google_vision_api_key)
    else:
        information += filter_part_information_from_text(location, part_label.replace(' ', '_'), api_token)
    return information


def filter_part_information_from_text(location, part_label, api_token):
    prefiltered_information = get_prefiltered_information(location, part_label, 0.5, 200)

    if len(prefiltered_information) == 0:
        print("  ! Could not find information about " + part_label)
        return ""

    # TODO ALISA: use filtered_information to further combin the prefiltered
    #  information of the knowledge base with location and part_label
    return combine_knowledgebase_information(location, part_label, prefiltered_information, api_token)


# failed attempt to filter information with open assistant
def old_filter_information(location, part_label, api_token):
    country_information = get_full_information_of_country(location)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
    prompt = ("<|prompter|>Context information: '" + country_information
              + "'. Filter out information about " + part_label
              + " from given text. Filtered information: <|endoftext|><|assistant|>")

    configuration = {'return_full_text': False, 'num_return_sequences': 1,
                     'max_new_tokens': 20, 'no_repeat_ngram_size': 3,
                     'max_time': 120.0, 'num_beams': 1, 'do_sample': True,
                     'top_k': 20, 'Temperature': 0.6}

    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]
    (success, return_text) = query_text_generation(query, endpoint, headers)
    if success:
        return return_text
    else:
        print("Could not find information about " + part_label)
        print(return_text)
        return ""


# Placeholder for Alisas function to combine prefiltered knowledge base information with location and part
def combine_knowledgebase_information(location, part_label, part_information, api_token):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
    prompt = ("<|prompter|>Context information: '" + part_information
              + "'. Combine information about" + part_label + " in " + location +
              " from given text. Filtered information: <|endoftext|><|assistant|>")

    configuration = {'return_full_text': False, 'num_return_sequences': 1,
                     'max_new_tokens': 75, 'max_time': 120.0,
                     'no_repeat_ngram_size': 3, 'num_beams': 3, 'do_sample': True,
                     'top_p': 0.92, 'temperature': 0.6}

    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]
    (success, return_text) = query_text_generation(query, endpoint, headers)
    if success:
        return return_text
    else:
        print("! Failed to combine part information about " + part_label)
        return ""
