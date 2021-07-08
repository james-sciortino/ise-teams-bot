# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime
from recognizers_number import recognize_number, Culture
from recognizers_date_time import recognize_datetime
from botbuilder.schema import (
    ChannelAccount, 
    Attachment, 
    Activity, 
    ActivityTypes
)
from botbuilder.core import (
    CardFactory,
    ActivityHandler,
    ConversationState,
    TurnContext,
    UserState,
    MessageFactory,
)

from data_models import ConversationFlow, Question, UserProfile
from xml.etree import ElementTree as ET
from requests.auth import HTTPBasicAuth
import xmltodict, json
import requests
import urllib3
import ise_code 
import re
import os

CARDS = [
    "C:/Users/james.sciortino/OneDrive/James/Python/Network-Automation/ISE/ISE-Context-Bot/bots/resources/0-welcome_bot.json",
    "C:/Users/james.sciortino/OneDrive/James/Python/Network-Automation/ISE/ISE-Context-Bot/bots/resources/1-endpoint_choice.json",
    "C:/Users/james.sciortino/OneDrive/James/Python/Network-Automation/ISE/ISE-Context-Bot/bots/resources/2-adaptive.json",
    "C:/Users/james.sciortino/OneDrive/James/Python/Network-Automation/ISE/ISE-Context-Bot/bots/resources/3-endpoint_session.json",
    "C:/Users/james.sciortino/OneDrive/James/Python/Network-Automation/ISE/ISE-Context-Bot/bots/resources/4-anc_option.json"
]

card1 = "Endpoints Search Result:"
card2 = "Context Visibility Actions:"
card3 = "Endpoint Session Details:"
card4 = "ANC Menu:"
card5 = "COA Menu:"
card6 = "Yale Quarantine Policies:"
card7 = "ANC Status:"


class ValidationResult:
    def __init__(
        self, is_valid: bool = False, value: object = None, message: str = None
    ):
        self.is_valid = is_valid
        self.value = value
        self.message = message


class CustomPromptBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        self.conversation_state = conversation_state
        self.user_state = user_state

        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.profile_accessor = self.user_state.create_property("UserProfile")
        
    def _create_adaptive_card_attachment(self, index, card, endpoint_string) -> Attachment:
        card_path = os.path.join(os.getcwd(), CARDS[index])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)
            card_data["body"][1]["text"] = card
            card_data["body"][2]["text"] = endpoint_string
        return CardFactory.adaptive_card(card_data)

    async def on_message_activity(self, turn_context: TurnContext):                    
        # Get the state properties from the turn context.
        endpoint_str = await self.profile_accessor.get(turn_context, UserProfile)
        flow = await self.flow_accessor.get(turn_context, ConversationFlow)

        await self._fill_out_user_profile(flow, endpoint_str, turn_context)

        # Save changes to UserState and ConversationState
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def _fill_out_user_profile(
        self, flow: ConversationFlow, endpoint_str: UserProfile, turn_context: TurnContext
    ):
        user_input = turn_context.activity.text.strip()

        # ask for MAC address
        if flow.last_question_asked == Question.NONE:
            await turn_context.send_activity(
                MessageFactory.text("Enter the MAC address of the Endpoint you want to manage!")
            )
            flow.last_question_asked = Question.ENDPOINT_INPUT

        # Validate MAC address syntax then ask to verify.
        elif flow.last_question_asked == Question.ENDPOINT_INPUT:
            validate_result = self._validate_search(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                endpoint_str = validate_result.value
                await turn_context.send_activity(
                        MessageFactory.text(f"Performing lookup for {endpoint_str}")
                    )
                if validate_result.message == "ip":
                    menu_search = ise_code.ip_search(endpoint_str
                    )
                    self.menu = ise_code.search_pick(menu_search
                    )
                elif validate_result.message == "mac":
                    menu_search = ise_code.mac_search(endpoint_str
                    )
                    self.menu = ise_code.search_pick(menu_search
                    )
                await turn_context.send_activity(
                    MessageFactory.text("Endpoints found.")
                )
                self.menu_pick = self.menu[0]
                self.menu_dict = self.menu[1]
                self.menu_items = self.menu[2]
                message = Activity(
                    text="Which endpoint do you want to manage?",
                    type=ActivityTypes.message,
                    attachments=[self._create_adaptive_card_attachment(2, card1, self.menu_pick)],
                )
                await turn_context.send_activity(message
                )
                flow.last_question_asked = Question.ENDPOINT_CHOICE

        # validate MAC or IP then prompt to take action.
        elif flow.last_question_asked == Question.ENDPOINT_CHOICE:
            validate_result = self._validate_endpoint(user_input, self.menu_items, flow.last_question_asked)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                endpoint_str.select = ise_code.menu_selection(validate_result.value, self.menu_pick, self.menu_dict)
                await turn_context.send_activity(
                    MessageFactory.text(f"{endpoint_str.select} has been selected.")
                )
                self.action = ise_code.act_pick()
                self.actions_pick = self.action[0]
                self.actions_dict = self.action[1]
                self.actions_items = self.action[2]
                message = Activity(
                    text=(f"Which action do you want to take on {endpoint_str.select}"),
                    type=ActivityTypes.message,
                    attachments=[self._create_adaptive_card_attachment(2, card2, self.actions_pick)]
                )
                await turn_context.send_activity(message
                )
                flow.last_question_asked = Question.ENDPOINT_ACTION


        # validate action
        elif flow.last_question_asked == Question.ENDPOINT_ACTION:
            validate_result = self._validate_endpoint(user_input, self.actions_dict, flow.last_question_asked )
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                endpoint_str.action = self.actions_dict[validate_result.value]
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"You selected to {endpoint_str.action} for {endpoint_str.select}."
                    )
                )
            if validate_result.value == 1:
                self.uuid = ise_code.endpoint_details(endpoint_str.select)
                self.session = ise_code.endpoint_session(endpoint_str.select, self.uuid)
                if self.session != False:
                    self.session_pick = self.session[0]
                    self.session_dict = self.session[1]
                    self.session_items = self.session[2]
                    message = Activity(
                        text=(f"Session details for {endpoint_str.select}"),
                        type=ActivityTypes.message,
                        attachments=[self._create_adaptive_card_attachment(2, card3, self.session_pick)]
                    )
                    await turn_context.send_activity(message
                    )
                    await turn_context.send_activity(
                            MessageFactory.text("Type anything to run the bot again.")
                        )
                    flow.last_question_asked = Question.NONE
                else:
                    await turn_context.send_activity(
                        MessageFactory.text(f"No active sessions available for endpoint {endpoint_str.select}. Please type anything to run the bot again.")
                        )
                    flow.last_question_asked = Question.NONE

            elif validate_result.value == 2:
                self.anc = ise_code.anc_assign()
                self.anc_pick = self.anc[0]
                self.anc_dict = self.anc[1]
                self.anc_items = self.anc[2]
                message = Activity(
                    text=(f"Available ANC options for {endpoint_str.select}"),
                    type=ActivityTypes.message,
                    attachments=[self._create_adaptive_card_attachment(2, card4, self.anc_pick)]
                )
                await turn_context.send_activity(message
                )
                flow.last_question_asked = Question.ENDPOINT_ANC
            
            elif validate_result.value == 3:
                self.coa = ise_code.coa_assign()
                self.coa_pick = self.coa[0]
                self.coa_dict = self.coa[1]
                self.coa_items = self.coa[2]
                message = Activity(
                    text=(f"Available COA options for {endpoint_str.select}"),
                    type=ActivityTypes.message,
                    attachments=[self._create_adaptive_card_attachment(2, card5, self.coa_pick)]
                )
                await turn_context.send_activity(message
                )
                flow.last_question_asked = Question.ENDPOINT_COA
        
        elif flow.last_question_asked == Question.ENDPOINT_COA:
            validate_result = self._validate_endpoint(user_input, self.coa_items, flow.last_question_asked)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                self.coa_action = ise_code.coa_get(validate_result.value, endpoint_str.select)
                if self.coa_action == True:
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"Successfully issued CoA for {endpoint_str.select}."
                        )
                    )
                    await turn_context.send_activity(
                        MessageFactory.text("Type anything to run the bot again.")
                    )
                elif self.coa_action == False:
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"Failed to issue CoA for {endpoint_str.select}."
                        )
                    )
                    await turn_context.send_activity(
                        MessageFactory.text("Type anything to run the bot again.")
                    )
                flow.last_question_asked = Question.NONE

        elif flow.last_question_asked == Question.ENDPOINT_ANC:
            validate_result = self._validate_endpoint(user_input, self.anc_items, flow.last_question_asked)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                if validate_result.value == 1:
                    self.quarantine = ise_code.quarantine_assign()
                    self.quarantine_pick = self.quarantine[0]
                    self.quarantine_dict = self.quarantine[1]
                    self.quarantine_items = self.quarantine[2]
                    print(self.quarantine_items)
                    message = Activity(
                        text=(f"Available ANC policies for {endpoint_str.select}"),
                        type=ActivityTypes.message,
                        attachments=[self._create_adaptive_card_attachment(2, card6, self.quarantine_pick)]
                    )
                    await turn_context.send_activity(message
                    )
                    flow.last_question_asked = Question.ANC_ASSIGN

                elif validate_result.value == 2:
                    self.anc_revoke = ise_code.quarantine_put(validate_result.value, endpoint_str.select)
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"Successfully revoked ANC policy for {endpoint_str.select}."
                        )
                    )
                    await turn_context.send_activity(
                        MessageFactory.text("Type anything to run the bot again.")
                    )
                    flow.last_question_asked = Question.NONE

                elif validate_result.value == 3:
                    self.anc_name = ise_code.anc_uuid(endpoint_str.select)
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"Checking status for {endpoint_str.select}."
                        )
                    )
                    if self.anc_name == None:
                        await turn_context.send_activity(
                        MessageFactory.text("Endpoint not assigned to an ANC policy.")
                        )
                        await turn_context.send_activity(
                        MessageFactory.text("Type anything to run the bot again.")
                        )
                        flow.last_question_asked = Question.NONE
                    
                    elif self.anc_name != None:
                        message = Activity(
                            text=(f"ANC Status for {endpoint_str.select}"),
                            type=ActivityTypes.message,
                            attachments=[self._create_adaptive_card_attachment(2, card7, self.anc_name)]
                        )
                        await turn_context.send_activity(message
                        )
                        await turn_context.send_activity(
                            MessageFactory.text("Type anything to run the bot again.")
                        )
                        flow.last_question_asked = Question.NONE

        elif flow.last_question_asked == Question.ANC_ASSIGN:
            validate_result = self._validate_endpoint(user_input, self.quarantine_dict, flow.last_question_asked)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                #endpoint_str.action = actions_dict[validate_result.value]
                self.anc_policy = ise_code.quarantine_assign()[1][validate_result.value]
                self.policy_assign = ise_code.quarantine_put(str(self.anc_policy), endpoint_str.select)
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Successfully applied {self.anc_policy} to {endpoint_str.select}."
                    )
                )
                await turn_context.send_activity(
                    MessageFactory.text("Type anything to run the bot again.")
                )
                flow.last_question_asked = Question.NONE

    def _validate_search(self, user_input: str) -> ValidationResult:
        ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        mac_regex = "[0-9a-fA-F][-:]"
        if(re.search(ip_regex, user_input)):
            message = "ip"
        elif(re.search(mac_regex, user_input)):
            message = "mac"
        else:
            return ValidationResult(
                is_valid=False,
                message="Please enter a valid EUI-48 MAC address.",
            )
        return ValidationResult(is_valid=True, message=message, value=user_input)
    
    def _validate_endpoint(self, user_input: str, list_select, convo) -> ValidationResult:
        # Attempt to convert the Recognizer result to an integer. This works for "a dozen", "twelve", "12", and so on.
        # The recognizer returns a list of potential recognition results, if any.
        # Convert user's input to an integer and match it to a generated list generated from the ISE API.
        try:
            results = recognize_number(user_input, Culture.English)
            max = len((list_select))
            min = 1
            add = range(min, max+1)
            total = []
            for i in add:
                total.append(i)
            # List comprehension
            numbers = [int(x) for x in total]
            for result in results:
                if "value" in result.resolution:
                    self.choice = int(result.resolution["value"])
                    if self.choice in numbers:
                        return ValidationResult(is_valid=True, value=self.choice) 

            if convo == Question.ENDPOINT_CHOICE:
                return ValidationResult(
                    is_valid=False, 
                    message="Please select a MAC address using the appropriate menu choice.\nWhich endpoint do you want to manage?"
                )
            elif convo  == Question.ENDPOINT_ACTION:
                return ValidationResult(
                    is_valid=False, 
                    message="Please select a enter a valid Context Visibility action.\nWhich action do you want to take?"
                ) 
            elif convo  == Question.ENDPOINT_ANC:
                return ValidationResult(
                    is_valid=False, 
                    message="Please select a enter a valid ANC action.\nWhich ANC action do you want to take?"
                ) 
            elif convo  == Question.ENDPOINT_COA:
                return ValidationResult(
                    is_valid=False, 
                    message="Please select a enter a valid COA type.\nWhich COA do you want to apply?"
                )             
            elif convo  == Question.ANC_ASSIGN:
                return ValidationResult(
                    is_valid=False, 
                    message="Please select a enter a valid ANC policy.\nWhich action ANC policy do you want to apply?"
                ) 
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, I could not interpret that as an appropriate "
                "action. Please enter an action from the available list.",
            )

    def _validate_anc(self, user_input: str) -> ValidationResult:
        try:
            results = recognize_number(user_input, Culture.English)
            numbers = range(1, 4)
            for number in numbers:
                if int(user_input) in numbers:
                    for result in results:
                        if "value" in result.resolution:
                            endpoint_select = int(result.resolution["value"])
                            return ValidationResult(is_valid=True, value=endpoint_select) 

            return ValidationResult(
                is_valid=False,
                message="I'm sorry, please enter a valid Context Visibility action.",
            )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, I could not interpret that as an appropriate "
                "action. Please enter an action from the available list.",
            )

            ####



### Would be dope if you could SCHEDULE your ANC and revocation using the datetime function

""" def _validate_action(self, user_input: str) -> ValidationResult:
        try:
            # Try to recognize the input as a date-time. This works for responses such as "11/14/2018", "9pm",
            # "tomorrow", "Sunday at 5pm", and so on. The recognizer returns a list of potential recognition results,
            # if any.
            results = recognize_datetime(user_input, Culture.English)
            for result in results:
                for resolution in result.resolution["values"]:
                    if "value" in resolution:
                        now = datetime.now()

                        value = resolution["value"]
                        if resolution["type"] == "date":
                            candidate = datetime.strptime(value, "%Y-%m-%d")
                        elif resolution["type"] == "time":
                            candidate = datetime.strptime(value, "%H:%M:%S")
                            candidate = candidate.replace(
                                year=now.year, month=now.month, day=now.day
                            )
                        else:
                            candidate = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

                        # user response must be more than an hour out
                        diff = candidate - now
                        if diff.total_seconds() >= 3600:
                            return ValidationResult(
                                is_valid=True,
                                value=candidate.strftime("%m/%d/%y"),
                            ) 

            return ValidationResult(
                is_valid=False,
                message="I'm sorry, please enter a valid Context Visibility action.",
            )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, I could not interpret that as an appropriate "
                "action. Please enter an action from the available list.",
            ) """
####