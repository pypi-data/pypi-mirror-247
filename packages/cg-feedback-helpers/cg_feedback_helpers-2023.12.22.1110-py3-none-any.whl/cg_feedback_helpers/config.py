"""Provides the configuration for the :class:`cg_feedback_helpers.assertions.Asserter` class.
"""

import os
import typing as t
from dataclasses import field, dataclass

from .types import (
    NO_FEEDBACK, Feedback, NoFeedback, ExitStrategy, FeedbackType
)

_Y = t.TypeVar("_Y")


@dataclass
class ExpectFeedbackMakerInput(t.Generic[_Y]):
    """Provides the parameters for :class:`ExpectFeedbackMaker` instances.
    Defines the contents of the feedback provided to the user.
    """
    #: What is the feedback about. Should be just a name.
    what: str
    #: The value that was received.
    value: _Y
    #: The value that was expected.
    expected: t.Union[_Y, str]


@dataclass
class ExistFeedbackMakerInput(t.Generic[_Y]):
    """Provides the parameters for :class:`ExistFeedbackMaker` instances.
    Defines the contents of the feedback provided to the user.
    """
    #: What is the feedback about. Should be just a name.
    what: str
    #: The value that was expected.
    expected: _Y


ExpectFeedbackMakerF = t.Callable[[ExpectFeedbackMakerInput], Feedback]
"""A function that takes a :class:`ExpectFeedbackMakerInput` instance and
produces a valid piece of feedback.
"""
ExistFeedbackMakerF = t.Callable[[ExistFeedbackMakerInput], Feedback]
"""A function that takes a :class:`ExistFeedbackMakerInput` instance and
produces a valid piece of feedback.
"""


@dataclass
class DefaultExpectFeedback():
    """Default feedback maker functions for :class:`ExpectFeedbackMaker`.
    """
    #: Maker function for positive feedback.
    positive: ExpectFeedbackMakerF
    #: Maker function for negative feedback.
    negative: ExpectFeedbackMakerF


@dataclass
class DefaultExistFeedback():
    """Default feedback maker functions for :class:`ExistFeedbackMaker`.
    """
    #: Maker function for positive feedback.
    positive: ExistFeedbackMakerF
    #: Maker function for negative feedback.
    negative: ExistFeedbackMakerF


#: A function that has been primed with configuration data and can be used
#: to produce feedback pieces from the user override.
PrimedFeedbackMakerF = t.Callable[[t.Optional[Feedback], FeedbackType],
                                  Feedback]


@dataclass
class ExpectFeedbackMaker:
    """Factory class used to generate feedback based on user input data and the
    defaults provided when configuring the 
    :class:`cg_feedback_helpers.assertions.Asserter` object.
    """

    defaults: DefaultExpectFeedback

    def get_feedback_maker(
        self,
        inp: ExpectFeedbackMakerInput,
    ) -> PrimedFeedbackMakerF:
        """Generates a primed function that takes a potential user feedback
        override, and the type of feedback to be produced. With this, it
        generates a piece of feedback that is guaranteed to not be `None`.

        :param inp: The input data for the feedback maker function.
        :returns: A function that produces a piece of feedback.
        """
        def get_feedback(
            custom: t.Optional[Feedback],
            typ: FeedbackType,
        ) -> Feedback:
            # Simple case: no feedback symbol is valid feedback.
            if isinstance(custom, NoFeedback):
                return custom

            # Simple case: any non-empty string is valid feedback.
            if custom is not None and custom.strip() != '':
                return custom

            if typ is FeedbackType.NEGATIVE:
                return self.defaults.negative(inp)
            return self.defaults.positive(inp)

        return get_feedback


@dataclass
class ExistFeedbackMaker:
    """Factory class used to generate feedback based on user input data and the
    defaults provided when configuring the 
    :class:`cg_feedback_helpers.assertions.Asserter` object.
    """

    defaults: DefaultExistFeedback

    def get_feedback_maker(
        self,
        inp: ExistFeedbackMakerInput,
    ) -> PrimedFeedbackMakerF:
        """Generates a primed function that takes a potential user feedback
        override, and the type of feedback to be produced. With this, it
        generates a piece of feedback that is guaranteed to not be `None`.

        :param inp: The input data for the feedback maker function.
        :returns: A function that produces a piece of feedback.
        """
        def get_feedback(
            custom: t.Optional[Feedback],
            typ: FeedbackType,
        ) -> Feedback:
            # Simple case: no feedback symbol is valid feedback.
            if isinstance(custom, NoFeedback):
                return custom

            # Simple case: any non-empty string is valid feedback.
            if custom is not None and custom.strip() != '':
                return custom

            if typ is FeedbackType.NEGATIVE:
                return self.defaults.negative(inp)
            return self.defaults.positive(inp)

        return get_feedback


@dataclass
class ConfigData:
    """Configuration data for the :class:`cg_feedback_helpers.assertions.Asserter`.
    """
    #: The exit strategy to use in case of a failed assertion.
    exit_strategy: t.Optional[ExitStrategy] = field(default=None)

    #: The default feedback makers for assertions that compare a value
    #: to another parameter. Used for expectations that should be met.
    expect_feedback: t.Optional[DefaultExpectFeedback] = field(default=None)
    #: The default feedback makers for assertions that compare a value
    #: to another parameter. Used for expectation that should not be met.
    not_expect_feedback: t.Optional[DefaultExpectFeedback] = field(
        default=None
    )
    #: The default feedback makers for assertions that expect something
    #: to exist.
    exist_feedback: t.Optional[DefaultExistFeedback] = field(default=None)
    #: The default feedback makers for assertions that expect something to
    #: not exist.
    not_exist_feedback: t.Optional[DefaultExistFeedback] = field(default=None)

    #: The default message to display when calling
    #: `cg_feedback_helpers.assertions.Asserter::emit_success`.
    success_message: t.Optional[str] = field(default=None)


# For simplicity generating the documentation, the docstring is applied to the
# __init__ method.
class Config:  # pylint: disable=too-few-public-methods,missing-class-docstring
    #: The exit strategy to use in case of a failed assertion.
    exit_strategy: ExitStrategy

    #: A maker object used by :class:`cg_feedback_helpers.assertions.Asserter`
    #: to produce the feedback messages for its assertions.
    expect_feedback_maker: ExpectFeedbackMaker
    #: A maker object used by :class:`cg_feedback_helpers.assertions.Asserter`
    #: to produce the feedback messages for its assertions.
    not_expect_feedback_maker: ExpectFeedbackMaker
    #: A maker object used by :class:`cg_feedback_helpers.assertions.Asserter`
    #: to produce the feedback messages for its assertions.
    exist_feedback_maker: ExistFeedbackMaker
    #: A maker object used by :class:`cg_feedback_helpers.assertions.Asserter`
    #: to produce the feedback messages for its assertions.
    not_exist_feedback_maker: ExistFeedbackMaker

    #: The message to display by default when calling `emit_success` on the
    #: :class:`cg_feedback_helpers.assertions.Asserter` object.
    success_message: str

    def __init__(self, data: t.Optional[ConfigData]) -> None:
        """Configuration class used by
        :class:`cg_feedback_helpers.assertions.Asserter` to determine runtime
        feedback maker functions, where the feedback should be output, and how
        to exit in case of an assertion failure.

        :param data: The configuration data that can be provided to override
            the default configuration.
        """
        self.exit_strategy = self._default_exit_strategy

        expect_feedback = self._default_expect_feedback
        not_expect_feedback = self._default_not_expect_feedback
        exist_feedback = self._default_exist_feedback
        not_exist_feedback = self._default_not_exist_feedback

        self.success_message = self._default_success_message

        if data is not None:
            if data.exit_strategy is not None:
                self.exit_strategy = data.exit_strategy

            if data.expect_feedback is not None:
                expect_feedback = data.expect_feedback
            if data.not_expect_feedback is not None:
                not_expect_feedback = data.not_expect_feedback
            if data.exist_feedback is not None:
                exist_feedback = data.exist_feedback
            if data.not_exist_feedback is not None:
                not_exist_feedback = data.not_exist_feedback

            if data.success_message is not None:
                self.success_message = data.success_message

        self.expect_feedback_maker = ExpectFeedbackMaker(expect_feedback)
        self.not_expect_feedback_maker = ExpectFeedbackMaker(
            not_expect_feedback
        )
        self.exist_feedback_maker = ExistFeedbackMaker(exist_feedback)
        self.not_exist_feedback_maker = ExistFeedbackMaker(not_exist_feedback)

    @property
    def is_atv2(self) -> bool:
        """Whether the package is running in ATv2 environment.
        """
        return os.getenv('CG_ATV2') == "true"

    @property
    def _default_exit_strategy(self) -> ExitStrategy:
        return ExitStrategy.SYS_EXIT if self.is_atv2 else ExitStrategy.RAISE

    @property
    def _default_expect_feedback(self) -> DefaultExpectFeedback:
        def mk_negative(inp: ExpectFeedbackMakerInput) -> Feedback:
            return (
                f'Expected {inp.what} to be {inp.expected}, instead got'
                f' {inp.value}'
            )

        if self.is_atv2:
            return DefaultExpectFeedback(
                positive=lambda _: NO_FEEDBACK, negative=mk_negative
            )
        return DefaultExpectFeedback(
            positive=lambda inp: f'Got expected {inp.what} {inp.expected}',
            negative=mk_negative,
        )

    @property
    def _default_not_expect_feedback(self) -> DefaultExpectFeedback:
        def mk_negative(inp: ExpectFeedbackMakerInput) -> Feedback:
            return f'Expected {inp.what} not to be {inp.expected}'

        if self.is_atv2:
            return DefaultExpectFeedback(
                positive=lambda _: NO_FEEDBACK, negative=mk_negative
            )
        return DefaultExpectFeedback(
            positive=lambda inp:
            f'Did not get disallowed {inp.what} {inp.expected}',
            negative=mk_negative,
        )

    @property
    def _default_exist_feedback(self) -> DefaultExistFeedback:
        def mk_negative(inp: ExistFeedbackMakerInput) -> Feedback:
            return f'Expected {inp.what} {inp.expected} to exist'

        if self.is_atv2:
            return DefaultExistFeedback(
                positive=lambda _: NO_FEEDBACK, negative=mk_negative
            )
        return DefaultExistFeedback(
            positive=lambda inp: f'Found expected {inp.what} {inp.expected}',
            negative=mk_negative,
        )

    @property
    def _default_not_exist_feedback(self) -> DefaultExistFeedback:
        def mk_negative(inp: ExistFeedbackMakerInput) -> Feedback:
            return f'Expected {inp.what} {inp.expected} to not exist'

        if self.is_atv2:
            return DefaultExistFeedback(
                positive=lambda _: NO_FEEDBACK, negative=mk_negative
            )
        return DefaultExistFeedback(
            positive=lambda inp:
            f'Did not find disallowed {inp.what} {inp.expected}',
            negative=mk_negative,
        )

    @property
    def _default_success_message(self) -> str:
        return 'Everything was correct! Good job!'
