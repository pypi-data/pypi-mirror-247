"""Definition of the :class:`Asserter`. Provides also a default instance that
can be easily used importing `asserter`.
"""

import os
import sys
import json
import math
import typing as t
import subprocess
from types import ModuleType

from .types import (
    NO_FEEDBACK, BASE_FILTER_OUT_GLOBALS, Feedback, NoFeedback, ExitStrategy,
    FeedbackType, FeedbackPiece, FeedbackMessage
)
from .config import (
    Config, ConfigData, PrimedFeedbackMakerF, ExistFeedbackMakerInput,
    ExpectFeedbackMakerInput
)

_T = t.TypeVar("_T")


def json_dumps(obj: object) -> str:
    """Dump an object to JSON without any extra formatting.
    """
    # Make sure only ASCII characters are used so that the string length as
    # python's `len` function reports it is equal to the string's byte length.
    # Do not insert spaces after each separator.
    return json.dumps(obj, ensure_ascii=True, separators=(',', ':'))


# For simplicity generating the documentation, the docstring is applied to the
# __init__ method.
class Asserter:  # pylint: disable=missing-class-docstring
    #: See :class:`cg_feedback_helpers.config.Config`.
    config: Config
    _output_file: t.IO[bytes]
    _proc: t.Union[subprocess.Popen, None] = None

    def __init__(self, config: t.Optional[ConfigData]) -> None:
        """This class provides access to the assertion methods of the feedback
        helpers.

        Each assertion can output either a positive or a negative feedback,
        depending on whether the assertion passes or fails. A default feedback
        maker is defined in the configuration.

        You have two ways of overriding the feedback:
        - Provide a custom piece of feedback for each assertion using
        `positive_feedback` or `negative_feedback` keyword arguments;
        - Define custom feedback makers in the
        :class:`cg_feedback_helpers.config.ConfigData` when instantiating
        the :class:`Asserter`.

        :param config: The configuration overrides. Check
            :class:`cg_feedback_helpers.config.ConfigData`.
        """
        self.config = Config(config)
        self._open_output()

    def _open_output(self) -> None:
        if self.config.is_atv2 or 'CG_FEEDBACK_HELPERS_TRUNCATE' in os.environ:
            # pylint: disable=consider-using-with
            self._proc = subprocess.Popen(
                ['cg', 'truncate'],
                # The `cg` command already does buffering for us, so disable
                # buffering.
                bufsize=0,
                stdin=subprocess.PIPE,
                close_fds=False,
            )
            assert self._proc.stdin is not None
            # pylint: disable=consider-using-with
            self._output_file = self._proc.stdin
        else:
            # pylint: disable=consider-using-with
            self._output_file = open(2, 'wb', buffering=0)

    def finalize(self) -> None:
        """You should call this method at the end of your test routine to make
        sure file handles are correctly closed. You will not be able to provide
        other feedback once the asserter has been finalized.
        """
        if not self._output_file.closed:
            self._output_file.close()
        if self._proc is not None and self._proc.poll() is None:
            self._proc.wait()  # pragma: no cover

    def __del__(self) -> None:
        self.finalize()

    def _write_feedback(
        self,
        feedback: Feedback,
        ftype: FeedbackType,
    ) -> None:
        if not isinstance(feedback, NoFeedback):
            message = FeedbackMessage(
                tag='feedback',
                contents=[
                    FeedbackPiece(
                        value=feedback,
                        sentiment=ftype.value,
                    ),
                ],
            )
            self._output_file.write(
                (json_dumps(message) + '\n').encode('utf8')
            )

    def _fail(
        self,
        feedback: Feedback,
    ) -> None:
        if self.config.exit_strategy == ExitStrategy.SYS_EXIT:
            self._write_feedback(feedback, FeedbackType.NEGATIVE)
            sys.exit(1)
        elif self.config.exit_strategy == ExitStrategy.RAISE:
            raise AssertionError(feedback)

    def emit_success(self, *, feedback: t.Optional[Feedback] = None) -> None:
        """Writes to the configured output a message giving the user feedback
        that all the assertions have passed and he successfully passed the
        tests.

        :param feedback: Overrides the default feedback displayed to the user.
        """
        self._write_feedback(
            feedback if feedback is not None else self.config.success_message,
            FeedbackType.POSITIVE,
        )
        if self.config.exit_strategy == ExitStrategy.SYS_EXIT:
            sys.exit(0)

    def _assert(
        self,
        cond: bool,
        maker: PrimedFeedbackMakerF,
        positive_feedback: t.Optional[Feedback],
        negative_feedback: t.Optional[Feedback],
    ) -> None:
        if not cond:
            self._fail(maker(negative_feedback, FeedbackType.NEGATIVE))
        else:
            self._write_feedback(
                maker(positive_feedback, FeedbackType.POSITIVE),
                FeedbackType.POSITIVE,
            )

    def variable_exists(
        self,
        varname: str,
        variables: t.Dict[str, t.Any],
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts whether a variable exists in the given set of variables.

        :param varname: The name of the variable that should exist.
        :param variables: The set of variables. Usually, you want this to be
            `globals()`.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExistFeedbackMakerInput("variable", f'"{varname}"')
        self._assert(
            varname in variables,
            self.config.exist_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def is_set(
        self,
        key: str,
        dictionary: t.Dict[str, t.Any],
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts whether a certain key exists in the given dictionary.

        It currently only works with string-keys.

        :param key: The key that should exist in the dictionary.
        :param dictionary: The dictionary that should contain the provided key.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExistFeedbackMakerInput("key", f'"{key}"')
        self._assert(
            key in dictionary,
            self.config.exist_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def is_not_set(
        self,
        key: str,
        dictionary: t.Dict[str, t.Any],
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts whether a certain key does not exist in the given dictionary.

        It currently only works with string-keys.

        :param key: The key that should not exist in th dictionary.
        :param dictionary: The dictionary that should not contain the provided
            key.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExistFeedbackMakerInput("key", f'"{key}"')
        self._assert(
            key not in dictionary,
            self.config.not_exist_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def only_defined_names(
        self,
        keys: t.List[str],
        dictionary: t.Dict[str, t.Any],
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that only certain keys are exist in the given dictionary.

        It currently only works with string-keys.

        Other than the keys provided, a set of keys is added to make sure that
        this works as expected also with `globals()`.

        :param keys: The list of the only keys that should exist in the
            dictionary.
        :param dictionary: The dictionary that should only contain the provided
            keys.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExistFeedbackMakerInput("only keys", keys)
        filter_out = BASE_FILTER_OUT_GLOBALS + keys
        self._assert(
            len([x for x in dictionary.keys() if x not in filter_out]) == 0,
            self.config.exist_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def not_equals(
        self,
        val: _T,
        not_expected: _T,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the two values are not equal.

        :param val: The value to check.
        :param not_expected: The value that `val` should not be equal to.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExpectFeedbackMakerInput("value", val, not_expected)
        self._assert(
            val != not_expected,
            self.config.not_expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def equals(
        self,
        val: _T,
        expected: _T,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the two values are equal.

        :param val: The value to check.
        :param expected: The expected value `val` should be equal to.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExpectFeedbackMakerInput("value", val, expected)
        self._assert(
            val == expected,
            self.config.expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def equals_float(
        self,
        val: float,
        expected: float,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the two floating point values are equal.

        It uses `math.isclose` with the default relative and absolute
        tolerances.

        :param val: The value to check.
        :param expected: The expected value `val` should be equal to.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExpectFeedbackMakerInput("float value", val, expected)
        self._assert(
            math.isclose(val, expected),
            self.config.expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def is_of_type(
        self,
        val: _T,
        expected: t.Type,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the value is of the provided type.

        :param val: The value to check.
        :param expected: The type `val` should be.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        typ = type(val)
        inp = ExpectFeedbackMakerInput("type", typ, expected)
        self._assert(
            typ == expected,
            self.config.expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def not_none(
        self,
        val: _T,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the value is not `None`.

        :param val: The value that should not be `None`.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExpectFeedbackMakerInput("value", val, "None")
        self._assert(
            val is not None,
            self.config.not_expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def has_length(
        self,
        val: t.Sequence,
        expected_length: int,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the provided sequence is of a certain length.

        :param val: The sequence to check.
        :param expected_length: The length `val` should have.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        length = len(val)
        inp = ExpectFeedbackMakerInput("length", length, expected_length)
        self._assert(
            length == expected_length,
            self.config.expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def string_contains(
        self,
        val: str,
        expected: str,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the a certain string contains the provided value.

        :param val: The value that should exist in the string.
        :param expected: The string that should contain `val`.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExpectFeedbackMakerInput("substring", val, expected)
        self._assert(
            expected in val,
            self.config.expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def is_imported(
        self,
        module_name: str,
        modules: t.Dict[str, ModuleType],
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Assrets that the provided module exists in a certain set of modules.

        Usually, you want `modules` to be `sys.modules`.

        :param module_name: The module that should be imported.
        :param modules: The dictionary of imported modules.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExistFeedbackMakerInput("module", module_name)
        self._assert(
            module_name in modules,
            self.config.exist_feedback_maker.get_feedback_maker(inp),
            positive_feedback, negative_feedback
        )

    def file_exists(
        self,
        file_name: str,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the provided file exists in the file system.

        :param file_name: The file that should exist.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExistFeedbackMakerInput("file", file_name)
        self._assert(
            os.path.exists(file_name),
            self.config.exist_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def has_attr(
        self,
        attr: str,
        obj: object,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that a given attribute exists in a certain object.

        :param attr: The attribute that should exist in the object.
        :param obj: The object that should have the given attribute.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExistFeedbackMakerInput("attribute", attr)
        self._assert(
            hasattr(obj, attr),
            self.config.exist_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def is_true(
        self,
        val: bool,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the value is `True`.

        :param val: The value to check.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExpectFeedbackMakerInput("boolean", val, True)
        self._assert(
            val is True,
            self.config.expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def is_false(
        self,
        val: bool,
        *,
        positive_feedback: t.Optional[Feedback] = None,
        negative_feedback: t.Optional[Feedback] = None,
    ) -> None:
        """Asserts that the value is `False`.

        :param val: The value to check.
        :param positive_feedback: Overrides the feedback the user receives if
            the assertion passes.
        :param negative_feedback: Overrides the feedback the user receives if
            the assertion fails.
        """
        inp = ExpectFeedbackMakerInput("boolean", val, False)
        self._assert(
            val is False,
            self.config.expect_feedback_maker.get_feedback_maker(inp),
            positive_feedback,
            negative_feedback,
        )

    def never(
        self,
        feedback: Feedback,
    ) -> None:
        """Assertion that always fails. Should be used in branches of execution
        that should not be called.

        :param feedback: The feedback to provide the user in case this
            assertion is called.
        """
        inp = ExpectFeedbackMakerInput("assertion", "reached", "reached")
        self._assert(
            False,
            self.config.not_expect_feedback_maker.get_feedback_maker(inp),
            NO_FEEDBACK,
            feedback,
        )


asserter = Asserter(None)
"""Default asserter exported for comodity. It will use all the default config.
"""
