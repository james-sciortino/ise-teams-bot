# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class Question(Enum):
    ENDPOINT_INPUT = 1
    ENDPOINT_CHOICE = 2
    ENDPOINT_ACTION = 3
    ENDPOINT_SESSION = 4
    ENDPOINT_ANC = 5
    ENDPOINT_COA = 6
    ANC_ASSIGN = 7
    ANC_REVOKE = 8
    ANC_CHECK = 9
    NONE = 10


class ConversationFlow:
    def __init__(
        self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked
